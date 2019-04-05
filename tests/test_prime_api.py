import unittest
import os
from corsair.cisco.prime import Api


CREDENTIALS = {
    'url': '',
    'user': '',
    'pass': ''
}


class TestRequest(unittest.TestCase):
    def test_api(self):
        url = CREDENTIALS['url']
        user = CREDENTIALS['user']
        password = CREDENTIALS['pass']
        prime = Api(url, user, password)
        devices = prime.devices.filter()
        aps = prime.access_points.filter(full='true')
        self.assertIsInstance(devices, list)
        self.assertIsInstance(aps, list)


if __name__ == '__main__':
    unittest.main()
    