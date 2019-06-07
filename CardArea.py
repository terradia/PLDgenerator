"""
    This module provide the class that generate the xml for card's area
"""
import xml.etree.ElementTree as Et
import random
from AXmlComponent import AXmlComponent
from Page import CellType, CellConst


def rand_color():
    """
        randomize each 3 RGB component of the color and store it in a string in an hexadecimal format
        @return: a string containing a randomized color in an hexadecimal format
    """
    return '#{:02x}{:02x}{:02x}'.format(random.randint(0, 255),
                                        random.randint(0, 255),
                                        random.randint(0, 255))


class CardArea(AXmlComponent):
    """
        The CardArea class is used to create colored background area in the diagram
    """
    def __init__(self, page, hidden=False):
        super().__init__(page=page, level=CellType.CARD, hidden=hidden)
        self.color = rand_color()
        self.nb_card = 0
        self.pos.y += CellConst.HEIGHT.value * 2 + (CellConst.PADDING_TOP.value * 4)
        self.render()

    def render(self):
        """
            erase the cell if it exist
            render the cell in the xml tree
        """
        if self.node is not None:
            self.page.root.remove(self.node)
        style = "strokeColor=none;opacity=30;"
        if not self.hidden:
            style += ";fillColor=" + self.color
        self.node = Et.SubElement(self.page.root, 'mxCell', {"id": str(id(self)),
                                                             "value": "",
                                                             "style": style,
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
        """
            update the x and the y coordinate of the child passed in parameter
            @param child: the child to update
        """
        child.pos.x = self.pos.x + CellConst.PADDING_LEFT.value
        if self._find_first_child_of_type(child, "") == child:
            child.pos.y = self.pos.y + CellConst.PADDING_TOP.value
        else:
            child.pos.y = self._find_last_child_of_type(child, "y")\
                          + CellConst.HEIGHT.value + CellConst.PADDING_TOP.value

    def _add_child_component(self, child):
        """
            update the cell position and size depends on the child type
            @param child: the added child
        """
        if len(self._children) == 1:
            self.pos.height = CellConst.HEIGHT.value + (CellConst.PADDING_TOP.value * 2)
        else:
            self.pos.height += CellConst.HEIGHT.value + CellConst.PADDING_TOP.value
        self.nb_card += 1
