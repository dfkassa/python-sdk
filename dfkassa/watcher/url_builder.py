import collections
import enum
import typing

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
