import unittest
import os
from corsair.digitalocean.netbox import Api
from corsair import CorsairError


CREDENTIALS = {
    'url': '',
    'token': ''
}


class TestRequest(unittest.TestCase):
    def test_api(self):
        url = CREDENTIALS['url']
        token = CREDENTIALS['token']
        netbox = Api(url, token)
        test_addr = '255.255.255.255'

        netbox.ip_addresses.create(address=test_addr, description='Foobar')
        ip1 = netbox.ip_addresses.filter(address=test_addr)[0]
        self.assertIsInstance(ip1, dict)

        ip2 = netbox.ip_addresses.update(ip1['id'], description='Desktop')
        self.assertEqual(ip2['description'], 'Desktop')

        netbox.ip_addresses.delete(ip1['id'])
        try:
            ip2 = netbox.ip_addresses.fetch(ip1['id'])
        except CorsairError:
            ip2 = None
        self.assertIsNone(ip2)

        prefixes = netbox.prefixes.filter()
        self.assertIsInstance(prefixes, list)


if __name__ == '__main__':
    unittest.main()
    