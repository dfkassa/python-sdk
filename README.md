# DFKassa Python SDK
> DFKassa Python SDK
This repository contains abstraction over DFKassa solution for Python.

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dfkassa)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/dfkassa)
![PyPI](https://img.shields.io/pypi/v/dfkassa)
[![Coverage Status](https://coveralls.io/repos/github/dfkassa/python-sdk/badge.svg?branch=main)](https://coveralls.io/github/dfkassa/python-sdk?branch=main)
***

## Overview
For example, you want to accept `ETH` in `Goerli Testnet`

```python
import asyncio

import dfkassa


async def callback(
    ctx: dfkassa.NewPaymentContext
):
    # We recommend you to save transaction hash
    # (ctx.receipt["transactionHash"])
    # to prevent double receiveing
    try:
        await ctx.ensure_payment_is_ok(
            price_expected_amount=0.1,
            price_slippage_tolerance=0.05
        )
    except dfkassa.SlippageIsToHighError:
        print("Price are changed, payment USD value is too low")
    except dfkassa.TokenIsNotAcceptedError:
        print("This token should not be accepted, user added it by himself")
    else:
        payment_as_usd = await ctx.fetch_payment_as_usd_e2()
        payment_token = await ctx.fetch_payment_token()
        print(
            "[ New Payment ]",
            f"USD: {payment_as_usd.amount / 100}",
            f"Amount: {ctx.args.amount / 10 ** payment_token.decimals}",
            f"Token: {payment_token.symbol}",
            f"Payload: {ctx.args.payload}",
            f"Block: {ctx.receipt['blockNumber']}",
            sep="\n"
        )


async def from_block_shifted_callback(network, block_number):
    # Save the block number you then should start with.
    # This block number integer will used in main()
    # for other runs
    print(
        "from_block updated for chain",
        network.chain_id,
        ":",
        block_number
    )


async def main():
    watcher_settings = dfkassa.DFKassaWatcherSettings(
        merchant_address="0x13BCAC23aC6916a348E2E61f0aCa7Fb3713b058A",
        callback=callback,
        networks=[
            dfkassa.GoerliTestnetNetwork(
                w3client=dfkassa.w3_from_https_urls(
                    "https://rpc.ankr.com/eth_goerli",
                    "https://rpc.goerli.eth.gateway.fm"
                ),
                accepted=[
                    dfkassa.GoerliTestnetToken.ETH,
                    dfkassa.GoerliTestnetToken.TERC20
                ],
                # Do not forget to save latest from_block
                # number for specific chain from callback and add it here
                # from_block=<some number>
            ),
        ],
        on_block_number_shifted=from_block_shifted_callback
    )
    print(await dfkassa.build_accept_param_for_health_nodes(watcher_settings.networks))
    await watcher_settings.coroutine_run_watching()


asyncio.run(main())
```
Within a successful payment it will show
```
[ New Payment ]
USD: 8.99
Amount: 0.004324823042657171
Token: ETH
Payload: 0
Block: 864532
```

# Installation
Via PyPI:
```shell
python -m pip install dfkassa
```
Or via GitHub
```shell
python -m pip install https://github.com/dfkassa/python-sdk/archive/main.zip
```
# Contributing
Check out [site Contributing section](https://dfkassa.github.io/python-sdk/latest/contributing/)
