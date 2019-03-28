# Corsair > Digital Ocean > NetBox
This is the [Digital Ocean NetBox](https://github.com/digitalocean/netbox) API wrapper.  It's based on [pynetbox](https://github.com/digitalocean/pynetbox), Digital Ocean's official API client library for NetBox and it's well documented at `https://NETBOX_ADDR/api/docs`.

To start using this wrapper, you must create a token for the user in NetBox that will be used by this script to access NetBox's data.

Compatibility:

* NetBox 2.4

Actually, it works internally with JSON responses, so, if you need to receive XML responses, this code must be modified.


### Basic Usage
At least you'll need the following data to start:

* NetBox URL in this format: `https://NETBOX_ADDR/api/`
* Access token

```python
>>> from corsair.digitalocean.netbox import Api
>>> netbox = Api('https://netbox_addr/api', 'aR3allyl000ngtok3n')
>>> netbox.ip_addresses.all()
```
