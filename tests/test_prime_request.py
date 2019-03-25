import unittest
from corsair.cisco.prime.api import Request


class TestRequest(unittest.TestCase):
    def test_request(self):
        url = 'https://prime/webacs/api/v4/data/Devices.json'
        filters = {'full':'true','sort':'ipAddress','maxResults':'100'}
        auth = 'user:password'
        self.assertIsInstance(Request(url, filters, auth), Request)


if __name__ == '__main__':
    unittest.main()
    