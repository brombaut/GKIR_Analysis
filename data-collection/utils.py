import csv
import glob
import json
import os
import requests
import time
from datetime import datetime, timedelta, timezone


def load_json_file(file_path):
    with open(file_path, 'r') as f:
        contents = json.load(f)
    return contents


def write_to_json_file(output_file_name, json_data):
    with open(output_file_name, "w") as f:
        json.dump(json_data, f)


def create_csv_file_if_necessary(file_path, headers):
    if not os.path.isfile(file_path):
        with open(file_path, 'w') as csv_file:
            writer = csv.DictWriter(csv_file, headers)
            writer.writeheader()


def create_csv_file(file_path, headers):
    with open(file_path, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, headers)
        writer.writeheader()


def read_csv_ignore_headers(file_path, headers):
    result = list()
    with open(file_path) as csv_file:
        reader = csv.DictReader(csv_file, headers)
        next(reader, None)  # skip the headers
        for row in reader:
            result.append(row)
    return result


def write_lines_to_existing_csv(output_file_path, headers, dicts_to_write):
    with open(output_file_path, 'a') as csv_file:
        writer = csv.DictWriter(csv_file, headers)
        for line in dicts_to_write:
            writer.writerow(line)


def write_one_line_to_existing_csv(output_file_path, headers, line_dict):
    with open(output_file_path, 'a') as csv_file:
        writer = csv.DictWriter(csv_file, headers)
        writer.writerow(line_dict)


def write_lines_to_new_csv(output_file_path, headers, dicts_to_write):
    with open(output_file_path, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, headers)
        writer.writeheader()
        for line in dicts_to_write:
            writer.writerow(line)


def send_request(url, gh_token, ignore_token=False, sleep_time=1):
    headers = {}
    if not ignore_token:
        headers = {'Authorization': 'token %s' % gh_token}
    res = requests.get(url, headers=headers)
    time.sleep(sleep_time)
    response = res.json()
    while 'next' in res.links.keys():
        res = requests.get(res.links['next']['url'], headers=headers)
        time.sleep(sleep_time)
        response += res.json()
    return response


def make_date(string, date_format):
    return datetime.strptime(string.replace("Z", "+0000"), date_format)


def make_date_string(date, date_format):
    return date.strftime(date_format)


def now():
    return datetime.now(timezone.utc)


def get_list_of_unread_files(search_dir_path, file_name_search_string):
    result = glob.glob("{}/{}".format(search_dir_path, file_name_search_string))
    return result


def mark_file_as_read(file_path):
    os.rename(file_path, "{}.READ".format(file_path))


def file_or_read_file_already_exists(output_file_name):
    read_output_file_name = "{}.READ".format(output_file_name)
    return os.path.isfile(output_file_name) or os.path.isfile(read_output_file_name)