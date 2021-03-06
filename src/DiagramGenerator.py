"""
    The DiagramGenerator regroup all the function that is needed to create the xml's and svg's files
"""
import xml.etree.ElementTree as Et
from datetime import datetime
from src.RootArea import RootArea
from src.DelivarableArea import DeliverableArea
from src.CardAreas import CardAreas
from src.Cell import Cell
from src.Page import Page
from src.FileManager import FileManager
from src.UserStories import UserStories


class DiagramGenerator:
    """
        The DiagramGenerator regroup all the function that is needed to create the xml's and svg's files
    """
    def __init__(self):
        self.gen_date = "_" + str(datetime.now().month) + "_" + str(
            datetime.now().year)
        self.UserStorie = UserStories()
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

    def parse_storie_info(self, storie_name, storie_info):
        if storie_info == "":
            return None
        storie_info = storie_info.split(";")
        if len(storie_info) < 5 or len(storie_info) > 7:
            return None
        storie = {"StorieName": storie_name,
                 "CustomerType": storie_info[0].strip('\n ,;'),
                 "Need": storie_info[1].strip('\n ,;'),
                 "Description": storie_info[2].strip('\n ,;'),
                 "DoD": storie_info[3].strip('\n ,;'),
                 "TimeCharge": storie_info[4].strip('\n ,;')}
        return storie

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
            card_group = CardAreas(page)
            page.deliverable_group_cell.append_child(card_group)
            if isinstance(cards, dict):
                self.create_xml_tree(deliverable, cards)
                for card in cards:
                    cell = Cell(page, card_group, card)
                    card_group.append_child(cell)
            if isinstance(cards, list):
                for card in cards:
                    cell = Cell(page, card_group, card["storie"], card["done"])
                    card_group.append_child(cell)
                    storie = self.parse_storie_info(card['storie'], card["storie_info"])
                    if storie:
                        self.UserStorie.gen_user_stories(storie)
        self.fm.io(root_name,
                   path="../xml/",
                   extension=self.gen_date + ".xml",
                   content=Et.tostring(page.tree, encoding="UTF-8"))
        self.fm.close()
