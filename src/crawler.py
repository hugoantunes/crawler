# encoding: utf-8
import requests
from bs4 import BeautifulSoup


class Crawler(object):

    def __init__(self, url):
        self.url = url
        self.domain = self._get_domain()
        self.product_name = self._get_product_name()
        self.response = self.body_parser(self.check_status_code())
        self.resources = {'urls': set(['/']), 'assets': {}}

    def _get_domain(self):
        return self.url.split('/')[2]

    def _get_product_name(self):
        return self.domain.split('.')[0]

    def check_status_code(self):
        response = requests.get(self.url)
        if response.status_code == 404:
            raise Exception('Url does not exist')
        return response

    def body_parser(self, response):
        return BeautifulSoup(response.text, 'lxml')

    def build_resources(self, url=None):
        if not url:
            page = '/index.html'
        self.resources['assets'].update({page: set()})
        tags = self.response.find_all(['a', 'img', 'link', 'script'])
        for tag in tags:
            if tag.name == 'a':
                href = tag['href']
                if href.startswith(self.url):
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

            elif tag.name == 'link':
                self.resources['assets'][page].add(tag['href'])
            else:
                self.resources['assets'][page].add(tag['src'])
