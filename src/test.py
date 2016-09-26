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
    def test_build_create_resources_correctly(self, mock):
        body = 'u<html><a href="#"></a><a href="founders.html"></a><a href="benefits.html"></a><a href="http://tests.com/extras/">\
        </a><a href="http://tests.com/extras/comon"></a><a href="http://facebook.com/tests"></a>\
        <a href="http://anything.tests.com/any"></a><img src="assets/images/icons/rewards-offers.png" class="overlay-icon">\
        <script src="assets/js/modernizr-2.6.2-min.js"></script><link rel="stylesheet" href="assets/css/sss.css"></html>'

        expected = {
            'assets': {
                '/index.html': set([
                    'http://anything.tests.com/any',
                    'http://facebook.com/tests',
                    'assets/images/icons/rewards-offers.png',
                    'assets/js/modernizr-2.6.2-min.js',
                    'assets/css/sss.css'])
            },
            'urls': set([
                '/',
                '/extras/index.html',
                '/founders.html',
                '/benefits.html',
                '/extras/comon/index.html'])
        }

        mock.get(self.url, text=body)
        crawler = Crawler(self.url)
        crawler.build_resources()
        self.assertEquals(expected, crawler.resources)

    @requests_mock.mock()
    def test_a_tags_and_scritps_without_links_are_ignored(self, mock):
        body = 'u<html><a ></a><script "></script></html>'

        expected = {
            'assets': {
                '/index.html': set()
            },
            'urls': set(['/', ])
        }

        mock.get(self.url, text=body)
        crawler = Crawler(self.url)
        crawler.build_resources()
        self.assertEquals(expected, crawler.resources)

    @requests_mock.mock()
    def test_external_links_with_no_reference_are_ignored(self, mock):
        body = 'u<html><a href="http://www.forbes.com/sites/ilyapozin/2015/09/10/3-trends-in-mobile-payments-you-need-to-know-about/"></a></html>'

        expected = {
            'assets': {
                '/index.html': set()
            },
            'urls': set(['/', ])
        }

        mock.get(self.url, text=body)
        crawler = Crawler(self.url)
        crawler.build_resources()
        self.assertEquals(expected, crawler.resources)

if __name__ == '__main__':
    unittest.main()
