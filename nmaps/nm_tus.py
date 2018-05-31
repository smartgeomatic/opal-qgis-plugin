# -*- coding: utf-8 -*-
from __future__ import print_function
from qgis.core import QgsMessageLog
import os
import base64
import argparse
import time

try:
    from urllib.parse import urlparse, urlunparse
except ImportError:
    from urlparse import urlparse, urlunparse

import requests


class TusError(Exception):
    def __init__(self, message, response=None):
        super(TusError, self).__init__(message)
        self.response = response

class NmTus:

    tus_version = '1.0.0'

    def __init__(self, endpoint, file_obj, chunk_size=1572864):
        self._endpoint        = endpoint
        self._chunk_size      = chunk_size
        self._file_obj        = file_obj
        self._file_name       = os.path.basename(file_obj.name)
        self._file_size       = self._get_file_size(file_obj)
        self._resume_endpoint = None
        self._upload_callback = None
        self._headers         = {}

    def add_header(self, key, value):
        self._headers[key] = value

    def _get_file_size(self,f):
        pos = f.tell()
        f.seek(0, os.SEEK_END)
        size = f.tell()
        f.seek(pos)
        return size

    def _upload_chunk(self, data, offset):

        headers = {
            'Content-Type': 'application/offset+octet-stream',
            'Upload-Offset': str(offset),
            'Tus-Resumable': self.tus_version,
        }

        if self._headers:
            headers.update(self._headers)

        response = requests.patch(self._resume_endpoint, headers=headers, data=data)
        if response.status_code != 204:
            raise TusError("Upload chunk failed: Status=%s" % response.status_code,
                           response=response)
        return int(response.headers["Upload-Offset"])

    def _get_offset(self):

        headers = {"Tus-Resumable": TUS_VERSION}

        if self._headers:
            headers.update(self._headers)

        response = requests.head(self._resume_endpoint, headers=headers)
        response.raise_for_status()

        offset = int(response.headers["Upload-Offset"])

        return offset

    def _absolute_file_location(self, file_endpoint):
        parsed_file_endpoint = urlparse(file_endpoint)
        if parsed_file_endpoint.netloc:
            return file_endpoint

        parsed_tus_endpoint = urlparse(self._endpoint)
        return urlunparse((
                              parsed_tus_endpoint.scheme,
                              parsed_tus_endpoint.netloc,
                          ) + parsed_file_endpoint[2:])

    def location(self):
        return self._location

    def file_id(self):
        return self._file_id

    def upload(self):
        self.create()
        self.resume()

    def upload_callback(self, upload_callback):
        self._upload_callback = upload_callback

    def create(self, metadata=None):

        headers = {
            "Tus-Resumable": self.tus_version,
            "Upload-Length": str(self._file_size),
        }

        if self._headers:
            headers.update(self._headers)

        if metadata:
            pairs = [
                k + ' ' + base64.b64encode(v.encode('utf-8')).decode()
                for k, v in metadata.items()
            ]
            headers["Upload-Metadata"] = ','.join(pairs, headers)

        response = requests.post(self._endpoint, headers=headers)
        if response.status_code != 201:
            raise TusError("Create failed: Status=%s" % response.status_code,
                           response=response)

        location = response.headers["Location"]
        self._location        = location
        self._file_id         = location.replace(self._endpoint, '')
        self._resume_endpoint = self._absolute_file_location(location)

    def progress_chunk(self, file_size):
        return 100 * self._chunk_size / file_size

    def resume(self, offset=0):
        if offset is None:
            offset = self._get_offset(self._endpoint)

        total_sent = 0
        file_size = self._get_file_size(self._file_obj)
        while offset < file_size:
            self._file_obj.seek(offset)
            data = self._file_obj.read(self._chunk_size)
            offset = self._upload_chunk(data, offset)
            total_sent += self.progress_chunk(file_size)
            self._upload_callback(total_sent,  "Wysyłanie pliku:".decode("utf-8"))
            time.sleep(0.3)





