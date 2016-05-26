# ovirt_storage_add role

This role will add storage domains to ovirt 3.6 hosted engine.

##Requirements
Centos 7
Ansible 1.4 and a above

##Role variables
```yaml
ovirt_storage_add:
      - {
        type: #storage to use can be nfs glusterfs

        host: hosted_engine_1 #Name of host to attach data domain.

        datacenter: Default #The datacenter the domain belongs to.

        storage_type: data #Domain storage type can be data export, iso.

        path: '/data' #Path to storage domain.

        storage_url: 192.168.15.51 # ip or fqdn of storage.

        engine_fqdn: https://engine.example.com.com # Hosted engine. username

        engine_password: somepassword # hosted engine password.

        engine_user: admin@internal # hosted engine username.
        }
```
## Example Playbook
```yaml
- hosts: ovirt_host
  roles:
    - HighOps.ovirt_storage_add
```

See defaults for values.
