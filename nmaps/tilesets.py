from nm_requests import NmRequests


class Tilesets(NmRequests):

    def __init__(self, token):
        super(Tilesets, self).__init__()
        self.token = token
        self.add_header('X-Auth-Token', self.token.raw())

    def list(self):
        self.endpoint = 'tilesets/%s' % (self.token.data('u'))
        req = self.request('get')
        print req.status_code
        if req.status_code == 200:
            res = self.response_dict(req)
            return res.get('tilesets')
        else:
            raise Exception("Can't get tileset list")

    def replace(self, tileset_id, file_name, file_id):
        self.endpoint = 'tiling/%s?replace=%s' % (self.token.data('u'), tileset_id)
        self.body = {'name': file_name, 'id': file_id}
        req = self.request('post')
        if req.status_code == 200:
            res = self.response_dict(req)
        else:
            raise Exception("Can't replace tileset")

    def create(self, file_name, file_id):
        self.endpoint = 'tiling/%s' % (self.token.data('u'))
        self.body = {'name': file_name, 'id': file_id}
        print self.endpoint
        req = self.request('post')
        if req.status_code == 200:
            res = self.response_dict(req)
        else:
            raise Exception("Can't create tileset")

    def remove(self, tileset_id):
        self.endpoint = 'tilesets/%s/%s' % (self.token.data('u'), tileset_id)
        req = self.request('delete')
        if req.status_code == 204:
            res = self.response_dict(req)
        else:
            raise Exception("Can't remove tileset")

    def job(self, property):
        self.endpoint = 'tiling/%s' % (self.token.data('u'))
        req = self.request('get')
        if req.status_code == 200:
            res = self.response_dict(req)
            job = res.get('tilingJobs')[0]
            return job.get(property)
        elif req.status_code != 500:
            return job.get(property)
        else:
            raise Exception("Can't get jobs")

    def jobs(self):
        self.endpoint = 'tiling/%s' % (self.token.data('u'))
        req = self.request('get')
        if req.status_code == 200:
            res = self.response_dict(req)
            jobs = res.get('tilingJobs')
            return jobs
        elif req.status_code != 500:
            return jobs
        else:
            raise Exception("Can't get jobs")

    def hide(self, job_id):
        self.endpoint = 'tiling/%s/%s' % (self.token.data('u'), job_id)
        self.body = {'hidden': True}
        req = self.request('put')
        if req.status_code == 200:
            res = self.response_dict(req)
        else:
            raise Exception("Can't hide notification")
