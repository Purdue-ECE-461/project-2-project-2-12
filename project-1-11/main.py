import json
from urllib.parse import urlparse
from metrics import *
import os
import re
import logging
from bs4 import BeautifulSoup
import urllib
import urllib.request

class Package:
    def __init__(self, url):
        self.url = url
        self.total_score = self.getTotalScore(url)

    def getTotalScore(self, url):
        printStrings = {}
        npm_flag = 'www.npmjs.com'
        line_copy = url
        if npm_flag in url:
            owner, module = self.urlParse(url)
            line_copy = self.getNpmRepo(url)
        owner, module = self.urlParse(line_copy)

        logging.info(f"URL: {url}")
        logging.info(f"Repository Owner: {owner} " + f" Module: {module}")

        # Change the owner and module name to corresponding names to test for different repo
        test_response = getRepo(owner, module)
        if 'message' in test_response:
            logging.warning("bad credentials")
            import sys
            sys.exit()
        logging.info("Fetching repo, calculating scores...")
        rsp_score = getResponsiveness(owner, module)
        rmp_score = getRampUpTime(owner, module)
        cor_score = getCorrectness(owner, module)
        bus_score = getBusFactor(owner, module)
        license_score = getLicenseComp(owner, module)
        depend_score = getDependencyScore(owner, module)
        total_score = getTotalScore(rsp_score, rmp_score, cor_score, bus_score, license_score, depend_score)
        logging.info("Metric scores succesfully calculated.")
        printStrings[url] = f"{total_score}"
        return json.dumps(printStrings)

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


if __name__ == "__main__":
    # pkg = Package('https://github.com/lodash/lodash')
    # json = pkg.total_score
    # print(json)

    pkg2 = Package('https://www.npmjs.com/package/browserify')
    json2 = pkg2.total_score
    print(json2)

