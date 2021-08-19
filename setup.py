from setuptools import setup

dependencies = [
    "blspy==1.0.5",  # Signature library
    "chiavdf==1.0.2",  # timelord and vdf verification
    "chiabip158==1.0",  # bip158-style wallet filters
    "chiapos==1.0.4",  # proof of space
    "clvm==0.9.7",
    "clvm_rs==0.1.10",
    "clvm_tools==0.4.3",
    "aiohttp==3.7.4",  # HTTP server for full node rpc
    "aiosqlite==0.17.0",  # asyncio wrapper for sqlite, to store blocks
    "bitstring==3.1.9",  # Binary data management library
    "colorama==0.4.4",  # Colorizes terminal output
    "colorlog==5.0.1",  # Adds color to logs
    "concurrent-log-handler==0.9.19",  # Concurrently log and rotate logs
    "cryptography==3.4.7",  # Python cryptography library for TLS - keyring conflict
    "fasteners==0.16.3",  # For interprocess file locking
    "keyring==23.0.1",  # Store keys in MacOS Keychain, Windows Credential Locker
    "keyrings.cryptfile==1.3.4",  # Secure storage for keys on Linux (Will be replaced)
    #  "keyrings.cryptfile==1.3.8",  # Secure storage for keys on Linux (Will be replaced)
    #  See https://github.com/frispete/keyrings.cryptfile/issues/15
    "PyYAML==5.4.1",  # Used for config file format
    "setproctitle==1.2.2",  # Gives the chia processes readable names
    "sortedcontainers==2.3.0",  # For maintaining sorted mempools
    "websockets==8.1.0",  # For use in wallet RPC and electron UI
    "click==7.1.2",  # For the CLI
    "dnspython==2.1.0",  # Query DNS seeds
    "watchdog==2.1.3",  # Filesystem event watching - watches keyring.yaml
]

upnp_dependencies = [
    "miniupnpc==2.2.2",  # Allows users to open ports on their router
]

dev_dependencies = [
    "pytest",
    "pytest-asyncio",
    "flake8",
    "mypy",
    "black",
    "aiohttp_cors",  # For blackd
    "ipython",  # For asyncio debugging
]

kwargs = dict(
    name="chaingreen-blockchain",
    author="Mariano Sorgente & Mio Sukakura",
    author_email="miosukakura@gmail.com",
    description="Chaingreen blockchain full node, farmer, timelord, and wallet.",
    url="https://chaingreen.org/",
    license="Apache License",
    python_requires=">=3.7, <4",
    keywords="chaingreen blockchain node",
    install_requires=dependencies,
    setup_requires=["setuptools_scm"],
    extras_require=dict(
        uvloop=["uvloop"],
        dev=dev_dependencies,
        upnp=upnp_dependencies,
    ),
    packages=[
        "build_scripts",
        "chaingreen",
        "chaingreen.cmds",
        "chaingreen.clvm",
        "chaingreen.consensus",
        "chaingreen.daemon",
        "chaingreen.full_node",
        "chaingreen.timelord",
        "chaingreen.farmer",
        "chaingreen.harvester",
        "chaingreen.introducer",
        "chaingreen.plotting",
        "chaingreen.pools",
        "chaingreen.protocols",
        "chaingreen.rpc",
        "chaingreen.server",
        "chaingreen.simulator",
        "chaingreen.types.blockchain_format",
        "chaingreen.types",
        "chaingreen.util",
        "chaingreen.wallet",
        "chaingreen.wallet.puzzles",
        "chaingreen.wallet.rl_wallet",
        "chaingreen.wallet.cc_wallet",
        "chaingreen.wallet.did_wallet",
        "chaingreen.wallet.settings",
        "chaingreen.wallet.trading",
        "chaingreen.wallet.util",
        "chaingreen.ssl",
        "mozilla-ca",
    ],
    entry_points={
        "console_scripts": [
            "chaingreen = chaingreen.cmds.chaingreen:main",
            "chaingreen_wallet = chaingreen.server.start_wallet:main",
            "chaingreen_full_node = chaingreen.server.start_full_node:main",
            "chaingreen_harvester = chaingreen.server.start_harvester:main",
            "chaingreen_farmer = chaingreen.server.start_farmer:main",
            "chaingreen_introducer = chaingreen.server.start_introducer:main",
            "chaingreen_timelord = chaingreen.server.start_timelord:main",
            "chaingreen_timelord_launcher = chaingreen.timelord.timelord_launcher:main",
            "chaingreen_full_node_simulator = chaingreen.simulator.start_simulator:main",
        ]
    },
    package_data={
        "chaingreen": ["pyinstaller.spec"],
        "": ["*.clvm", "*.clvm.hex", "*.clib", "*.clinc", "*.clsp", "py.typed"],
        "chaingreen.util": ["initial-*.yaml", "english.txt"],
        "chaingreen.ssl": ["chaingreen_ca.crt", "chaingreen_ca.key", "dst_root_ca.pem"],
        "mozilla-ca": ["cacert.pem"],
    },
    use_scm_version={"fallback_version": "unknown-no-.git-directory"},
    zip_safe=False,
)


if __name__ == "__main__":
    setup(**kwargs)
