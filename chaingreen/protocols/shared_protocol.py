from dataclasses import dataclass
from enum import IntEnum
from typing import List, Tuple

from chaingreen.util.ints import uint8, uint16
from chaingreen.util.streamable import Streamable, streamable
from chaingreen.util.config import load_config
from chaingreen.util.default_root import DEFAULT_ROOT_PATH


protocol_version = "0.0.32"
config = load_config(DEFAULT_ROOT_PATH, "config.yaml")
fork_id = config["FORK_ID"]

"""
Handshake when establishing a connection between two servers.
Note: When changing this file, also change protocol_message_types.py
"""


# Capabilities can be added here when new features are added to the protocol
# These are passed in as uint16 into the Handshake
class Capability(IntEnum):
    BASE = 1  # Base capability just means it supports the chaingreen protocol at mainnet


@dataclass(frozen=True)
@streamable
class Handshake(Streamable):
    network_id: str
    protocol_version: str
    fork_id: str
    software_version: str
    server_port: uint16
    node_type: uint8
    capabilities: List[Tuple[uint16, str]]
