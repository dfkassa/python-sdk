import enum

import web3.constants

import dfkassa.constants
from dfkassa.watcher.context import Token
from dfkassa.watcher.networks.base import BaseNetwork


class BSCMainnetToken(str, enum.Enum):
    BNB = web3.constants.ADDRESS_ZERO
    BUSD = "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56"
    USDC = "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"
    DAI = "0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3"
    USDT = "0x55d398326f99059fF775485246999027B3197955"


class BSCMainnetNetwork(BaseNetwork[BSCMainnetToken]):
    @property
    def native_currency(self) -> Token:
        return Token(name="Binance Coin", symbol="BNB", decimals=18)

    @property
    def chain_id(self) -> int:
        return 56

    @property
    def dfkassa_contract_address(self) -> str:
        return dfkassa.constants.DFKASSA_CONTRACT_ADDRESS_BSC_MAINNET

    @property
    def oracle_contract_address(self) -> str:
        return dfkassa.constants.TOKEN_USD_ORACLE_ADDRESS_BSC_MAINNET
