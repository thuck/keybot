import sys
import toml
import os
from card import SmartCard

CONFIG_FILE = '~/.config/keybot/config'


if __name__ == "__main__":
    with open(os.path.expanduser(CONFIG_FILE)) as keybot_config:
         config = toml.loads(keybot_config.read())

    if 'cards' in config:
        cards = [SmartCard(card, parameters) for card, parameters in config['cards'].items()]
        for card in cards:
            card.start()

    for card in cards:
        card.join()
