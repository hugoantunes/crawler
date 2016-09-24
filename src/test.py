import unittest
import requests_mock

from crawler import Crawler


class TestCrawler(unittest.TestCase):

    def setUp(self):
        self.url = "http://tests.com"

    @requests_mock.mock()
    def test_requested_url_should_raise_exception_when_status_code_is_404(self, mock):
        mock.get(self.url, status_code=404)
        with self.assertRaises(Exception):
            Crawler(self.url)

if __name__ == '__main__':
    unittest.main()
