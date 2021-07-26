import os
import requests
import time
import utils

from dotenv import load_dotenv

load_dotenv()
USE_DEBUG_CONFIG = False

PROJECT_PATH = os.getenv('PROJECT_ROOT_PATH')
GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')

INPUT_CSV_FILE = 'ngkirs_to_collect_issue_events_for.csv'
INPUT_CSV_FILE_PATH = "{}/csv/{}".format(PROJECT_PATH, INPUT_CSV_FILE)
INPUT_CSV_FILE_FIELD_NAMES = [
    "id",
    'repo_name',
    'number',
    'events_url'
]

OUTPUT_FOLDER_PATH = "{}/json/issue_events".format(PROJECT_PATH)


def main():
    if PROJECT_PATH is None:
        raise Exception("No PROJECT_ROOT_PATH")
    if GITHUB_ACCESS_TOKEN is None:
        raise Exception("No GITHUB_ACCESS_TOKEN")
    issues = utils.read_csv_ignore_headers(INPUT_CSV_FILE_PATH, INPUT_CSV_FILE_FIELD_NAMES)
    print("Starting...")
    total = len(issues)
    count = 0
    print('Skipping thru read ones...')
    for issue in issues:
        try:
            count += 1
            issue_id = issue['id']
            repo_name = issue['repo_name']
            events_url = issue['events_url']
            output_file_name = "{}/issue_events@issue@{}@{}.json".format(OUTPUT_FOLDER_PATH, issue_id, repo_name.replace('/', '@'))
            if utils.file_or_read_file_already_exists(output_file_name):
                continue
            print("\t{}/{} repo={}".format(count, total, repo_name))
            issue_events = get_events(events_url)
            utils.write_to_json_file(output_file_name, issue_events)
        except Exception as e:
            print("ERROR: Failed getting comments for issue={}".format(issue['id']))
    print("Done")


def get_events(events_url):
    url = "{}?per_page=100".format(events_url)
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
