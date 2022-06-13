import os
import threading
import pyotp
import time


class TOTP(threading.Thread):
    def __init__(self, name, conf):
        self._name = name
        self._secret = conf.get('secret')
        self._path = os.path.expanduser(conf.get('path'))
        self._token = pyotp.TOTP(self._secret)
        self._tmp = None
        self._stop = False

    def _generate_token(self):
        token = self._token.now()
        if token != self._tmp:
            with open(self._path, 'w') as token_file:
                token_file.write(token)
                self._tmp = token

    def run(self):
        while self._stop is False:
            self._generate_token()
            time.sleep(1)

    def stop(self):
        self._stop = True
