import urllib.request

from base64 import b64encode
from json import loads


class Api(object):
    def __init__(self, url, user, password, json=True):
        self.url = url
        self.auth = b64encode(f'{user}:{password}'.encode()).decode()
        output = '.json' if json else ''
        self.devices = Endpoint(self, f'data/Devices{output}')


class Endpoint(object):
    def __init__(self, api, path):
        self.url = f'{api.url}/{path}'
        self.auth = api.auth

    def count(self):
        response = Request(self.url, self.auth, {'maxResults':1}).get()
        return int(response['queryResponse']['@count'])
    
    def all(self, **kwargs):
        maxresults = int(kwargs.get('maxResults')) if 'maxResults' in kwargs else 100
        responses = list()
        if 'firstResult' not in kwargs:
            kwargs['firstResult'] = 0
        for i in range(0, self.count(), maxresults):
            kwargs['firstResult'] = i
            responses.append(Request(self.url, self.auth, kwargs).get())
        return responses


class Request(object):
    def __init__(self, base, auth, filters):
        self.url = self.make_url(base, filters)
        self.auth = auth

    def make_url(self, base, filters):
        if filters:
            # Prime filters start with a dot
            f = '&'.join([f'{k}={v}' for k,v in {f'.{k}':v 
                for k,v in filters.items()}.items()])
            return f'{base}?{f}'
        else:
            return base

    def get(self):
        req =  urllib.request.Request(self.url, 
            headers={'Authorization':f'Basic {self.auth}'}, method='GET')
        with urllib.request.urlopen(req) as r:
            return loads(r.read())
