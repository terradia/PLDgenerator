import re
import os
import sys
from Naked.toolshed.shell import execute_js


class FileManager:
    def __init__(self, filename="", path="", extension="", content="", encoding="utf-8"):
        self.fs_comp = re.compile(r'(?u)[^-\w.]')
        self.create_storage_dir()
        self.stream = None
        if filename != "" and content != "":
            self.io(filename, path=path, extension=extension, content=content, encoding=encoding)

    @staticmethod
    def get_valid_filename(filename):
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
        return re.sub(r'(?u)[^-\w.]', '', filename)

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

    def io(self, filename, path="", extension="", content="", encoding="utf-8"):
        try:
            mode = "r"
            if content != "":
                mode = "w"
                if type(content) == bytes:
                    mode += "b"
                self.stream = open(path + self.get_valid_filename(filename) + extension, mode)
            else:
                self.stream = open(path + self.get_valid_filename(filename) + extension, mode, encoding=encoding)
            if content != "":
                self.stream.write(content)
                self.close()
                return
            return self.stream.read()
        except OSError as err:
            sys.stderr("[ERR] File Manager:", err.strerror)
        except ValueError as err:
            sys.stderr("[ERR] File Manager:")
            print(err)

    def close(self):
        self.stream.close()

    @staticmethod
    def generate_svg_from_xml():
        """
            Loop through all the xml files that are generated and transform it
            into an svg diagram using node js package
            called drawio-batch that is a package wrapper of the draw.io app
            and launched it using naked toolshed's function
            execute_js
            drawio-batch: https://github.com/languitar/drawio-batch
            Naked toolshed's: https://naked.readthedocs.io/toolshed_shell.html
        """
        for filename in os.listdir('../xml'):
            execute_js('../drawio-batch-master/drawio-batch.js',
                       "../xml/" + filename + " ../svg/" + os.path.splitext(filename)[0] + '.svg')
