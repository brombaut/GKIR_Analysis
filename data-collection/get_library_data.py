import os
import utils
from dotenv import load_dotenv

load_dotenv()

PROJECT_PATH = os.getenv('PROJECT_ROOT_PATH')
LIBRARIES_IO_ACCESS_TOKEN = os.getenv('LIBRARIES_IO_ACCESS_TOKEN')

OUTPUT_FOLDER_PATH = "{}/json/libraries".format(PROJECT_PATH)

GREENKEEPER_ISSUES_FILE_PATH = "{}/csv/greenkeeper_issues.csv".format(PROJECT_PATH)
GREENKEEPER_ISSUES_FIELD_NAMES = [
    'issue_id',
    'issue_number',
    'issue_url',
    'issue_title',
    'issue_state',
    'issue_is_locked',
    'issue_created_at',
    'issue_updated_at',
    'issue_closed_at',
    'issue_user_login',
    'issue_labels',
    'issue_num_comments',
    'issue_events_url',
    'issue_dependency_name',
    'issue_dependency_type',
    'issue_dependency_actual_version',
    'issue_dependency_next_version',
    'issue_dependency_bundle_name',
    'issue_body_parser',
    'issue_repo_url'
]


def main():
    gk_issues = utils.read_csv_ignore_headers(GREENKEEPER_ISSUES_FILE_PATH, GREENKEEPER_ISSUES_FIELD_NAMES)
    library_names = list()
    for issue in gk_issues:
        if issue['issue_dependency_name'] not in library_names:
            library_names.append(issue['issue_dependency_name'])
    total = len(library_names)
    count = 0
    for lib_name in library_names:
        count += 1
        try:
            print("\t{}/{} pr_url={}".format(count, total, lib_name))
            if not lib_name:
                continue
            lib_name_for_url = lib_name.replace('/', '%2F')
            url = 'https://libraries.io/api/NPM/{}?api_key={}'.format(lib_name_for_url, LIBRARIES_IO_ACCESS_TOKEN)
            lib_info = utils.send_request(url, None, ignore_token=True, sleep_time=1.2)
            lib_name_for_file = lib_name.replace('/', '%2F')
            file_name = "{}/{}.json".format(OUTPUT_FOLDER_PATH, lib_name_for_file)
            utils.write_to_json_file(file_name, lib_info)
        except Exception as e:
            print("Error on {}".format(lib_name))


if __name__ == "__main__":
    main()
