import os
import requests
import time
import utils

from dotenv import load_dotenv

load_dotenv()
USE_DEBUG_CONFIG = False

PROJECT_PATH = os.getenv('PROJECT_ROOT_PATH')
GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')

INPUT_CSV_FILE = 'to_recollect_commits_for.csv'
INPUT_CSV_FILE_PATH = "{}/csv/{}".format(PROJECT_PATH, INPUT_CSV_FILE)
INPUT_CSV_FILE_FIELD_NAMES = [
    'repo_name',
    'issue_id',
    'sha',
]

OUTPUT_FOLDER_PATH = "{}/json/commits".format(PROJECT_PATH)


def main():
    if PROJECT_PATH is None:
        raise Exception("No PROJECT_ROOT_PATH")
    if GITHUB_ACCESS_TOKEN is None:
        raise Exception("No GITHUB_ACCESS_TOKEN")
    commits_to_collect = utils.read_csv_ignore_headers(INPUT_CSV_FILE_PATH, INPUT_CSV_FILE_FIELD_NAMES)
    print("Getting all comments for issues...")
    total = len(commits_to_collect)
    count = 0
    for c in commits_to_collect:
        try:
            issue_id = c['issue_id']
            repo_name = c['repo_name']
            sha = c['sha']
            count += 1
            print("\t{}/{} sha={}".format(count, total, sha))
            output_file_name = "{}/commit@{}@issue@{}@{}.json".format(OUTPUT_FOLDER_PATH, sha, issue_id, repo_name.replace('/', '@'))
            if utils.file_or_read_file_already_exists(output_file_name):
                print("File Exists - Continuing")
                continue
            commit_url = f'https://api.github.com/repos/{repo_name}/commits/{sha}'
            commit_json = get_commit_json(commit_url)
            utils.write_to_json_file(output_file_name, commit_json)
        except Exception as e:
            print("ERROR: Failed getting comments for issue={}".format(issue['id']))
    print("Done")


def get_commit_json(comments_url):
    url = "{}?per_page=100".format(comments_url)
    headers = {'Authorization': 'token %s' % GITHUB_ACCESS_TOKEN}
    res = requests.get(url, headers=headers)
    time.sleep(0.8)
    # result = list()
    response = res.json()
    return response
    # for pr in response:
    #     result.append(pr)
    # while 'next' in res.links.keys():
    #     res = requests.get(res.links['next']['url'], headers=headers)
    #     time.sleep(0.8)
    #     response = res.json()
    #     for pr in response:
    #         result.append(pr)
    # return result


if __name__ == "__main__":
    main()
