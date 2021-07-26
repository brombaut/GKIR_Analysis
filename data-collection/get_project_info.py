import os
import requests
import time
import utils

from dotenv import load_dotenv

load_dotenv()
USE_DEBUG_CONFIG = False

PROJECT_PATH = os.getenv('PROJECT_ROOT_PATH')
GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')

INPUT_CSV_FILE = 'gkir_repos.csv'
INPUT_CSV_FILE_PATH = f"{PROJECT_PATH}/csv/{INPUT_CSV_FILE}"
INPUT_CSV_FILE_FIELD_NAMES = [
    'repo_name',
]

OUTPUT_FILE_PATH = f"{PROJECT_PATH}/csv/gkir_repos_info.csv"
OUTPUT_FILE_FIELD_NAMES = [
    'repo_name',
    'is_fork',
    'size',
    'stargazers_count',
    'watchers_count',
    'language',
]


def main():
    if PROJECT_PATH is None:
        raise Exception("No PROJECT_ROOT_PATH")
    if GITHUB_ACCESS_TOKEN is None:
        raise Exception("No GITHUB_ACCESS_TOKEN")
    repos = utils.read_csv_ignore_headers(INPUT_CSV_FILE_PATH, INPUT_CSV_FILE_FIELD_NAMES)
    print("Starting...")
    total = len(repos)
    count = 0
    lines_to_write = list()
    for repo in repos:
        try:
            count += 1
            repo_name = repo['repo_name']
            print("\t{}/{} repo={}".format(count, total, repo_name))
            repos_info = get_repo_info(repo_name)
            lines_to_write.append({
                'repo_name': repo_name,
                'is_fork': repos_info['fork'],
                'size': repos_info['size'],
                'stargazers_count': repos_info['stargazers_count'],
                'watchers_count': repos_info['watchers_count'],
                'language': repos_info['language'],
            })
        except Exception as e:
            print("ERROR: Failed getting comments for issue={}".format(repo['repo_name']))
    utils.create_csv_file_if_necessary(OUTPUT_FILE_PATH, OUTPUT_FILE_FIELD_NAMES)
    utils.write_lines_to_existing_csv(OUTPUT_FILE_PATH, OUTPUT_FILE_FIELD_NAMES, lines_to_write)

    print("Done")


def get_repo_info(repo_name):
    url = f"https://api.github.com/repos/{repo_name}"
    headers = {'Authorization': 'token %s' % GITHUB_ACCESS_TOKEN}
    res = requests.get(url, headers=headers)
    time.sleep(0.8)
    response = res.json()
    return response


if __name__ == "__main__":
    main()
