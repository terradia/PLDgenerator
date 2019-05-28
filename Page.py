import xml.etree.ElementTree as Et
from enum import Enum


class PageConst(Enum):
    HEIGHT = 1080
    WIDTH = 1920


class Page:
    def __init__(self):
        self.cell_id = 3
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

    def add_id(self):
        self.cell_id += 1
        return self


class CellType(Enum):
    ROOT = 0
    DELIVERABLE = 1
    CARD = 2
    INNER_CELL = 3


class CellConst(Enum):
    WIDTH = 200
    HEIGHT = 80
    PADDING_TOP = 20
    PADDING_LEFT = 20

