import os
from pathlib import Path

DEFAULT_ROOT_PATH = Path(os.path.expanduser(os.getenv("CHAINGREEN_ROOT", "~/.chaingreen/mainnet"))).resolve()
DEFAULT_KEYS_ROOT_PATH = Path(os.path.expanduser(os.getenv("CHAINGREEN_KEYS_ROOT", "~/.chaingreen_keys"))).resolve()
