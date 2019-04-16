# Corsair > IBM > QRadar
The [IBM QRadar](https://www.ibm.com/security/security-intelligence/qradar) API wrapper uses `https://qradar.corp/api_docs` as its base.

Prerequisites:

* QRadar 7.3.0
* API 8.0
* Access credentials (token)


## Basic Usage

```python
>>> from corsair.ibm.qradar import Api
>>> qradar = Api('https://qradar.corp/api', '4-53cur3-tok3n-h3r3')
>>> qradar.searches.read()
>>> qradar.searches.fetch('search-id-goes-here', results=True)
>>> qradar.offenses.fetch(40322)
>>> qradar.searches.create(query_expression='select * from flows last 5 minutes')
```
