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

import contextlib

from requests.compat import OrderedDict
from requests_staticmock import adapter


@contextlib.contextmanager
def mock_session_with_fixtures(session, path, url):
    """
    Context Manager

    Mock the responses with a particular session
    to any files found within a static path

    :param session: The requests session object
    :type  session: :class:`requests.Session`

    :param path: The path to the fixtures
    :type  path: ``str``

    :param url: The base URL to mock, e.g. http://mock.com, http://
        supports a single URL or a list
    :type  url: ``str`` or ``list``
    """
    _orig_adapters = session.adapters
    mock_adapter = adapter.Adapter()
    session.adapters = OrderedDict()
    if isinstance(url, (list, tuple)):
        for u in url:
            session.mount(u, mock_adapter)
    else:
        session.mount(url, mock_adapter)
    mock_adapter.register_path(path)
    yield
    session.adapters = _orig_adapters


@contextlib.contextmanager
def mock_session_with_class(session, cls, url):
    """
    Context Manager

    Mock the responses with a particular session
    to any private methods for the URLs

    :param session: The requests session object
    :type  session: :class:`requests.Session`

    :param cls: The class instance with private methods for URLs
    :type  cls: ``object``

    :param url: The base URL to mock, e.g. http://mock.com, http://
        supports a single URL or a list
    :type  url: ``str`` or ``list``
    """
    _orig_adapters = session.adapters
    mock_adapter = adapter.ClassAdapter(cls)
    session.adapters = OrderedDict()
    if isinstance(url, (list, tuple)):
        for u in url:
            session.mount(u, mock_adapter)
    else:
        session.mount(url, mock_adapter)
    yield
    session.adapters = _orig_adapters
