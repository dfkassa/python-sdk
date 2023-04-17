
import web3
import web3.eth
import web3_async_multi_provider as w3amp


def w3_from_wss_urls(*urls: str):
    provider = w3amp.AsyncWSMultiProvider([web3.WebsocketProvider(url) for url in urls])
    return web3.Web3(
        provider, modules={"eth": [web3.eth.AsyncEth]}, middlewares=[]  # noqa
    )
