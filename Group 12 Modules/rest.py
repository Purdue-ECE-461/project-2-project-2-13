import requests
import os


class GitRestAPI:

    def __init__(self, owner, repo):
        self.owner = owner
        self.repo = repo
        self.token = os.getenv('GITHUB_TOKEN')

    def getRepo(self):
        query_url = f"https://api.github.com/repos/{self.owner}/{self.repo}"
        params = {}

        headers = {'Authorization': f'token {self.token}'}
        r = requests.get(query_url, headers=headers, params=params)

        return r.json()
    # State can be open, closed, or all (default)
    def getIssues(self, state="all"):
        query_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/issues"
        params = {
            "state": state,
        }

        headers = {'Authorization': f'token {self.token}'}
        r = requests.get(query_url, headers=headers, params=params)

        return r.json()

    def getLicense(self):
        query_url = f"https://api.github.com/repos/{self.owner}/{self.repo}"
        params = {}

        headers = {'Authorization': f'token {self.token}'}
        r = requests.get(query_url, headers=headers, params=params)
        # print("this: ", r.json().get('license'))
        return r.json().get('license')

    def getCommits(self):
        query_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/commits"
        params = {}

        headers = {'Authorization': f'token {self.token}'}
        r = requests.get(query_url, headers=headers, params=params)

        #return len(r.json())
        return r.json()

    def getContributors(self):
        query_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/contributors"
        params = {}

        headers = {'Authorization': f'token {self.token}'}
        r = requests.get(query_url, headers=headers, params=params)

        return r.json()

    def getPullRequests(self, state="all"):
        query_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/pulls"
        params = {
            "state": state,
        }

        headers = {'Authorization': f'token {self.token}'}
        r = requests.get(query_url, headers=headers, params=params)

        return r.json()

    def getAllContributorsActivity(self):
        query_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/stats/contributors"
        params = {}

        headers = {'Authorization': f'token {self.token}'}
        r = requests.get(query_url, headers=headers, params=params)

        return r.json()

    def getREADME(self, branch="master"):
        query_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/readme"
        params = {
            "ref": branch,
        }

        headers = {'Authorization': f'token {self.token}'}
        r = requests.get(query_url, headers=headers, params=params)

        return r.json()

    def getURL(self):
        query_url = f"https://api.github.com/repos/{self.owner}/{self.repo}"
        params = {}

        headers = {'Authorization': f'token {self.token}'}
        r = requests.get(query_url, headers=headers, params=params)

        return r.json()['html_url']

    def getRateLimit(self):
        query_url = f"https://api.github.com/rate_limit"
        params = {}

        headers = {'Authorization': f'token {self.token}'}
        r = requests.get(query_url, headers=headers, params=params)
        return r.json()