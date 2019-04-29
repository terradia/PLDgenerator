from enum import Enum
import xml.etree.ElementTree as Et
import random
from Page import PageConst


class CellType(Enum):
    ROOT = 0
    DELIVERABLE = 1
    CARD = 2


class DeliverableConst(Enum):
    WIDTH = 200
    HEIGHT = 80
    PADDING_TOP = 20
    PADDING_LEFT = 20


class CellPosition:
    def __init__(self, cell):
        """

        @param cell:
        """
        self.cell = cell
        self._x = PageConst.WIDTH.value / 2 - DeliverableConst.WIDTH.value / 2
        self._y = PageConst.HEIGHT.value / 4 - DeliverableConst.HEIGHT.value / 2
        self._width = DeliverableConst.WIDTH.value
        self._height = DeliverableConst.HEIGHT.value

    @property
    def x(self):
        """

        @return:
        """
        return self._x

    @property
    def y(self):
        """

        @return:
        """
        return self._y

    @property
    def width(self):
        """

        @return:
        """
        return self._width

    @property
    def height(self):
        """

        @return:
        """
        return self._height

    @x.setter
    def x(self, value):
        """

        @param value:
        @return:
        """
        self._x = value
        self.cell.render()

    @y.setter
    def y(self, value):
        """

        @param value:
        @return:
        """
        self._y = value
        self.cell.render()

    @width.setter
    def width(self, value):
        """

        @param value:
        @return:
        """
        self._width = value
        self.cell.render()

    @height.setter
    def height(self, value):
        """

        @param value:
        @return:
        """
        self._height = value
        self.cell.render()


class GroupCell:
    def __init__(self, page, level=CellType.ROOT):
        """

        @param page:
        @param level:
        """
        self.id = str(page.cell_id)
        self.level = level.name
        self.node = None
        self.parent = page
        self.page = page
        self.page.add_id()
        self.pos = CellPosition(self)
        self._children = []
        if level == CellType.ROOT:
            self.color = "#AE4132"
        elif level == CellType.DELIVERABLE:
            self.color = "#10739E"
            self.nbDeliverable = 0
            self.pos.width = 0
            self.pos.y += DeliverableConst.HEIGHT.value + DeliverableConst.PADDING_TOP.value
        elif level == CellType.CARD:
            self.color = rand_color()
            self.nbCard = 0
            self.pos.y += DeliverableConst.HEIGHT.value * 2 + DeliverableConst.PADDING_TOP.value
        self.render()

    def render(self):
        """

        @return:
        """
        print("render(): ")
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
        print("append_child(): ")
        self._children.append(child)
        self._add_child_component()
        self.render()
        self._update_children()
        return self

    def _update_children(self):
        """

        @return:
        """
        print("update_children(): ")
        for index, child in enumerate(self._children):
            if index == 0:
                child.pos.x = self.pos.x
                continue
            child.pos.x = self._children[index - 1].pos.x + DeliverableConst.WIDTH.value + \
                DeliverableConst.PADDING_LEFT.value
        return self

    def _add_child_component(self):
        """

        @return:
        """
        print("add_child_component(): ")
        if self.level == "DELIVERABLE":
            if len(self._children) == 1:
                self.pos.width += DeliverableConst.WIDTH.value
            else:
                self.pos.width += DeliverableConst.WIDTH.value + DeliverableConst.PADDING_LEFT.value
            self.pos.x = PageConst.WIDTH.value / 2 - self.pos.width / 2
            self.nbDeliverable += 1
        if self.level == "CARD":
            self.pos.height += DeliverableConst.HEIGHT + DeliverableConst.PADDING_TOP
            self.nbCard += 1
        return self
