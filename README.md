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
    try:
        # This call check that tha payment is
        # for 9 USD (allows 5% price movements difference)
        # and used token is what you want to accept
        await ctx.ensure_payment_is_ok(
            price_expected_amount=9,
            price_slippage_tolerance=0.05
        )
    except dfkassa.SlippageIsToHighError:
        print("Price is changed, payment USD value is too low")
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
            sep="\n"
        )


async def main():
    watcher_settings = dfkassa.DFKassaWatcherSettings(
        merchant_address="0xF621E6645BDE67bd3BDEcFA9A674Ad5e7EDad756",
        callback=callback,
        networks=[
            dfkassa.GoerliTestnetNetwork(
                w3client=dfkassa.w3_from_wss_urls(
                    "wss://some-wss-url...",
                    "wss://another-wss-url...",
                ),
                accepted=[
                    dfkassa.GoerliTestnetToken.ETH,
                ]
            )
        ]
    )
    print(
        "Redirect user with this param",
        dfkassa.build_accept_param(watcher_settings.networks)
    )
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
