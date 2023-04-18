import collections
import enum
import typing

import web3_async_multi_provider

from dfkassa.watcher.networks.base import BaseNetwork
from dfkassa.watcher.settings import DFKassaWatcherSettings


def build_accept_param(networks: typing.List[BaseNetwork]):
    accepted = collections.defaultdict(list)
    for network in networks:
        for token in network.accepted:
            if isinstance(token, enum.Enum):
                accepted[token.name].append(str(network.chain_id))
            else:
                accepted[token].append(str(network.chain_id))

    query_param_values = []
    for token, chains in accepted.items():
        query_param_values.append(f"{token}/{','.join(chains)}/auto")

    return ";".join(query_param_values)


async def build_accept_param_for_health_nodes(networks: typing.List[BaseNetwork]):
    accepted = collections.defaultdict(list)
    for network in networks:
        try:
            is_connected = await network.w3client.is_connected()
        except web3_async_multi_provider.AllNodesAreDownError:
            continue
        else:
            for token in network.accepted:
                if isinstance(token, enum.Enum):
                    accepted[token.name].append(str(network.chain_id))
                else:
                    accepted[token].append(str(network.chain_id))

    query_param_values = []
    for token, chains in accepted.items():
        query_param_values.append(f"{token}/{','.join(chains)}/auto")

    return ";".join(query_param_values)
