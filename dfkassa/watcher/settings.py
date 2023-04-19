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
    on_block_number_shifted: typing.Optional[typing.Callable[
        [BaseNetwork, int],
        typing.Awaitable[typing.Any]
    ]] = None
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

        _from_block_number: int
        # If None, use latest
        if network.from_block is None:
            _from_block_number = await network.w3client.eth.block_number  # noqa
        else:
            _from_block_number = network.from_block

        while True:
            _newest_block_number = await network.w3client.eth.block_number  # noqa
            entries = await dfkassa.events.NewPayment.get_logs(
                argument_filters={},
                fromBlock=_from_block_number,
                toBlock=_newest_block_number,
            )

            handle_payment_tasks = []
            for raw_event in entries:
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
                handle_payment_tasks.append(asyncio.create_task(self.callback(ctx)))

            await asyncio.gather(*handle_payment_tasks)

            # Shift fromBlock to tha latest checked
            _from_block_number = _newest_block_number + 1

            # When all payments are processed,
            # call a callback to notify about shifting
            if self.on_block_number_shifted is not None:
                await self.on_block_number_shifted(network, _from_block_number)

            await asyncio.sleep(self.poll_interval)
            _newest_block_number = await network.w3client.eth.block_number  # noqa
            # This prevents end < start (we shifted _from_block_number to 1 before)
            while _newest_block_number < _from_block_number:
                await asyncio.sleep(self.poll_interval)
                _newest_block_number = await network.w3client.eth.block_number  # noqa

    async def coroutine_run_watching(self) -> typing.NoReturn:
        tasks = []
        for network in self.networks:
            task = asyncio.create_task(
                self._run_coroutine_watching_for_network(network)
            )
            tasks.append(task)

        await asyncio.gather(*tasks)
