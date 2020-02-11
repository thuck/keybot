import sys
import toml
import os
from .card import SmartCard

CONFIG_FILE = '~/.config/keybot/config'


if __name__ == "__main__":
    cards = []
    try:
        with open(os.path.expanduser(CONFIG_FILE)) as keybot_config:
             config = toml.loads(keybot_config.read())

    except FileNotFoundError as e:
        print(f"Missing configuration file: {CONFIG_FILE}")
        sys.exit(1)

    if 'cards' in config:
        for name, parameters in config['cards'].items():
            try:
                cards = SmartCard(name, parameters)
            except Exception as e:
                print(e)
                sys.exit(1)
            card.start()

    for card in cards:
        card.join()
