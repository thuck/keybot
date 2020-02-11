import threading
import time
import subprocess
import PyKCS11
import pexpect
from .ui import get_pin
from .ui import show_error


class SmartCard(threading.Thread):
    def __init__(self, name, conf):
        super().__init__()
        self._name = name
        self._lib = conf.get('path')
        self._token_serial_number = conf.get('token_serial_number')
        self._pin = str(conf.get('pin')) if conf.get('pin') else None
        self._remember_pin = conf.get('remember_pin') if conf.get('remember_pin') else False
        self._card = PyKCS11.PyKCS11Lib()
        self._card.load(conf.get('path'))
        self._stop = False
        self._state = False
        self._model = None
        self._manufacturer = None
        self._slot = None

    def _present(self):
        state = False
        for slot in self._card.getSlotList(True):
            try:
                info = self._card.getTokenInfo(slot)
                if self._token_serial_number == info.serialNumber.strip():
                    state = True
                    self._model = info.model.strip()
                    self._manufacturer = info.manufacturerID.strip()
                    self._slot = slot
            except PyKCS11.PyKCS11Error as e:
                pass

        return state

    def _check_pin(self):
        correct = False
        try:
            session = self._card.openSession(self._slot)
            session.login(self._pin)
            session.logout()
            correct = True

        except PyKCS11.PyKCS11Error as e:
            show_error("Wrong pin")

        return correct

    def _add_key(self):
        title = f'{self._name}  {self._manufacturer}:{self._model}:{self._token_serial_number}'
        self._remove_key(show=False)
        while True:
            if self._pin is None:
                self._pin = get_pin(title)

            if self._pin is not None:
                if self._check_pin() is True:
                    ssh_add = pexpect.spawn(f'/usr/bin/ssh-add -s {self._lib}')
                    ssh_add.expect('Enter passphrase for PKCS#11:.*')
                    ssh_add.sendline(self._pin)
                    result = ssh_add.read().strip().decode('utf-8')
                    if 'Card added:' not in result:
                        show_error(result)

                    else:
                        if self._remember_pin is False:
                            self._pin = None
                        break
                else:
                    self._pin = None

            else:
                break

    def _remove_key(self, show=True):
        result = subprocess.run(['/usr/bin/ssh-add', '-e', f'{self._lib}'],
                            capture_output=True).stderr.strip().decode('utf-8')

        if 'Card removed:' not in result and show is True:
            show_error(result)

    def run(self):
        state = None
        while self._stop is False:
            state = self._present()
            if state != self._state:
                if state is True:
                    self._add_key()

                else:
                    self._remove_key()

                self._state = state

            time.sleep(0.1)

    def stop(self):
        self._stop = True
