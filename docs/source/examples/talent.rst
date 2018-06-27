Examples for the Talent API
===========================

The following code examples are for Workday 30.1.

See https://community.workday.com/sites/default/files/file-hosting/productionapi/Talent/v30.1/Talent.html for full reference documentation.

The following examples require a file called `.tenant.yml` in your local directory with the configuration of the tenant API and the integration user.
if you wish to use a proxy, you will need to disable SSL verification.

.. code-block:: yaml

    # proxy_url: http://localhost:8888/
    user: integration_user@tenantname
    password: dfgjidfogi
    wsdls:
      talent: https://wd3-impl-services1.workday.com/ccx/service/tenantname/Talent/v30.1



Get all available Certifications
--------------------------------

.. code-block:: Python

    import yaml
    import workday
    from workday.auth import WsSecurityCredentialAuthentication


    def main():
        with open('.tenant.yml', 'r') as tenant_cfg:
            config = yaml.safe_load(tenant_cfg)

        client = workday.WorkdayClient(
            wsdls=config['wsdls'], 
            authentication=WsSecurityCredentialAuthentication(config['user'], config['password']),
            disable_ssl_verification=False, 
            )

        # print(client.talent.Get_Certification_Issuers().data)
        results = []
        for certs in client.talent.Get_Certifications():
            results.extend(certs.data['Certification'])
        print(results)


    if __name__ == '__main__':
        main()