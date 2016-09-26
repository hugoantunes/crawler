# encoding: utf-8
import requests

from urlparse3 import parse_url
from bs4 import BeautifulSoup


class Crawler(object):

    def __init__(self, url):
        self.url = parse_url(url)
        self.response = self.body_parser(self.check_status_code())
        self.resources = {'urls': set(['/']), 'assets': {}}

    @property
    def product_name(self):
        return self.domain.split('.')[0]

    @property
    def domain(self):
        return self.url.domain

    @property
    def base_url(self):
        return self.url.scheme + '://' + self.url.domain + '/'

    def check_status_code(self, url=None):
        if url is None:
            url = self.url.geturl()
        response = requests.get(url)
        if response.status_code == 404:
            raise Exception('Url does not exist')
        return response

    def body_parser(self, response):
        return BeautifulSoup(response.text, 'lxml')

    def build_resources(self, url=None, response=None):
        if not url:
            page = '/index.html'
        if not response:
            response = self.response

        self.resources['assets'].update({page: set()})
        tags = response.find_all(['a', 'img', 'link', 'script'])
        for tag in tags:
            if tag.name == 'a':
                try:
                    href = tag['href']
                    if href.startswith(self.base_url):
                        href = href.split(self.domain)[1]
                        if href.endswith('index.html'):
                            pass
                        elif href.endswith('/'):
                            href += 'index.html'
                        else:
                            href += '/index.html'
                        self.resources['urls'].add(href)
                    elif not href.startswith(('http', 'https')) and '#' not in href:
                        self.resources['urls'].add('/' + href)
                    elif self.product_name in href:
                        self.resources['assets'][page].add(href)
                except KeyError:
                    pass

            elif tag.name == 'link':
                self.resources['assets'][page].add(tag['href'])
            else:
                try:
                    self.resources['assets'][page].add(tag['src'])
                except KeyError:
                    pass
