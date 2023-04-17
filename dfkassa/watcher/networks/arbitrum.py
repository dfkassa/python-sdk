import enum

import web3.constants

import dfkassa.constants
from dfkassa.watcher.context import Token
from dfkassa.watcher.networks.base import BaseNetwork


class ArbitrumOneMainnetToken(str, enum.Enum):
    ETH = web3.constants.ADDRESS_ZERO
    USDC = "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8"
    DAI = "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1"
    USDT = "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9"
    ARB = "0x912CE59144191C1204E64559FE8253a0e49E6548"
    WBTC = "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f"


class ArbitrumOneMainnetNetwork(BaseNetwork[ArbitrumOneMainnetToken]):
    @property
    def native_currency(self) -> Token:
        return Token(name="Ether", symbol="ETH", decimals=18)

    @property
    def chain_id(self) -> int:
        return 42161

    @property
    def dfkassa_contract_address(self) -> str:
        return dfkassa.constants.DFKASSA_CONTRACT_ADDRESS_ARBITRUM_MAINNET

    @property
    def oracle_contract_address(self) -> str:
        return dfkassa.constants.TOKEN_USD_ORACLE_ADDRESS_ARBITRUM_MAINNET
