# Corsair > Cisco > ISE
This is the [Cisco Identity Services Engine (ISE)](https://www.cisco.com/c/en/us/products/security/identity-services-engine/index.html) API wrapper.  First, you must enable the "External Restful Services" in ISE, so the system will be able to be accessed through API.  After that, the whole documentation can be read at `https://ise.corp:9060/ers/sdk`.

Prerequisites:

* Tested under ISE 2.2
* URL for API (usually `https://ise.corp:9060/ers`)
* Credentials for API access


## Basic Usage

```python
>>> from corsair.cisco.ise import Api
>>> ise = Api('https://ise.corp:9060/ers', 'cors', 'Strong_P4$$w0rd!')
>>> ise.devices.read()
```
