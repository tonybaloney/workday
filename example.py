import yaml
import workday

def main():
    with open('.tenant.yml', 'r') as tenant_cfg:
        config = yaml.safe_load(tenant_cfg)

    print(config)
    client = workday.WorkdayClient(
        wsdls=config['wsdls'], 
        credentials=(config['user'], 
        config['password']), 
        proxy_url=config.get('proxy_url', None),
        disable_ssl_verification=(config['proxy_url'] != None))

    print(client.talent._client.service)

if __name__ == '__main__':
    main()
