# Python client for Workday

This is a Python client (2.7 or 3.4+) for communicating with one of the Workday XML/SOAP APIs.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# Features

This client facilitates the authentication to a Workday SOAP API (Workday Web Services) and the parsing of data.

This client supports Anonymous, Basic HTTP and WS-Security (which is the prefered configuration in Workday)

## Supported APIs

* Talent Management API

## Example

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