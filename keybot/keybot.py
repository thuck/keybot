#!/usr/bin/python3

import sys
import toml
import os
import click
import signal
from keybot import card


@click.command()
@click.option('--config', default='~/.config/keybot/config', help='Configuration file')
def main(config):
    instances = []

    try:
        with open(os.path.expanduser(config)) as keybot_config:
             config = toml.loads(keybot_config.read())

    except FileNotFoundError as e:
        print(f"Missing configuration file: {config}")
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

    signal.pause()
    sys.exit(0)

if __name__ == "__main__":
    main()
