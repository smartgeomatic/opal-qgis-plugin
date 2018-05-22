# -*- coding: utf-8 -*-
import requests, json
from qgis.core import QgsMessageLog


class NmRequests(object):

    def __init__(self):
        self._headers  = {'Content-Type': 'application/json'}
        self._body     = {}
        self._endpoint = None
        self._baseurl  = 'https://api.smartgeomatic.eu/api/v1/'

    def addHeader(self, key, value):
        self._headers[key] = value

    def setBody(self, body):
        self._body = json.dumps(body)

    def headers(self):
        return self._headers

    def body(self):
        return self._body

    def responseToDict(self, resp):
        try:
            result = json.loads(resp.text)
            return result
        except:
            return None

    def request(self, method):
        try:
            res = getattr(requests, method)(url=self._endpoint,
                                        data=self._body,
                                        headers=self._headers)
            return res
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise Exception("Can't connect")

