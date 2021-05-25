from typing import KeysView, Generator

SERVICES_FOR_GROUP = {
    "all": "chaingreen_harvester chaingreen_timelord_launcher chaingreen_timelord chaingreen_farmer \
        chaingreen_full_node chaingreen_wallet".split(),
    "node": "chaingreen_full_node".split(),
    "harvester": "chaingreen_harvester".split(),
    "farmer": "chaingreen_harvester chaingreen_farmer chaingreen_full_node chaingreen_wallet".split(),
    "farmer-no-wallet": "chaingreen_harvester chaingreen_farmer chaingreen_full_node".split(),
    "farmer-only": "chaingreen_farmer".split(),
    "timelord": "chaingreen_timelord_launcher chaingreen_timelord chaingreen_full_node".split(),
    "timelord-only": "chaingreen_timelord".split(),
    "timelord-launcher-only": "chaingreen_timelord_launcher".split(),
    "wallet": "chaingreen_wallet chaingreen_full_node".split(),
    "wallet-only": "chaingreen_wallet".split(),
    "introducer": "chaingreen_introducer".split(),
    "simulator": "chaingreen_full_node_simulator".split(),
}


def all_groups() -> KeysView[str]:
    return SERVICES_FOR_GROUP.keys()


def services_for_groups(groups) -> Generator[str, None, None]:
    for group in groups:
        for service in SERVICES_FOR_GROUP[group]:
            yield service


def validate_service(service: str) -> bool:
    return any(service in _ for _ in SERVICES_FOR_GROUP.values())
