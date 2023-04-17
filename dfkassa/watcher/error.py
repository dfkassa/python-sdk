from __future__ import annotations

import dataclasses
import typing

if typing.TYPE_CHECKING:
    from dfkassa.watcher.context import PaymentAsUSD


@dataclasses.dataclass
class SlippageIsToHighError(Exception):
    percent_difference: float
    usd_difference: float
    payment_as_usd: PaymentAsUSD


@dataclasses.dataclass
class TokenIsNotAcceptedError(Exception):
    pass
