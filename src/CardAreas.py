"""
    This module provide the class that generate the xml for card's area
"""
import xml.etree.ElementTree as Et
from src.AXmlComponent import AXmlComponent
from src.Page import CellType, CellConst
from src.CardArea import CardArea


class CardAreas(AXmlComponent):
    """
        The CardArea class is used to create colored background area in the diagram
    """
    def __init__(self, page, hidden=False):
        super().__init__(page=page, level=CellType.CARD, hidden=hidden)
        self.nb_card = 0
        self.pos.y += CellConst.HEIGHT.value + (CellConst.PADDING_TOP.value * 2)
        self.render()

    def render(self):
        """
            erase the cell if it exist
            render the cell in the xml tree
        """
        for area in self._children:
            area.render()

    def append_child(self, child):
        self._add_child_component(child)
        self.render()
        self.update_children()

    def _update_deliverable(self, child):
        pass

    def _update_card(self, child):
        """
            update the x coordinate of the card child passed in parameter
            @param child: the child to update
            @return:
        """
        child.pos.x = self.pos.x
        if self._find_first_child_of_type(child, "") == child:
            child.pos.y = self.pos.y + CellConst.HEIGHT.value + (CellConst.PADDING_TOP.value * 2)
        else:
            child.pos.y = self._find_last_child_of_type(child, "y") + CellConst.HEIGHT.value + (CellConst.PADDING_TOP.value * 2)

    def _update_inner_cell(self, child):
        """
            update the x and the y coordinate of the child passed as parameter
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
        self._children.append(CardArea(self.page,
                                       self,
                                       done=child.done))
        self._children[-1].index = len(self._children)
        self._children[-1].append_child(child)
        self.nb_card += 1
