import urllib.request

from base64 import b64encode
from json import loads


class Api(object):
    def __init__(self, base_url, user, password):
        self.base_url = base_url if base_url[-1] != '/' else base_url[:-1]
        self.auth = b64encode(f'{user}:{password}'.encode()).decode()

        self.data_devices = Endpoint(self, f'data/Devices.json')
        self.data_access_points = Endpoint(self, f'data/AccessPoints.json')


class Endpoint(object):
    def __init__(self, api, path):
        self.base_url = f'{api.base_url}/{path}'
        self.auth = api.auth
    
    def all(self, **kwargs):
        kwargs['firstResult'] = 0
        kwargs['maxResults'] = 1000
        responses = [Request(self.base_url, self.auth).get(**kwargs)]
        while (responses[0]['queryResponse']['@last'] + 1) < responses[0]['queryResponse']['@count']:
            kwargs['firstResult'] = responses[0]['queryResponse']['@last'] + 1
            responses.insert(0, Request(self.base_url, self.auth).get(**kwargs))
        return responses


class Request(object):
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = auth

    def make_url(self, base, **kwargs):
        'Converts kwargs into Prime filters'
        if kwargs:
            # Prime filters start with a dot
            f = '&'.join([f'{k}={v}' for k,v in {f'.{k}':v 
                for k,v in kwargs.items()}.items()])
            return f'{base}?{f}'
        else:
            return base

    def get(self, **kwargs):
        url = self.make_url(self.base_url, **kwargs)
        req = urllib.request.Request(url, 
            headers={'Authorization':f'Basic {self.auth}'}, method='GET')
        with urllib.request.urlopen(req) as r:
            return loads(r.read())
