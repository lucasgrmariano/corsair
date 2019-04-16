import urllib.request

from json import loads, dumps
from copy import copy

from corsair import CorsairError


class Api(object):
    def __init__(self, base_url, token):
        self.base_url = base_url if base_url[-1] != '/' else base_url[:-1]
        self.auth = token

        self.circuit_terminations = Endpoint(self, 'circuits/circuit-terminations')
        self.circuit_types = Endpoint(self, 'circuits/circuit-types')
        self.circuits = Endpoint(self, 'circuits/circuits')
        self.providers = Endpoint(self, 'circuits/providers')

        self.connected_device = Endpoint(self, 'dcim/connected-device')
        self.console_connections = Endpoint(self, 'dcim/console-connections')
        #TODO Add the rest of DCIM endpoints.
        #WARNING Remember to check if property already exists before adding!

        self.config_contexts = Endpoint(self, 'extras/config-contexts')
        self.export_templates = Endpoint(self, 'extras/export-templates')
        self.graphs = Endpoint(self, 'extras/graphs')
        self.image_attachments = Endpoint(self, 'extras/image-attachments')
        self.object_changes = Endpoint(self, 'extras/object-changes')
        self.recent_activity = Endpoint(self, 'extras/recent-activity')
        self.tags = Endpoint(self, 'extras/tags')
        self.topology_maps = Endpoint(self, 'extras/topology-maps')

        self.aggregates = Endpoint(self, 'ipam/aggregates')
        self.ip_addresses = Endpoint(self, 'ipam/ip-addresses')
        self.prefixes = Endpoint(self, 'ipam/prefixes')
        self.rirs = Endpoint(self, 'ipam/rirs')
        self.roles = Endpoint(self, 'ipam/roles')
        self.services = Endpoint(self, 'ipam/services')
        self.vlan_groups = Endpoint(self, 'ipam/vlan-groups')
        self.vlans = Endpoint(self, 'ipam/vlans')
        self.vrfs = Endpoint(self, 'ipam/vrfs')
        
        self.tenant_groups = Endpoint(self, 'tenancy/tenant-groups')
        self.tenants = Endpoint(self, 'tenancy/tenants')

        self.cluster_groups = Endpoint(self, 'virtualization/cluster-groups')
        self.cluster_types = Endpoint(self, 'virtualization/cluster-types')
        self.clusters = Endpoint(self, 'virtualization/clusters')
        self.interfaces = Endpoint(self, 'virtualization/interfaces')
        self.virtual_machines = Endpoint(self, 'virtualization/virtual-machines')


class Endpoint(object):
    def __init__(self, api, resource):
        self.base_url = f'{api.base_url}/{resource}'
        self.auth = api.auth
        self.request = Request(self.base_url, self.auth)

    def create(self, **kwargs):
        'Create a new element'
        res = self.request.post(**kwargs)
        if res.status == 201:
            return loads(res.read())
        else:
            raise CorsairError(f'Error creating element: {kwargs}')
    
    def read(self, **kwargs):
        'Gets multiple elements filtered by kwargs - blank to show all'
        offset, limit = (0, 1000)
        kwargs.update({'offset':offset,'limit':limit})
        res = self.request.get(**kwargs)
        json = loads(res.read())
        elements = json['results']
        while json['next']:
            offset += limit
            kwargs.update({'offset':offset})
            res = self.request.get(**kwargs)
            json = loads(res.read())
            elements.extend(json['results'])
        if elements:
            return elements
        else:
            raise CorsairError(f'Not found: {kwargs}')
    
    def fetch(self, id, **kwargs):
        'Retrieves only one element'
        req = copy(self.request)
        req.base_url += f'/{id}/'
        try:
            res = req.get(**kwargs)
        except urllib.error.HTTPError as e:
            raise CorsairError(f'Unable to access {req.base_url}: {e}')
        return loads(res.read())
    
    def update(self, id, **kwargs):
        'Set the properties of a given element'
        res = self.request.patch(id, **kwargs)
        if res.status == 200:
            return loads(res.read())
        else:
            raise CorsairError(f'Error updating: {id}')
        
    def delete(self, id):
        'Deletes a given element'
        res = self.request.delete(id)
        if res.status == 204:
            return res.status
        else:
            raise CorsairError(f'Error deleting: {kwargs}')


class Request(object):
    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json', 
            'Authorization': f'Token {auth}'
        }
    
    def get(self, **kwargs):
        url = self.parse_url_filters(self.base_url, **kwargs)
        req = urllib.request.Request(url, headers=self.headers, method='GET')
        return urllib.request.urlopen(req)
    
    def patch(self, id, **kwargs):
        url = f'{self.base_url}/{id}/'
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

    def parse_url_filters(self, url_base, **kwargs):
        if kwargs:
            f = '&'.join([f'{k}={v}' for k,v in kwargs.items()])
            return f'{url_base}?{f}'
        else:
            return url_base
