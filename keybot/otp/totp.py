import os
import threading
import pyotp


class TOTP:
    def __init__(self, name, conf):
        self._name = name
        self._secret = conf.get("secret")
        self._path = os.path.expanduser(conf.get("path"))
        self._token = pyotp.TOTP(self._secret)
        self._tmp = None

    def _generate_token(self):
        token = self._token.now()
        if token != self._tmp:
            with open(self._path, "w") as token_file:
                token_file.write(token)
                self._tmp = token

    def run(self):
        self._generate_token()
        threading.Timer(1.0, self.run).start()
