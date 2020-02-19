import sys
import click
import daemon
from keybot import manager


@click.command()
@click.option('-c', '--config', default='~/.config/keybot/config', help='Configuration file')
@click.option('-d', '--daemon', 'dm', default=False, is_flag=True, help='Run as daemon')
def main(config, dm):
    if dm is True:
        with daemon.DaemonContext():
            manager.manager(config)

    else:
        manager.manager(config)

    sys.exit(0)

if __name__ == '__main__':
    main()
