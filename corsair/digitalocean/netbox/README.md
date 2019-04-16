# Corsair > Digital Ocean > NetBox
This is the [Digital Ocean NetBox](https://github.com/digitalocean/netbox) API wrapper.  It's based on [pynetbox](https://github.com/digitalocean/pynetbox), Digital Ocean's official API client library for NetBox.  API is well documented NetBox is self-explanatory and is available at API's root address (see below).

Prerequisites:

* NetBox 2.4.4 (the environment I had to test)
* Access credentials (token)


## Basic Usage

```python
>>> from corsair.digitalocean.netbox import Api
>>> netbox = Api('https://netbox.corp/api', 'aR3allyl000ngtok3n')
>>> netbox.ip_addresses.create(address='10.11.12.13', description='Foobar')
>>> ip = netbox.ip_addresses.read(address='10.11.12.13')[0]
>>> ip = netbox.ip_addresses.update(ip['id'], description='Desktop')
>>> ip['description']
>>> netbox.ip_addresses.delete(ip['id'])
>>> all_ips = netbox.ip_addresses.read()
```
