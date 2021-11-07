import sys
import requests
from random import *
import os
from dotenv import load_dotenv
import logging
from bs4 import BeautifulSoup
import re
load_dotenv()

# Put your GITHUB_TOKEN to the variable in the .env file
header = {
    'accept': 'application/vnd.github.v3+json',
    'Authorization': f"token {os.getenv('GITHUB_TOKEN')}"
}


def getDependencies(owner, module):
    url = 'https://github.com/{}/network/dependencies'.format(owner + '/' + module)

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")

    data = [
        "{}/{}".format(
            t.find('a', {"data-repository-hovercards-enabled": ""}).text,
            t.find('a', {"data-hovercard-type": "repository"}).text
        )
        for t in soup.findAll("div", {"class": "Box-row"})
    ]
    p = "([a-zA-Z]+ [/] [a-zA-Z]+)"

    for d in data:
        d = d.strip()
        m = re.findall(p, d)
        d = m[0]
    return data


def getRepo(owner, module):  # Returns the general information of the repo
    params = {}
    response = requests.get(url='https://api.github.com/repos/' + owner + '/' + module, headers=header,
                            params=params).json()
    if (len(response)) == 0:
        logging.warning("Error")
    return response


def getIssues(owner, module):  # Returns Issues directory
    params = {
        'state': 'closed',
        'per_page': '100',
    }
    response = requests.get(url='https://api.github.com/repos/' + owner + '/' + module + '/issues',
                            headers=header).json()
    if (len(response)) == 0:
        logging.warning("Error")
    return response


def getNumOfIssues(owner, module):  # Returns number of closed issues
    numOfIssues = 1
    response = requests.get(
        url='https://api.github.com/search/issues?q=repo:' + owner + '/' + module + '+type:issue+state:closed',
        headers=header).json()
    numOfIssues = response['total_count']
    if (len(response)) == 0:
        logging.warning("Error")
    return numOfIssues


def getNumofContributors(owner, module):
    response = getRepo(owner, module)

    contributors_url = response['contributors_url']
    response = requests.get(contributors_url)
    return len(response.json())
