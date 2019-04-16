# Corsair > Cisco > Prime
This is the [Cisco Prime](https://www.cisco.com/c/en/us/products/cloud-systems-management/prime-infrastructure/index.html) API wrapper.  Prime is self-explanatory and it's highly recommended to read it before start using any endpoints.  You can access this documentation page at API's root address (see below).

Prerequisites:

* Tested under Prime 3.4 and API v4
* URL for API (usually `https://prime.corp/webacs/api/v4`)
* Credentials for API access

To start using this wrapper, you must create a user in Prime with NBI permissions, according to the resources you need to access.  Read `?id=authentication-doc` under Prime's own documentation to learn more about such privileges.

Actually, it works internally with JSON responses, so, if you need to receive XML responses, this code must be modified.  This version only supports `/data` endpoint, so any `/op/` resources will not work, for instance.


## Basic Usage

```python
>>> from corsair.cisco.prime import Api
>>> prime = Api('https://prime.corp/webacs/api/v4', 'cors', 'Strong_P4$$w0rd!')
>>> prime.devices.read()
>>> prime.devices.read(full='true')
```
