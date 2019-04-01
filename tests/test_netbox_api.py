import unittest
import os
from corsair.digitalocean.netbox import Api


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
        ip = netbox.ip_addresses.find(address=test_addr)
        self.assertIsInstance(ip, dict)

        netbox.ip_addresses.update(id=ip['id'], description='Desktop')
        desc = netbox.ip_addresses.find(address=test_addr)['description']
        self.assertEqual(desc, 'Desktop')

        netbox.ip_addresses.delete(ip['id'])
        ip = netbox.ip_addresses.find(address=test_addr)
        self.assertIsNone(ip, 'Desktop')

        ips = netbox.ip_addresses.filter()
        self.assertIsInstance(ips, list)


if __name__ == '__main__':
    unittest.main()
    