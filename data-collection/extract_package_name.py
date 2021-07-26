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

OUTPUT_FILE_PATH = f"{PROJECT_PATH}/csv/repo_npm_package_info.csv"
OUTPUT_FIELD_NAMES = [
    'repo_name',
    'package_name',
]

def main():
    if PROJECT_PATH is None:
        raise Exception("No PROJECT_ROOT_PATH")
    if GITHUB_ACCESS_TOKEN is None:
        raise Exception("No GITHUB_ACCESS_TOKEN")
    repos = utils.read_csv_ignore_headers(INPUT_CSV_FILE_PATH, INPUT_CSV_FILE_FIELD_NAMES)
    total = len(repos)
    count = 0
    list_to_write = list()
    for repo in repos:
        repo_name = repo['repo_name']
        try:
            count += 1
            print("\t{}/{} repo={}".format(count, total, repo_name))
            project_git_folder = f"{REPOS_PATH}/repos/{repo_name.replace('/', '#')}"
            if os.path.isdir(project_git_folder):
                package_json_path = f"{project_git_folder}/package.json"
                if utils.file_or_read_file_already_exists(package_json_path):
                    package_json_contents = utils.load_json_file(package_json_path)
                    # Will throw if 'name' is not there
                    list_to_write.append({
                        'repo_name': repo_name,
                        'package_name': package_json_contents['name']
                    })
                else:
                    # package.json doesn't exist
                    list_to_write.append({
                        'repo_name': repo_name,
                        'package_name': None
                    })
            else:
                # Could not clone project
                list_to_write.append({
                    'repo_name': repo_name,
                    'package_name': None
                })
        except Exception as e:
            list_to_write.append({
                'repo_name': repo_name,
                'package_name': None
            })
    utils.write_lines_to_new_csv(OUTPUT_FILE_PATH, OUTPUT_FIELD_NAMES, list_to_write)
    print("Done")


if __name__ == "__main__":
    main()
