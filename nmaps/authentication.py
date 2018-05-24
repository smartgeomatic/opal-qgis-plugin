from qt_requests import QtRequests

class Authetication(QtRequests):

    def __init__(self, apikey_manager, client_id):
        super(Authetication,self).__init__()
        self._apikey    = apikey_manager.read()
        self._client_id = client_id

    def authenticate(self):
        self._endpoint = 'tokens'
        self.addHeader('X-AUTH-TOKEN',self._apikey)
        self.setBody({"clientId": self._client_id})
        req = self.request('put')
        #if req.status_code == 200:
        res = self.responseToDict(req)
        return res.get('token')
        #else:
        #    raise Exception("Authentication failed")



