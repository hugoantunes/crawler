# -*- coding: utf-8

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

    @requests_mock.mock()
    def test_should_keep_only_same_domain_url(self, mock):
        body = 'u<html><a href="#"></a><a href="founders.html"></a><a href="benefits.html"></a><a href="http://tests.com/extras/">\
        </a><a href="http://tests.com/extras/comon"></a><a href="http://facebook.com/tests_page"></a>\
        <a href="http://anything.tests.com/any"></a></html>'
        mock.get(self.url, text=body)
        crawler = Crawler(self.url)
        self.assertEquals(set([
            '/founders.html',
            '/extras/index.html',
            '/extras/comon/index.html',
            '/benefits.html']), crawler.get_sitemap()['urls'])


if __name__ == '__main__':
    unittest.main()
