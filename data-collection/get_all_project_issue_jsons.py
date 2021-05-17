import os
import requests
import time
import utils

from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()
USE_DEBUG_CONFIG = False

PROJECT_PATH = os.getenv('PROJECT_ROOT_PATH')
GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')

REPO_CSV_FILE = 'package_dependents.csv'
REPOS_FILE_PATH = "{}/csv/{}".format(PROJECT_PATH, REPO_CSV_FILE)
REPOs_FILED_NAMES = [
    'repo_name',
    'dependent',
]

OUTPUT_FOLDER_PATH = "{}/json/issues".format(PROJECT_PATH)


def main():
    if PROJECT_PATH is None:
        raise Exception("No PROJECT_ROOT_PATH")
    if GITHUB_ACCESS_TOKEN is None:
        raise Exception("No GITHUB_ACCESS_TOKEN")
    repos = utils.read_csv_ignore_headers(REPOS_FILE_PATH, REPOs_FILED_NAMES)
    print("Getting all Issues for repos...")
    total = len(repos)
    count = 0
    for repo in repos:
        try:
            repo_name = repo['dependent']
            count += 1
            print("\t{}/{} repo={}".format(count, total, repo_name))
            output_file_name = "{}/issues@{}.json".format(OUTPUT_FOLDER_PATH, repo_name.replace('/', '@'))
            if utils.file_or_read_file_already_exists(output_file_name):
                print("File Exists - Continuing -- repo={}".format(repo_name))
                continue
            repo_issues = get_issues(repo_name)
            utils.write_to_json_file(output_file_name, repo_issues)
        except Exception as e:
            print("ERROR: Failed getting issues for repo={}".format(repo['repo']))
    print("Done")


def get_issues(repo_full_name):
    url = "https://api.github.com/repos/{}/issues?state=all&sort=created&direction=asc&per_page=100".format(repo_full_name)
    headers = {'Authorization': 'token %s' % GITHUB_ACCESS_TOKEN}
    res = requests.get(url, headers=headers)
    time.sleep(1)
    result = list()
    response = res.json()
    for pr in response:
        result.append(pr)
    while 'next' in res.links.keys():
        res = requests.get(res.links['next']['url'], headers=headers)
        time.sleep(1)
        response = res.json()
        for pr in response:
            result.append(pr)
    return result


if __name__ == "__main__":
    main()
