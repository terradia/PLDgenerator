"""
    The DiagramGenerator regroup all the function that is needed to create the xml's and svg's files
"""
import os
import xml.etree.ElementTree as Et
from datetime import datetime
from Naked.toolshed.shell import execute_js
from src.RootArea import RootArea
from src.DelivarableArea import DeliverableArea
from src.CardArea import CardArea
from src.Cell import Cell
from src.Page import Page
from src.FileManager import FileManager


class DiagramGenerator:
    """
        The DiagramGenerator regroup all the function that is needed to create the xml's and svg's files
    """
    def __init__(self):
        self.gen_date = "_" + str(datetime.now().month) + "_" + str(
            datetime.now().year)
        self.fm = FileManager()

    @staticmethod
    def init_xml_tree(root_name):
        """
            Create the base xml element of a jgraph xml file format using the Page class that provide some base element,
            the root cell zone and the root cell itself
            @param root_name: the name if the diagram's root cell
            @return: The Page class where the base xml tree is stored
        """
        page = Page()
        page.root_group_cell = RootArea(page)
        cell = Cell(page, page.root_group_cell, root_name)
        page.root_group_cell.append_child(cell)
        page.deliverable_group_cell = DeliverableArea(page)
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
            if not cards:
                card_group = CardArea(page, hidden=True)
            else:
                card_group = CardArea(page)
            page.deliverable_group_cell.append_child(card_group)
            if isinstance(cards, dict):
                self.create_xml_tree(deliverable, cards)
            for card in sorted(cards):
                cell = Cell(page, card_group, card)
                card_group.append_child(cell)
        self.fm.io(root_name + self.gen_date + ".xml", Et.tostring(page.tree, encoding="UTF-8"))

    @staticmethod
    def generate_svg_from_xml_tree():
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
