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

import yaml
import workday
from workday.auth import WsSecurityCredentialAuthentication


def main():
    with open('.tenant.yml', 'r') as tenant_cfg:
        config = yaml.safe_load(tenant_cfg)

    client = workday.WorkdayClient(
        wsdls=config['wsdls'], 
        authentication=WsSecurityCredentialAuthentication(config['user'], config['password']),
        disable_ssl_verification=True, 
        )

    print(client.talent.Get_Competencies().data)

if __name__ == '__main__':
    main()
