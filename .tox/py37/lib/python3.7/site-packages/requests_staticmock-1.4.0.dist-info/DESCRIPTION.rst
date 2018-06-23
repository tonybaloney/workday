===============================
requests-staticmock
===============================

.. image:: https://img.shields.io/pypi/v/requests-staticmock.svg
        :target: https://pypi.python.org/pypi/requests-staticmock

.. image:: https://img.shields.io/travis/tonybaloney/requests-staticmock.svg
        :target: https://travis-ci.org/tonybaloney/requests-staticmock

.. image:: https://readthedocs.org/projects/requests-staticmock/badge/?version=latest
        :target: https://readthedocs.org/projects/requests-staticmock/?badge=latest
        :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/tonybaloney/requests-staticmock/badge.svg?branch=master
        :target: https://coveralls.io/github/tonybaloney/requests-staticmock?branch=master


A static HTTP mock interface for testing classes that leverage Python `requests` with **no** monkey patching!

* Free software: Apache 2 License
* Documentation: https://requests-staticmock.readthedocs.org.

Usage
-----

As a context manager for requests Session instances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `requests_staticmock`

.. code-block:: python

    import requests
    import requests_staticmock

    session = requests.Session()
    with requests_staticmock.mock_session_with_fixtures(session, 'tests/fixtures', 'http://test_context.com'):
        # will return a response object with the contents of tests/fixtures/test.json
        response = new_session.request('get', 'http://test_context.com/test.json')

As an adapter
~~~~~~~~~~~~~

You can inject the `requests_staticmock` adapter into an existing (or new) requests session to mock out a particular URL
or domain, e.g.

.. code-block:: python

    import requests
    from requests_staticmock import Adapter

    session = requests.Session()
    special_adapter = Adapter('fixtures')
    session.mount('http://specialwebsite.com', special_adapter)
    session.request('http://normal.com/api/example') # works as normal
    session.request('http://specialwebsite.com') # returns static mocks

Class adapter
~~~~~~~~~~~~~

Instead of using a static asset adapter, you can use an adapter that expects an internal method to respond with a string, e.g.

GET `/test/example.xml` will call method `_test_example_xml(self, request)`

GET `/test/example.xml?query=param` will call method `_test_example_xml(self, request)`

This can be used via `requests_staticmock.ClassAdapter` or the context manager


.. code-block:: python

    import requests
    import requests_staticmock


    class MyTestClass(requests_staticmock.BaseMockClass):
        def _api_v1_idea(self, request):
            return "woop woop"

    session = requests.Session()
    with requests_staticmock.mock_session_with_class(session, MyTestClass, 'http://test_context.com'):
        # will return a response object with the contents 'woop woop'
        response = new_session.request('get', 'http://test_context.com/api/v1/idea')

Class adapter with unpacked requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The class adapter supports unpacking of the following components, just add these keyword arguments
to your callback methods and the class adapter will match them to the arguments.

* `method` - The HTTP verb, e.g. GET
* `url` - The full URL
* `params` - The dict with the request parameters
* `headers` - The request headers
* `body` - The request body text

.. code-block:: python

    import requests
    import requests_staticmock

    class_session = Session()
    class TestMockClass(BaseMockClass):
        def _api_v1_idea(self, method, params, headers):
            if params['special'] == 'value':
                return 'yes'
        def _api_v1_brillo(self, url, body):
            if json.loads(body)['special'] == 'value':
                return 'yes'

    a = ClassAdapter(TestMockClass)

    session = requests.Session()
    with requests_staticmock.mock_session_with_class(session, MyTestClass, 'http://test_context.com'):
        response = new_session.request('get', 'http://test_context.com/api/v1/idea')

Features
--------

* Allow mocking of HTTP responses via a directory of static fixtures
* Support for sub-directories matching URL paths


Credits
---------

This project takes inspiration and ideas from the `requests_mock` package, maintained by the OpenStack foundation.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


=======
History
=======


1.4.0 (2017-09-01)
------------------

* Class adapter correctly maps - character to _ as - is invalid method name in Python

1.3.0 (2017-09-01)
------------------

* Add a property in MockClass for the adapter instance, helps when you want to respond
  with static fixture data

1.2.0 (2017-05-10)
------------------

* Add support for case-insensitive file matching

1.1.0 (2017-05-10)
------------------

* Add support for query params being part of the file path

0.8.0 (2017-02-02)
------------------

* Add support for streaming requests and iter_content/iter_lines

0.7.0 (2017-01-29)
------------------

* Add support version unpacking, class adapters now support a range of keyword arguments,
  provided in no particular order.

0.6.0 (2017-01-29)
------------------

* Add support for the class adapter methods to return either a string or
  a response object
* Moved to Py.Test

0.3.0 (2017-01-29)
------------------

* Added a class adapter

0.2.0 (2017-01-28)
------------------

* Added a context manager for the static mocks

0.1.0 (2017-01-01)
------------------

* First release on PyPI.


