import enum

import web3.constants

import dfkassa.constants
from dfkassa.watcher.context import Token
from dfkassa.watcher.networks.base import BaseNetwork


class OptimismMainnetToken(str, enum.Enum):
    ETH = web3.constants.ADDRESS_ZERO
    USDC = "0x7F5c764cBc14f9669B88837ca1490cCa17c31607"
    DAI = "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1"
    USDT = "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58"
    OP = "0x4200000000000000000000000000000000000042"


class OptimismMainnetNetwork(BaseNetwork[OptimismMainnetToken]):
    @property
    def native_currency(self) -> Token:
        return Token(name="Ether", symbol="ETH", decimals=18)

    @property
    def chain_id(self) -> int:
        return 10

    @property
    def dfkassa_contract_address(self) -> str:
        return dfkassa.constants.DFKASSA_CONTRACT_ADDRESS_OPTIMISM_MAINNET

    @property
    def oracle_contract_address(self) -> str:
        return dfkassa.constants.TOKEN_USD_ORACLE_ADDRESS_OPTIMISM_MAINNET
