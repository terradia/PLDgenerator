import sys
from string import Template
from datetime import datetime
from functools import wraps
from src.FileManager import FileManager


def required(mandatory):
    def decorator(f):
        @wraps(f)
        def wrapper(*dicts):
            for key in mandatory:
                if key not in dicts[1]:
                    raise ValueError('Key "%s" is missing from argument' % (
                        key))
            return f(*dicts)
        return wrapper
    return decorator


class UserStories:
    def __init__(self):
        self.gen_date = "_" + str(datetime.now().month) + "_" + str(
            datetime.now().year)
        self.fm = FileManager()
        self.template = Template(self.fm.io("UserStorieTemplate", path="../assets/", extension=".xml"))

    @required(["StorieName", "CustomerType", "Need", "Description", "DoD", "TimeCharge"])
    def gen_user_stories(self, stories_info):
        print("Generating", stories_info.get("StorieName"))
        try:
            self.fm.io(stories_info.get("StorieName"), path="../xml/", extension=self.gen_date + ".xml",
                       content=self.template.substitute(stories_info).encode('utf-8'))
        except TypeError as err:
            print(err)
            sys.exit("[ERR] UserStories: a template error occurred")
        except ValueError as err:
            print(err)
            sys.exit("[ERR] UserStories: a template error occurred")
