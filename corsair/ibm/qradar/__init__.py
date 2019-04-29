import urllib.request

from urllib.parse import quote
from json import loads
from copy import copy
from socket import timeout

from corsair import CorsairError


class Api(object):
    def __init__(self, base_url, auth):
        self.base_url = base_url if base_url[-1] != '/' else base_url[:-1]
        self.auth = auth
        self.credentials = (self.base_url, self.auth)

        self.analytics = Endpoint(self.credentials, 'analytics')
        self.ariel = Endpoint(self.credentials, 'ariel')
        self.asset_model = Endpoint(self.credentials, 'asset_model')
        self.auth = Endpoint(self.credentials, 'auth')
        self.config = Endpoint(self.credentials, 'config')
        self.data_classification = Endpoint(self.credentials, 'data_classification')
        self.forensics = Endpoint(self.credentials, 'forensics')
        self.gui_app_framework = Endpoint(self.credentials, 'gui_app_framework')
        self.help = Endpoint(self.credentials, 'help')
        self.qrm = Endpoint(self.credentials, 'qrm')
        self.reference_data = Endpoint(self.credentials, 'reference_data')
        self.scanner = Endpoint(self.credentials, 'scanner')
        self.services = Endpoint(self.credentials, 'services')
        self.siem = Endpoint(self.credentials, 'siem')
        self.staged_config = Endpoint(self.credentials, 'staged_config')
        self.system = Endpoint(self.credentials, 'system')


class Endpoint(object):
    def __init__(self, credentials, endpoint):
        self.base_url = credentials[0]
        self.endpoint = endpoint
        self.resource = ''
        self.auth = credentials[1]
    
    def create(self, resource, **kwargs):
        self.resource = resource
        req = Request(self.make_url(), self.auth)
        res = req.post(**kwargs)
        if res.status == 201:
            return loads(res.read())
        else:
            raise CorsairError('Could not create requisition')
        
    def read(self, resource, **kwargs):
        'Gets all elements from a resource'
        self.resource = resource
        req = Request(self.make_url(), self.auth)

        try:
            res = req.get(**kwargs)
        except timeout:
            raise CorsairError('Operation timedout')

        if res.status == 200:
            return loads(res.read())
        else:
            raise CorsairError('Not found')
    
    def fetch(self, resource, id, **kwargs):
        'Gets a single element'
        self.resource = f'{resource}/{id}'
        req = Request(self.make_url(), self.auth)

        # QRadar requires a '/results' to show details of a query.
        # The 'results=True' flag tells this wrapper to append it.
        if kwargs.get('results'):
            req.url += '/results'
            kwargs.pop('results')
        
        res = req.get(**kwargs)
        if res.status == 200:
            return loads(res.read())
        else:
            raise CorsairError('Not found')
    
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
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Version': '8.0',
            'SEC': auth
        }
    
    def get(self, **kwargs):
        url = f'{self.url}?{self.parse_filters(**kwargs)}' if kwargs else self.url
        req = urllib.request.Request(url, headers=self.headers, method='GET')
        return urllib.request.urlopen(req, timeout=self.timeout)
    
    def post(self, **kwargs):
        url = f'{self.url}?{self.parse_filters(**kwargs)}' if kwargs else self.url
        req = urllib.request.Request(url, headers=self.headers, method='POST')
        return urllib.request.urlopen(req)
    
    def parse_filters(self, **kwargs):
        if kwargs:
            return '&'.join([f'{k}={quote(v)}' for k,v in kwargs.items()])
        else:
            return ''
