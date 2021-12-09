import math
import requests
import os
from pprint import pprint
import logging

from requests import api
from github import Github
import rest
import re

import sys
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import urllib.request
import urllib3
from datetime import datetime
os.environ["LOG_FILE"] = "./log.txt"
os.environ["GITHUB_TOKEN"] = "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"

# Use this base url for now
# https://github.com/githubtraining/hellogitworld
# You can see the repo at https://github.com/MartinHeinz/python-project-blueprint
# This will make it easier to get the grading working then we can use run.py to get all the URLs


def getNetScore(owner, repo, log):
    token = os.getenv('GITHUB_TOKEN')
    # Base API Object used to call methods in rest.py
    apiObj = rest.GitRestAPI(owner, repo)
    repo = apiObj.getRepo()
    
    array_name = repo['html_url'].split('/')
    array_name.reverse()
    first = array_name[1]
    second = array_name[0]
    final = first+'/'+second


    

    if len(repo) == 2 and apiObj.getCommits()['message'] == 'Not Found':
        log.error("GitHub repository not found\nExiting safely")
        return 1, -1

    responsivenessScore = gradeResponsiveness(apiObj, log)
    if responsivenessScore == -1:
        return 1, -1
    busScore = gradeBusFactor(apiObj, log)
    if busScore == -1:
        return 1, -1
    licenseScore = gradeLicense(apiObj, log)
    if licenseScore == -1:
        return 1, -1
    rampUpScore = gradeRampUp(apiObj, log)
    if rampUpScore == -1:
        return 1, -1
    correctnessScore = gradeCorrectness(apiObj, log)
    if correctnessScore == -1:
        return 1, -1
    versionScore = grade_version(apiObj,log,first,second)
    if versionScore == -1:
        return 1,-1
    versionScore = versionScore 
    totalScore = licenseScore * (0.3 * responsivenessScore) + (0.1 * busScore) + (.2 * correctnessScore) + (
            .1 * rampUpScore) * (0.3 * (versionScore/10))

    print(
        f"{repo['html_url']} {round(totalScore, 2)} {round(rampUpScore, 2)} {round(correctnessScore, 2)} {round(busScore, 2)} {round(responsivenessScore, 2)} {round(licenseScore, 2)} {round(versionScore, 2)}")
    
    logger.info("Net score calculated")
    return 0, totalScore

def printOutput():
    pass


# For these functions, call apiObj functions and use that information to calculate grades

# if repo has a README and if README has content
def gradeRampUp(apiObj, log) -> float:
    logger.info("Grading Ramp Up")
    if 'message' in apiObj.getRepo().keys():
        log.error("Repo not found")
        return -1
    readme = apiObj.getREADME()
    if len(readme) == 2 and 'message' in readme.keys():
        return 0
    elif readme['size'] > 0:
        return 1

def grade_version(apiObj,log,first,second)->float:
    headers = {"Authorization": "Bearer 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",
                "Accept":"application/vnd.github.hawkgirl-preview+json"}


    def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
        request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
    
    
       
    # The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.       
    query = """
    {
    repository(owner:"%s", name:"%s") {
        dependencyGraphManifests {
        totalCount
        nodes {
            filename
        }
        edges {
            node {
            blobPath
            dependencies {
                totalCount
                nodes {
                packageName
                requirements
                hasDependencies
                packageManager
                }
            }
            }
        }
        }
    }
    }
    """%(first,second)
    all_dependencies = []
    result = run_query(query) # Execute the query

    if(result['data']['repository'] == None):
        return 0
        
    result = result["data"]["repository"]["dependencyGraphManifests"]["edges"]
    if(result == []):
        return 1
    for i in range(len(result[0]['node']['dependencies']['nodes'])):
        all_dependencies.append(result[0]['node']['dependencies']['nodes'][i]['requirements'])
    if(len(all_dependencies) > 2):
        return 0
# Need Number of issues, sum of open and closed issues, active contributors, total contributors
def gradeCorrectness(apiObj, log) -> float:
    logger.info("Grading Correctness")
    if 'message' in apiObj.getRepo().keys():
        log.error("Repo not found")
        return -1
    numOpenIssues = apiObj.getRepo()['open_issues_count']
    numClosedIssues = len(apiObj.getIssues('closed'))
    totalNumContributors = len(apiObj.getContributors())

    contributorActivity = apiObj.getAllContributorsActivity()
    numActiveContributors = getNumActiveContributors(contributorActivity, totalNumContributors)

    if numClosedIssues == 0:
        return numActiveContributors / totalNumContributors

    outScore = (numOpenIssues / numClosedIssues) + (numActiveContributors / totalNumContributors)
    if outScore > 1:
        outScore = 1

    return outScore


def getNumActiveContributors(contributorActivity, totalNumContributors) -> float:
    totalAdditions = 0
    totalCommits = 0
    totalDeletions = 0
    contAct = []
    for contributor in contributorActivity:
        additions = []
        commits = []
        deletions = []
        summary = {}
        for week in contributor['weeks']:
            additions.append(week['a'])
            deletions.append(week['d'])
            commits.append(week['c'])

        summary['a'] = sum(additions)
        summary['c'] = sum(commits)
        summary['d'] = sum(deletions)
        contAct.append(summary)
        totalAdditions += sum(additions)
        totalCommits += sum(commits)
        totalDeletions += sum(deletions)

    avgNumAdditions = totalAdditions / totalNumContributors
    avgNumCommits = totalCommits / totalNumContributors
    avgNumDeletions = totalDeletions / totalNumContributors
    num = 0
    for contributor in contAct:
        if contributor['a'] > avgNumAdditions or contributor['c'] > avgNumCommits or contributor['d'] > avgNumDeletions:
            num += 1
    return num




def gradeResponsiveness(apiObj, log) -> float:
    logger.info("Grading Responsiveness")
    closedIssues = apiObj.getIssues('closed')
    if len(closedIssues) == 2 and 'message' in closedIssues.keys():
        log.error(f"This repository cannot be obtained due to: {closedIssues['message']}")
        return -1
    count = 0
    issuesCreatedAt = []
    issuesClosedAt = []
    timeOfIssue = []

    for issue in closedIssues:
        issuesCreatedAt.append(issue['created_at'])
        issuesClosedAt.append(issue['closed_at'])
        timeOfIssue.append(getTime(issuesCreatedAt[count], issuesClosedAt[count]))
        count += 1

    avgTimeInSec = sum(timeOfIssue) / len(timeOfIssue)
    avgTimeInDays = avgTimeInSec / 60 / 60 / 24

    score = 1 / math.sqrt(.25 * avgTimeInDays + 1)
    return score


def gradeLicense(apiObj, log) -> float:
    logger.info("Grading License")
    compatibleLicenses = ['MIT License', None, 'BSD-new License']
    if 'message' in apiObj.getRepo().keys():
        log.error("Repo not found")
        return -1

    license = apiObj.getLicense()
    if license == None:
        return 1
    elif license['name'] in compatibleLicenses:
        return 1
    else:
        return 0


def gradeBusFactor(apiObj, log) -> float:
    logger.info("Grading Bus Factor")
    if 'message' in apiObj.getRepo().keys():
        log.error("Repo not found")
        return -1

    numContributors = len(apiObj.getContributors())
    numCommits = len(apiObj.getCommits())
    firstCommitDate = apiObj.getCommits()[numCommits - 1].get('commit').get('author').get('date')
    lastCommitDate = apiObj.getCommits()[0].get('commit').get('author').get('date')

    yearsActive = getTime(firstCommitDate, lastCommitDate)
    score = numCommits * (numCommits / numContributors) * (numCommits / numContributors / yearsActive)
    
    return score


def getTime(created, closed) -> datetime.time:
    issueCreated = created
    createdDate = re.search("[0-9]{4}-[0-9]{2}-[0-9]{2}", issueCreated).group()
    createdTime = re.search("[0-9]{2}:[0-9]{2}:[0-9]{2}", issueCreated).group()

    issueClosed = closed
    closedDate = re.search("[0-9]{4}-[0-9]{2}-[0-9]{2}", issueClosed).group()
    closedTime = re.search("[0-9]{2}:[0-9]{2}:[0-9]{2}", issueClosed).group()

    format = '%Y-%m-%d %H:%M:%S'
    timeClosed = datetime.strptime(closedDate + ' ' + closedTime, format)
    timeCreated = datetime.strptime(createdDate + ' ' + createdTime, format)
    totalTime = abs(timeClosed - timeCreated)
    sec = totalTime.seconds
    day = totalTime.days * 24 * 60 * 60
    return sec + day


if __name__ == "__main__":
    logLevel = 0
    if os.getenv('LOG_FILE') is None:
        print("Please set your LOG_FILE environment variable")
        sys.exit(1)
    if os.getenv('GITHUB_TOKEN') is None:
        print("Please set your GITHUB_TOKEN environment variable")
        sys.exit(1)
    if os.getenv('LOG_LEVEL') != None:
        logLevel = os.getenv('LOG_LEVEL')
        
    LOG = os.getenv('LOG_FILE')
    if logLevel == '1':
        logging.basicConfig(filename=LOG, filemode="w", level=logging.INFO)
    elif logLevel == '2':
        logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)

    logger = logging.getLogger(__name__)

    logger.info('Environment variables set up correctly! Proceeding with execution')
        
    
    
    if len(sys.argv) == 2:
        try:
            with open(sys.argv[1], "r") as f:
                
                lines = f.readlines()
                urls = []
                allScores = {}
                for i in range(len(lines)):
                    urls.append(lines[i].strip('\n'))
                for url in urls:
                    try:
                        inputUrl = ''
                        if "npmjs" in url:
                            page = urllib.request.urlopen(url)
                            soup = BeautifulSoup(page, 'html.parser')
                            git_url_box = soup.find('a', attrs={'class': 'b2812e30 f2874b88 fw6 mb3 mt2 truncate black-80 f4 link'})
                            git_url = 'https://' + git_url_box.text[3:]
                            inputUrl = git_url
                            logger.info("Found NPM URL")
                        else:
                            inputUrl = url
                            logger.info("Found GitHub URL")

                        response = requests.get(inputUrl)
                        directories = (urlparse(inputUrl).path.strip('/').split('/'))
                        directories[1] = directories[1].strip()
                        logger.info("Calculating total score")
                        exitCode, totalScore = getNetScore(directories[0], directories[1], logger)
                        allScores[totalScore] = url
                    except:
                        logger.error("invalid url")
                        # sys.exit(1)t

                sortedScores = list(allScores.keys())
                sortedScores.sort(reverse=True)
                file = open("trustworthyModules", "w")
                for score in sortedScores:
                    file.write(allScores[score])
                    file.write(" ")
                    file.write(str(round(score, 2)))
                    file.write("\n")
                file.close()
                sys.exit(0)
        except IOError:
            logger.debug("Input file does not exist")
            sys.exit(1)
    else:
        LOG = "LOG_FILE"
        logging.basicConfig(filename=LOG, filemode="w", level=0)
        logger = logging.getLogger(__name__)
        logger.debug("Please provide an input file")
        sys.exit(1)
