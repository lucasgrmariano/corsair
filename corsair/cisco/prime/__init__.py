import urllib.request

from base64 import b64encode
from json import loads


class Api(object):
    def __init__(self, base_url, user, password):
        self.base_url = base_url if base_url[-1] != '/' else base_url[:-1]
        self.auth = b64encode(f'{user}:{password}'.encode()).decode()

        # /data/* endpoints
        self.ap_onboarding_profile = Endpoint(self, 'data/ApOnboardingProfile.json')
        self.api_health_records = Endpoint(self, 'data/ApiHealthRecords.json')
        self.api_response_time_summary = Endpoint(self, 'data/ApiResponseTimeSummary.json')
        self.applications = Endpoint(self, 'data/Applications.json')
        self.cli_template = Endpoint(self, 'data/CliTemplate.json')
        self.client_counts = Endpoint(self, 'data/ClientCounts.json')
        self.client_details = Endpoint(self, 'data/ClientDetails.json')
        self.client_sessions = Endpoint(self, 'data/ClientSessions.json')
        self.clients = Endpoint(self, 'data/Clients.json')
        self.client_traffics = Endpoint(self, 'data/ClientTraffics.json')
        self.historical_client_counts = Endpoint(self, 'data/HistoricalClientCounts.json')
        self.historical_client_traffics = Endpoint(self, 'data/HistoricalClientTraffics.json')
        self.bulk_sanitized_config_archives = Endpoint(self, 'data/BulkSanitizedConfigArchives.json')
        self.bulk_unsanitized_config_archives = Endpoint(self, 'data/BulkUnsanitizedConfigArchives.json')
        self.config_archives = Endpoint(self, 'data/ConfigArchives.json')
        self.config_versions = Endpoint(self, 'data/ConfigVersions.json')
        self.alarms = Endpoint(self, 'data/Alarms.json')
        self.devices = Endpoint(self, 'data/Devices.json')
        self.events = Endpoint(self, 'data/Events.json')
        self.inventory_details = Endpoint(self, 'data/InventoryDetails.json')
        self.rogue_ap_alarms = Endpoint(self, 'data/RogueApAlarms.json')
        self.syslogs = Endpoint(self, 'data/Syslogs.json')
        self.guest_user = Endpoint(self, 'data/GuestUsers.json')
        self.job_summary = Endpoint(self, 'data/JobSummary.json')
        self.mac_filter_templates = Endpoint(self, 'data/MacFilterTemplates.json')
        self.user_defined_field_definition = Endpoint(self, 'data/UserDefinedFieldDefinition.json')
        self.vd_associated_access_points = Endpoint(self, 'data/VDAssociatedAccessPoints.json')
        self.vd_associated_dynamic_groups = Endpoint(self, 'data/VDAssociatedDynamicGroups')
        self.vd_associated_groups = Endpoint(self, 'data/VDAssociatedGroups.json')
        self.vd_associated_devices = Endpoint(self, 'data/VDAssociatedDevices.json')
        self.vd_associated_site_maps = Endpoint(self, 'data/VDAssociatedSiteMaps.json')
        self.vd_associated_virtual_elements = Endpoint(self, 'data/VDAssociatedVirtualElements.json')
        self.wlan_profiles = Endpoint(self, 'data/WlanProfiles.json')
        self.wlan_templates = Endpoint(self, 'data/WlanTemplates.json')
        self.auto_ap_radio_details = Endpoint(self, 'data/AutoApRadioDetails.json')
        self.client_stats = Endpoint(self, 'data/ClientStats.json')
        self.historical_client_stats = Endpoint(self, 'data/HistoricalClientStats.json')
        self.historical_rf_counters = Endpoint(self, 'data/HistoricalRFCounters.json')
        self.historical_rf_load_stats = Endpoint(self, 'data/HistoricalRFLoadStats.json')
        self.historical_rf_stats = Endpoint(self, 'data/HistoricalRFStats.json')
        self.historical_wlc_cpu_utilizations = Endpoint(self, 'data/HistoricalWLCCPUUtilizations.json')
        self.historical_wlc_mem_utilizations = Endpoint(self, 'data/HistoricalWLCMemUtilizations.json')
        self.historical_wlc_utilizations = Endpoint(self, 'data/HistoricalWLCUtilizations.json')
        self.radio_details = Endpoint(self, 'data/RadioDetails.json')
        self.rf_counters = Endpoint(self, 'data/RFCounters.json')
        self.rf_load_stats = Endpoint(self, 'data/RFLoadStats.json')
        self.rf_stats = Endpoint(self, 'data/RFStats.json')
        self.radios = Endpoint(self, 'data/Radios.json')
        self.third_party_access_points = Endpoint(self, 'data/ThirdpartyAccessPoints.json')
        self.access_point_details = Endpoint(self, 'data/ThirdpartyAccessPoints.json')
        self.access_points = Endpoint(self, 'data/AccessPoints.json')
        self.wlc_cpu_utilizations = Endpoint(self, 'data/WLCCPUUtilizations.json')
        self.wlan_controller_details = Endpoint(self, 'data/WlanControllerDetails.json')
        self.wlc_memory_utilizations = Endpoint(self, 'data/WLCMemoryUtilizations.json')
        self.wlan_controllers = Endpoint(self, 'data/WlanControllers.json')
        self.wlc_utilizations = Endpoint(self, 'data/WLCUtilizations.json')
        
        # /op/* has different behavior, so Endpoint() must be rewritten


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
            json = loads(res.read())['queryResponse']
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
