# Corsair > Digital Ocean > NetBox
This is the [Digital Ocean NetBox](https://github.com/digitalocean/netbox) API wrapper.  It's based on [pynetbox](https://github.com/digitalocean/pynetbox), Digital Ocean's official API client library for NetBox and it's well documented at `https://NETBOX_ADDR/api/docs`.

To start using this wrapper, you must create a token for the user in NetBox that will be used by this script to access NetBox's data.

Compatibility:

* NetBox 2.4


## Basic Usage
At least you'll need the following data to start:

* NetBox URL in this format: `https://NETBOX_ADDR/api/`
* Access token

```python
>>> from corsair.digitalocean.netbox import Api
>>> netbox = Api('https://netbox_addr/api', 'aR3allyl000ngtok3n')
>>> netbox.ip_addresses.create(address='10.11.12.13', description='Foobar')
>>> ip = netbox.ip_addresses.find(address='10.11.12.13')
>>> netbox.ip_addresses.update(id=ip['id'], description='Desktop')
>>> netbox.ip_addresses.find(address='10.11.12.13')['description']
>>> netbox.ip_addresses.delete(ip['id'])
>>> all_addrs = netbox.ip_addresses.filter()
```
