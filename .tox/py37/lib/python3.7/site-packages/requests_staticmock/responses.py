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

from requests import Response
from io import BytesIO

__all__ = ['StaticResponseFactory']

DEFAULT_RESPONSE_HEADERS = {}
DEFAULT_GOOD_STATUS_CODE = 200
DEFAULT_BAD_STATUS_CODE = 500


class StaticResponseFactory(object):
    """
    Static factory for producing internal instances of `requests`
    Response objects
    """
    @staticmethod
    def GoodResponse(body, request, status_code=None,
                     headers=None):
        """
        Construct a Good HTTP response

        :param body: The body of the response
        :type  body: ``str``

        :param request: The HTTP request
        :type  request: :class:`requests.Request`

        :param status_code: The return status code, defaults
            to DEFAULT_GOOD_STATUS_CODE if not specified
        :type  status_code: ``int``

        :param headers: Response headers, defaults to
            DEFAULT_RESPONSE_HEADERS if not specified
        :type  headers: ``dict``

        :rtype: :class:`requests.Response`
        :returns : a Response object
        """
        response = Response()
        response.url = request.url
        response.raw = BytesIO(body)
        if status_code:
            response.status_code = status_code
        else:
            response.status_code = DEFAULT_GOOD_STATUS_CODE
        if headers:
            response.headers = headers
        else:
            response.headers = DEFAULT_RESPONSE_HEADERS
        response.request = request
        response._content = body
        return response

    @staticmethod
    def BadResponse(body, request, status_code=None,
                    headers=None):
        """
        Construct a Good HTTP response

        :param body: The body of the response
        :type  body: ``str``

        :param request: The HTTP request
        :type  request: :class:`requests.Request`

        :param status_code: The return status code, defaults
            to DEFAULT_GOOD_STATUS_CODE if not specified
        :type  status_code: ``int``

        :param headers: Response headers, defaults to
            DEFAULT_RESPONSE_HEADERS if not specified
        :type  headers: ``dict``

        :rtype: :class:`requests.Response`
        :returns : a Response object
        """
        response = Response()
        response.url = request.url
        response.raw = BytesIO(body)
        if status_code:
            response.status_code = status_code
        else:
            response.status_code = DEFAULT_BAD_STATUS_CODE
        if headers:
            response.headers = headers
        else:
            response.headers = DEFAULT_RESPONSE_HEADERS
        response.request = request
        response._content = body
        return response
