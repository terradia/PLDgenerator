"""
This module contain the class and functions used to generate the User Stories
"""

import sys
from string import Template
from datetime import datetime
from functools import wraps
from src.FileManager import FileManager


def required(mandatory):
    """
    This decorator is used to check if a function that take a dict as param contain the mandatory field.4
    Raise a ValueError exception if one of the mandatory field doesn't exist
    @param mandatory: this is an array of the mandatory field that the function must handle
    @return: the return value of the decorated function
    """
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
    """
    Generate the User stories
    """
    def __init__(self):
        """
        init the creation date used as suffix for the filename
        init the FileManager used for reading the template and generate tge xml
        init the template engine
        """
        self.gen_date = "_" + str(datetime.now().month) + "_" + str(
            datetime.now().year)
        self.fm = FileManager()
        self.template = Template(self.fm.io("UserStorieTemplate", path="../assets/", extension=".xml"))

    @required(["StorieName", "CustomerType", "Need", "Description", "DoD", "TimeCharge"])
    def gen_user_stories(self, stories_info):
        """
        This function generate an xml that has been filled with the stories_info dict
        passed as parameter using the template engine
        @param stories_info: a dict that contain all the filed needed to generate a user stories
        """
        for k, info in stories_info.items():
            info = info.replace("&", "&amp;")
            info = info.replace("\"", "&quot;")
            stories_info.update({k: info})
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
