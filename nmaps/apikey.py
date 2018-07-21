import os
import random
from uuid import getnode as get_mac

class ApiKey:

    file_name = "api.key"

    def __init__(self):
        self._apikey_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..', self.file_name)
        self._apikey = None
        self.key = "abcdefghijklmnopqrstuvwxyz012356789"
        self.n = 5

    def apikeyFile(self):
        return self._apikey_file

    def encrypt(self, plaintext):
        result = ''
        for l in plaintext:
            try:
                i = (self.key.index(l) + self.n) % len(self.key)
                result += self.key[i]
            except ValueError:
                result += l

        return result

    def decrypt(self, ciphertext):
        result = ''
        for l in ciphertext:
            try:
                i = (self.key.index(l) - self.n) % len(self.key)
                result += self.key[i]
            except ValueError:
                result += l

        return result

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