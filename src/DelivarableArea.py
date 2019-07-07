"""
    This module provide the class that generate the xml for the deliverable's area
"""
import xml.etree.ElementTree as Et
from src.AXmlComponent import AXmlComponent
from src.Page import CellType, CellConst, PageConst


class DeliverableArea(AXmlComponent):
    """
        The GroupCell class is used to create colored background area in the diagram
    """
    def __init__(self, page):
        super().__init__(page=page, level=CellType.DELIVERABLE)
        self.nb_deliverable = 0
        self.pos.width = 0
        self.pos.y += CellConst.HEIGHT.value + (CellConst.PADDING_TOP.value * 2)
        self.render()

    def render(self):
        """
            erase the cell if it exist
            render the cell in the xml tree
        """
        if self.node is not None:
            self.page.root.remove(self.node)
        self.node = Et.SubElement(self.page.root, 'mxCell', {"id": str(id(self)),
                                                             "value": "",
                                                             "style": "strokeColor=none;opacity=30;;fillColor=#10739E",
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
        """
            update the x coordinate of the card child passed in parameter
            @param child: the child to update
            @return:
        """
        if self._find_first_child_of_type(child, "") == child:
            child.pos.x = self.pos.x
        else:
            child.pos.x = self._find_last_child_of_type(child, "x") + CellConst.WIDTH.value + \
                          (CellConst.PADDING_LEFT.value * 2)

    def _update_inner_cell(self, child):
        """
            update the x and the y coordinate of the child passed in parameter
            @param child: the child to update
            @return:
        """
        child.pos.y = self.pos.y + CellConst.PADDING_TOP.value
        if self._find_first_child_of_type(child, "") == child:
            child.pos.x = self.pos.x + CellConst.PADDING_LEFT.value
        else:
            child.pos.x = self._find_last_child_of_type(child, "x") +\
                CellConst.WIDTH.value +\
                (CellConst.PADDING_LEFT.value * 2)

    def _add_child_component(self, child):
        """
            update the cell position and size depends on the child type
            @param child: the added child
        """
        if len(self._children) == 1:
            self.pos.width += CellConst.WIDTH.value + (CellConst.PADDING_LEFT.value * 2)
        else:
            self.pos.width += CellConst.WIDTH.value + (CellConst.PADDING_LEFT.value * 2)
            self.pos.x = PageConst.WIDTH.value / 2 - self.pos.width / 2
        self.nb_deliverable += 1
