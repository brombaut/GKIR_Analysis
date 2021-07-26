import os
import utils
from dotenv import load_dotenv

load_dotenv()

PROJECT_PATH = os.getenv('PROJECT_ROOT_PATH')
LIBRARIES_IO_ACCESS_TOKEN = os.getenv('LIBRARIES_IO_ACCESS_TOKEN')

# SEARCH_DIR_PATH = "{}/json/commits".format(PROJECT_PATH)
# OUTPUT_FILE_PATH = "{}/csv/bens_collected_issue_commits.csv".format(PROJECT_PATH)

SEARCH_DIR_PATH = "{}/json/commits_from_commit_events".format(PROJECT_PATH)
OUTPUT_FILE_PATH = "{}/csv/ngkir_bens_collected_issue_commits.csv".format(PROJECT_PATH)

FILE_NAME_SEARCH_STRING = "*.json"
OUTPUT_FIELD_NAMES = [
    'commit_sha',
    'issue_id',
    'repo_name',
    'url',
    'html_url',
    'message',
    'author_login',
    'author_type',
    'committer_login',
    'committer_type',
    'stats_total',
    'stats_additions',
    'stats_deletions',
    'file_name',
    'file_status',
    'file_additions',
    'file_deletions',
    'file_changes',
    'file_patch',
]


def main():
    utils.create_csv_file_if_necessary(OUTPUT_FILE_PATH, OUTPUT_FIELD_NAMES)
    print("Finding files to parse that match {} in {}".format(FILE_NAME_SEARCH_STRING, SEARCH_DIR_PATH))
    files_to_parse = utils.get_list_of_unread_files(SEARCH_DIR_PATH, FILE_NAME_SEARCH_STRING)
    total = len(files_to_parse)
    print("Found {} files".format(total))
    count = 0
    for ftp in files_to_parse:
        try:
            count += 1
            print("{}/{}: Parsing + writing {}".format(count, total, ftp))
            commit = utils.load_json_file(ftp)
            if 'message' in commit and 'No commit found for SHA' in commit['message']:
                print('No Commit found...continuing')
                continue
            commit_sha, issue_id, repo_name = parse_artifacts_from_file_name(ftp)
            message = commit['commit']['message']
            url = commit['url']
            html_url = commit['html_url']
            author_login = commit['author']['login'] if commit['author'] is not None else ''
            author_type = commit['author']['type'] if commit['author'] is not None else ''
            committer_login = commit['committer']['login'] if commit['committer'] is not None else ''
            committer_type = commit['committer']['type'] if commit['committer'] is not None else ''
            stats_total = commit['stats']['total']
            stats_additions = commit['stats']['additions']
            stats_deletions = commit['stats']['deletions']

            def make_new_commit_line(f):
                return {
                    'commit_sha': commit_sha,
                    'issue_id': issue_id,
                    'repo_name': repo_name,
                    'url': url,
                    'html_url': html_url,
                    'message': message,
                    'author_login': author_login,
                    'author_type': author_type,
                    'committer_login': committer_login,
                    'committer_type': committer_type,
                    'stats_total': stats_total,
                    'stats_additions': stats_additions,
                    'stats_deletions': stats_deletions,
                    'file_name': f['filename'],
                    'file_status': f['status'],
                    'file_additions': f['additions'],
                    'file_deletions': f['deletions'],
                    'file_changes': f['changes'],
                    'file_patch': f['patch'] if 'patch' in f else None,
                }

            lines_to_write = list()
            for file in commit['files']:
                new_line = make_new_commit_line(file)
                lines_to_write.append(new_line)
            utils.write_lines_to_existing_csv(OUTPUT_FILE_PATH, OUTPUT_FIELD_NAMES, lines_to_write)
            utils.mark_file_as_read(ftp)
        except Exception as e:
            print("[ERROR] on file {}. Continuing from next file.".format(ftp))
    print("DONE")


def parse_artifacts_from_file_name(file_path):
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    split_name = file_name.split('@')
    # 'commit@a4a263d33871beb1bc66740611a03d960e985a9b@issue@320422390@jstransformers@jstransformer-lodash'
    # or
    # commit@da8fb535c9df84f3cd1086f3c8651b5f7ee8989c@showdownjs@showdown
    if len(split_name) == 6:
        commit_sha = split_name[1]
        issue_id = split_name[3]
        repo_name = f'{split_name[4]}/{split_name[5]}'
    else:
        commit_sha = split_name[1]
        issue_id = None
        repo_name = f'{split_name[2]}/{split_name[3]}'
    return commit_sha, issue_id, repo_name


if __name__ == "__main__":
    main()