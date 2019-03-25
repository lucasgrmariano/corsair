import unittest
from corsair.cisco.prime.api import Api


class TestRequest(unittest.TestCase):
    def test_api(self):
        url = 'https://prime.cemig.ad.corp/webacs/api/v4'
        user = ''
        password = ''
        api = Api(url, user, password)
        responses = api.devices.all(full='true')
        self.assertIsInstance(api, Api)


if __name__ == '__main__':
    unittest.main()
    