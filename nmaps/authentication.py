from nm_requests import NmRequests


class Authentication(NmRequests):

    def __init__(self, apikey_manager, client_id):
        super(Authentication, self).__init__()
        self._apikey    = apikey_manager.read()
        self._client_id = client_id

    def authenticate(self):
        self.endpoint = 'tokens'
        self.add_header('X-AUTH-TOKEN',self._apikey)
        self.body = {"clientId": self._client_id}
        req = self.request('put')
        print req
        if req.status_code == 200:
            res = self.response_dict(req)
            return res.get('token')
        else:
            raise Exception("Authentication failed")



