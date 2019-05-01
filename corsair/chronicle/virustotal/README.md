# Corsair > Chronicle > VirusTotal
This [VirusTotal](https://virustotal.com) (HIBP) API wrapper is based in the official developer guide, available at `https://developers.virustotal.com/reference`.

Prerequisites:

* API v2
* 1 request by 15 seconds

An example on how VirusTotal structures URLs and how it's mapped in Corsair follows:

```
https://www.virustotal.com/vtapi/v2/file/scan/upload_url?apikey=alongapikey
\_________________________________/\____/\___/\________/\_________________/
           Base URL              Endpoint Resource Suffix     Filters
```

As I don't have access to paid API, the restricted features wasn't tested, but if they follow the same pattern the public ones have, it'll be quite simple to use them with this wrapper.


## Basic Usage

```python
>>> from corsair.chronicle.virustotal import Api
>>> vt = Api('https://www.virustotal.com/vtapi/v2', 'my-apikey')
>>>
>>> vt.url.read('report', resource='http://www.my-homepage.com', scan='1')
```
