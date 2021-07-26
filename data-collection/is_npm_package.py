import os
import time
import utils
import requests

# from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
USE_DEBUG_CONFIG = False

PROJECT_PATH = os.getenv('PROJECT_ROOT_PATH')
GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')
LIBRARIES_IO_ACCESS_TOKEN = os.getenv('LIBRARIES_IO_ACCESS_TOKEN')


INPUT_CSV_FILE_PATH = f"{PROJECT_PATH}/csv/repo_npm_package_info.csv"
INPUT_CSV_FILE_FIELD_NAMES = [
    'repo_name',
    'package_name',
]

OUTPUT_FILE_PATH = f"{PROJECT_PATH}/csv/repo_npm_package_info_with_libraries_io.csv"
OUTPUT_FIELD_NAMES = [
    'repo_name',
    'package_name',
    'use_repo_name',
    'on_libraries_io_npm',
    'npm_dependent_repos_count',
    'npm_dependents_count',
    'npm_forks',
    'npm_language',
    'npm_rank',
    'npm_stars',
]


def main():
    if PROJECT_PATH is None:
        raise Exception("No PROJECT_ROOT_PATH")
    if GITHUB_ACCESS_TOKEN is None:
        raise Exception("No GITHUB_ACCESS_TOKEN")
    if LIBRARIES_IO_ACCESS_TOKEN is None:
        raise Exception("No LIBRARIES_IO_ACCESS_TOKEN")
    utils.create_csv_file_if_necessary(OUTPUT_FILE_PATH, OUTPUT_FIELD_NAMES)
    entries = utils.read_csv_ignore_headers(INPUT_CSV_FILE_PATH, INPUT_CSV_FILE_FIELD_NAMES)
    total = len(entries)
    count = 0
    for x in entries:
        lines_to_write = list()
        repo_name = x['repo_name']
        package_name = x['package_name']
        use_repo_name = False
        try:
            count += 1
            print("\t{}/{} repo={}".format(count, total, package_name))
            if not package_name:
                use_repo_name = True
                package_name = repo_name.split('/')[1]
            libraries_io_response = get_libraries_io_response(package_name)
            if 'error' in libraries_io_response:
                lines_to_write.append({
                    'repo_name': repo_name,
                    'package_name': package_name,
                    'use_repo_name': use_repo_name,
                    'on_libraries_io_npm': False,
                    'npm_dependent_repos_count': None,
                    'npm_dependents_count': None,
                    'npm_forks': None,
                    'npm_language': None,
                    'npm_rank': None,
                    'npm_stars': None,
                })
                utils.write_lines_to_existing_csv(OUTPUT_FILE_PATH, OUTPUT_FIELD_NAMES, lines_to_write)
            else:
                lines_to_write.append({
                    'repo_name': repo_name,
                    'package_name': package_name,
                    'use_repo_name': use_repo_name,
                    'on_libraries_io_npm': True,
                    'npm_dependent_repos_count': libraries_io_response['dependent_repos_count'],
                    'npm_dependents_count': libraries_io_response['dependents_count'],
                    'npm_forks': libraries_io_response['forks'],
                    'npm_language': libraries_io_response['language'],
                    'npm_rank': libraries_io_response['rank'],
                    'npm_stars': libraries_io_response['stars'],
                })
                utils.write_lines_to_existing_csv(OUTPUT_FILE_PATH, OUTPUT_FIELD_NAMES, lines_to_write)
        except Exception as e:
            lines_to_write.append({
                'repo_name': repo_name,
                'package_name': package_name,
                'use_repo_name': use_repo_name,
                'on_libraries_io_npm': False,
                'npm_dependent_repos_count': None,
                'npm_dependents_count': None,
                'npm_forks': None,
                'npm_language': None,
                'npm_rank': None,
                'npm_stars': None,
            })
            utils.write_lines_to_existing_csv(OUTPUT_FILE_PATH, OUTPUT_FIELD_NAMES, lines_to_write)
    print("Done")


def get_libraries_io_response(repo_half_name):
    lib_name_for_url = repo_half_name.replace('/', '%2F')
    url = 'https://libraries.io/api/NPM/{}?api_key={}'.format(lib_name_for_url, LIBRARIES_IO_ACCESS_TOKEN)
    res = requests.get(url)
    time.sleep(0.8)
    response = res.json()
    return response


# def get_dependents(repo_full_name):
#     url = 'https://github.com/{}/network/dependents?dependent_type=PACKAGE'.format(repo_full_name)
#     result = list()
#     count = 0
#     while True:
#         r = requests.get(url)
#         print('\tRequest {}'.format(str(count)))
#         count += 1
#         soup = BeautifulSoup(r.content, "html.parser")
#         ts = soup.findAll("div", {"class": "Box-row"})
#         data = list()
#         for t in ts:
#             try:
#                 data.append(
#                     "{}/{}".format(
#                         t.find('a', {"data-repository-hovercards-enabled": ""}).text,
#                         t.find('a', {"data-hovercard-type": "repository"}).text
#                     )
#                 )
#             except Exception:
#                 continue
#         result.extend(data)
#         pagination_containers = soup.find("div", {"class": "paginate-container"}).find_all('a')
#         pagination_container = None
#         for pc in pagination_containers:
#             href = pc['href']
#             if 'dependents_after' in href:
#                 pagination_container = pc
#         if pagination_container:
#             url = pagination_container["href"]
#             time.sleep(0.8)
#         else:
#             break
#     return result


if __name__ == "__main__":
    main()
