"""
    The DiagramGenerator regroup all the function that is needed to create the xml's and svg's files
"""
import re
import os
import sys
import xml.dom.minidom as dom
import xml.etree.ElementTree as Et
from datetime import datetime
from Naked.toolshed.shell import execute_js
from GroupeCell import GroupCell, CellType
from Cell import Cell
from Page import Page


class DiagramGenerator:
    """
    The DiagramGenerator regroup all the function that is needed to create the xml's and svg's files
    """
    def __init__(self):
        self.gen_date = "_" + str(datetime.now().month) + "_" + str(
            datetime.now().year)

    @staticmethod
    def _get_valid_filename(filename):
        """
        This function is from the django framework (https://github.com/django/django/blob/master/django/utils/text.py):
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
            if not os.path.isdir('./xml'):
                os.makedirs('./xml')
        except OSError:
            sys.exit('Fatal: output directory ./xml does not exist and cannot be created')
        try:
            if not os.path.isdir('./svg'):
                os.makedirs('./svg')
        except OSError:
            sys.exit('Fatal: output directory ./svg does not exist and cannot be created')

    def xml_write_to_file(self, page, root_name):
        """
        Create and open the file named by the root_name param and a suffix composed of the current month and year
        Then write the xml tree to this file in an utf-8 encoded format
        @param page: A Page class that store the xml tree
        @param root_name: the root name of the generated diagram that is used to create the filename
        """
        filename = self._get_valid_filename(root_name) + self.gen_date + ".xml"
        self.create_storage_dir()
        stream = open("./xml/" + filename, "wb")
        xml_string = dom.parseString(Et.tostring(page.tree, encoding="UTF-8"))
        stream.write(xml_string.toprettyxml(encoding="utf-8"))
        stream.close()

    @staticmethod
    def init_xml_tree(root_name):
        """
        Create the base xml element of a jgraph xml file format using the Page class that provide some base element,
        the root cell zone and the root cell itself
        @param root_name: the name if the diagram's root cell
        @return: The Page class where the base xml tree is stored
        """
        page = Page()
        page.root_group_cell = GroupCell(page, CellType.ROOT)
        cell = Cell(page, page.root_group_cell, root_name)
        page.root_group_cell.append_child(cell)
        page.deliverable_group_cell = GroupCell(page, CellType.DELIVERABLE)
        return page

    def create_xml_tree(self, root_name, diagram_dict):
        """
        Loop through the diagram_dict param to create the xml tree
        Recursively called if another dict is found
        @param root_name: the name if the diagram's root cell
        @param diagram_dict: the retrieved dictionary from asana used to create the xml tree
        """
        page = self.init_xml_tree(root_name)
        for deliverable, cards in sorted(diagram_dict.items()):
            cell = Cell(page, page.deliverable_group_cell, deliverable)
            page.deliverable_group_cell.append_child(cell)
            if len(cards) == 0:
                card_group = GroupCell(page, CellType.CARD, hidden=True)
            else:
                card_group = GroupCell(page, CellType.CARD)
            page.deliverable_group_cell.append_child(card_group)
            if isinstance(cards, dict):
                self.create_xml_tree(deliverable, cards)
            for card in sorted(cards):
                cell = Cell(page, card_group, card)
                card_group.append_child(cell)
        self.xml_write_to_file(page, root_name)

    @staticmethod
    def generate_svg_from_xml_tree():
        """
        Loop through all the xml files that are generated and transform it into an svg diagram using node js package
        called drawio-batch that is a package wrapper of the draw.io app and launched it using naked toolshed's function
        execute_js
        drawio-batch: https://github.com/languitar/drawio-batch
        Naked toolshed's: https://naked.readthedocs.io/toolshed_shell.html
        """
        for filename in os.listdir('xml'):
            execute_js('./drawio-batch-master/drawio-batch.js',
                       "./xml/" + filename + " ./svg/" + os.path.splitext(filename)[0] + '.svg')
