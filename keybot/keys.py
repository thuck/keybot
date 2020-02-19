import subprocess
import pexpect
import os
from keybot import ui

class Key:
    def __init__(self, name, conf):
        self._name = name
        self._path = os.path.expanduser(conf.get('path'))
        self._pin = conf.get('pin')
        self._remember_pin = conf.get('remember_pin') if conf.get('remember_pin') else False

    def add(self):
        title = f'{self._name} {self._path}'

        while self._pin is None:
            self._pin = ui.get_pin(title)

        ssh_add = pexpect.spawn(f'/usr/bin/ssh-add {self._path}')
        ssh_add.expect('Enter passphrase for.*')
        ssh_add.sendline(self._pin)

        try:
            ssh_add.expect('Identity added', timeout=2)
            result = ssh_add.read().strip().decode('utf-8')

        except pexpect.exceptions.TIMEOUT as e:
            result = str(e)

        if 'Identity added:' not in result:
            ui.show_error(result)

        else:
            if self._remember_pin is False:
                self._pin = None

