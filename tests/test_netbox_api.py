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
        ip_addresses = netbox.ip_addresses.all()
        self.assertIsInstance(ip_addresses, list)


if __name__ == '__main__':
    unittest.main()
    