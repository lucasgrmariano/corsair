import urllib.request

from json import loads, dumps
from json.decoder import JSONDecodeError


class Api(object):
    def __init__(self, base_url, token):
        self.base_url = base_url if base_url[-1] != '/' else base_url[:-1]
        self.auth = token

        self.ip_addresses = Endpoint(self, 'ipam/ip-addresses')


class Endpoint(object):
    def __init__(self, api, endpoint):
        self.base_url = f'{api.base_url}/{endpoint}'
        self.auth = api.auth
        self.request = Request(self.base_url, self.auth)

    def create(self, **kwargs):
        'Create a new element'
        res = self.request.post(**kwargs)
        return res.status
    
    def find(self, **kwargs):
        'Retrieves only one element identified by key in kwargs.'
        res = self.request.get(**kwargs)  #TODO check results
        try:
            return loads(res.read())['results'][0]
        except JSONDecodeError:
            return None
    
    def filter(self, **kwargs):
        'Retrieves multiple elements identified by key in kwargs - without args works like all'
        offset, limit = (0, 1000)
        kwargs.update({'offset':offset,'limit':limit})
        res = self.request.get(**kwargs)  #TODO check results
        json = loads(res.read())
        elements = json['results']
        while json['next']:
            offset += limit
            kwargs.update({'offset':offset})
            res = self.request.get(**kwargs)  #TODO check results
            json = loads(res.read())
            elements.extend(json['results'])
        return elements
    
    def update(self, **kwargs):
        'Set the properties of a given element'
        res = self.request.patch(**kwargs)
        return res.status
        
    def delete(self, id):
        'Deletes a given element'
        res = self.request.delete(id)
        return res.status


class Request(object):
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json', 
            'Authorization': f'Token {auth}'
        }
    
    def get(self, **kwargs):
        url = self.make_url(self.base_url, **kwargs)
        req = urllib.request.Request(url, headers=self.headers, method='GET')
        return urllib.request.urlopen(req)
    
    def patch(self, **kwargs):
        url = f'{self.base_url}/{kwargs["id"]}/'
        req = urllib.request.Request(url, headers=self.headers, 
            data=dumps(kwargs).encode('utf-8'), method='PATCH')
        return urllib.request.urlopen(req)
    
    def post(self, **kwargs):
        url = f'{self.base_url}/'
        req = urllib.request.Request(url, headers=self.headers,
            data=dumps(kwargs).encode('utf-8'), method='POST')
        return urllib.request.urlopen(req)
    
    def delete(self, id):
        url = f'{self.base_url}/{id}/'
        req = urllib.request.Request(url, headers=self.headers, 
            method='DELETE')
        return urllib.request.urlopen(req)

    def make_url(self, base, **kwargs):
        'Converts kwargs into NetBox filters'
        if kwargs:
            f = '&'.join([f'{k}={v}' for k,v in kwargs.items()])
            return f'{base}?{f}'
        else:
            return base
