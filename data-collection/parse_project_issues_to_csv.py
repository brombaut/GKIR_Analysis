import os
import utils
from dotenv import load_dotenv

load_dotenv()

PROJECT_PATH = os.getenv('PROJECT_ROOT_PATH')
LIBRARIES_IO_ACCESS_TOKEN = os.getenv('LIBRARIES_IO_ACCESS_TOKEN')

SEARCH_DIR_PATH = "{}/json/issues".format(PROJECT_PATH)
FILE_NAME_SEARCH_STRING = "*.json"
OUTPUT_FILE_PATH = "{}/csv/all_project_issues.csv".format(PROJECT_PATH)
ISSUE_FIELD_NAMES = [
    'id',
    'repo_name',
    'url',
    'repository_url',
    'comments_url',
    'events_url',
    'html_url',
    'number',
    'title',
    'user_id',
    'user_login',
    'user_type',
    'state',
    'locked',
    'comments',
    'created_at',
    'updated_at',
    'closed_at',
    'body',
    'is_pull_request',
]


def main():
    utils.create_csv_file_if_necessary(OUTPUT_FILE_PATH, ISSUE_FIELD_NAMES)
    print("Finding files to parse that match {} in {}".format(FILE_NAME_SEARCH_STRING, SEARCH_DIR_PATH))
    files_to_parse = utils.get_list_of_unread_files(SEARCH_DIR_PATH, FILE_NAME_SEARCH_STRING)
    print("Found {} files".format(len(files_to_parse)))
    count = 0
    for ftp in files_to_parse:
        try:
            count += 1
            print("{}: Parsing + writing {}".format(count, ftp))
            issues = utils.load_json_file(ftp)
            repo_name = parse_repo_name_form_file_name(ftp)
            lines_to_write = list()
            for i in issues:
                lines_to_write.append({
                    'id': i['id'],
                    'repo_name': repo_name,
                    'url': i['url'],
                    'repository_url': i['repository_url'],
                    'comments_url': i['comments_url'],
                    'events_url': i['events_url'],
                    'html_url': i['html_url'],
                    'number': i['number'],
                    'title': i['title'],
                    'user_id': i['user']['id'],
                    'user_login': i['user']['login'],
                    'user_type': i['user']['type'],
                    'state': i['state'],
                    'locked': i['locked'],
                    'comments': i['comments'],
                    'created_at': i['created_at'],
                    'updated_at': i['updated_at'],
                    'closed_at': i['closed_at'],
                    'body': i['body'],
                    'is_pull_request': 'pull_request' in i
                })
            utils.write_lines_to_existing_csv(OUTPUT_FILE_PATH, ISSUE_FIELD_NAMES, lines_to_write)
            utils.mark_file_as_read(ftp)
        except Exception as e:
            print("[ERROR] on file {}. Continuing from next file.".format(ftp))
    print("DONE")


def parse_repo_name_form_file_name(json_issue_file_path):
    file_name = os.path.splitext(os.path.basename(json_issue_file_path))[0]
    split_name = file_name.split('@')
    repo_name = f'{split_name[1]}/{split_name[2]}'
    return repo_name


if __name__ == "__main__":
    main()