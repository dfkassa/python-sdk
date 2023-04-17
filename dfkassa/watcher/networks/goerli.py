import enum

import web3.constants

import dfkassa.constants
from dfkassa.watcher.context import Token
from dfkassa.watcher.networks.base import BaseNetwork


class GoerliTestnetToken(str, enum.Enum):
    ETH = web3.constants.ADDRESS_ZERO
    TERC20 = "0x776D5ee1b948e64f8BeEF2f829Fdde494c0d2776"


class GoerliTestnetNetwork(BaseNetwork[GoerliTestnetToken]):
    @property
    def native_currency(self) -> Token:
        return Token(name="Ether", symbol="ETH", decimals=18)

    @property
    def chain_id(self) -> int:
        return 5

    @property
    def dfkassa_contract_address(self) -> str:
        return dfkassa.constants.DFKASSA_CONTRACT_ADDRESS_GOERLI_TESTNET

    @property
    def oracle_contract_address(self) -> str:
        return dfkassa.constants.TOKEN_USD_ORACLE_ADDRESS_GOERLI_TESTNET
