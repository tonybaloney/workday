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

import workday
import workday.auth
import workday.soap
import workday.exceptions

from requests_staticmock import ClassAdapter
from requests_staticmock.abstractions import BaseMockClass
from requests_staticmock.responses import StaticResponseFactory

import zeep.exceptions


class BaseAuthMockSoapClass(BaseMockClass):
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


def test_wssec_credential_authentication(test_wsdl):
    class WssecMockClass(BaseAuthMockSoapClass):
        def _api_test(self, request, url, method, params, headers):
            root = etree.XML(request.body)
            auth_header = root.getchildren()[0].getchildren()[0]
            soap_request = root.getchildren()[1].getchildren()[0]
            assert auth_header.tag == "{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd}Security"
            token = auth_header.getchildren()[0]
            assert token.tag == '{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd}UsernameToken'
            assert token.getchildren()[0].text == 'user1'
            assert token.getchildren()[1].text == 'password2'
            assert soap_request.tag == "{urn:examples:helloservice}sayHello"
            kwargs = {}
            for arg in soap_request.getchildren():
                kwargs[arg.tag] = arg.text
            assert kwargs == {"firstName": "xavier"}
            return self._response(request, "test_soap_response")

    wssec_cred = workday.auth.WsSecurityCredentialAuthentication("user1", "password2")
    client = workday.WorkdayClient(wsdls=test_wsdl, authentication=wssec_cred)
    client._session.adapters = {}
    adapter = ClassAdapter(WssecMockClass)
    client._session.mount("https://workday.com/", adapter)
    assert hasattr(client, "test")
    assert hasattr(client.test, "sayHello")
    assert isinstance(
        client.test.sayHello("xavier"), workday.soap.WorkdayResponse
    )


def test_wssec_signature_authentication(test_wsdl):
    class WssecMockClass(BaseAuthMockSoapClass):
        def _api_test(self, request, url, method, params, headers):
            root = etree.XML(request.body)
            auth_header = root.getchildren()[0].getchildren()[0]
            soap_request = root.getchildren()[1].getchildren()[0]
            assert auth_header.tag == "{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd}Security"
            token = auth_header.getchildren()[0]
            assert token.tag == '{http://www.w3.org/2000/09/xmldsig#}Signature'
            info, value, keyinfo = token.getchildren()
            assert info.text == '\n'
            assert '==' in value.text
            assert keyinfo.text == '\n'
            assert soap_request.tag == "{urn:examples:helloservice}sayHello"
            kwargs = {}
            for arg in soap_request.getchildren():
                kwargs[arg.tag] = arg.text
            assert kwargs == {"firstName": "xavier"}
            return self._response(request, "test_soap_response")

    wssec_cred = workday.auth.WsSecurityCertificateAuthentication("tests/fixtures/privatekey.key", "tests/fixtures/certificate.crt")
    client = workday.WorkdayClient(wsdls=test_wsdl, authentication=wssec_cred)
    client._session.adapters = {}
    adapter = ClassAdapter(WssecMockClass)
    client._session.mount("https://workday.com/", adapter)

    #  I provided bad certs in the tests.. this should send but fail
    with pytest.raises(zeep.exceptions.SignatureVerificationFailed):
        assert hasattr(client, "test")
        assert hasattr(client.test, "sayHello")
        assert isinstance(
            client.test.sayHello("xavier"), workday.soap.WorkdayResponse
        )


@pytest.mark.xfail(reason="See #1")
def test_wssec_signature_cred_authentication(test_wsdl):
    class WssecMockClass(BaseAuthMockSoapClass):
        def _api_test(self, request, url, method, params, headers):
            root = etree.XML(request.body)
            auth_header = root.getchildren()[0].getchildren()[0]
            soap_request = root.getchildren()[1].getchildren()[0]
            assert auth_header.tag == "{http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd}Security"
            token = auth_header.getchildren()[0]
            assert token.tag == '{http://www.w3.org/2000/09/xmldsig#}Signature'
            info, value, keyinfo = token.getchildren()
            assert info.text == '\n'
            assert '==' in value.text
            assert keyinfo.text == '\n'
            assert soap_request.tag == "{urn:examples:helloservice}sayHello"
            kwargs = {}
            for arg in soap_request.getchildren():
                kwargs[arg.tag] = arg.text
            assert kwargs == {"firstName": "xavier"}
            return self._response(request, "test_soap_response")

    wssec_cred = workday.auth.WsSecurityCertificateCredentialAuthentication("user1", "password2", "tests/fixtures/privatekey.key", "tests/fixtures/certificate.crt")
    client = workday.WorkdayClient(wsdls=test_wsdl, authentication=wssec_cred)
    client._session.adapters = {}
    adapter = ClassAdapter(WssecMockClass)
    client._session.mount("https://workday.com/", adapter)
    #  I provided bad certs in the tests.. this should send but fail
    with pytest.raises(zeep.exceptions.SignatureVerificationFailed):
        assert hasattr(client, "test")
        assert hasattr(client.test, "sayHello")
        assert isinstance(
            client.test.sayHello("xavier"), workday.soap.WorkdayResponse
        )
