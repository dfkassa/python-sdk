import enum

import web3.constants

import dfkassa.constants
from dfkassa.watcher.context import Token
from dfkassa.watcher.networks.base import BaseNetwork


class PolygonMainnetToken(str, enum.Enum):
    MATIC = web3.constants.ADDRESS_ZERO
    USDC = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
    DAI = "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063"
    USDT = "0xc2132D05D31c914a87C6611C10748AEb04B58e8F"


class PolygonMainnetNetwork(BaseNetwork[PolygonMainnetToken]):
    @property
    def native_currency(self) -> Token:
        return Token(name="MATIC", symbol="MATIC", decimals=18)

    @property
    def chain_id(self) -> int:
        return 137

    @property
    def dfkassa_contract_address(self) -> str:
        return dfkassa.constants.DFKASSA_CONTRACT_ADDRESS_POLYGON_MAINNET

    @property
    def oracle_contract_address(self) -> str:
        return dfkassa.constants.TOKEN_USD_ORACLE_ADDRESS_POLYGON_MAINNET
