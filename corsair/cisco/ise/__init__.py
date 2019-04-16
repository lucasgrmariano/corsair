import urllib.request

from base64 import b64encode

from corsair import CorsairError


class Api(object):
    def __init__(self, base_url, user, password):
        self.base_url = base_url if base_url[-1] != '/' else base_url[:-1]
        self.auth = b64encode(f'{user}:{password}'.encode()).decode()

        self.anc_endpoint(self, 'config/ancendpoint')


class Endpoint(object):
    def __init__(self, api, resource):
        self.base_url = f'{api.base_url}/{resource}'
        self.auth = api.auth
        self.request = Request(self.base_url, self.auth)
    
    def create(self):
        pass
    
    def read(self):
        pass
    
    def fetch(self):
        pass
    
    def update(self):
        pass
    
    def delete(self):
        pass


class Request(object):
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = auth
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Basic {self.auth}'
        }
    
    def get(self):
        url = self.parse_url_filters(self.base_url, **kwargs)
        req = urllib.request.Request(url, headers=self.headers, method='GET')
        return urllib.request.urlopen(req)
