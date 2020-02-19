#!/usr/bin/python3

import sys
import toml
import os
import signal
from keybot import card
from keybot import keys


def manager(config):
    instances = []

    try:
        with open(os.path.expanduser(config)) as keybot_config:
             config = toml.loads(keybot_config.read())

    except FileNotFoundError as e:
        print(f'Missing configuration file: {config}')
        sys.exit(1)

    if 'keys' in config:
        for name, conf in config['keys'].items():
            key = keys.Key(name, conf)
            key.add()

    if 'cards' in config:
        for name, conf in config['cards'].items():
            try:
                instance = card.SmartCard(name, conf)
                instance.start()
                instances.append(instance)
            except Exception as e:
                print(e)
                sys.exit(1)

        for instance in instances:
            instance.join()

    signal.pause()
