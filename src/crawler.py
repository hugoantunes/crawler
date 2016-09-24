# encoding: utf-8
import requests


class Crawler(object):

    def __init__(self, url):
        self.url = url
        self.check_status_code()

    def check_status_code(self):
        response = requests.get(self.url)
        if response.status_code == 404:
            raise Exception("Url does not exist")
