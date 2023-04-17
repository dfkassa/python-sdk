import enum

import web3.constants

import dfkassa.constants
from dfkassa.watcher.context import Token
from dfkassa.watcher.networks.base import BaseNetwork


class EthereumMainnetToken(str, enum.Enum):
    ETH = web3.constants.ADDRESS_ZERO
    USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    DAI = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
    USDT = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
    WBTC = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"



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
