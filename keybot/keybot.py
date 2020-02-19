#!/usr/bin/python3

import sys
import toml
import os
from keybot import card


CONFIG_FILE = '~/.config/keybot/config'

def main():
    instances = []
    try:
        with open(os.path.expanduser(CONFIG_FILE)) as keybot_config:
             config = toml.loads(keybot_config.read())

    except FileNotFoundError as e:
        print(f"Missing configuration file: {CONFIG_FILE}")
        sys.exit(1)

    if 'cards' in config:
        for name, parameters in config['cards'].items():
            try:
                instance = card.SmartCard(name, parameters)
                instance.start()
                instances.append(instance)
            except Exception as e:
                print(e)
                sys.exit(1)

    for instance in instances:
        instance.join()

if __name__ == "__main__":
    main()
