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
import workday.soap
import workday.exceptions


def test_client_instantiation(workday_client):
    assert hasattr(workday_client, "test")
    assert hasattr(workday_client.test, "sayHello")
    assert isinstance(
        workday_client.test.sayHello("xavier"), workday.soap.WorkdayResponse
    )


def test_client_instantiation_bad_api(workday_client):
    """
    Test that the client doesn't have a property for an API you didn't configure
    and raises a suitable exception
    """
    assert hasattr(workday_client, "test")
    assert hasattr(workday_client.test, "sayHello")
    with pytest.raises(workday.exceptions.WsdlNotProvidedError):
        workday_client.banana


def test_ssl_verification(test_wsdl, test_authentication):
    """
    Test that the client has SSL verification enabled by default
    """
    client = workday.WorkdayClient(
        wsdls=test_wsdl,
        authentication=test_authentication,
        disable_ssl_verification=None,
    )
    assert client._session.verify == True


def test_disable_ssl_auth(test_wsdl, test_authentication):
    """
    Test that the client has SSL verification disabled if specified
    """
    client = workday.WorkdayClient(
        wsdls=test_wsdl,
        authentication=test_authentication,
        disable_ssl_verification=True,
    )
    assert client._session.verify == False


def test_proxy_configuration(test_wsdl, test_authentication):
    """
    Test that the client has a https proxy if specified
    """
    _PROXY_URL = "https://proxy.com:8888"
    client = workday.WorkdayClient(
        wsdls=test_wsdl, authentication=test_authentication, proxy_url=_PROXY_URL
    )
    assert client._session.proxies == {"https": _PROXY_URL}


def test_client_auth(test_wsdl):
    """
    WorkdayClient should check that authentication argument is one of
    :class:`workday.auth.BaseAuthentication`
    """
    with pytest.raises(ValueError):
        workday.WorkdayClient(wsdls=test_wsdl, authentication=("username", "password"))


bad_wsdl_types = (None, 1, "banana", (12,), {1, 2, 3})


@pytest.mark.parametrize("wsdl", bad_wsdl_types)
def test_bad_wsdl_types(wsdl, test_authentication):
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
