import subprocess
import pexpect
import os

class Key:
    def __init__(self, name, conf, ui):
        self._name = name
        self._ui = ui
        self._path = os.path.expanduser(conf.get('path'))
        self._ssh_auth_sock = conf.get('ssh_auth_sock')
        self._pin = conf.get('pin')
        self._remember_pin = conf.get('remember_pin') if conf.get('remember_pin') else False
        self._title = f'{self._name} {self._path}'

    def add(self):
        while self._pin is None:
            self._pin = self._ui.get_pin(title)

        try:
            os.environ['SSH_AUTH_SOCK'] = self._ssh_auth_sock # I think this will fail somedays due of changing the environ between threads
            ssh_add = pexpect.spawn(f'/usr/bin/ssh-add {self._path}')
            result = ssh_add.expect(['Enter passphrase for.*', 'Error connecting to agent:'])

            if result == 0:
                ssh_add.sendline(self._pin)
                result = ssh_add.expect(['Identity added', 'Bad passphrase'], timeout=2)

                if result == 1:
                    self._ui.show_error(f'{self._title} Bad passphrase')

            elif result == 1:
                self._ui.show_error(f'{self._title} Error connecting to agent: {self._ssh_auth_sock}')

        except pexpect.exceptions.TIMEOUT as e:
            self._ui.show_error(f'{self._title} {e}')

        except pexpect.exceptions.EOF as e:
            self._ui.show_error(f'{self._title} {e}')

        finally:
            if self._remember_pin is False:
                self._pin = None
