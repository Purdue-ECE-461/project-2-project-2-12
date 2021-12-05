import json
from urllib.parse import urlparse
from .metrics import *
import re
import logging
from bs4 import BeautifulSoup
import urllib
import urllib.request


class Package:
    def __init__(self, url):
        npm_flag = 'www.npmjs.com'
        line_copy = url
        if npm_flag in url:
            owner, module = self.urlParse(url)
            line_copy = self.getNpmRepo(url)
        owner, module = self.urlParse(line_copy)

        test_response = getRepo(owner, module)
        if 'message' in test_response:
            logging.warning("bad credentials")
            import sys
            sys.exit()

        self.url = url
        self.rampup = getRampUpTime(owner, module)
        self.correctness = getCorrectness(owner, module)
        self.bus_factor = getBusFactor(owner, module)
        self.responsiveness = getResponsiveness(owner, module)
        self.license_score = getLicenseComp(owner, module)
        self.good_pinning_practice = getDependencyScore(owner, module)

    def getNpmRepo(self, url):
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        git_url_box = soup.find('a', attrs={'class': 'b2812e30 f2874b88 '
                                                     'fw6 mb3 mt2 truncate black-80 f4 link'})
        git_url = 'https://' + git_url_box.text[3:]

        """ This is the original code """
        # response = requests.get(git_url).json()
        # print(response["results"][0]["package"]["links"])
        # git_url = response["results"][0]["package"]["links"]["repository"]
        return git_url

    def urlParse(self, url):
        parse = urlparse(url)  # Parses URL to specific components
        path = parse[2]  # Variable for storing path (ex: /lodash/lodash)
        ownerModule = re.split(r'/', path)
        owner = ownerModule[1]

        module = ownerModule[2].strip('\n')
        return owner, module
