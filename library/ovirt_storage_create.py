#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Author: Rob Cousins - @highops <rob@highops1.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible. If not, see <http://www.gnu.org/licenses/>.

from ansible.module_utils.basic import *

try:
    from ovirtsdk.api import API
    from ovirtsdk.xml import params
except ImportError:
    module.fail_json(msg='ovirtsdk required for this module')

#---- Documentation Start ----------------------------------------------------#
DOCUMENTATION = '''
---

module: ovirt_create_storage
author: Rob Cousins - @highops
short_description: creates storage domain
description:
  - This module adds storage domain.
version_added: "1.0"
options:
  name:
    description:
      Name of storagedomain.
    default: null
    required: true
    aliases: []
  datacenter:
    description:
      Name of datacenter to add storage.
    default: Default
    required: false
    aliases: []
  host:
    description:
      Name of host to add storage.
    default: Default
    required: false
    aliases: []
  storage_url:
    description:
      Storage url. 
    default: null
    required: true
    aliases: [] 
  path:
    description:
      Path to storage.
    default: null
    required: true
    aliases: []
  type:
    description:
      Type of storage.
    default: nfs
    required: false  
    choices: [ 'nfs', 'glusterfs' ]
    aliases: []  
  storage_type:
    description:
      Type of ovirt storage domain.
    default: data
    required: false  
    choices: [ 'data', 'iso', 'export' ]
    aliases: [] 
  url:
    description:
      Url for ovirt api.
    default: null
    required: true
    aliases: []
  username:
    description:
      Username for ovirt api.
    default: admin@internal
    required: false  
    aliases: [] 
  password:
    description:
      Password for ovirt api.
    default: null
    required: true
    aliases: []      
  requirements:
    - "python >= 2.6"
    - "ovirt-engine-sdk-python"

'''

EXAMPLES = '''
- ovirt_create_storage: name=data 
                        datacenter=Default
                        host=hosted_engine_1
                        path='/data'
                        type=nfs
                        storage_type=data
                        storage_url=localhost
                        url=https://engine.example.com 
                        username=admin 
                        password=somepassword 
'''


#---- Logic Start ------------------------------------------------------------#

def ovirt_create_storage(module):
    
    name = module.params['name']
    datacenter = module.params['datacenter']
    host = module.params['host']
    path = module.params['path']
    type = module.params['type']
    storage_type = module.params['storage_type']
    storage_url = module.params['storage_url']
    username = module.params['username']
    password = module.params['password']
    url = module.params['url']
    
    try:
        api = API(url=url,username=username,password=password,insecure=True,session_timeout=60)
    except Exception as ex:
        module.fail_json(msg='could not connect to ovirt api')
  
    isoParams = params.StorageDomain(name=name,
                                   data_center=api.datacenters.get(datacenter),
                                   type_=storage_type,
                                   host=api.hosts.get(host),
                                   storage = params.Storage(   type_=type,
                                                               address=storage_url,
                                                               path=path,
                                                               ))
    
    if api.datacenters.get(datacenter).storagedomains.get(name):
         module.exit_json(changed=False)
    
    if module.check_mode:    
         module.exit_json(changed=True)
         
    try:
        sd = api.storagedomains.add(isoParams)
        api.datacenters.get(datacenter).storagedomains.add(api.storagedomains.get(name))
    except Exception as ex:
        module.fail_json(msg='Adding storage domain failed'+str(ex))
        
    module.exit_json(changed=True)
    
def main():

    # Note: 'AnsibleModule' is an Ansible utility imported below
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True,type='str'),
            datacenter=dict(required=False,type='str',default='Default'),
            host=dict(required=False,type='str',default='Default'),
            path=dict(required=True,type='str'),
            type=dict(required=False,type='str',default='nfs',choices=['nfs', 'glusterfs'] ),
            storage_type=dict(required=False,type='str',default='data',choices=['data', 'iso' , 'export']),
            storage_url=dict(required=True,type='str'),
            url=dict(required=True,type='str'),
            username=dict(required=False,type='str',default='admin@internal'),
            password=dict(required=True,type='str')
        ),
        supports_check_mode=True
    )

    ovirt_create_storage(module)        

#---- Import Ansible Utilities (Ansible Framework) ---------------------------#

main()
