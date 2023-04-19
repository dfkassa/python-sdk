import abc
import dataclasses
import typing

import web3
import web3.types

# TypeVar Tokens Accepted
import dfkassa.constants
from dfkassa.watcher.context import Token

TTA = typing.TypeVar("TTA")


@dataclasses.dataclass
class BaseNetwork(abc.ABC, typing.Generic[TTA]):
    w3client: web3.Web3
    accepted: typing.List[str]
    filter_id: typing.Optional[str] = None
    from_block: web3.types.BlockIdentifier = "latest"

    # def __post_init__(self):
    #     # Validate generic args?
    #     print(self.__class__.__orig_bases__[0].__args__[0])

    @property
    @abc.abstractmethod
    def chain_id(self) -> int:
        pass

    @property
    @abc.abstractmethod
    def native_currency(self) -> Token:
        pass

    @property
    @abc.abstractmethod
    def dfkassa_contract_address(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def oracle_contract_address(self) -> str:
        pass

    @property
    def dfkassa_contract_abi(self) -> str:
        return dfkassa.constants.DFKASSA_CONTRACT_ABI

    @property
    def oracle_contract_abi(self) -> str:
        return dfkassa.constants.TOKEN_USD_ORACLE_CONTRACT_ABI
