import re
import os
import sys


class FileManager:
    def __init__(self, filename="", content=""):
        self.fs_comp = re.compile(r'(?u)[^-\w.]')
        self.create_storage_dir()
        if filename != "" and content != "":
            self.io(filename, content)

    def get_valid_filename(self, filename):
        """
            This function is from the django framework:
                (https://github.com/django/django/blob/master/django/utils/text.py):
            Return the given string converted to a string that can be used for a clean
            filename. Remove leading and trailing spaces; convert other spaces to
            underscores; and remove anything that is not an alphanumeric, dash,
            underscore, or dot.
            @param filename: filename string to process
            @return: The converted string
        """
        filename = str(filename).strip().replace(' ', '_')
        return self.fs_comp.match(filename)

    @staticmethod
    def create_storage_dir():
        """
            Create the root storage directory where are generated xml and svg files if they didn't exist
            Exit the program if one directory can not be created
        """
        try:
            if not os.path.isdir('../xml'):
                os.makedirs('../xml')
        except OSError:
            sys.exit('Fatal: output directory ./xml does not exist and cannot be created')
        try:
            if not os.path.isdir('../svg'):
                os.makedirs('../svg')
        except OSError:
            sys.exit('Fatal: output directory ./svg does not exist and cannot be created')

    def io(self, filename, content=""):
        try:
            mode = "r"
            if content != "":
                mode = "w"
            if type(content) == bytes:
                mode += "b"
            stream = open(filename, mode)
            if content != "":
                return stream.write(content)
            return stream.read()
        except OSError as err:
            sys.stderr("[ERR] File Manager:", err.strerror)
