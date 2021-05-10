import os
import requests
import time
import utils

from dotenv import load_dotenv

load_dotenv()
USE_DEBUG_CONFIG = False

PROJECT_PATH = os.getenv('PROJECT_ROOT_PATH')
GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')

ISSUES_TO_COLLECT_COMMENTS_FOR_CSV_FILE = 'issues_to_collect_comments_for.csv'
ISSUES_TO_COLLECT_COMMENTS_FOR_CSV_FILE_PATH = "{}/csv/{}".format(PROJECT_PATH, ISSUES_TO_COLLECT_COMMENTS_FOR_CSV_FILE)
ISSUES_CSV_FILE_FIELD_NAMES = [
    "id",
    'repo_name',
    'comments_url',
]

OUTPUT_FOLDER_PATH = "{}/json/comments".format(PROJECT_PATH)


def main():
    if PROJECT_PATH is None:
        raise Exception("No PROJECT_ROOT_PATH")
    if GITHUB_ACCESS_TOKEN is None:
        raise Exception("No GITHUB_ACCESS_TOKEN")
    issues = utils.read_csv_ignore_headers(ISSUES_TO_COLLECT_COMMENTS_FOR_CSV_FILE_PATH, ISSUES_CSV_FILE_FIELD_NAMES)
    print("Getting all comments for issues...")
    total = len(issues)
    count = 0
    print('Skipping thru read ones...')
    for issue in issues:
        try:
            count += 1
            issue_id = issue['id']
            repo_name = issue['repo_name']
            comments_url = issue['comments_url']
            output_file_name = "{}/comments@issue@{}@{}.json".format(OUTPUT_FOLDER_PATH, issue_id, repo_name.replace('/', '@'))
            if utils.file_or_read_file_already_exists(output_file_name):
                continue
            print("\t{}/{} repo={}".format(count, total, repo_name))
            issue_comments = get_comments(comments_url)
            utils.write_to_json_file(output_file_name, issue_comments)
        except Exception as e:
            print("ERROR: Failed getting comments for issue={}".format(issue['id']))
    print("Done")


def get_comments(comments_url):
    url = "{}?per_page=100".format(comments_url)
    headers = {'Authorization': 'token %s' % GITHUB_ACCESS_TOKEN}
    res = requests.get(url, headers=headers)
    time.sleep(0.8)
    result = list()
    response = res.json()
    for pr in response:
        result.append(pr)
    while 'next' in res.links.keys():
        res = requests.get(res.links['next']['url'], headers=headers)
        time.sleep(0.8)
        response = res.json()
        for pr in response:
            result.append(pr)
    return result


if __name__ == "__main__":
    main()
