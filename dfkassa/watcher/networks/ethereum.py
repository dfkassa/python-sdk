import enum

import web3.constants

import dfkassa.constants
from dfkassa.watcher.context import Token
from dfkassa.watcher.networks.base import BaseNetwork


class EthereumMainnetToken(str, enum.Enum):
    ETH = web3.constants.ADDRESS_ZERO


class EthereumMainnetNetwork(BaseNetwork[EthereumMainnetToken]):
    @property
    def native_currency(self) -> Token:
        return Token(name="Ether", symbol="ETH", decimals=18)

    @property
    def chain_id(self) -> int:
        return 1

    @property
    def dfkassa_contract_address(self) -> str:
        return dfkassa.constants.DFKASSA_CONTRACT_ADDRESS_ETH_MAINNET

    @property
    def oracle_contract_address(self) -> str:
        return dfkassa.constants.TOKEN_USD_ORACLE_ADDRESS_ETH_MAINNET
