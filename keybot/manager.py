#!/usr/bin/python3

import sys
import toml
import os
import signal
from keybot.ui import gui
from keybot.ssh import card
from keybot.ssh import key
from keybot.otp import totp


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

    if 'totp' in config:
        for name, conf in config['totp'].items():
            totp.TOTP(name, conf).run()

    if 'keys' in config:
        for name, conf in config['keys'].items():
            conf['ssh_auth_sock'] = conf.get('ssh_auth_sock', ssh_auth_sock)
            instance = key.Key(name, conf, ui)
            instance.add()

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
