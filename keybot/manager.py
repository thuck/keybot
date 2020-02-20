#!/usr/bin/python3

import sys
import toml
import os
import signal
from keybot import card
from keybot import keys
from keybot.ui import gui


def manager(config):
    ssh_auth_sock = os.environ.get('SSH_AUTH_SOCK',)
    ui = gui.GUI()
    instances = []

    try:
        with open(os.path.expanduser(config)) as keybot_config:
             config = toml.loads(keybot_config.read())

    except FileNotFoundError as e:
        print(f'Missing configuration file: {config}')
        sys.exit(1)

    if 'general' in config:
        ssh_auth_sock = config['general'].get('ssh_auth_sock', ssh_auth_sock)

    if 'keys' in config:
        for name, conf in config['keys'].items():
            conf['ssh_auth_sock'] = conf.get('ssh_auth_sock', ssh_auth_sock)
            key = keys.Key(name, conf, ui)
            key.add()

    if 'cards' in config:
        for name, conf in config['cards'].items():
            conf['ssh_auth_sock'] = conf.get('ssh_auth_sock', ssh_auth_sock)
            try:
                instance = card.SmartCard(name, conf, ui)
                instance.start()
                instances.append(instance)
            except Exception as e:
                print(e)
                sys.exit(1)

        for instance in instances:
            instance.join()

    signal.pause()
