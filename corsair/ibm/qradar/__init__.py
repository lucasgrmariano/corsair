import urllib.request

from urllib.parse import quote
from json import loads
from copy import copy

from corsair import CorsairError


class Api(object):
    def __init__(self, base_url, token):
        self.base_url = base_url if base_url[-1] != '/' else base_url[:-1]
        self.auth = token

        self.searches = Endpoint(self, 'ariel/searches')
        self.offenses = Endpoint(self, 'siem/offenses')
        
        self.dig_lookups = Endpoint(self, 'services/dig_lookups')
        self.dns_lookups = Endpoint(self, 'services/dns_lookups')
        self.port_scans = Endpoint(self, 'services/port_scans')
        self.whois_lookups = Endpoint(self, 'services/whois_lookups')


class Endpoint(object):
    def __init__(self, api, resource):
        self.base_url = f'{api.base_url}/{resource}'
        self.auth = api.auth
        self.request = Request(self.base_url, self.auth)
    
    def create(self, **kwargs):
        res = self.request.post(**kwargs)
        if res.status == 201:
            return loads(res.read())
        else:
            CorsairError('Could not create requisition')
        
    def read(self, **kwargs):
        'Gets all elements from a resource'
        res = self.request.get(**kwargs)
        if res.status == 200:
            return loads(res.read())
        else:
            raise CorsairError('Not found')
    
    def fetch(self, id, **kwargs):
        'Gets a single element'
        req = copy(self.request)
        req.base_url += '' if not id else f'/{id}'
        if kwargs.get('results'):
            req.base_url += '/results'
            kwargs.pop('results')
        res = req.get(**kwargs)
        if res.status == 200:
            return loads(res.read())
        else:
            raise CorsairError('Not found')


class Request(object):
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json',
            'SEC': auth,
            'Version': '8.0'
        }
    
    def get(self, **kwargs):
        url = self.parse_url_filters(self.base_url, **kwargs)
        req = urllib.request.Request(url, headers=self.headers, method='GET')
        return urllib.request.urlopen(req)
    
    def post(self, **kwargs):
        url = self.parse_url_filters(self.base_url, **kwargs)
        req = urllib.request.Request(url, headers=self.headers, method='POST')
        return urllib.request.urlopen(req)
    
    def parse_url_filters(self, url_base, **kwargs):
        if kwargs:
            f = '&'.join([f'{k}={quote(v)}' for k,v in kwargs.items()])
            return f'{url_base}?{f}'
        else:
            return url_base
