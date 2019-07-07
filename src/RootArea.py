"""
    This module provide the class that generate the xml for the root's area
"""
import xml.etree.ElementTree as Et
from src.AXmlComponent import AXmlComponent
from src.Page import CellType


class RootArea(AXmlComponent):
    """
    The GroupCell class is used to create colored background area in the diagram
    """
    def __init__(self, page):
        super().__init__(page=page, level=CellType.ROOT, hidden=False)
        self.render()

    def __index__(self):
        """
        @return: self index position from the parent's children array
        """
        return self.index

    def render(self):
        """
            erase the cell if it exist
            render the cell in the xml tree
        """
        if self.node is not None:
            self.page.root.remove(self.node)
        self.node = Et.SubElement(self.page.root, 'mxCell', {"id": str(id(self)),
                                                             "value": "",
                                                             "style": "strokeColor=none;opacity=30;;fillColor=#AE4132",
                                                             "parent": "1",
                                                             "vertex": "1"})
        Et.SubElement(self.node, 'mxGeometry', {"x": str(self.pos.x),
                                                "y": str(self.pos.y),
                                                "width": str(self.pos.width),
                                                "height": str(self.pos.height),
                                                "as": "geometry"})

    def _update_deliverable(self, child):
        pass

    def _update_card(self, child):
        pass

    def _update_inner_cell(self, child):
        pass

    def _add_child_component(self, child):
        pass
