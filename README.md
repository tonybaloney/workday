# Python client for Workday

This is a Python client (2.7 or 3.4+) for communicating with one of the Workday XML/SOAP APIs.

[![PyPI version](https://badge.fury.io/py/workday.svg)](https://badge.fury.io/py/workday)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# Features

This client 
* facilitates the authentication to a Workday SOAP API (Workday Web Services) and the parsing of data.
* supports Anonymous, Basic HTTP and WS-Security (which is the prefered configuration in Workday)
* allows the setup of multiple WWS endpoints

# Configuring WSDLs

The first parameter of the `WorkdayClient` constructor is a dictionary. This dictinary contains all the APIs you want to access and the endpoints of them.

The key used in the dictionary will then become a *property* of the client instance with the methods for that API.

```python
import workday

apis = {
    'talent': 'https://workday.com/tenant/434$sd.xml',
    'hcm': 'https://workday.com/tenant/hcm$sd.xml'
}

client = workday.WorkdayClient(
    wsdls=apis, 
    authentication=... 
    )

users = client.hcm.Get_Users()
```

Any calls to an API method will return an instance of `workday.client.WorkdayResponse`. If you want to page results, the paging data is in the response.

The data will be in the `data` property of any API response.

# Authentication Examples

All authentication methods are in the `workday.auth` module and the instance of them should be passed to the `WorkdayClient` constructor as the `authentication` argument.

## No authentication

```python
from workday.auth import AnonymousAuthentication

anon = AnonymousAuthentication()

client = workday.WorkdayClient(
    authentiation=anon,
    ...
)
```


## WS-Security username/password

```python
from workday.auth import WsSecurityCredentialAuthentication

auth = WsSecurityCredentialAuthentication('my_user@tenant_name', 'mypassword')

client = workday.WorkdayClient(
    authentiation=auth,
    ...
)
```

## WS-Security X509-only authentication

```python
from workday.auth import WsSecurityCertificateAuthentication

auth = WsSecurityCertificateAuthentication('/path/to/private.key', '/path/to/public.key')

client = workday.WorkdayClient(
    authentiation=auth,
    ...
)
```

## WS-Security X509-only signed credentials (Recommended by Workday)

```python
from workday.auth import WsSecurityCertificateCredentialAuthentication

auth = WsSecurityCertificateCredentialAuthentication(
    'user@tenant',
    'password',
    '/path/to/private.key',
    '/path/to/public.key')

client = workday.WorkdayClient(
    authentiation=auth,
    ...
)
```

# Example

This simple example returns a list of dictionaries back from the Workday API for each configured language.

```python

import workday
from workday.auth import WsSecurityCredentialAuthentication

client = workday.WorkdayClient(
    wsdls={'talent': 'https://workday.com/tenant/434$sd.xml'}, 
    authentication=WsSecurityCredentialAuthentication(config['user'], config['password']), 
    )

print(client.talent.Get_Languages().data)
```

# Credits

This module was written by Anthony Shaw at Dimension Data

# Contributions

Always welcome. See CONTRIBUTING.rst