from nm_requests import NmRequests

class Tilesets(NmRequests):

    def __init__(self, token):
        super(Tilesets, self).__init__()
        self.token     = token
        self.addHeader('X-Auth-Token', self.token.raw())

    def list(self):
        self._endpoint = self._baseurl + 'tilesets/'
        self._endpoint = self._endpoint + self.token.data('u')
        req = self.request('get')
        print req.status_code
        if req.status_code == 200:
            res = self.responseToDict(req)
            return res.get('tilesets')
        else:
            raise Exception("Can't get tileset list")

    def replace(self, tileset_id, file_name, file_id):
        self._endpoint = self._baseurl + 'tiling/'
        self._endpoint = self._endpoint + self.token.data('u') + '?' + 'replace=' + tileset_id
        self.setBody({'name': file_name, 'id': file_id})
        req = self.request('post')
        if req.status_code == 200:
            res = self.responseToDict(req)
        else:
            raise Exception("Can't replace tileset")


    def create(self, file_name, file_id):
        self._endpoint = self._baseurl + 'tiling/'
        self._endpoint = self._endpoint + self.token.data('u')
        self.setBody({'name': file_name, 'id': file_id})
        req = self.request('post')
        if req.status_code == 200:
            res = self.responseToDict(req)
        else:
            raise Exception("Can't create tileset")


    def remove(self, tileset_id):
        self._endpoint = self._baseurl + 'tilesets/'
        self._endpoint = self._endpoint + self.token.data('u') + '/' + tileset_id
        req = self.request('delete')
        if req.status_code == 204:
            res = self.responseToDict(req)
        else:
            raise Exception("Can't remove tileset")

    def  job(self, property):
        self._endpoint = self._baseurl + 'tiling/'
        self._endpoint = self._endpoint + self.token.data('u')
        req = self.request('get')
        if req.status_code == 200:
            res = self.responseToDict(req)
            job = res.get('tilingJobs')[0]
            return job.get(property)
        elif req.status_code != 500:
            return 100
        else:
            raise Exception("Can't get jobs")
