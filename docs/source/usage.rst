Usage
=====

In this simple example, a client is instantiated with the endpoint to an API called 'talent'.

The `Get_Languages` method is called on that API and the data return is printed on the screen.

.. code-block:: python

    import workday
    from workday.auth import WsSecurityCredentialAuthentication

    client = workday.WorkdayClient(
        wsdls={'talent': 'https://workday.com/tenant/434$sd.xml'}, 
        authentication=WsSecurityCredentialAuthentication('user', 'password'), 
        )

    print(client.talent.Get_Languages().data)
