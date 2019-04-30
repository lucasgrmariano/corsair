import urllib.request

from json import loads, dumps
from socket import timeout

from corsair import CorsairError


class Api(object):
    def __init__(self, base_url, auth):
        self.base_url = base_url if base_url[-1] != '/' else base_url[:-1]
        self.auth = auth
        self.credentials = (self.base_url, self.auth)

        self.circuits = Endpoint(self.credentials, 'circuits')
        self.dcim = Endpoint(self.credentials, 'dcim')
        self.extras = Endpoint(self.credentials, 'extras')
        self.ipam = Endpoint(self.credentials, 'ipam')
        self.secrets = Endpoint(self.credentials, 'secrets')
        self.tenancy = Endpoint(self.credentials, 'tenancy')
        self.virtualization = Endpoint(self.credentials, 'virtualization')


class Endpoint(object):
    def __init__(self, credentials, endpoint):
        self.base_url = credentials[0]
        self.endpoint = endpoint
        self.resource = ''
        self.auth = credentials[1]

    def create(self, resource, **filters):
        self.resource = resource
        req = Request(self.make_url(), self.auth)
        res = req.post(**filters)
        if res.status == 201:
            return loads(res.read())
        else:
            raise CorsairError(f'Error creating element: {filters}')
    
    def read(self, resource, **filters):
        'Gets multiple elements filtered by filters - blank to show all'
        self.resource = resource
        req = Request(self.make_url(), self.auth)
        offset, limit = (0, 1000)
        filters.update({'offset':offset,'limit':limit})  #TODO test if it is already in **filters
        try:
            res = req.get(**filters)
        except timeout:
            raise CorsairError('Operation timedout')
        json = loads(res.read())
        elements = json['results']

        while json['next']:
            offset += limit
            filters.update({'offset':offset})
            try:
                res = req.get(**filters)
            except timeout:
                raise CorsairError('Operation timedout')
            json = loads(res.read())
            elements.extend(json['results'])
        if elements:
            return elements
        else:
            raise CorsairError(f'Not found: {resource}')
    
    def fetch(self, resource, **filters):
        'Retrieves only one element'
        self.resource = resource
        req = Request(self.make_url(), self.auth)
        try:
            res = req.get(**filters)
        except timeout:
            raise CorsairError(f'Operation timedout')
        if res.status == 200:
            return loads(res.read())
        else:
            raise CorsairError(f'Not found: {resource}')
    
    def update(self, resource, **filters):
        'Set the properties of a given element'
        self.resource = resource
        req = Request(self.make_url(), self.auth)
        try:
            res = req.patch(**filters)
        except timeout:
            raise CorsairError(f'Operation timedout')
        if res.status == 200:
            return loads(res.read())
        else:
            raise CorsairError(f'Error updating: {resource}')
        
    def delete(self, resource, **filters):
        'Deletes a given element'
        self.resource = resource
        req = Request(self.make_url(), self.auth)
        try:
            res = req.delete(**filters)
        except timeout:
            raise CorsairError(f'Operation timedout')
        if res.status == 204:
            return res.status
        else:
            raise CorsairError(f'Error deleting: {resource}')
    
    def make_url(self):
        url = f'{self.base_url}/{self.endpoint}/{self.resource}'
        url.replace('//', '/')
        url = url[:-1] if url.endswith('/') else url
        return url


class Request(object):
    def __init__(self, url, auth):
        self.url = url
        self.timeout = 20  # seconds
        self.headers = {
            'Content-Type': 'application/json', 
            'Authorization': f'Token {auth}'
        }
    
    def get(self, **filters):
        url = f'{self.url}?{self.parse_filters(**filters)}' if filters else self.url
        req = urllib.request.Request(url, headers=self.headers, method='GET')
        return urllib.request.urlopen(req, timeout=self.timeout)
    
    def patch(self, **filters):
        url = f'{self.url}/'
        req = urllib.request.Request(url, headers=self.headers, 
            data=dumps(filters).encode('utf-8'), method='PATCH')
        return urllib.request.urlopen(req, timeout=self.timeout)
    
    def post(self, **filters):
        url = f'{self.url}/?{self.parse_filters(**filters)}' if filters else f'{self.url}/'
        req = urllib.request.Request(url, headers=self.headers,
            data=dumps(filters).encode('utf-8'), method='POST')
        return urllib.request.urlopen(req, timeout=self.timeout)
    
    def delete(self):
        url = f'{self.url}/'
        req = urllib.request.Request(url, headers=self.headers, 
            method='DELETE')
        return urllib.request.urlopen(req, timeout=self.timeout)

    def parse_filters(self, **filters):
        if filters:
            return '&'.join([f'{k}={v}' for k,v in filters.items()])
        else:
            return ''
