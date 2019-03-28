import urllib.request

from json import loads


class Api(object):
    def __init__(self, base_url, token):
        self.base_url = base_url if base_url[-1] != '/' else base_url[:-1]
        self.auth = token

        self.ip_addresses = Endpoint(self, 'ipam/ip-addresses')


class Endpoint(object):
    def __init__(self, api, endpoint):
        self.base_url = f'{api.base_url}/{endpoint}'
        self.auth = api.auth
    
    def all(self, **kwargs):
        kwargs['offset'] = 0
        kwargs['limit'] = 1000
        responses = [Request(self.base_url, self.auth).get(**kwargs)]
        while responses[0]['next']:
            kwargs['offset'] += kwargs['limit']
            responses.insert(0, Request(self.base_url, self.auth).get(**kwargs))
        return responses


class Request(object):
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = auth

    def make_url(self, base, **kwargs):
        'Converts kwargs into NetBox filters'
        if kwargs:
            f = '&'.join([f'{k}={v}' for k,v in kwargs.items()])
            return f'{base}?{f}'
        else:
            return base

    def get(self, **kwargs):
        url = self.make_url(self.base_url, **kwargs)
        req = urllib.request.Request(url, 
            headers={'Authorization':f'Token {self.auth}'}, method='GET')
        with urllib.request.urlopen(req) as r:
            return loads(r.read())
