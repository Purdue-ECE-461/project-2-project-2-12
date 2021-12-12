from .request_handle import *


def getDependencyScore(owner, module):
    score = 0
    response = getDependencies(owner, module)
    if len(response) == 0:
        return 1
    else:
        return 1 / len(response)


def getResponsiveness(owner, module):
    score = 0
    repo = getRepo(owner, module)
    issues = getIssues(owner, module)
    #   Calculating the Issue close ratio
    open_issues = repo['open_issues']
    if open_issues == 0:
        score = 1
    else:
        closed_issues = getNumOfIssues(owner, module)
        score = 100 - (100 / ((closed_issues + open_issues) / open_issues))
    #   Adjust score based on the number of subscribers (More subscribes, better responsiveness)
    sub_count = repo['subscribers_count']
    if sub_count < 999:
        score = score + (sub_count / 100)
    else:
        score = score + 10
    #   Check if the Repo has a wiki, if not, decrease the score.
    has_wiki = repo['has_wiki']
    if not has_wiki:
        score = score * 0.7
    #   Check if the Repo is archived, if so, decrease the score significantly.
    is_archived = repo['archived']
    if is_archived:
        score = score * 0.5
    score = score / 100
    if score >= 1:
        score = 1
    return score


def getRampUpTime(owner, module):
    # TODO: Calculate score for Ramp up time, return integer between 1-10 as score
    score = 0
    repo = getRepo(owner, module)
    # if repo has a wiki (more than a readme) increase score
    if repo['has_wiki']:
        score += 4

    # if repo has many watchers increase the score
    watchers_count = repo['watchers_count']
    if watchers_count != 0:
        score += 3 * pow(9000, -1000.0 / repo['watchers_count'])
    # if repo has many forks increase the score
    forks_count = repo['forks_count']
    if forks_count != 0:
        score += 3 * pow(2, -1000.0 / repo['forks_count'])
    return score / 10


def getCorrectness(owner, module):
    # TODO: Calculate score for Ramp up time, return integer between 1-10 as score
    score = 0
    repo = getRepo(owner, module)
    # if repo has many issues, reduce the score
    score += 10 * pow(1.001, 0 - repo['open_issues_count'])
    return score / 10


def getBusFactor(owner, module):
    # TODO: Calculate score for Ramp up time, return integer between 1-10 as score
    numOfContributors = getNumofContributors(owner, module)
    score = 15 ** (-1 / numOfContributors)
    return score


def getLicenseComp(owner, module):
    # TODO: Calculate score for Ramp up time, return 1 or 0 as score
    compatibleLicenses = ["bsd-2-clause",
                          "bsd-3-clause", "lgpl-2.1", "mit", "unlicense"]
    response = getRepo(owner, module)

    if response['license'] is None:
        return 1

    if response['license']['key'] in compatibleLicenses:
        return 1

    return 0


def getTotalScore(rsp_score, rmp_score, cor_score, bus_score, license_score, depen_score):

    totalScore = ((2 * rsp_score + rmp_score + cor_score + 2 *
                  bus_score + depen_score) * license_score) / 6
    return totalScore
