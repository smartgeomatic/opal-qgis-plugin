import os
import base64
import hashlib
from uuid import getnode as get_mac
from Crypto import Random
from Crypto.Cipher import AES

class ApiKey:

    file_name = "api.key"

    def __init__(self):
        self._apikey_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..', self.file_name)
        self._apikey = None
        self.bs = 32
        self.key = hashlib.sha256(str(get_mac())).digest()

    def apikeyFile(self):
        return self._apikey_file

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    def set(self, apikey):
        apikey_file = open(self._apikey_file, 'w')
        apikey_file.write(self.encrypt(apikey.strip()))
        apikey_file.close()

    def read(self):
        if not os.path.isfile(self._apikey_file):
            open(self._apikey_file, 'w').close()
        else:
            apikey_file = open(self._apikey_file, 'r')
            apikey_data = apikey_file.readlines()
            if len(apikey_data) > 0:
                self._apikey = self.decrypt(apikey_data[0])

        return self._apikey