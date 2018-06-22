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

from zeep.wsse.signature import Signature
from zeep.wsse.username import UsernameToken


class BaseAuthentication(object):
    @property
    def kwargs(self):
        """
        Keyword arguments to add to the instantiation of zeep.Client
        """
        return self._kwargs


class AnonymousAuthentication(BaseAuthentication):
    """
    No authentication
    """
    def __init__(self):
        self._kwargs = {}


class WsSecurityCredentialAuthentication(BaseAuthentication):
    def __init__(self, username, password):
        """
        WS-Security plaintext username/password request

        :param username: Username to authenticate as, typically user@tenant
        :type  username: ``str``

        :param password: Password for the integration user
        :type  password: ``str``
        """
        self._kwargs = {"wsse": UsernameToken(username, password)}


class WsSecurityCertificateAuthentication(BaseAuthentication):
    def __init__(
        self, private_certificate_path, public_certificate_path, optional_password=None
    ):
        """
        WS-Security X509 encoded requests

        :param private_certificate_path: The path to the x509 private cert 
        :type  private_certificate_path: ``str``

        :param public_certificate_path: The path to the x509 public cert 
        :type  public_certificate_path: ``str``

        :param optional_password: (Optional) password for the x509 private cert
        :type  optional_password: ``str``
        """
        self._kwargs = {
            "wsse": Signature(
                private_key_filename, public_key_filename, optional_password
            )
        }


class WsSecurityCertificateCredentialAuthentication(BaseAuthentication):
    def __init__(
        self,
        username,
        password,
        private_certificate_path,
        public_certificate_path,
        optional_password=None,
    ):
        """
        WS-Security X509 encoded requests with credentials

        :param username: Username to authenticate as, typically user@tenant
        :type  username: ``str``

        :param password: Password for the integration user
        :type  password: ``str``

        :param private_certificate_path: The path to the x509 private cert 
        :type  private_certificate_path: ``str``

        :param public_certificate_path: The path to the x509 public cert 
        :type  public_certificate_path: ``str``

        :param optional_password: (Optional) password for the x509 private cert
        :type  optional_password: ``str``
        """
        self._kwargs = {
            "wsse": [
                UsernameToken(username, password),
                Signature(private_key_filename, public_key_filename, optional_password),
            ]
        }
