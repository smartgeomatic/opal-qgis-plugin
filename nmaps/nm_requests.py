# -*- coding: utf-8 -*-
import requests, json

class NmRequests(object):

    def __init__(self):
        self._headers  = {'Content-Type': 'application/json'}
        self._body     = {}
        self._endpoint = None
        self._baseurl  = 'https://api.smartgeomatic.eu/api/v1/'

    @property
    def endpoint(self):
        return self._endpoint

    @endpoint.setter
    def endpoint(self, endpoint):
        self._endpoint = self._baseurl + endpoint

    @property
    def headers(self):
        return self._headers

    def add_header(self, key, value):
        self._headers[key] = value

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body):
        self._body = json.dumps(body)

    def response_dict(self, resp):
        try:
            result = json.loads(resp.text)
            return result
        except:
            return None

    def request(self, method):
        try:
            res = getattr(requests, method)(url=self.endpoint,
                                        data=self.body,
                                        headers=self.headers)
            return res

        except requests.exceptions.RequestException as e:
            raise Exception("Can't connect")

