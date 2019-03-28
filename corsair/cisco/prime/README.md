# Corsair > Cisco > Prime
This is the [Cisco Prime](https://www.cisco.com/c/en/us/products/cloud-systems-management/prime-infrastructure/index.html) API wrapper.  Fortunately, Prime API is well documented, usually accessible at `https://PRIME_ADDR/webacs/api/VERSION`.

To start using this wrapper, you must create a user in Prime with NBI permissions, according to the resources you need to access.  Read `?id=authentication-doc` under Prime's own documentation to learn more about such privileges.

Compatibility:

* Prime 3.4
* API v4

Actually, it works internally with JSON responses, so, if you need to receive XML responses, this code must be modified.


### Basic Usage
At least you'll need the following data to start:

* Prime URL in this format: `https://PRIME_ADDR/webacs/api/VERSION`
* User and password

```python
>>> from corsair.cisco.prime import Api
>>> prime = Api('https://prime_addr/webacs/api/v4/', 'cors', 'Strong_P4$$w0rd!')
>>> prime.devices.all()
>>> prime.devices.all(full='true')
```
