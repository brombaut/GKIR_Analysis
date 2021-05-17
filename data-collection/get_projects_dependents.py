import os
import time
import utils
import requests

from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
USE_DEBUG_CONFIG = False

PROJECT_PATH = os.getenv('PROJECT_ROOT_PATH')
GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')
LIBRARIES_IO_ACCESS_TOKEN = os.getenv('LIBRARIES_IO_ACCESS_TOKEN')


INPUT_CSV_FILE = 'to_collect_project_dependents_for.csv'
INPUT_CSV_FILE_PATH = "{}/csv/{}".format(PROJECT_PATH, INPUT_CSV_FILE)
INPUT_CSV_FILE_FIELD_NAMES = [
    'repo_name',
]

OUTPUT_FOLDER_PATH = "{}/json/package_dependents".format(PROJECT_PATH)


def main():
    if PROJECT_PATH is None:
        raise Exception("No PROJECT_ROOT_PATH")
    if GITHUB_ACCESS_TOKEN is None:
        raise Exception("No GITHUB_ACCESS_TOKEN")
    if LIBRARIES_IO_ACCESS_TOKEN is None:
        raise Exception("No LIBRARIES_IO_ACCESS_TOKEN")
    entity_to_collect_for = utils.read_csv_ignore_headers(INPUT_CSV_FILE_PATH, INPUT_CSV_FILE_FIELD_NAMES)
    total = len(entity_to_collect_for)
    count = 0
    for x in entity_to_collect_for:
        try:
            repo_half_name = x['repo_name']
            count += 1
            print("\t{}/{} repo={}".format(count, total, repo_half_name))
            repo_full_name = get_repo_full_name_from_libraries_io(repo_half_name)

            output_file_name = "{}/{}.json".format(OUTPUT_FOLDER_PATH, repo_full_name.replace('/', '@'))
            if utils.file_or_read_file_already_exists(output_file_name):
                print("File Exists - Continuing")
                continue
            dependents = get_dependents(repo_full_name)
            utils.write_to_json_file(output_file_name, dependents)
        except Exception as e:
            print("ERROR: Failed for repo={}".format(x['repo_name']))
    print("Done")


def get_repo_full_name_from_libraries_io(repo_half_name):
    lib_name_for_url = repo_half_name.replace('/', '%2F')
    url = 'https://libraries.io/api/NPM/{}?api_key={}'.format(lib_name_for_url, LIBRARIES_IO_ACCESS_TOKEN)
    res = requests.get(url)
    response = res.json()
    gh_url = response['repository_url']
    repo_full_name = gh_url.split('https://github.com/')[1]
    return repo_full_name


def get_dependents(repo_full_name):
    url = 'https://github.com/{}/network/dependents?dependent_type=PACKAGE'.format(repo_full_name)
    result = list()
    count = 0
    while True:
        r = requests.get(url)
        print('\tRequest {}'.format(str(count)))
        count += 1
        soup = BeautifulSoup(r.content, "html.parser")
        ts = soup.findAll("div", {"class": "Box-row"})
        data = list()
        for t in ts:
            try:
                data.append(
                    "{}/{}".format(
                        t.find('a', {"data-repository-hovercards-enabled": ""}).text,
                        t.find('a', {"data-hovercard-type": "repository"}).text
                    )
                )
            except Exception:
                continue
        result.extend(data)
        pagination_containers = soup.find("div", {"class": "paginate-container"}).find_all('a')
        pagination_container = None
        for pc in pagination_containers:
            href = pc['href']
            if 'dependents_after' in href:
                pagination_container = pc
        if pagination_container:
            url = pagination_container["href"]
            time.sleep(0.8)
        else:
            break
    return result


if __name__ == "__main__":
    main()
