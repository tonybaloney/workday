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

import six

import requests
from requests.auth import HTTPBasicAuth

from .auth import BaseAuthentication
from .exceptions import WsdlNotProvidedError
from .soap import BaseSoapApiClient


class WorkdayClient(object):
    """
    Entry point for the workday APIs.
    """

    _apis = {}
    _session = None
    _authentication = None

    def __init__(
        self, wsdls, authentication, proxy_url=None, disable_ssl_verification=False
    ):
        """
        Instantiate a Workday API client

        :param wsdls: Dictionary of WSDL endpoints to use
        :type  wsdls: ``dict``

        :param authentication: Authentication configuration
        :type  authentication: :class:`workday.auth.BaseAuthentication`

        :param credentials: (Optional) tuple of credentials, e.g. username, password depending on auth_mode
        :type  credentials: ``tuple``

        :param proxy_url: Optional URL to proxy requests through
        :type  proxy_url: ``str``
        """
        if not isinstance(authentication, BaseAuthentication):
            raise ValueError(
                "authentication argument must be of type BaseAuthentication"
            )

        if not isinstance(wsdls, dict):
            raise TypeError("WSDLs argument must be a dictionary")

        self.proxy_url = proxy_url
        self._session = requests.Session()

        if proxy_url:
            self._session.proxies = {"https": proxy_url}

        if disable_ssl_verification:
            self._session.verify = False

        self._authentication = authentication
        self._apis = {}

        for name, value in wsdls.items():
            if not isinstance(value, six.string_types):
                raise ValueError(
                    "WSDL value must be a string with the URL of the Workday Web Service."
                )
            self._apis[name] = value

    def __getattr__(self, api):
        if api not in self._apis:
            raise WsdlNotProvidedError("API '{0}' was not loaded".format(api))
        else:
            if isinstance(self._apis[api], six.string_types):
                self._apis[api] = BaseSoapApiClient(
                    name=api,
                    session=self._session,
                    wsdl_url=self._apis[api] + "?wsdl",
                    authentication=self._authentication,
                )
            return self._apis[api]
