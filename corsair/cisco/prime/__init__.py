import urllib.request

from base64 import b64encode
from json import loads


class Api(object):
    def __init__(self, base_url, user, password):
        self.base_url = base_url if base_url[-1] != '/' else base_url[:-1]
        self.auth = b64encode(f'{user}:{password}'.encode()).decode()

        self.devices = Endpoint(self, 'data/Devices.json')
        self.access_points = Endpoint(self, f'data/AccessPoints.json')


class Endpoint(object):
    def __init__(self, api, endpoint):
        self.base_url = f'{api.base_url}/{endpoint}'
        self.auth = api.auth
        self.request = Request(self.base_url, self.auth)
    
    def filter(self, **kwargs):
        first_result, max_results = (0, 1000)
        kwargs.update({'firstResult':first_result,'maxResults':max_results})
        res = self.request.get(**kwargs)
        json = loads(res.read())['queryResponse']
        try:  # Prime has different returns if '.full=true'
            elements = json['entity']
        except KeyError:
            elements = json['entityId']
        while (json['@last'] + 1) < json['@count']:
            kwargs.update({'firstResult':json['@last'] + 1})
            res = self.request.get(**kwargs)
            json = loads(res.read())
            try:  # Prime has different returns if '.full=true'
                elements.extend(json['entity'])
            except KeyError:
                elements.extend(json['entityId'])
        return elements


class Request(object):
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = auth
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {self.auth}'
        }

    def get(self, **kwargs):
        url = self.make_url(self.base_url, **kwargs)
        req = urllib.request.Request(url, headers=self.headers, method='GET')
        return urllib.request.urlopen(req) 
    
    def make_url(self, base, **kwargs):
        'Converts kwargs into Prime filters'
        if kwargs:
            # Prime filters start with a dot
            f = '&'.join([f'{k}={v}' for k,v in {f'.{k}':v 
                for k,v in kwargs.items()}.items()])
            return f'{base}?{f}'
        else:
            return base
