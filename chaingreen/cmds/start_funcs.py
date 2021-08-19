import asyncio
import os
import subprocess
import sys

from pathlib import Path
from typing import Optional

from chaingreen.cmds.passphrase_funcs import get_current_passphrase
from chaingreen.daemon.client import DaemonProxy, connect_to_daemon_and_validate
from chaingreen.util.service_groups import services_for_groups
from chaingreen.util.keychain import KeyringMaxUnlockAttempts


def launch_start_daemon(root_path: Path) -> subprocess.Popen:
    os.environ["CHAINGREEN_ROOT"] = str(root_path)
    # TODO: use startupinfo=subprocess.DETACHED_PROCESS on windows
    chaingreen = sys.argv[0]
    process = subprocess.Popen(f"{chaingreen} run_daemon --wait-for-unlock".split(), stdout=subprocess.PIPE)
    return process


async def create_start_daemon_connection(root_path: Path) -> Optional[DaemonProxy]:
    connection = await connect_to_daemon_and_validate(root_path)
    if connection is None:
        print("Starting daemon")
        # launch a daemon
        process = launch_start_daemon(root_path)
        # give the daemon a chance to start up
        if process.stdout:
            process.stdout.readline()
        await asyncio.sleep(1)
        # it prints "daemon: listening"
        connection = await connect_to_daemon_and_validate(root_path)
    if connection:
        passphrase = None
        if await connection.is_keyring_locked():
            passphrase = get_current_passphrase()

        if passphrase:
            print("Unlocking daemon keyring")
            await connection.unlock_keyring(passphrase)

        return connection
    return None


async def async_start(root_path: Path, group: str, restart: bool) -> None:
    try:
        daemon = await create_start_daemon_connection(root_path)
    except KeyringMaxUnlockAttempts:
        print("Failed to unlock keyring")
        return None

    if daemon is None:
        print("Failed to create the chaingreen daemon")
        return None

    for service in services_for_groups(group):
        if await daemon.is_running(service_name=service):
            print(f"{service}: ", end="", flush=True)
            if restart:
                if not await daemon.is_running(service_name=service):
                    print("not running")
                elif await daemon.stop_service(service_name=service):
                    print("stopped")
                else:
                    print("stop failed")
            else:
                print("Already running, use `-r` to restart")
                continue
        print(f"{service}: ", end="", flush=True)
        msg = await daemon.start_service(service_name=service)
        success = msg and msg["data"]["success"]

        if success is True:
            print("started")
        else:
            error = "no response"
            if msg:
                error = msg["data"]["error"]
            print(f"{service} failed to start. Error: {error}")
    await daemon.close()
