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

import zeep
import zeep.exceptions
import zeep.transports
from zeep.wsse.username import UsernameToken

import requests
from requests.auth import HTTPBasicAuth

from .exceptions import WsdlNotProvidedError, WorkdaySoapApiError


class WorkdayClient(object):
    """
    Entry point for the workday APIs.
    """

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
        self.proxy_url = proxy_url
        self._session = requests.Session()

        if proxy_url:
            self._session.proxies = {"https": proxy_url}
        if disable_ssl_verification:
            self._session.verify = False

        self._apis = {}

        for name, value in wsdls.items():
            self._apis[name] = BaseSoapApiClient(
                name=name,
                session=self._session,
                wsdl_url=value + "?wsdl",
                authentication=authentication,
            )
            setattr(self, name, self._apis[name])


class WorkdayResponse(object):
    """
    Response from the Workday API
    """
    def __init__(self, response):
        self._response = response

    @property
    def references(self):
        return self._response['Request_References']
   
    @property
    def filter(self):
        return self._response['Response_Filter']

    @property
    def total_results(self):
        return self._response['Response_Results']['Total_Results']
    
    @property
    def total_pages(self):
        return self._response['Response_Results']['Total_Pages']

    @property
    def page_results(self):
        return self._response['Response_Results']['Page_Results']

    @property
    def page(self):
        return self._response['Response_Results']['Page']

    @property
    def data(self):
        return self._response['Response_Data']


class BaseSoapApiClient(object):
    def __init__(self, name, session, wsdl_url, authentication, proxy_url=None):
        """
        :param name: Name of this API
        :type  name: ``str``

        :param session: HTTP session to use for communication
        :type  session: :class:`requests.Session`

        :param wsdl_url: Path to the WSDL
        :type  wsdl_url: ``str``

        :param authentication: Authentication configuration
        :type  authentication: :class:`workday.auth.BaseAuthentication`

        :param proxy_url: (Optional) HTTP Proxy URL
        :type  proxy_url: ``str``
        """
        auth_kwargs = authentication.kwargs
        self._client = zeep.Client(
            wsdl=wsdl_url,
            transport=zeep.transports.Transport(session=session),
            **auth_kwargs
        )

    def __getattr__(self, attr):
        """
        :rtype: :class:`WorkdayResponse`
        """
        def call_soap_method(*args, **kwargs):
            try:
                result = getattr(self._client.service, attr)(*args, **kwargs)
                return WorkdayResponse(result)
            except zeep.exceptions.Fault as fault:
                raise WorkdaySoapApiError(fault)

        return call_soap_method
