import asyncio
import dataclasses
import typing

import web3._utils.filters  # noqa
import web3.logs
import web3.types

from dfkassa.watcher.context import (NewPaymentArgs, NewPaymentContext,
                                     NewPaymentTip)
from dfkassa.watcher.networks.base import BaseNetwork

TE = typing.TypeVar("TE")


@dataclasses.dataclass
class DFKassaWatcherSettings(typing.Generic[TE]):
    callback: typing.Callable[[NewPaymentContext[TE]], typing.Any]
    networks: typing.List[BaseNetwork]
    extra: typing.Optional[TE] = None
    poll_interval: int = 5
    on_filter_attaching: typing.Optional[
        typing.Callable[[BaseNetwork, web3._utils.filters.AsyncFilter], typing.Awaitable[typing.Any]]
    ] = None
    merchant_address: typing.Optional[str] = None


    async def _run_coroutine_watching_for_network(
        self,
        network: BaseNetwork,
    ):
        dfkassa = network.w3client.eth.contract(
            address=network.w3client.to_checksum_address(
                network.dfkassa_contract_address
            ),
            abi=network.dfkassa_contract_abi,
        )
        oracle = network.w3client.eth.contract(
            address=network.w3client.to_checksum_address(
                network.oracle_contract_address
            ),
            abi=network.oracle_contract_abi,
        )

        _block_number = await network.w3client.eth.block_number  # noqa
        events_filter = await dfkassa.events.NewPayment.create_filter(
            fromBlock=_block_number, argument_filters=(
                {"merchant": self.merchant_address}
                if self.merchant_address is None
                else {}
            )
        )
        await self.on_filter_attaching(network, events_filter)

        while True:
            # Sometime nodes are clearing filters,
            # so that's why we renew it sometimes
            try:
                new_entries = await events_filter.get_new_entries()
            except ValueError as err:
                if err.args[0]["message"] == "filter not found":
                    events_filter = await dfkassa.events.NewPayment.create_filter(
                        fromBlock=_block_number, argument_filters=(
                            {"merchant": self.merchant_address}
                            if self.merchant_address is None
                            else {}
                        )
                    )
                    continue

                # Unknown error
                else:
                    break

            for raw_event in new_entries:
                receipt = await network.w3client.eth.wait_for_transaction_receipt(
                    raw_event["transactionHash"]
                )
                all_events = dfkassa.events.NewPayment().process_receipt(
                    receipt,
                    errors=web3.logs.DISCARD  # Ignore ERC20 transfers
                )
                event = all_events[-1]
                payment_args = NewPaymentArgs(
                    amount=event["args"]["amount"],
                    payload=event["args"]["payload"],
                    token=event["args"]["token"],
                    merchant=event["args"]["merchant"],
                    tips=[
                        NewPaymentTip(
                            receiver=tip["reciever"],  # Our fault, there is a mistake,
                            amount=tip["amount"],
                        )
                        for tip in event["args"]["tips"]
                    ],
                )
                ctx = NewPaymentContext(
                    receipt=receipt,
                    raw_event=event,
                    extra=self.extra,
                    args=payment_args,
                    dfkassa=dfkassa,
                    oracle=oracle,
                    network=network,
                    watcher_settings=self,
                )
                asyncio.create_task(self.callback(ctx))

                # If filters will be cleared, we should
                # start from the next block of the last handled payment's block
                _block_number = receipt["blockNumber"] + 1

            await asyncio.sleep(self.poll_interval)

    async def coroutine_run_watching(self) -> typing.NoReturn:
        tasks = []
        for network in self.networks:
            task = asyncio.create_task(
                self._run_coroutine_watching_for_network(network)
            )
            tasks.append(task)

        await asyncio.gather(*tasks)
