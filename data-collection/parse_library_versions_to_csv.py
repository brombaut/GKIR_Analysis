import os
import utils
from dotenv import load_dotenv

load_dotenv()

PROJECT_PATH = os.getenv('PROJECT_ROOT_PATH')
LIBRARIES_IO_ACCESS_TOKEN = os.getenv('LIBRARIES_IO_ACCESS_TOKEN')

SEARCH_DIR_PATH = "{}/json/libraries".format(PROJECT_PATH)
FILE_NAME_SEARCH_STRING = "*.json"
OUTPUT_FILE_PATH = "{}/csv/breaking_library_versions.csv".format(PROJECT_PATH)
BREAKING_LIBRARY_VERSIONS_FIELD_NAMES = [
    "package_name",
    "version",
    "version_published_at"
]


def main():
    utils.create_csv_file_if_necessary(OUTPUT_FILE_PATH, BREAKING_LIBRARY_VERSIONS_FIELD_NAMES)
    print("Finding files to parse that match {} in {}".format(FILE_NAME_SEARCH_STRING, SEARCH_DIR_PATH))
    files_to_parse = utils.get_list_of_unread_files(SEARCH_DIR_PATH, FILE_NAME_SEARCH_STRING)
    print("Found {} files".format(len(files_to_parse)))
    count = 0
    for ftp in files_to_parse:
        try:
            count += 1
            print("{}: Parsing + writing {}".format(count, ftp))
            file_contents = utils.load_json_file(ftp)
            lines_to_write = list()
            package_name = file_contents['name']
            for v in file_contents['versions']:
                lines_to_write.append({
                    'package_name': package_name,
                    "version": v['number'],
                    "version_published_at": v['published_at']
                })
            utils.write_lines_to_existing_csv(OUTPUT_FILE_PATH, BREAKING_LIBRARY_VERSIONS_FIELD_NAMES, lines_to_write)
            utils.mark_file_as_read(ftp)
        except Exception as e:
            print("[ERROR] on file {}. Continuing from next file.".format(ftp))
    print("DONE")


if __name__ == "__main__":
    main()