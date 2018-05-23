import os

class ApiKey:

    file_name = "api.key"

    def __init__(self):
        self._apikey_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..', self.file_name)
        self._apikey = None

    def apikeyFile(self):
        return self._apikey_file

    def set(self, apikey):
        apikey_file = open(self._apikey_file, 'w')
        apikey_file.write(apikey.strip())
        apikey_file.close()

    def read(self):
        if not os.path.isfile(self._apikey_file):
            open(self._apikey_file, 'w').close()
        else:
            apikey_file = open(self._apikey_file, 'r')
            apikey_data = apikey_file.readlines()
            if len(apikey_data) > 0:
                self._apikey = apikey_data[0]

        return self._apikey