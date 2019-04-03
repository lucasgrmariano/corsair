import urllib.request
from json import loads


class Api(object):
    def __init__(self, base_url, token):
        self.base_url = base_url if base_url[-1] != '/' else base_url[:-1]
        self.auth = token

        self.searches = Endpoint(self, 'ariel/searches')


class Endpoint(object):
    def __init__(self, api, endpoint):
        self.base_url = f'{api.base_url}/{endpoint}'
        self.auth = api.auth
        self.request = Request(self.base_url, self.auth)
    
    def filter(self, **kwargs):
        req = self.request.get(**kwargs)
        return loads(req.read())


class Request(object):
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json',
            'SEC': auth,
            'Version': '8.0'
        }
    
    def get(self, **kwargs):
        url = self.make_url(self.base_url, **kwargs)
        req = urllib.request.Request(url, headers=self.headers, method='GET')
        return urllib.request.urlopen(req)
    
    def make_url(self, url_base, **kwargs):
        'Converts kwargs into QRadar filters'
        if kwargs:
            f = '&'.join([f'{k}={v}' for k,v in kwargs.items()])
            return f'{url_base}?{f}'
        else:
            return url_base
