# encoding: utf-8
import requests
from bs4 import BeautifulSoup


class Crawler(object):

    def __init__(self, url):
        self.url = url
        self.domain = self._get_domain()
        self.response = self.body_parser(self.check_status_code())
        self.sitemap = {"urls": set()}

    def _get_domain(self):
        return self.url.split('/')[2]

    def check_status_code(self):
        response = requests.get(self.url)
        if response.status_code == 404:
            raise Exception('Url does not exist')
        return response

    def body_parser(self, response):
        return BeautifulSoup(response.text, 'lxml')

    def get_sitemap(self):
        all_links = self.response.find_all('a', href=True)
        for idx, link in enumerate(all_links):
            url = link['href']
            if not url.startswith(self.url):
                if not url.startswith(("http", "https")) and "#" not in url:
                    self.sitemap['urls'].add('/' + url)
            else:
                url = url.split(self.domain)[1]
                if url.endswith("index.html"):
                    pass
                elif url.endswith("/"):
                    url += "index.html"
                else:
                    url += "/index.html"
                self.sitemap['urls'].add(url)
        return self.sitemap
