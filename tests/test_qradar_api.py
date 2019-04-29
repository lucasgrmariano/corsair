import unittest
import os
from corsair.ibm.qradar import Api


CREDENTIALS = {
    'url': '',
    'token': ''
}


class TestRequest(unittest.TestCase):
    def test_api(self):
        url = CREDENTIALS['url']
        token = CREDENTIALS['token']
        qradar = Api(url, token)
        query = qradar.ariel.create('searches', query_expression='select * from flows last 1 minutes')
        self.assertIsInstance(query, dict)
        offenses = qradar.siem.read('offenses')
        self.assertIsInstance(offenses, list)


if __name__ == '__main__':
    unittest.main()
    