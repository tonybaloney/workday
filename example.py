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

    # print(client.talent.Get_Certification_Issuers().data)
    certs = client.talent.Get_Certifications()
    results = certs.data['Certification']
    for page in range(1, certs.total_pages):
        response = client.talent.Get_Certifications(Response_Filter={'Page': page+1})
        results.extend(response.data['Certification'])
    print(results)

    # print(client.talent.Get_Competencies().data)
    # print(client.talent.Get_Competency_Categories().data)
    # print(client.talent.Get_Competency_Classes().data)
    # #print(client.talent.Get_Connection_Types().data)
    # #print(client.talent.Get_Contact_Connections().data)
    # print(client.talent.Get_Degrees().data)
    # print(client.talent.Get_Development_Item_Categories().data)
    # print(client.talent.Get_Development_Item_Status().data)
    # # print(client.talent.Get_Development_Items().data)
    # print(client.talent.Get_Fields_Of_Study().data)
    # print(client.talent.Get_Job_History_Companies().data)
    # print(client.talent.Get_Language_Proficiency_Levels().data)
    # print(client.talent.Get_Languages().data)
    # #print(client.talent.Get_Mentor_Options().data)
    # #print(client.talent.Get_Mentorships().data)
    # print(client.talent.Get_Proficiency_Rating_Scales().data)


if __name__ == '__main__':
    main()
