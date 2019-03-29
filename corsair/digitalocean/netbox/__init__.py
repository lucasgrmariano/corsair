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

    def create(self):
        pass
    
    def find(self, **kwargs):
        'Retrieves only one element identified by key in kwargs.'
        req = Request(self.base_url, self.auth)
        res = req.get(**kwargs)  #TODO check results
        return loads(res.read())['results']
    
    def filter(self, **kwargs):
        'Retrieves multiple elements identified by key in kwargs - without args works like all'
        offset, limit = (0, 1000)
        kwargs.update({'offset':offset,'limit':limit})
        req = Request(self.base_url, self.auth)
        res = req.get(**kwargs)  #TODO check results
        json = loads(res.read())
        elements = json['results']
        while json['next']:
            offset += limit
            kwargs.update({'offset':offset})
            res = req.get(**kwargs)  #TODO check results
            json = loads(res.read())
            elements.extend(json['results'])
        return elements
    
    def update(self, element):  #TODO NOT WORKING YET!  MUST TEST!
        'Set the properties of a given element'
        old = self.find(element['id'])
        new = {'id': element['id']}
        for k,v in element:
            if k in old.keys():
                new.update({k:v})
        req = Request(self.base_url, self.auth).patch(new)
        return req.status
        
    def delete(self, element):
        'Deletes a given element'
        pass


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
    
    def patch(self, element):
        url = f'{self.base_url}/{element["id"]}/'
        req = urllib.request.Request(url, headers=self.headers, 
            data=dumps(data), method='PATCH')
        return urllib.request.urlopen(req)

    def make_url(self, base, **kwargs):
        'Converts kwargs into NetBox filters'
        if kwargs:
            f = '&'.join([f'{k}={v}' for k,v in kwargs.items()])
            return f'{base}?{f}'
        else:
            return base
