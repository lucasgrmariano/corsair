# Corsair > IBM > QRadar

* QRadar 7.3.0
* API 8.0

## Basic Usage

```python
>>> from corsair.ibm.qradar import Api
>>> qradar = Api('https://qradar_addr/api', '4-53cur3-tok3n-h3r3')
>>> qradar.searches.filter()
```