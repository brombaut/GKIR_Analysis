import json
import requests
import time
import datetime
import glob
import re
import csv
import base64

from html.parser import HTMLParser
from os import listdir
from os.path import isfile, join

prefix_date = "2020-09-16"

start_day = "2020-06-03"
end_day = datetime.datetime(2016, 10, 20)

MY_GIT_TOKEN = "" # Put your token here

# search_file_path = "/scratch/filipe-cogo/wip-19-filipe-npm_greenkeeper_build_failures-data/2019-07-14/"
# search_file_path = "/Users/filipe/Dropbox/wip-19-filipe-npm_greenkeeper_build_failures-data/{}/".format(prefix_date)
search_file_path = "/home/local/SAIL/filipe-cogo/wip-19-filipe-npm_greenkeeper_build_failures-data/{}/".format(prefix_date)
search_file_path_test = "/home/local/SAIL/filipe-cogo/wip-19-filipe-npm_greenkeeper_build_failures-data/test/"

class GreenkeeperHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)

class IssueBodyParser():
    def parse_issue_body(self, body):
        pass

class NewDepVersionIssueBodyParser(IssueBodyParser):
    def parse_issue_body(self, body):
        regexp = re.compile("\\n?## Version \*\*([\d|\.?]+?-?.*?\+?.*?)\*\* of \[(.+?)\]\(.*?\) [was just published|just got published].*")
        parsed_body = regexp.match(body)
        # print(parsed_body.group(0))
        # print(parsed_body.group(1))
        # print(parsed_body.group(2))
        # TODO: check if "issue_dependency_type" can be parsed
        return [{
            "issue_dependency_name": parsed_body.group(2),
            "issue_dependency_type": None,
            "issue_dependency_actual_version": parsed_body.group(1),
            "issue_dependency_next_version": None,
            "issue_dependency_bundle_name": None,
            "issue_body_parser": self.__class__.__name__
        }]


class NewDepVersion2IssueBodyParser(IssueBodyParser):
    def parse_issue_body(self, body):
        regexp = re.compile("\\n?## Version \*\*([\d|\.?]+?-?.*?\+?.*?)\*\* of \*\*(.+?)\*\*\(?.*?\)? [was just published|just got published].*")
        parsed_body = regexp.match(body)
        # print(parsed_body.group(0))
        # print(parsed_body.group(1))
        # print(parsed_body.group(2))
        # TODO: check if "issue_dependency_type" can be parsed
        return [{
            "issue_dependency_name": parsed_body.group(2),
            "issue_dependency_type": None,
            "issue_dependency_actual_version": parsed_body.group(1),
            "issue_dependency_next_version": None,
            "issue_dependency_bundle_name": None,
            "issue_body_parser": self.__class__.__name__
        }]


class NewDepVersion3IssueBodyParser(IssueBodyParser):
    def parse_issue_body(self, body):
        regexp = re.compile("\\n?## Version \*\*([\d|\.?]+?-?.*?\+?.*?)\*\* of the \*\*(.+?)\*\*\(?.*?\)? packages [was just published|just got published].*")
        parsed_body = regexp.match(body)
        # print(parsed_body.group(0))
        # print(parsed_body.group(1))
        # print(parsed_body.group(2))
        # TODO: check if "issue_dependency_type" can be parsed
        return [{
            "issue_dependency_name": parsed_body.group(2),
            "issue_dependency_type": None,
            "issue_dependency_actual_version": parsed_body.group(1),
            "issue_dependency_next_version": None,
            "issue_dependency_bundle_name": None,
            "issue_body_parser": self.__class__.__name__
        }]

class NewDepVersion4IssueBodyParser(IssueBodyParser):
    def parse_issue_body(self, body):
        regexp = re.compile("^.*## Version \*\*([\d|\.?]+?-?.*?\+?.*?)\*\* of \[(.+?)\]\(.*?\) [was just published|just got published].*", flags=re.U | re.DOTALL)
        parsed_body = regexp.match(body)
        # print(parsed_body.group(0))
        # print(parsed_body.group(1))
        # print(parsed_body.group(2))
        # TODO: check if "issue_dependency_type" can be parsed
        return [{
            "issue_dependency_name": parsed_body.group(2),
            "issue_dependency_type": None,
            "issue_dependency_actual_version": parsed_body.group(1),
            "issue_dependency_next_version": None,
            "issue_dependency_bundle_name": None,
            "issue_body_parser": self.__class__.__name__
        }]

class NewDepVersion5IssueBodyParser(IssueBodyParser):
    def parse_issue_body(self, body):
        regexp = re.compile("Version ([\d|\.?]+?-?.*?\+?.*?) of (.+?) [was just published|just got published].*")
        parsed_body = regexp.match(body)
        # print(parsed_body.group(0))
        # print(parsed_body.group(1))
        # print(parsed_body.group(2))
        # TODO: check if "issue_dependency_type" can be parsed
        return [{
            "issue_dependency_name": parsed_body.group(2),
            "issue_dependency_type": None,
            "issue_dependency_actual_version": parsed_body.group(1),
            "issue_dependency_next_version": None,
            "issue_dependency_bundle_name": None,
            "issue_body_parser": self.__class__.__name__
        }]

class NewDepUpdatedFromToIssueBodyParser(IssueBodyParser):
    def parse_issue_body(self, body):
        regexp = re.compile("\\n## The ([a-zA-Z]+?) \[(.+?)\]\(.*?\) was updated from `([\d|\.?]+?-?.*?\+?.*?)` to `([\d|\.?]+?-?.*?\+?.*?)`.*")
        parsed_body = regexp.match(body)
        # print(parsed_body.group(0))
        # print(parsed_body.group(1))
        # print(parsed_body.group(2))
        # print(parsed_body.group(3))
        # print(parsed_body.group(4))
        # TODO: check if "issue_dependency_type" can be parsed
        return [{
            "issue_dependency_name": parsed_body.group(2),
            "issue_dependency_type": parsed_body.group(1),
            "issue_dependency_actual_version": parsed_body.group(3),
            "issue_dependency_next_version": parsed_body.group(4),
            "issue_dependency_bundle_name": None,
            "issue_body_parser": self.__class__.__name__
        }]

class NewDepUpdatedFromTo2IssueBodyParser(IssueBodyParser):
    def parse_issue_body(self, body):
        regexp = re.compile("\\n## The ([a-zA-Z]+?) \[(.+?)\]\(.*?\) was updated from `(undefined)` to `([\d|\.?]+?-?.*?\+?.*?)`.*")
        parsed_body = regexp.match(body)
        # print(parsed_body.group(0))
        # print(parsed_body.group(1))
        # print(parsed_body.group(2))
        # print(parsed_body.group(3))
        # print(parsed_body.group(4))
        # TODO: check if "issue_dependency_type" can be parsed
        return [{
            "issue_dependency_name": parsed_body.group(2),
            "issue_dependency_type": parsed_body.group(1),
            "issue_dependency_actual_version": parsed_body.group(3),
            "issue_dependency_next_version": parsed_body.group(4),
            "issue_dependency_bundle_name": None,
            "issue_body_parser": self.__class__.__name__
        }]

class BundleUpdateIssueBodyParser(IssueBodyParser):
    def parse_issue_body(self, body):
        #regexp = re.compile("\\n## There have been updates to the \*(.*?)\* monorepo:\\n\\n \+ (\- The ([a-zA-Z]+?) \[(.+?)\]\(.+?\) was updated from `([\d|\.?]+?-?.*?\+?.*?)` to `([\d|\.?]+?-?.*?\+?.*?)`\.\\n)+?.*?")
        regexp = re.compile("\\n## There have been updates to the \*(.*?)\* monorepo:.*")
        parsed_body = regexp.match(body)
        monorepo_name = parsed_body.group(1)
        list_of_parsed_body = list()
        lines = body.split("\n")
        for line in lines:
            regexp = re.compile(".*?(\- The `([a-zA-Z]+?)` \[(.+?)\]\(.+?\) was updated from `([\d|\.?]+?-?.*?\+?.*?)` to `([\d|\.?]+?-?.*?\+?.*?)`\.\\n?)")
            parsed_body = regexp.match(line)
            try:
                # print(parsed_body.group(0))
                # print(parsed_body.group(1))
                # print(parsed_body.group(2))   # devDependency
                # print(parsed_body.group(3))   # @babel/parser
                # print(parsed_body.group(4))   # 7.2.3
                # print(parsed_body.group(5))   # 7.3.0
                list_of_parsed_body.append({
                    "issue_dependency_name": parsed_body.group(3),
                    "issue_dependency_type": parsed_body.group(2),
                    "issue_dependency_actual_version": parsed_body.group(4),
                    "issue_dependency_next_version": parsed_body.group(5),
                    "issue_dependency_bundle_name": monorepo_name,
                    "issue_body_parser": self.__class__.__name__
                })
            except AttributeError as ae:
                continue
        # TODO: check if "issue_dependency_type" can be parsed
        return list_of_parsed_body

class BundleUpdate2IssueBodyParser(IssueBodyParser):
    def parse_issue_body(self, body):
        #regexp = re.compile("\\n## There have been updates to the \*(.*?)\* monorepo:\\n\\n \+ (\- The ([a-zA-Z]+?) \[(.+?)\]\(.+?\) was updated from `([\d|\.?]+?-?.*?\+?.*?)` to `([\d|\.?]+?-?.*?\+?.*?)`\.\\n)+?.*?")
        regexp = re.compile("\\n## There have been updates to the \*(.*?)\* monorepoundefined.*")
        parsed_body = regexp.match(body)
        monorepo_name = parsed_body.group(1)
        list_of_parsed_body = list()
        lines = body.split("\n")
        for line in lines:
            regexp = re.compile(".*?(\- The `([a-zA-Z]+?)` \[(.+?)\]\(.+?\) was updated from `([\d|\.?]+?-?.*?\+?.*?)` to `([\d|\.?]+?-?.*?\+?.*?)`\.\\n?)")
            parsed_body = regexp.match(line)
            try:
                # print(parsed_body.group(0))
                # print(parsed_body.group(1))
                # print(parsed_body.group(2))   # devDependency
                # print(parsed_body.group(3))   # @babel/parser
                # print(parsed_body.group(4))   # 7.2.3
                # print(parsed_body.group(5))   # 7.3.0
                list_of_parsed_body.append({
                    "issue_dependency_name": parsed_body.group(3),
                    "issue_dependency_type": parsed_body.group(2),
                    "issue_dependency_actual_version": parsed_body.group(4),
                    "issue_dependency_next_version": parsed_body.group(5),
                    "issue_dependency_bundle_name": monorepo_name,
                    "issue_body_parser": self.__class__.__name__
                })
            except AttributeError as ae:
                continue
        # TODO: check if "issue_dependency_type" can be parsed
        return list_of_parsed_body

class IssueBodyParserImpl():
    def parse(self, body):
        try:
            parser = NewDepVersionIssueBodyParser()
            return parser.parse_issue_body(body)
        except AttributeError as e:
            try:
                parser = NewDepVersion2IssueBodyParser()
                return parser.parse_issue_body(body)
            except AttributeError as e:
                try:
                    parser = NewDepVersion3IssueBodyParser()
                    return parser.parse_issue_body(body)
                except AttributeError as e:
                    try:
                        parser = NewDepVersion4IssueBodyParser()
                        return parser.parse_issue_body(body)
                    except AttributeError as e:
                        try:
                            parser = NewDepVersion5IssueBodyParser()
                            return parser.parse_issue_body(body)
                        except AttributeError as e:
                            try:
                                parser = NewDepUpdatedFromToIssueBodyParser()
                                return parser.parse_issue_body(body)
                            except AttributeError as e:
                                try:
                                    parser = NewDepUpdatedFromTo2IssueBodyParser()
                                    return parser.parse_issue_body(body)
                                except AttributeError as e:
                                    try:
                                        parser = BundleUpdateIssueBodyParser()
                                        return parser.parse_issue_body(body)
                                    except AttributeError as e:
                                        try:
                                            parser = BundleUpdate2IssueBodyParser()
                                            return parser.parse_issue_body(body)
                                        except AttributeError as e:
                                            print("Parsing error")

        return [{
            "issue_dependency_name": None,
            "issue_dependency_type": None,
            "issue_dependency_actual_version": None,
            "issue_dependency_next_version": None,
            "issue_dependency_bundle_name": None,
            "issue_body_parser": None
        }]


def fetch_events(issues_merged_path, issues_merged_file_name, suffix=prefix_date):
    # TODO: check if item wasn't previously fetched
    # TODO: read events file and store all issues id that
    # TODO: were previously fetched
    try:
        if not issues_merged_path.endswith("/"):
            issues_merged_path = issues_merged_path + "/"
        file_path = issues_merged_path + issues_merged_file_name
        with open(issues_merged_path + issues_merged_file_name) as json_file:
            try:
                data = json.load(json_file)
            except ValueError as ve:
                print("[FATAL ERROR] Not a valid json file '{}': {}".format(file_path, str(ve)))
            try:
                for item in data['items']:
                    try:
                        if isfile(issues_merged_path + "[{}]events@{}.json".format(item['id'], suffix)):
                            print("[WARNING] Event associated with issue ID {} was already fetched".format(item['id']))
                            continue
                    except KeyError as ke:
                        print(
                            "[ERROR] Item {} on file '{}' doesn't contain field '{}'. Continuing from next item.".format(
                                str(item), file_path, str(ke)))
                        continue
                    success = False
                    while not success:
                        try:
                            events_url = item['events_url']
                            try:
                                print("[REQUEST] {}".format(events_url))
                                git_token = MY_GIT_TOKEN
                                headers = {'Authorization': 'token {}'.format(git_token)}
                                events_request = requests.get(events_url, headers=headers)
                                if events_request.status_code == 200:
                                    events_json = events_request.json()
                                    out_json = dict()
                                    try:
                                        out_json.update({"issue_url": item['url']})
                                        out_json.update({"issue_id": item['id']})
                                        out_json.update({"items": events_json})
                                    except KeyError as ke:
                                        print("[ERROR] Item {} on file '{}' doesn't contain field '{}'. Continuing from next item.".format(file_path, str(item), str(ke)))
                                        success = True
                                        break
                                    with open(issues_merged_path + "[{}]events@{}.json".format(item['id'], suffix), 'w') as file:
                                        json.dump(out_json, file)
                            except requests.exceptions.ConnectionError as ce:
                                print("[ERROR] Request to '{}' failed due to connection error on item {}: {}. Trying again in one minute".format(events_url, str(item), str(ce)))
                                time.sleep(60)
                                continue
                            except requests.exceptions.HTTPError as ce:
                                print("[ERROR] Request to '{}' failed due to invalid HTTP response on item {}: {}. Continuing from next item.".format(events_url, str(item), str(ce)))
                                success = True
                                break
                            except requests.exceptions.Timeout as ce:
                                print("[ERROR] Request to '{}' had a timeout on item {}: {}. Trying again in one minute.".format(events_url, str(item), str(ce)))
                                time.sleep(60)
                                continue
                        except KeyError as ke:
                            print("[ERROR] Item {} on file '{}' doesn't contain field '{}'. Continuing from next item.".format(file_path, str(item), str(ke)))
                            break
                        finally:
                            success = True
                            time.sleep(3)
            except KeyError as ke:
                print("[FATAL ERROR] File '{}' doesn't contain field '{}'.".format(file_path, str(ke)))
    except FileNotFoundError as fnf:
        print("File {} not found.".format(file_path))


def fetch_issues(search_file_path):
    time_now = datetime.datetime.now().strftime('%Y-%m-%d')
    # start_day = time_now
    # start_day = "2019-07-14" # this is the beginning date of the first data collection
    # start_day = "2020-09-04" # this is the beginning date of the second data collection
    week = datetime.datetime.strptime(start_day, "%Y-%m-%d")
    prior_week = week - datetime.timedelta(days=2)
    # end_day = datetime.datetime(2017, 1, 1) # this is the final date of the first data collection
    # end_day = datetime.datetime(2019, 7, 14) # this is the final date of the second data collection
    while week > end_day:
        created_1 = prior_week.strftime("%Y-%m-%d")
        created_2 = week.strftime("%Y-%m-%d")
        url = "https://api.github.com/search/issues?q=An+in-range+update+is+breaking+build+in:title+created:{}..{}&per_page=100&page=1".format(created_1, created_2)
        print("[REQUEST] " + url)
        #res = requests.get(url, headers={"Authorization": git_token})
        git_token = MY_GIT_TOKEN
        headers = {'Authorization': 'token {}'.format(git_token)}
        res = requests.get(url, headers=headers)
        issues = res.json()
        if res.status_code == 200:
            while 'next' in res.links.keys():
                time.sleep(3)
                link_next = res.links['next']['url']
                print("[REQUEST] " + link_next)
                res_2 = requests.get(link_next, headers=headers)
                # headers={"Authorization": git_token})
                if res_2.status_code == 200:
                    issues_again = res_2.json()
                    items_list = issues['items']
                    items_list = items_list + issues_again['items']
                    issues.update({"items": items_list})
                    res = res_2
                else:
                    print("Status code is {}. Retrying to retrieve contents of page".format(res_2.status_code))
            with open(search_file_path + "[{}]issues@{}.json".format(created_1, prefix_date), 'w') as outfile:
                json.dump(issues, outfile)
        week = datetime.datetime.strptime(created_1, "%Y-%m-%d")
        prior_week = week - datetime.timedelta(days=2)
        time.sleep(3)


def fetch_first_pull_request(search_file_path):
    time_now = datetime.datetime.now().strftime('%Y-%m-%d')
    # start_day = time_now
    # start_day = "2019-07-14"
    week = datetime.datetime.strptime(start_day, "%Y-%m-%d")
    prior_week = week - datetime.timedelta(days=2)
    # end_day = datetime.datetime(2017, 1, 1)
    while week > end_day:
        git_token = MY_GIT_TOKEN
        created_1 = prior_week.strftime("%Y-%m-%d")
        created_2 = week.strftime("%Y-%m-%d")
        url = "https://api.github.com/search/issues?q=Update+dependencies+to+enable+Greenkeeper+in:title+created:{}..{}&per_page=100&page=1".format(created_1, created_2)
        print("[REQUEST] " + url)
        git_token = MY_GIT_TOKEN
        headers = {'Authorization': 'token {}'.format(git_token)}
        res = requests.get(url, headers=headers)
        issues = res.json()
        if res.status_code == 200:
            while 'next' in res.links.keys():
                time.sleep(3)
                link_next = res.links['next']['url']
                print("[REQUEST] " + link_next)
                res_2 = requests.get(link_next, headers=headers)
                # headers={"Authorization": git_token})
                if res_2.status_code == 200:
                    issues_again = res_2.json()
                    items_list = issues['items']
                    items_list = items_list + issues_again['items']
                    issues.update({"items": items_list})
                    res = res_2
                else:
                    print("Status code is {}. Retrying to retrieve contents of page".format(res_2.status_code))
            with open(search_file_path + "[{}]first_pull_request@{}.json".format(created_1, prefix_date), 'w') as outfile:
                json.dump(issues, outfile)
        week = datetime.datetime.strptime(created_1, "%Y-%m-%d")
        prior_week = week - datetime.timedelta(days=2)
        time.sleep(3)

def merge_issues_json_files(files_patch):
    def remove_duplicate(seq):
        seen = set()
        unique = list()
        for s in seq:
            i = s['url']
            if i not in seen:
                unique.append(s)
            seen.add(i)
        return unique

    if not files_patch.endswith("/"):
        files_patch = files_patch + "/"
    # files = glob.glob(files_patch + "*issues@{}.json".format(prefix_date))
    files = glob.glob(files_patch + "issue_reports*.json")
    unique_json = {"items": list()}
    visited_issues = list()
    for file in files:
        with open(file, 'r') as f:
            try:
                data = json.load(f)
            except ValueError as ve:
                print("[ERROR] Invalid JSON on file {}. Continuing from next file.".format(file))
            actual_items = unique_json["items"]
            try:
                new_item = actual_items + data["items"]
                # l = [{"a": 123, "b": 1234}, {"a": 321, "b": 1234}, {"a": 123, "b": 1234}]
                # Remove duplicates
                new_item_no_dup = remove_duplicate(new_item)
                # s = set(tuple(d.items()) for d in new_item)
                # d = [dict(t) for t in s]
                # new_item_no_dup = [dict(t) for t in set(tuple(d.items()) for d in new_item)]
                unique_json.update({"items": new_item_no_dup})
            except KeyError as ke:
                print("[ERROR] File {} doesn't have field {}. Continuing from next file.".format(file, str(ke)))
                continue
    with open(files_patch + "issues@{}-merge.json".format(prefix_date), "w") as f:
        json.dump(unique_json, f)

def merge_events_json_files(search_file_path, files_suffix="events@{}".format(prefix_date)):
    if not search_file_path.endswith("/"):
        files_patch = search_file_path + "/"
    else:
        files_patch = search_file_path
    files = glob.glob(files_patch + "*" + files_suffix + ".json")
    events = {"events": list()}
    for file in files:
        with open(file, "r") as f:
            events_json = json.load(f)
            events_list = events['events']
            events_list.append(events_json)
            events.update({"events": events_list})
    with open(search_file_path +  files_suffix + "-merged.json", "w") as f:
        json.dump(events, f)


def fetch_commits(events_merged_path, events_merged_file_name, suffix=prefix_date):
    try:
        if not events_merged_path.endswith("/"):
            events_merged_path = events_merged_path + "/"
        file_path = events_merged_path + events_merged_file_name
        fetched_commits = [f for f in listdir(events_merged_path) if isfile(join(events_merged_path, f))]
        fetched_commit_ids = set()
        for fetched_commit in fetched_commits:
            try:
                m = re.search("\[(\d+?)\]\[(.+?)\]commits@" + suffix + ".json", fetched_commit)
                fetched_commit_id = m.group(2)
            except AttributeError as ae:
                print("[WARNING] Couldn't get event id from file named " + fetched_commit)
                continue
            fetched_commit_ids.add(fetched_commit_id)
        with open(file_path, "r") as json_file:
            try:
                data = json.load(json_file)
            except ValueError as ve:
                print("[FATAL ERROR] Not a valid json file '{}': {}".format(file_path, str(ve)))
        try:
            data = data['events']
            for items in data:
                # TODO: check if item wasn't previously fetched
                for item in items['items']:
                    if item['event'] in ("merge", "referenced") or item['commit_url'] is not None:
                        if item['commit_id'] in fetched_commit_ids:
                            continue
                        success = False
                        while not success:
                            try:
                                commit_url = item['commit_url']

                                try:
                                    print("[REQUEST] {}".format(commit_url))

                                    git_token = MY_GIT_TOKEN
                                    headers = {'Authorization': 'token {}'.format(git_token)}

                                    commits_request = requests.get(commit_url,
                                                                   headers=headers)

                                    if commits_request.status_code == 200:
                                        commits_json = commits_request.json()
                                        out_json = dict()

                                        try:
                                            out_json.update({"event_url": item['url']})
                                            out_json.update({"event_id": item['id']})
                                            out_json.update({"items": commits_json})
                                        except KeyError as ke:
                                            print(
                                                "[ERROR] Item {} on file '{}' doesn't contain field '{}'. Continuing from next item.".format(
                                                    file_path, str(item), str(ke)))

                                            success = True
                                            break

                                        with open(events_merged_path + "[{}][{}]commits@{}.json".format(item['id'], item['commit_id'], suffix),
                                                  'w') as file:
                                            json.dump(out_json, file)

                                except requests.exceptions.ConnectionError as ce:
                                    print(
                                        "[ERROR] Request to '{}' failed due to connection error on item {}: {}. Trying again in one minute".format(
                                            events_url, str(item), str(ce)))

                                    time.sleep(60)
                                    continue
                                except requests.exceptions.HTTPError as ce:
                                    print(
                                        "[ERROR] Request to '{}' failed due to invalid HTTP response on item {}: {}. Continuing from next item.".format(
                                            events_url, str(item), str(ce)))

                                    success = True
                                    break
                                except requests.exceptions.Timeout as ce:
                                    print(
                                        "[ERROR] Request to '{}' had a timeout on item {}: {}. Trying again in one minute.".format(
                                            events_url, str(item), str(ce)))

                                    time.sleep(60)
                                    continue
                            except KeyError as ke:
                                print(
                                    "[ERROR] Item {} on file '{}' doesn't contain field '{}'. Continuing from next item.".format(
                                        file_path, str(item), str(ke)))

                                break
                            finally:
                                success = True

                                time.sleep(3)
        except KeyError as ke:
            print("[FATAL ERROR] File '{}' doesn't contain field '{}'.".format(file_path, str(ke)))

    except FileNotFoundError as fnf:
        print("File {} not found.".format(file_path))


def merge_commits_json_files(search_file_path, files_suffix="commits@{}".format(prefix_date)):
    if not search_file_path.endswith("/"):
        files_patch = search_file_path + "/"
    else:
        files_patch = search_file_path

    files = glob.glob(files_patch + "*" + files_suffix + ".json")

    items = {"items": list()}

    for file in files:
        with open(file, "r") as f:
            commits_json = json.load(f)

            commit_info = dict()
            commit_info.update({"event_url": commits_json['event_url']})
            commit_info.update({"event_id": commits_json['event_id']})
            commit_info.update({"commit": commits_json['items']})

            items_list = items['items']
            items_list.append(commit_info)

            items.update({"items": items_list})

    with open(search_file_path + files_suffix + "-merged.json", "w") as f:
        json.dump(items, f)


def count_commits(events_merged_path, events_merged_file_name, suffix=prefix_date):
    try:
        if not events_merged_path.endswith("/"):
            events_merged_path = events_merged_path + "/"

        file_path = events_merged_path + events_merged_file_name

        with open(file_path, "r") as json_file:

            try:
                data = json.load(json_file)
            except ValueError as ve:
                print("[FATAL ERROR] Not a valid json file '{}': {}".format(file_path, str(ve)))

        num_commits = 0
        num_commits_url = 0
        try:
            data = data['events']

            for items in data:
                for item in items['items']:
                    if item['event'] in ("merge", "referenced"):
                        num_commits = num_commits + 1

                    if item['commit_url'] != None:
                        num_commits_url = num_commits_url + 1
        except KeyError as ke:
            print("[FATAL ERROR] File '{}' doesn't contain field '{}'.".format(file_path, str(ke)))

    except FileNotFoundError as fnf:
        print("File {} not found.".format(file_path))

    print("Number of commits:" + str(num_commits))
    print("Number of commits URL:" + str(num_commits_url))


def read_gh_search_json(search_file_path):
    parser = GreenkeeperHTMLParser()

    with open(search_file_path + "issues@{}-merge.json".format(prefix_date)) as json_file:
        data = json.load(json_file)

        i = 1
        for item in data['items']:
            print("Item {} of {}".format(i, len(data['items'])))

            print("url:" + item['url'])
            print("repo_url:" + item['repository_url'])
            print("id:" + str(item['id']))
            print("title:" + item['title'])
            print("state:" + item['state'])
            print("num_comments:" + str(item['comments']))
            print("created_at:" + item['created_at'])
            print("updated_at:" + item['updated_at'])
            print("closed_at:" + str(item['closed_at']))
            print("body:" + str(item['body']))
            # print("parsed_body:\n")
            # parser.feed(item['body'])

            i = i + 1


def get_issue_labels(labels_list):
    labels_str = "["

    for label in labels_list:
        labels_str = labels_str + label['name'] + ","

    if labels_str != "[":
        labels_str = labels_str[:-1]
        labels_str = labels_str + "]"
    else:
        labels_str = "[]"

    return {"issue_labels": labels_str}


def parse_issue_body(body):
    parser = IssueBodyParserImpl()
    return parser.parse(body)


def generate_issues_csv(search_file_path, merge_file_name):
    with open(search_file_path + merge_file_name) as json_file:
        data = json.load(json_file)

    with open(search_file_path + "greenkeeper_issues.csv", "w") as csv_file:
        field_names = ["issue_id",
                       "issue_number",
                       "issue_url",
                       "issue_title",
                       "issue_state",
                       "issue_is_locked",
                       "issue_created_at",
                       "issue_updated_at",
                       "issue_closed_at",
                       "issue_user_login",
                       "issue_labels",
                       "issue_num_comments",
                       "issue_events_url",
                       "issue_dependency_name",
                       "issue_dependency_type",
                       "issue_dependency_actual_version",
                       "issue_dependency_next_version",
                       "issue_dependency_bundle_name",
                       # "issue_body_parser",
                       "issue_repo_url"]

        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()

    with open(search_file_path + "greenkeeper_issues.csv", "a") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        i = 0
        for item in data['items']:
            # parsed_body_list = parse_issue_body(item['body'])
            i = i + 1

            # for pb in parsed_body_list:
            issue_csv = dict()
            issue_csv.update({"issue_id": item['id']})
            issue_csv.update({"issue_number": item['number']})
            issue_csv.update({"issue_url": item['url']})
            issue_csv.update({"issue_title": item['title']})
            issue_csv.update({"issue_state": item['state']})
            issue_csv.update({"issue_is_locked": item['locked']})
            issue_csv.update({"issue_created_at": item['created_at']})
            issue_csv.update({"issue_updated_at": item['updated_at']})
            issue_csv.update({"issue_closed_at": item['closed_at']})
            issue_csv.update({"issue_user_login": item['user']['login']})
            issue_csv.update(get_issue_labels(item['labels']))
            issue_csv.update({"issue_num_comments": item['comments']})
            issue_csv.update({"issue_events_url": item['events_url']})
            # issue_csv.update(pb)
            issue_csv.update({"issue_repo_url": item['repository_url']})

            writer.writerow(issue_csv)

        print("{} issues processed.".format(i))


def generate_events_csv(search_file_path, merge_file_name):
    with open(search_file_path + merge_file_name) as json_file:
        data = json.load(json_file)

    with open(search_file_path + "greenkeeper_events.csv", "w") as csv_file:
        field_names = ["event_issue_url",
                       "event_issue_id",
                       "event_id",
                       "event_url",
                       "event_created_at",
                       "event_description",
                       "event_actor_id",
                       "event_actor_login",
                       "event_commit_id",
                       "event_commit_url",
                       "event_label"]

        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()

    with open(search_file_path + "greenkeeper_events.csv", "a") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        for d in data['events']:
            events_dict = dict()

            events_dict.update({"event_issue_url": d['issue_url']})
            events_dict.update({"event_issue_id": d['issue_id']})

            for i in d['items']:
                events_dict.update({"event_id": i['id']})
                events_dict.update({"event_url": i['url']})
                events_dict.update({"event_created_at": i['created_at']})
                events_dict.update({"event_description": i['event']})
                try:
                    events_dict.update({"event_actor_id": i['actor']['id']})
                except TypeError:
                    events_dict.update({"event_actor_id": None})
                except KeyError:
                    events_dict.update({"event_actor_id": None})

                try:
                    events_dict.update({"event_actor_login": i['actor']['login']})
                except TypeError:
                    events_dict.update({"event_actor_login": None})
                except KeyError:
                    events_dict.update({"event_actor_login": None})

                events_dict.update({"event_commit_id": i['commit_id']})
                events_dict.update({"event_commit_url": i['commit_url']})
                try:
                    events_dict.update({"event_label": i['label']['name']})
                except KeyError:
                    events_dict.update({"event_label": None})

                writer.writerow(events_dict)


def generate_comments_csv(search_file_path, merge_file_name):
    with open(search_file_path + merge_file_name) as json_file:
        data = json.load(json_file)

    with open(search_file_path + "greenkeeper_comments.csv", "w") as csv_file:
        field_names = ["comment_issue_url",
                       "comment_issue_id",
                       "comment_id",
                       "comment_url",
                       "comment_created_at",
                       "comment_updated_at",
                       "comment_body",
                       "comment_author_association",
                       "comment_user_id",
                       "comment_user_login",
                       "comment_user_type"]

        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()

    with open(search_file_path + "greenkeeper_comments.csv", "a") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        for d in data['comments']:
            comments_dict = dict()

            comments_dict.update({"comment_issue_url": d['issue_url']})
            comments_dict.update({"comment_issue_id": d['issue_id']})

            for i in d['items']:
                comments_dict.update({"comment_id": i['id']})
                comments_dict.update({"comment_url": i['url']})
                comments_dict.update({"comment_created_at": i['created_at']})
                comments_dict.update({"comment_updated_at": i['updated_at']})
                comments_dict.update({"comment_body": i['body']})
                comments_dict.update({"comment_author_association": i['author_association']})
                try:
                    comments_dict.update({"comment_user_id": i['user']['id']})
                except TypeError:
                    comments_dict.update({"comment_user_id": None})
                except KeyError:
                    comments_dict.update({"comment_user_id": None})

                try:
                    comments_dict.update({"comment_user_login": i['user']['login']})
                except TypeError:
                    comments_dict.update({"comment_user_login": None})
                except KeyError:
                    comments_dict.update({"comment_user_login": None})

                try:
                    comments_dict.update({"comment_user_type": i['user']['type']})
                except TypeError:
                    comments_dict.update({"comment_user_type": None})
                except KeyError:
                    comments_dict.update({"comment_user_type": None})

                writer.writerow(comments_dict)



def generate_commits_csv(search_file_path, merge_file_name):
    with open(search_file_path + merge_file_name) as json_file:
        data = json.load(json_file)

    with open(search_file_path + "greenkeeper_commits.csv", "w") as csv_file:
        field_names = ["commit_event_url",
                       "commit_event_id",
                       "commit_message",
                       "commit_git_committer_email",
                       "commit_git_committer_name",
                       "commit_git_author_email",
                       "commit_git_author_name",
                       "commit_github_committer_login",
                       "commit_github_committer_id",
                       "commit_github_committer_type",
                       "commit_github_author_login",
                       "commit_github_author_id",
                       "commit_github_author_type",
                       "commit_stats_deletions",
                       "commit_stats_additions",
                       "commit_stats_total",
                       "commit_tree_sha",
                       "commit_sha",
                       "commit_num_parents",
                       "commit_num_comments",
                       "commit_file_name",
                       "commit_file_additions",
                       "commit_file_deletions",
                       "commit_file_changes",
                       "commit_file_sha",
                       "commit_file_status"]

        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()

    with open(search_file_path + "greenkeeper_commits.csv", "a") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        for commit in data['items']:
            commits_dict = dict()

            commits_dict.update({"commit_event_url": commit['event_url']})
            commits_dict.update({"commit_event_id": commit['event_id']})

            c = commit['commit']

            commits_dict.update({"commit_message": c['commit']['message']})

            commits_dict.update({"commit_git_committer_email": c['commit']['committer']['email']})
            commits_dict.update({"commit_git_committer_name": c['commit']['committer']['name']})

            commits_dict.update({"commit_git_author_email": c['commit']['author']['email']})
            commits_dict.update({"commit_git_author_name": c['commit']['author']['name']})

            try:
                commits_dict.update({"commit_github_committer_login": c['committer']['login']})
                commits_dict.update({"commit_github_committer_id": c['committer']['id']})
                commits_dict.update({"commit_github_committer_type": c['committer']['type']})
            except TypeError:
                commits_dict.update({"commit_github_committer_login": None})
                commits_dict.update({"commit_github_committer_id": None})
                commits_dict.update({"commit_github_committer_type": None})

            try:
                commits_dict.update({"commit_github_author_login": c['author']['login']})
                commits_dict.update({"commit_github_author_id": c['author']['id']})
                commits_dict.update({"commit_github_author_type": c['author']['type']})
            except TypeError:
                commits_dict.update({"commit_github_author_login": None})
                commits_dict.update({"commit_github_author_id": None})
                commits_dict.update({"commit_github_author_type": None})

            commits_dict.update({"commit_stats_deletions": c['stats']['deletions']})
            commits_dict.update({"commit_stats_additions": c['stats']['additions']})
            commits_dict.update({"commit_stats_total": c['stats']['total']})

            commits_dict.update({"commit_tree_sha": c['commit']['tree']['sha']})
            commits_dict.update({"commit_sha": c['sha']})

            commits_dict.update({"commit_num_parents": len(c['parents'])})

            commits_dict.update({"commit_num_comments": c['commit']['comment_count']})

            for file in c['files']:
                commits_dict.update({"commit_file_name": file['filename']})

                commits_dict.update({"commit_file_additions": file['additions']})
                commits_dict.update({"commit_file_deletions": file['deletions']})
                commits_dict.update({"commit_file_changes": file['changes']})

                commits_dict.update({"commit_file_sha": file['sha']})

                commits_dict.update({"commit_file_status": file['status']})

                writer.writerow(commits_dict)


def fetch_package_names(search_file_path, merged_issues_file):
    fetched_package_names = set()
    field_names = ["package_name",
                   "package_gh_url_api",
                   "package_gh_url",
                   "package_author",
                   "package_description",
                   "package_repo_url",
                   "package_repo_type",
                   "package_version",
                   "package_dependencies",
                   "package_dev_dependencies",
                   "package_peer_dependencies"]

    # try to open existing package names file
    try:
        with open(search_file_path + "greenkeeper_package_names.csv", "r") as json_file:
            reader = csv.DictReader(json_file)

            for row in reader:
                fetched_package_names.add(row["package_repo_url"])
    except FileNotFoundError:
        with open(search_file_path + "greenkeeper_package_names.csv", "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()

    with open(search_file_path + merged_issues_file) as json_file:
        data = json.load(json_file)

    for item in data['items']:
        if item['repository_url'] in fetched_package_names:
            continue

        repo_url = item['repository_url']
        repo_url = repo_url + "/contents/package.json"

        success = False
        while not success:
            try:
                print("[REQUEST] {}".format(repo_url))

                git_token = MY_GIT_TOKEN
                headers = {'Authorization': 'token {}'.format(git_token)}

                contents_request = requests.get(repo_url,
                                                headers=headers)

                if contents_request.status_code == 200:
                    contents_json = contents_request.json()

                    try:
                        package_json_content = base64.b64decode(contents_json['content']).decode("utf-8")

                        package_json_content = json.loads(package_json_content)

                        try:
                            print("Package name: " + package_json_content['name'])
                            package_name = package_json_content['name']
                        except KeyError:
                            package_name = None

                        try:
                            package_author = package_json_content['author']
                        except KeyError:
                            package_author = None

                        try:
                            package_description = package_json_content['description']
                        except KeyError:
                            package_description = None

                        try:
                            package_repo_url = package_json_content['repository']['url']
                        except KeyError:
                            package_repo_url = None
                        except TypeError:
                            package_repo_url = None

                        try:
                            package_repo_type = package_json_content['repository']['type']
                        except KeyError:
                            package_repo_type = None
                        except TypeError:
                            package_repo_type = None

                        try:
                            package_version = package_json_content['version']
                        except KeyError:
                            package_version = None

                        try:
                            package_dependencies = package_json_content['dependencies']
                        except KeyError:
                            package_dependencies = None

                        try:
                            package_dev_dependencies = package_json_content['devDependencies']
                        except KeyError:
                            package_dev_dependencies = None

                        try:
                            package_peer_dependencies = package_json_content['peerDependencies']
                        except KeyError:
                            package_peer_dependencies = None

                        try:
                            package_gh_url_match = re.match("(https://github.com)/(.*?)/(.*?)/", contents_json['html_url'])
                            package_gh_url = package_gh_url_match.group(0)
                        except Exception:
                            package_gh_url = None

                        with open(search_file_path + "greenkeeper_package_names.csv", "a") as package_names_file:
                            writer = csv.DictWriter(package_names_file, fieldnames=field_names)
                            writer.writerow({"package_name": package_name,
                                             "package_gh_url_api": item['repository_url'],
                                             "package_gh_url": package_gh_url,
                                             "package_author": package_author,
                                             "package_description": package_description,
                                             "package_repo_url": package_repo_url,
                                             "package_repo_type": package_repo_type,
                                             "package_version": package_version,
                                             "package_dependencies": package_dependencies,
                                             "package_dev_dependencies": package_dev_dependencies,
                                             "package_peer_dependencies": package_peer_dependencies})
                    except Exception as e:
                        print("[ERROR] Exception when obtaining package name for repo {}: {}".format(item['repository_url'], str(e)))

                        with open(search_file_path + "greenkeeper_package_names.csv", "a") as package_names_file:
                            writer = csv.DictWriter(package_names_file, fieldnames=field_names)
                            writer.writerow({"package_name": None,
                                             "package_gh_url": item['repository_url']})
            except requests.exceptions.ConnectionError as ce:
                print(
                    "[ERROR] Request to '{}' failed due to connection error on item {}: {}. Trying again in one minute".format(
                        repo_url, str(item), str(ce)))

                time.sleep(60)
                continue
            except requests.exceptions.HTTPError as ce:
                print(
                    "[ERROR] Request to '{}' failed due to invalid HTTP response on item {}: {}. Continuing from next item.".format(
                        repo_url, str(item), str(ce)))

                success = True
                break
            except requests.exceptions.Timeout as ce:
                print(
                    "[ERROR] Request to '{}' had a timeout on item {}: {}. Trying again in one minute.".format(
                        repo_url, str(item), str(ce)))

                time.sleep(60)
                continue
            except KeyError as ke:
                print(
                    "[ERROR] Item '{}' on file '{}' doesn't contain field '{}'. Continuing from next item.".format(
                        "repository_url", merged_issues_file, str(ke)))

                break
            finally:
                success = True
                fetched_package_names.add(item['repository_url'])

                time.sleep(3)


def fetch_comments(issues_merged_path, issues_merged_file_name, suffix=prefix_date):
    # TODO: check if item wasn't previously fetched
    try:
        if not issues_merged_path.endswith("/"):
            issues_merged_path = issues_merged_path + "/"

        file_path = issues_merged_path + issues_merged_file_name

        with open(file_path) as json_file:

            try:
                data = json.load(json_file)
            except ValueError as ve:
                print("[FATAL ERROR] Not a valid json file '{}': {}".format(file_path, str(ve)))

            try:
                for item in data['items']:
                    # TODO: check if item wasn't previously fetched

                    success = False

                    while not success:
                        try:
                            comments_url = item['comments_url']

                            try:
                                print("[REQUEST] {}".format(comments_url))

                                git_token = MY_GIT_TOKEN
                                headers = {'Authorization': 'token {}'.format(git_token)}

                                comments_request = requests.get(comments_url,
                                                                headers=headers)

                                if comments_request.status_code == 200:
                                    comments_json = comments_request.json()
                                    out_json = dict()

                                    try:
                                        out_json.update({"issue_url": item['url']})
                                        out_json.update({"issue_id": item['id']})
                                        out_json.update({"items": comments_json})
                                    except KeyError as ke:
                                        print(
                                            "[ERROR] Item {} on file '{}' doesn't contain field '{}'. Continuing from next item.".format(
                                                file_path, str(item), str(ke)))

                                        success = True
                                        break

                                    with open(issues_merged_path + "[{}]comments@{}.json".format(item['id'], suffix),
                                              'w') as file:
                                        json.dump(out_json, file)

                            except requests.exceptions.ConnectionError as ce:
                                print(
                                    "[ERROR] Request to '{}' failed due to connection error on item {}: {}. Trying again in one minute".format(
                                        comments_url, str(item), str(ce)))

                                time.sleep(60)
                                continue
                            except requests.exceptions.HTTPError as ce:
                                print(
                                    "[ERROR] Request to '{}' failed due to invalid HTTP response on item {}: {}. Continuing from next item.".format(
                                        comments_url, str(item), str(ce)))

                                success = True
                                break
                            except requests.exceptions.Timeout as ce:
                                print(
                                    "[ERROR] Request to '{}' had a timeout on item {}: {}. Trying again in one minute.".format(
                                        comments_url, str(item), str(ce)))

                                time.sleep(60)
                                continue
                        except KeyError as ke:
                            print(
                                "[ERROR] Item {} on file '{}' doesn't contain field '{}'. Continuing from next item.".format(
                                    file_path, str(item), str(ke)))

                            break
                        finally:
                            success = True

                            time.sleep(3)
            except KeyError as ke:
                print("[FATAL ERROR] File '{}' doesn't contain field '{}'.".format(file_path, str(ke)))

    except FileNotFoundError as fnf:
        print("File {} not found.".format(file_path))


def merge_comments_json_files(search_file_path, files_suffix="comments@{}".format(prefix_date)):
    if not search_file_path.endswith("/"):
        files_patch = search_file_path + "/"
    else:
        files_patch = search_file_path

    files = glob.glob(files_patch + "*" + files_suffix + ".json")

    comments = {"comments": list()}

    for file in files:
        with open(file, "r") as f:
            comments_json = json.load(f)

            comments_list = comments['comments']
            comments_list.append(comments_json)

            comments.update({"comments": comments_list})

    with open(search_file_path + files_suffix + "-merged.json", "w") as f:
        json.dump(comments, f)


def extract_repo_name_from_url(repo_url):
    m = re.match("(https://api.github.com/repos)/(.*?)/(.*?)$", repo_url.rstrip())
    return m.group(2), m.group(3)


def request(url):
    git_token = MY_GIT_TOKEN
    headers = {'Authorization': 'token {}'.format(git_token)}
    print("[REQUEST] {}".format(url))
    res = requests.get(url,
                       headers=headers)

    return res


def fetch_all_project_events(issues_merged_path, issues_merged_file_name, event="issues", suffix=prefix_date):
    # TODO: check if item wasn't previously fetched
    try:
        if not issues_merged_path.endswith("/"):
            issues_merged_path = issues_merged_path + "/"

        file_path = issues_merged_path + issues_merged_file_name

        with open(file_path) as json_file:

            try:
                data = json.load(json_file)
            except ValueError as ve:
                print("[FATAL ERROR] Not a valid json file '{}': {}".format(file_path, str(ve)))
                return

            try:
                for item in data['items']:
                    # TODO: check if item wasn't previously fetched
                    try:
                        repository_url = item['repository_url']
                    except KeyError as ke:
                        print("[ERROR] Item {} on file '{}' doesn't contain field '{}'. Continuing from next issue report.".format(
                            file_path, str(item), str(ke)))

                        continue

                    try:
                        owner_repo = extract_repo_name_from_url(repository_url)
                        repo_name = "{}/{}".format(owner_repo[0], owner_repo[1])
                    except re.error as ree:
                        print("[ERROR] Bad repository URL {}. Continuing from next issue report.".format(repository_url))

                        continue

                    try:
                        if isfile("{}issue_reports@{}.json".format(issues_merged_path,
                                                                       repo_name.replace("/", "@"))):
                            print("[WARNING] Issue reports associated with repository '{}' were already fetched".format(repo_name))
                            continue
                    except KeyError as ke:
                        print(
                            "[ERROR] Item {} on file '{}' doesn't contain field '{}'. Continuing from next issue report.".format(
                                str(item), file_path, str(ke)))

                        continue

                    try:
                        try:
                            res = request("{}/issues?state=all&per_page=100".format(repository_url))
                            time.sleep(3)

                            issues = list()

                            try:
                                j = res.json()
                                issues = issues + j
                            except Exception:
                                print(
                                    "Repository '{}' has a bad JSON format. Continuing from next repository".format(
                                        repo_name))
                                continue

                            while 'next' in res.links.keys():
                                res = request(res.links['next']['url'])
                                time.sleep(3)

                                try:
                                    j = res.json()
                                    issues = issues + j
                                except Exception:
                                    print(
                                        "Repository '{}' has a bad JSON format. Continuing from next repository".format(
                                            repo_name))
                                    continue

                            i = {"repo_name": repo_name,
                                 "repo_url": repository_url,
                                 "items": issues}
                            with open("{}issue_reports@{}.json".format(issues_merged_path,
                                                                       repo_name.replace("/", "@")), "w") as f:
                                json.dump(i, f)


                            # #############
                            #
                            # print("[REQUEST] {}/{}".format(repository_url, event))
                            #
                            # git_token = MY_GIT_TOKEN
                            # headers = {'Authorization': 'token {}'.format(git_token)}
                            #
                            # events = requests.get(repository_url + "/{}".format(event),
                            #                       headers=headers)
                            #
                            # if events.status_code == 200:
                            #     events_json = events.json()
                            #     out_json = dict()
                            #
                            #     try:
                            #         out_json.update({"repo": "{}/{}".format(owner_repo[0], owner_repo[1])})
                            #         out_json.update({"repo_url": repository_url})
                            #         out_json.update({"issue_url": item['url']})
                            #         out_json.update({"issue_id": item['id']})
                            #         out_json.update({"items": events_json})
                            #     except KeyError as ke:
                            #         print(
                            #             "[ERROR] Item {} on file '{}' doesn't contain field '{}'. Continuing from next item.".format(
                            #                 file_path, str(item), str(ke)))
                            #
                            #         success = True
                            #         break
                            #
                            #     with open(issues_merged_path + "[{}:{}]{}@{}.json".format(owner_repo[0],
                            #                                                               owner_repo[1],
                            #                                                               event,
                            #                                                               suffix),
                            #               'w') as file:
                            #         json.dump(out_json, file)

                        except requests.exceptions.ConnectionError as ce:
                            print(
                                "[ERROR] Request to '{}' failed due to connection error on item {}: {}. Trying again in one minute".format(
                                    repository_url, str(item), str(ce)))
                            time.sleep(60)
                            continue
                        except requests.exceptions.HTTPError as ce:
                            print(
                                "[ERROR] Request to '{}' failed due to invalid HTTP response on item {}: {}. Continuing from next item.".format(
                                    repository_url, str(item), str(ce)))
                            success = True
                            break
                        except requests.exceptions.Timeout as ce:
                            print(
                                "[ERROR] Request to '{}' had a timeout on item {}: {}. Trying again in one minute.".format(
                                    repository_url, str(item), str(ce)))

                            time.sleep(60)
                            continue
                    except KeyError as ke:
                        print(
                            "[ERROR] Item {} on file '{}' doesn't contain field '{}'. Continuing from next item.".format(
                                file_path, str(item), str(ke)))
                        break
            except KeyError as ke:
                print("[FATAL ERROR] File '{}' doesn't contain field '{}'.".format(file_path, str(ke)))

    except FileNotFoundError as fnf:
        print("File {} not found.".format(file_path))

# def fetch_all_project_events2(search_file_path, input_file, event):
#     res = request("https://api.github.com/repos/{}/issues?state=all&per_page=100".format(repo_name))
#     time.sleep(3)
#
#     issues = list()
#
#     try:
#         j = res.json()
#         issues = issues + j
#     except Exception:
#         print("Repository '{}' has a bad JSON format. Continuing from next repository".format(repo_name))
# s        continue
#
#     while 'next' in res.links.keys():
#         res = request(res.links['next']['url'])
#         time.sleep(3)
#
#         try:
#             j = res.json()
#             issues = issues + j
#         except Exception:
#             print("Repository '{}' has a bad JSON format. Continuing from next repository".format(repo_name))
#             continue
#
#     i = {"repo_name": repo_name,
#          "items": issues}
#     with open("{}issue_reports@{}.json".format(search_files_path, repo_name.replace("/", "@")), "w") as f:
#         json.dump(i, f)


if __name__ == "__main__":

    # TODO [September 10th]: these two lines need to run on Brain2 after the current process that is running in there is done
    # TODO [September 10th]: need to write the script to generate the csv for the issues and pull requests
    # fetch_all_project_events(search_file_path, "issues@{}-merge.json".format(prefix_date), "issues")
    # fetch_all_project_events(search_file_path, "issues@{}-merge.json".format(prefix_date), "pulls")
    #fetch_all_project_events(search_file_path, "issues@{}-merge.json".format(prefix_date), "commits")

    # exit(1)

    # fetch_issues(search_file_path)
    # merge_issues_json_files(search_file_path)
    generate_issues_csv(search_file_path, "issues@{}-merge.json".format(prefix_date))
    exit(1)

    fetch_events(search_file_path, "issues@{}-merge.json".format(prefix_date))
    merge_events_json_files(search_file_path)
    fetch_commits(search_file_path, "events@{}-merged.json".format(prefix_date))
    count_commits(search_file_path, "events@{}-merged.json".format(prefix_date))
    merge_commits_json_files(search_file_path)
    fetch_package_names(search_file_path, "issues@{}-merge.json".format(prefix_date))
    fetch_first_pull_request(search_file_path)
    fetch_comments(search_file_path, "issues@{}-merge.json".format(prefix_date))
    merge_comments_json_files(search_file_path)
    fetch_all_project_events(search_file_path, "issues", "issues@{}-merge.json".format(prefix_date))
    fetch_all_project_events(search_file_path, "pulls", "issues@{}-merge.json".format(prefix_date))

    generate_issues_csv(search_file_path, "issues@{}-merge.json".format(prefix_date))
    generate_events_csv(search_file_path, "events@{}-merged.json".format(prefix_date))
    generate_commits_csv(search_file_path, "commits@{}-merged.json".format(prefix_date))
    generate_comments_csv(search_file_path, "comments@{}-merged.json".format(prefix_date))

    # read_gh_search_json(search_file_path)
