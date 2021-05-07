import os
import utils
from dotenv import load_dotenv

load_dotenv()

PROJECT_PATH = os.getenv('PROJECT_ROOT_PATH')
LIBRARIES_IO_ACCESS_TOKEN = os.getenv('LIBRARIES_IO_ACCESS_TOKEN')

SEARCH_DIR_PATH = "{}/json/comments".format(PROJECT_PATH)
FILE_NAME_SEARCH_STRING = "*.json"
OUTPUT_FILE_PATH = "{}/csv/non_gkirbbi_project_issue_comments.csv".format(PROJECT_PATH)
COMMENTS_FIELD_NAMES = [
    'id',
    'issue_id',
    'repo_name',
    'url',
    'issue_url',
    'user_id',
    'user_login',
    'user_type',
    'created_at',
    'updated_at',
    'body',
]


def main():
    utils.create_csv_file_if_necessary(OUTPUT_FILE_PATH, COMMENTS_FIELD_NAMES)
    print("Finding files to parse that match {} in {}".format(FILE_NAME_SEARCH_STRING, SEARCH_DIR_PATH))
    files_to_parse = utils.get_list_of_unread_files(SEARCH_DIR_PATH, FILE_NAME_SEARCH_STRING)
    print("Found {} files".format(len(files_to_parse)))
    count = 0
    for ftp in files_to_parse:
        try:
            count += 1
            print("{}: Parsing + writing {}".format(count, ftp))
            comments = utils.load_json_file(ftp)
            issue_id, repo_name = parse_issue_id_and_repo_name_from_file_name(ftp)
            lines_to_write = list()
            for c in comments:
                lines_to_write.append({
                    'id': c['id'],
                    'issue_id': issue_id,
                    'repo_name': repo_name,
                    'url': c['url'],
                    'issue_url': c['issue_url'],
                    'user_id': c['user']['id'],
                    'user_login': c['user']['login'],
                    'user_type': c['user']['type'],
                    'created_at': c['created_at'],
                    'updated_at': c['updated_at'],
                    'body': c['body'],
                })
            utils.write_lines_to_existing_csv(OUTPUT_FILE_PATH, COMMENTS_FIELD_NAMES, lines_to_write)
            utils.mark_file_as_read(ftp)
        except Exception as e:
            print("[ERROR] on file {}. Continuing from next file.".format(ftp))
    print("DONE")


def parse_issue_id_and_repo_name_from_file_name(json_issue_file_path):
    file_name = os.path.splitext(os.path.basename(json_issue_file_path))[0]
    split_name = file_name.split('@')
    # comments@issue@{issue_id}@{org}@{repo}.json
    issue_id = split_name[2]
    repo_name = f'{split_name[3]}/{split_name[4]}'
    return issue_id, repo_name


if __name__ == "__main__":
    main()