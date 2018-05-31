import jwt


class Token:

    def __init__(self, token):
        self.token = token
        self.decode()

    def decode(self):
        encoded_sections = self.token.split(".")
        encoded_sections.pop(0)
        self._token_data = jwt.decode(".".join(encoded_sections), verify=False)

    def raw(self):
        return self.token

    def data(self, key=None):
        if not key:
            return self._token_data
        else:
            return self._token_data.get(key)