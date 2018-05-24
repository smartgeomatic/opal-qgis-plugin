# -*- coding: utf-8 -*-
from PyQt4.QtCore import QUrl, QObject, QEventLoop, pyqtSignal, QSettings, \
    QBuffer, qDebug, QByteArray, QEventLoop
from PyQt4.QtNetwork import QNetworkRequest, QNetworkAccessManager, \
    QHttpMultiPart, QHttpPart, QNetworkReply, QHttpMultiPart, QHttpPart
from functools import partial
from urllib import urlencode

import json

class QtRequests(object):

    def __init__(self):
        self._headers  = {'Content-Type': 'application/json'}
        self._body     = {}
        self._endpoint = None
        self._baseurl  = 'https://api.smartgeomatic.eu/api/v1/'

    def formatUrl(self):
        url = QUrl(self._baseurl + self._endpoint)
        return url

    def addHeader(self, key, value):
        self._headers[key] = value

    def setBody(self, body):
        self._body = body

    def headers(self):
        return self._headers

    def body(self):
        return json.dumps(self._body)

    def responseToDict(self, resp):
        try:
            result = json.loads(resp)
            return result
        except:
            return None


    def request(self, method):
        request = QNetworkRequest(self.formatUrl())
        for k, v in self.headers().items():
            request.setRawHeader(k, v)

        databyte = QByteArray()
        databyte.append(self.body())

        self.manager = QNetworkAccessManager()
        res = self.manager.put(request, databyte)
        self.loop = QEventLoop()
        self.manager.finished.connect(self.loop.exit)
        self.loop.exec_()
        bytarray = res.readAll()
        content = str(bytarray)
        return content

