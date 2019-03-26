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
        api = Api(url, user, password)
        devices = api.data_devices.all()
        aps = api.data_access_points.all(full='true')
        self.assertIsInstance(devices, list)
        self.assertIsInstance(aps, list)


if __name__ == '__main__':
    unittest.main()
    