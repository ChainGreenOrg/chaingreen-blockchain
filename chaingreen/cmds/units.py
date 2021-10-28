from typing import Dict

# The rest of the codebase uses mios everywhere.
# Only use these units for user facing interfaces.
units: Dict[str, int] = {
    "chaingreen": 10 ** 12,  # 1 chaingreen (CGN) is 1,000,000,000,000 mio (1 trillion)
    "mio": 1,
    "colouredcoin": 10 ** 3,  # 1 coloured coin is 1000 colouredcoin mios
}
