from __future__ import annotations

import asyncio
import dataclasses
import typing

import web3
import web3.constants
import web3.contract

# TypeVar Extra
import dfkassa.constants
from dfkassa.watcher.error import (SlippageIsToHighError,
                                   TokenIsNotAcceptedError)

if typing.TYPE_CHECKING:
    from dfkassa.watcher.networks.base import BaseNetwork
    from dfkassa.watcher.settings import DFKassaWatcherSettings

TE = typing.TypeVar("TE")


@dataclasses.dataclass
class PaymentAsUSD:
    amount: int
    price: int


@dataclasses.dataclass
class Token:
    symbol: str
    name: str
    decimals: int


@dataclasses.dataclass
class NewPaymentTip:
    receiver: str
    amount: int


@dataclasses.dataclass
class NewPaymentArgs:
    amount: int
    payload: int
    token: str
    merchant: str
    tips: typing.List[NewPaymentTip]


@dataclasses.dataclass
class NewPaymentContext(typing.Generic[TE]):
    extra: TE
    raw_event: dict
    receipt: dict
    args: NewPaymentArgs
    dfkassa: web3.contract.Contract
    oracle: web3.contract.Contract
    network: BaseNetwork
    watcher_settings: DFKassaWatcherSettings

    async def fetch_payment_token(self) -> Token:
        if self.args.token == web3.constants.ADDRESS_ZERO:
            return self.network.native_currency

        erc20 = self.network.w3client.eth.contract(
            address=self.network.w3client.to_checksum_address(self.args.token),
            abi=dfkassa.constants.ERC20_ABI,
        )
        symbol, name, decimals = await asyncio.gather(
            erc20.functions.symbol().call(),
            erc20.functions.name().call(),
            erc20.functions.decimals().call(),
        )
        return Token(symbol=symbol, name=name, decimals=decimals)

    async def fetch_payment_as_usd_e2(self) -> PaymentAsUSD:
        usd_token_price, usd_amount = await self.oracle.functions.calcE2(
            self.args.token, self.args.amount
        ).call(block_identifier=self.raw_event["blockNumber"])
        return PaymentAsUSD(amount=usd_amount, price=usd_token_price)

    async def fetch_payment_as_usd_e18(self) -> PaymentAsUSD:
        usd_token_price, usd_amount = await self.oracle.functions.calcE18(
            self.args.token, self.args.amount
        ).call(block_identifier=self.raw_event["blockNumber"])
        return PaymentAsUSD(amount=usd_amount, price=usd_token_price)

    async def check_price_slippage(
        self, expected_amount: typing.Union[int, float], tolerance: float
    ) -> None:
        # calcE2 returns everything in cents
        payment_as_usd = await self.fetch_payment_as_usd_e2()
        payment_usd_amount = payment_as_usd.amount / 100
        if expected_amount - payment_usd_amount > expected_amount * tolerance:
            percent_diff = payment_usd_amount / expected_amount
            usd_diff = payment_usd_amount - expected_amount
            raise SlippageIsToHighError(
                percent_difference=percent_diff,
                usd_difference=usd_diff,
                payment_as_usd=payment_as_usd,
            )

    async def check_token_is_accepted(self):
        for token in self.network.accepted:
            if token == self.args.token:
                break
        else:
            raise TokenIsNotAcceptedError()

    async def ensure_payment_is_ok(
        self,
        price_expected_amount: typing.Union[int, float],
        price_slippage_tolerance: float,
    ) -> None:
        await self.check_price_slippage(
            expected_amount=price_expected_amount, tolerance=price_slippage_tolerance
        )
        await self.check_token_is_accepted()
