"""
    This module define some const and the base class for generating the xml tree
"""
import xml.etree.ElementTree as Et
from dataclasses import dataclass
from enum import Enum


class PageConst(Enum):
    """
    Define the default size of the page
    """
    HEIGHT = 1080
    WIDTH = 1920


@dataclass
class Page:
    """
    Create the base elements used in the xml tree
    """
    def __init__(self):
        self.root_group_cell = None
        self.deliverable_group_cell = None
        self.tree = Et.Element('mxGraphModel',
                               {"dx": "1920",
                                "dy": "1080",
                                "grid": "1",
                                "gridSize": "10",
                                "guides": "1",
                                "tooltips": "1",
                                "connect": "1",
                                "arrows": "1",
                                "fold": "1",
                                "page": "1",
                                "pageScale": "1.5",
                                "pageWidth": "1920",
                                "pageHeight": "1080",
                                "background": "#ffffff",
                                "math": "0",
                                "shadow": "0"})
        self.doc = Et.ElementTree(self.tree)
        self.root = Et.SubElement(self.tree, 'root')
        self.first = Et.SubElement(self.root, 'mxCell', {"id": "0"})
        self.background = Et.SubElement(self.root, 'mxCell', {"id": "1", "value": "Background", "parent": "0"})
        self.front = Et.SubElement(self.root, 'mxCell', {"id": "2", "value": "Front", "parent": "0"})


class CellType(Enum):
    """
    Define some constant used to define the cell type
    """
    UNDEFINED = 0
    ROOT = 1
    DELIVERABLE = 2
    CARD = 3
    INNER_CELL = 4


class CellConst(Enum):
    """
    Define the default size of a cell
    """
    WIDTH = 200
    HEIGHT = 80
    PADDING_TOP = 10
    PADDING_LEFT = 10
