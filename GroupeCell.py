from enum import Enum
import xml.etree.ElementTree as Et
import random
from Page import *
from CellPosition import *


def rand_color():
    """

    :rtype:
    """
    return '#{:02x}{:02x}{:02x}'.format(random.randint(0, 255),
                                        random.randint(0, 255),
                                        random.randint(0, 255))


class GroupCell:
    def __init__(self, page, level=CellType.ROOT):
        """

        @param page:
        @param level:
        """
        self.id = str(page.cell_id)
        self.level = level
        self.node = None
        self.parent = page
        self.page = page
        self.page.add_id()
        self.pos = CellPosition(self)
        self._children = []
        self.index = 0
        if level == CellType.ROOT:
            self.color = "#AE4132"
        elif level == CellType.DELIVERABLE:
            self.color = "#10739E"
            self.nbDeliverable = 0
            self.pos.width = 0
            self.pos.y += CellConst.HEIGHT.value + (CellConst.PADDING_TOP.value * 2)
        elif level == CellType.CARD:
            self.color = rand_color()
            self.nbCard = 0
            self.pos.y += CellConst.HEIGHT.value * 2 + (CellConst.PADDING_TOP.value * 4)
        self.render()

    def __index__(self):
        return self.index

    def render(self):
        """

        @return:
        """
        if self.node is not None:
            self.page.root.remove(self.node)
        self.node = Et.SubElement(self.page.root, 'mxCell', {"id": str(self.id),
                                                             "value": "",
                                                             "style": "fillColor=" + self.color +
                                                                      ";strokeColor=none "
                                                                      ";opacity=30;",
                                                             "parent": "1",
                                                             "vertex": "1"})
        Et.SubElement(self.node, 'mxGeometry', {"x": str(self.pos.x),
                                                "y": str(self.pos.y),
                                                "width": str(self.pos.width),
                                                "height": str(self.pos.height),
                                                "as": "geometry"})
        return self

    def append_child(self, child):
        """

        @param child:
        @return:
        """
        self._children.append(child)
        child.index = len(self._children)
        self._add_child_component(child)
        self.render()
        self.update_children()
        return self

    def _find_last_child_of_type(self, current_child, axis):
        for child in reversed(self._children[:current_child]):
            if current_child.level == child.level and child != current_child :
                if axis == "x":
                    return child.pos.x
                elif axis == "y":
                    return child.pos.y
            if axis == "" and child == current_child:
                return child
        return 0

    def _find_first_child_of_type(self, current_child, axis):
        first_of_type = False
        for child in self._children:
            if current_child.level == child.level and child != current_child :
                if axis == "x":
                    return child.pos.x
                elif axis == "y":
                    return child.pos.y
            if first_of_type is False and axis == "" and child == current_child:
                return child
            if current_child.level == child.level:
                first_of_type = True
        return 0

    def _nb_item_of_type(self, cell_type):
        nb = 0
        for item in self._children:
            if item.level == cell_type:
                nb += 1
        return nb

    def _update_deliverable(self, child):
        if self._find_first_child_of_type(child, "") == child:
            child.pos.x = self.pos.x + CellConst.PADDING_LEFT.value
        else:
            child.pos.x = self._find_last_child_of_type(child, "x") + CellConst.WIDTH.value + \
                          CellConst.PADDING_LEFT.value

    def _update_card(self, child):
        if self.level == CellType.DELIVERABLE:
            if self._find_first_child_of_type(child, "") == child:
                child.pos.x = self.pos.x
            else:
                child.pos.x = self._find_last_child_of_type(child, "x") + CellConst.WIDTH.value + \
                              (CellConst.PADDING_LEFT.value * 2)

    def _update_inner_cell(self, child):
        if self.level == CellType.DELIVERABLE:
            child.pos.y = self.pos.y + CellConst.PADDING_TOP.value
            if self._find_first_child_of_type(child, "") == child:
                child.pos.x = self.pos.x + CellConst.PADDING_LEFT.value
            else:
                child.pos.x = self._find_last_child_of_type(child, "x") +\
                    CellConst.WIDTH.value +\
                    (CellConst.PADDING_LEFT.value * 2)
        elif self.level == CellType.CARD:
            child.pos.x = self.pos.x + CellConst.PADDING_LEFT.value
            if self._find_first_child_of_type(child, "") == child:
                child.pos.y = self.pos.y + CellConst.PADDING_TOP.value
            else:
                child.pos.y = self._find_last_child_of_type(child, "y") + CellConst.HEIGHT.value + CellConst.PADDING_TOP.value

    def update_children(self):
        """
        ALL REWORK NEEDED
        @return:
        """
        switcher = {
            CellType.DELIVERABLE: self._update_deliverable,
            CellType.CARD: self._update_card,
            CellType.INNER_CELL: self._update_inner_cell
        }
        for child in self._children:
            switcher.get(child.level)(child)
        return self

    def _add_child_component(self, child):
        """

        @return:
        """
        if self.level == CellType.DELIVERABLE and child.level == CellType.INNER_CELL:
            if len(self._children) == 1:
                self.pos.width += CellConst.WIDTH.value + (CellConst.PADDING_LEFT.value * 2)
            else:
                self.pos.width += CellConst.WIDTH.value + (CellConst.PADDING_LEFT.value * 2)
                self.pos.x = PageConst.WIDTH.value / 2 - self.pos.width / 2
            self.nbDeliverable += 1
        if self.level == CellType.CARD:
            if len(self._children) == 1:
                self.pos.height = CellConst.HEIGHT.value + (CellConst.PADDING_TOP.value * 2)
            else:
                self.pos.height += CellConst.HEIGHT.value + CellConst.PADDING_TOP.value
            self.nbCard += 1
        return self
