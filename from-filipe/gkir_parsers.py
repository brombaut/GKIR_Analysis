import re

from html.parser import HTMLParser

prefix_date = "2020-09-16"

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