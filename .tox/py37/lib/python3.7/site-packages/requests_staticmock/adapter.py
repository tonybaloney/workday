# -*- coding: utf-8 -*-
# Licensed to Anthony Shaw (anthonyshaw@apache.org) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os.path
import os
import six
import inspect
from six import b
from six.moves.urllib.parse import (parse_qsl, urlparse, quote)

from requests.adapters import BaseAdapter
from requests_staticmock.responses import StaticResponseFactory
from requests_staticmock.abstractions import BaseMockClass

__all__ = [
    'Adapter',
    'ClassAdapter'
]

BASE_PATH = os.getcwd()


class Adapter(BaseAdapter):
    """
    A replacement session adapter that responds with the content
    of static files matching the path of the requested URL
    """
    def __init__(self, base_path=None):
        """
        :param base_path: Use the given base_path as the search path
        :type  base_path: ``str``
        """
        self.paths = []
        if base_path:
            self.register_path(base_path)

    def match_url(self, request):
        """
        Match the request against a file in the adapter directory

        :param request: The request
        :type  request: :class:`requests.Request`

        :return: Path to the file
        :rtype: ``str``
        """
        parsed_url = urlparse(request.path_url)
        path_url = parsed_url.path
        query_params = parsed_url.query
        match = None

        for path in self.paths:
            for item in self.index:
                target_path = os.path.join(BASE_PATH, path, path_url[1:])

                query_path = target_path.lower() + quote(
                    '?' + query_params).lower()
                if target_path.lower() == item[0]:
                    match = item[1]
                    break
                elif query_path == item[0]:
                    match = item[1]
                    break
        return match

    def response_from_fixture(self, request, fixture_path):
        with open(fixture_path, 'rb') as fo:
                body = fo.read()
        return StaticResponseFactory.GoodResponse(body=body,
                                                  request=request)

    def send(self, request, **kwargs):
        match = self.match_url(request)
        if match:
            return self.response_from_fixture(request=request,
                                              fixture_path=match)
        else:
            return StaticResponseFactory.BadResponse(status_code=404,
                                                     request=request,
                                                     body=b("'Not found.'"))

    def close(self):  # pragma: no cover
        # Hides NotImplementedError in base class
        pass

    def register_path(self, path):
        """
        Register a new search path

        :param path: The new search path
        :type  path: ``str``
        """
        self.paths.append(path)
        self._reindex()

    def _reindex(self):
        """
        Create a case-insensitive index of the paths
        """
        self.index = []
        for path in self.paths:
            target_path = os.path.normpath(os.path.join(BASE_PATH,
                                                        path))
            for root, subdirs, files in os.walk(target_path):
                for f in files:
                    self.index.append(
                        (os.path.join(root, f).lower(),
                         os.path.join(root, f)))


class ClassAdapter(Adapter):
    """
    A requests Adapter for a class that has methods matching the
    URLS, e.g. `def _api_v1_test()` would be called for
    session.get('api/v1/test')
    """

    def __init__(self, cls):
        """
        Create a new class adapter for a given class type

        :param cls: A class type
        :type  cls: ``class``
        """
        if not issubclass(cls, BaseMockClass):
            raise TypeError("Must be BaseMockClass")

        cls = cls(adapter=self)
        self.cls = cls

    def send(self, request, **kwargs):
        parsed_url = urlparse(request.path_url)
        method_name = parsed_url.path.replace(
            '/', '_').replace('.', '_').replace('-', '_')

        if hasattr(self.cls, method_name):
            match = getattr(self.cls, method_name)
            spec = inspect.getargspec(match)
            kwargs = {}
            if 'request' in spec.args:
                kwargs['request'] = request
            if 'method' in spec.args:
                kwargs['method'] = request.method
            if 'params' in spec.args:
                kwargs['params'] = dict(parse_qsl(parsed_url.query))
            if 'headers' in spec.args:
                kwargs['headers'] = request.headers
            if 'url' in spec.args:
                kwargs['url'] = request.url
            if 'body' in spec.args:
                kwargs['body'] = request.body
            response = match(**kwargs)
            if isinstance(response, six.string_types):
                return StaticResponseFactory.GoodResponse(
                    body=b(response),
                    request=request)
            else:
                return response
        else:
            return StaticResponseFactory.BadResponse(status_code=404,
                                                     request=request,
                                                     body=b("Not found."))
