#!/usr/bin/env python3
import argparse
from pathlib import Path
import os
import requests
import sys


SSH_STAMP = "#SSH ID - @{}"
SSH_URL = "https://sshid.io/{}"


def sshKeyTransform(text: str) -> list[str]:
    retval: list[str] = list()
    for item in text.split("\n"):
        item = item.rstrip()
        if item:
            retval.append(item)
    return retval


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", required=True, help="sshid.io id")
    args = parser.parse_args()

    if not args.user:
        sys.exit(1)

    ssh_url = SSH_URL.format(args.user)
    ssh_stamp = SSH_STAMP.format(args.user)

    res = requests.get(ssh_url)
    res.raise_for_status()
    items = sshKeyTransform(res.text)

    home_dir = Path.home()
    auth_keys = os.path.join(home_dir, ".ssh", "authorized_keys")
    current_items: list[str] = []

    if os.path.exists(auth_keys):
        with open(auth_keys) as file:
            for line in file:
                line = line.rstrip()
                if ssh_stamp not in line:
                    current_items.append(line)
                else:
                    print(f"Removed: {line}")

    current_items.extend(items)
    for item in items:
        print(f"Added: {item}")

    with open(auth_keys, "w") as file:
        for item in current_items:
            file.write(f"{item}\n")
    print("Success!")
    sys.exit(0)
