import git
import os
import requests
import time
import utils
import subprocess

from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()
USE_DEBUG_CONFIG = False

PROJECT_PATH = os.getenv('PROJECT_ROOT_PATH')
GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')

REPOS_PATH = f"{PROJECT_PATH}/repo-cloning"

INPUT_CSV_FILE = 'repos_list.csv'
INPUT_CSV_FILE_PATH = f"{REPOS_PATH}/{INPUT_CSV_FILE}"
INPUT_CSV_FILE_FIELD_NAMES = [
    'repo_name',
]

def main():
    if PROJECT_PATH is None:
        raise Exception("No PROJECT_ROOT_PATH")
    if GITHUB_ACCESS_TOKEN is None:
        raise Exception("No GITHUB_ACCESS_TOKEN")
    repos = utils.read_csv_ignore_headers(INPUT_CSV_FILE_PATH, INPUT_CSV_FILE_FIELD_NAMES)
    total = len(repos)
    count = 0
    for repo in repos:
        try:
            repo_name = repo['repo_name']
            count += 1
            print("\t{}/{} repo={}".format(count, total, repo_name))

            output_folder = f"{REPOS_PATH}/repos/{repo_name.replace('/', '#')}"
            if os.path.isdir(output_folder):
                continue
            os.mkdir(output_folder)
            subprocess.call(['git', 'clone', f'git@github.com:{repo_name}.git', output_folder])
            # git clone git@github.com:${repo}.git ${REPOS_DATA_DIR}${repo_dir}
        except Exception as e:
            print("ERROR: Failed getting issues for repo={}".format(repo['repo']))
    print("Done")


if __name__ == "__main__":
    main()
