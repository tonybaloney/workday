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

from requests_staticmock import ClassAdapter
from requests_staticmock.abstractions import BaseMockClass
from requests_staticmock.responses import StaticResponseFactory


class MockSoapClass(BaseMockClass):
    def _response(self, path):
        with open(fixture_path, 'rb') as fo:
            body = fo.read()

    def _v30(self, method, params, headers):
        return _response('fixtures/v30')


@pytest.fixture()
def client():
    client = WorkdayClient()
    client._session.mount('https://workday.com', MockSoapClass)

    return client

def test_basic_client(client):
    pass

def test_client_auth(client):
    """
    WorkdayClient should check that authentication argument is one of
    :class:`workday.auth.BaseAuthentication`
    """
    with pytest.raises(ValueError):
        workday.WorkdayClient(
            wsdls={'a': 'https://workday.com/test'},
            authentication=('username', 'password'))
