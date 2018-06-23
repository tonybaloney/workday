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

import pytest

import workday
import workday.auth

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
def workday_client(test_authentication, test_wsdl):
    class MockSoapClass(BaseMockClass):
        def _response(self, path):
            with open(fixture_path, "rb") as fo:
                body = fo.read()

        def _v30(self, method, params, headers):
            return _response("fixtures/v30")

    client = workday.WorkdayClient(wsdls=wsdls, authentication=authentication)
    client._session.mount("https://workday.com", MockSoapClass)
    return client


def test_client_auth(test_wsdl):
    """
    WorkdayClient should check that authentication argument is one of
    :class:`workday.auth.BaseAuthentication`
    """
    with pytest.raises(ValueError):
        workday.WorkdayClient(
            wsdls=test_wsdl,
            authentication=("username", "password"),
        )


bad_wsdl_types = (None, 1, "banana", (12,), {1, 2, 3})


@pytest.mark.parametrize("wsdl", bad_wsdl_types)
def test_bad_wsdl_values(wsdl, test_authentication):
    """
    Workday client should only accept a valid dictionary for the value
    of `wsdls`
    """
    with pytest.raises(TypeError):
        workday.WorkdayClient(wsdls=wsdl, authentication=test_authentication)


bad_wsdl_values = (
    {1: None},
    {"place": None},
    {"place": 1},
    {"place": dict()},
    {"place": (1,)},
)


@pytest.mark.parametrize("wsdl", bad_wsdl_values)
def test_bad_wsdl_values(wsdl, test_authentication):
    """
    Workday client should only accept a valid dictionary for the value
    of `wsdls`
    """
    with pytest.raises(ValueError):
        workday.WorkdayClient(wsdls=wsdl, authentication=test_authentication)
