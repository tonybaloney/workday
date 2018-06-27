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

import os

import pytest

from lxml import etree

import workday.auth

import requests.sessions
from requests_staticmock import ClassAdapter
from requests_staticmock.abstractions import BaseMockClass
from requests_staticmock.responses import StaticResponseFactory


@pytest.fixture()
def test_wsdl():
    return {"test": "https://workday.com/api/v30"}


@pytest.fixture()
def test_authentication():
    return workday.auth.AnonymousAuthentication()


@pytest.fixture()
def test_response_dict():
    return {
        "Response_Results": {
            "Page": 1,
            "Total_Pages": 2,
            "Total_Results": 200,
            "Page_Results": 100,
        },
        "Response_Data": {"TestData": [{"TestRecord": 1}]},
    }


@pytest.fixture()
def workday_client(test_authentication, test_wsdl, mocker):
    class MockSoapClass(BaseMockClass):
        base_path = "tests/fixtures/v30_1"

        def _response(self, request, path):
            with open(os.path.join(self.base_path, path), "rb") as fo:
                body = fo.read()
            return StaticResponseFactory.GoodResponse(body, request)

        def _wsdl(self, request):
            return self._response(request, "test_wsdl")

        def _api_v30(self, request, url, method, params, headers):
            if "?wsdl" in url:
                return self._wsdl(request)
            return self._response(request, method)

        def _api_test(self, request, url, method, params, headers):
            root = etree.XML(request.body)
            soap_request = root.getchildren()[0].getchildren()[0]
            assert soap_request.tag == "{urn:examples:helloservice}sayHello"
            kwargs = {}
            for arg in soap_request.getchildren():
                kwargs[arg.tag] = arg.text
            assert kwargs == {"firstName": "xavier"}
            return self._response(request, "test_soap_response")

    adapter = ClassAdapter(MockSoapClass)
    client = workday.WorkdayClient(wsdls=test_wsdl, authentication=test_authentication)
    client._session.adapters = {}
    client._session.mount("https://workday.com/", adapter)
    return client
