import json
from urllib.parse import urlparse
from metrics import *
import os
import re
import logging
from bs4 import BeautifulSoup
import urllib
import urllib.request


def getNpmRepo(url):
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


def urlParse(url):
    parse = urlparse(url)  # Parses URL to specific components
    path = parse[2]  # Variable for storing path (ex: /lodash/lodash)
    ownerModule = re.split(r'/', path)
    owner = ownerModule[1]

    module = ownerModule[2].strip('\n')
    return owner, module

def main(numArgs, input):
    npm_flag = 'www.npmjs.com'
    printOrder = []
    printStrings = {}
    levels = {'0': logging.CRITICAL, '1': logging.INFO, '2': logging.DEBUG}
    logging.basicConfig(filename=os.getenv('LOG_FILE'), level=levels[os.getenv('LOG_LEVEL')], filemode="w")
    if numArgs < 2:
        logging.info("DEBUG - Wrong number of inputs!")

    with open(input) as f:
        lines = f.readlines()
    for line in lines:
        line_copy = line
        if npm_flag in line:
            owner, module = urlParse(line)
            line_copy = getNpmRepo(line)
        owner, module = urlParse(line_copy)

        logging.info(f"URL: {line}")
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
        line = line.strip("\n")
        printOrder.append(total_score)
        printStrings[line] = f"{total_score}"
        # printStrings[
        #     total_score] = f"{line} {round(total_score, 2)} {round(rmp_score, 2)} {round(cor_score, 2)} {round(bus_score, 2)} {round(rsp_score, 2)} {round(license_score, 2)} {round(depend_score, 2)}"

    return json.dumps(printStrings)


if __name__ == "__main__":
    json = main(len(sys.argv), sys.argv[1])
    print(json)
    # print(printStrings)
    # printOrder.sort()
    # for i in printOrder[::-1]:
    #     print(printStrings[i])
