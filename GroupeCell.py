from enum import Enum
import xml.etree.ElementTree as Et
import random
from Page import *
from CellPosition import *


def rand_color():
    """
    randomize each 3 RGB component of the color and store it in a string in an hexadecimal format
    @return: a string containing a randomized color in an hexadecimal format
    """
    return '#{:02x}{:02x}{:02x}'.format(random.randint(0, 255),
                                        random.randint(0, 255),
                                        random.randint(0, 255))


class GroupCell:
    """
    The GroupCell class is used to create colored background area in the diagram
    """
    def __init__(self, page, level=CellType.ROOT, hidden=False):
        """
        Setup somme cell default information
        @param page: The related Page where the cell must be rendered
        @param level: Is an enum value from The CellType enum that represent the type of the cell
        @param hidden: A boolean that tell if the area must be displayed of just used for position processing
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
        self.hidden = hidden
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
        style = "strokeColor=none;opacity=30;"
        if not self.hidden:
            style += ";fillColor=" + self.color
        self.node = Et.SubElement(self.page.root, 'mxCell', {"id": str(self.id),
                                                             "value": "",
                                                             "style": style,
                                                             "parent": "1",
                                                             "vertex": "1"})
        Et.SubElement(self.node, 'mxGeometry', {"x": str(self.pos.x),
                                                "y": str(self.pos.y),
                                                "width": str(self.pos.width),
                                                "height": str(self.pos.height),
                                                "as": "geometry"})

    def append_child(self, child):
        """
        append a child to the _children array
        render the cell and then update each of the cell's children
        @param child: the new child to append
        """
        self._children.append(child)
        child.index = len(self._children)
        self._add_child_component(child)
        self.render()
        self.update_children()

    def _find_last_child_of_type(self, current_child, axis):
        """
        Loop through the children array in reverse from the position of current_child and return the first
        child of the same type
        @param current_child: current child position in where it has to start to search
        @param axis: return the x coordinate or the y coordinate
        @return: if the axis param is set return x or y coordinate of the founded child
                if the axis param is empty return the founded child
                if no child is found return 0
        """
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
        """
        Loop through the children array return the first
        child of the same type
        @param current_child: current child position in where it has to start to search
        @param axis: return the x coordinate or the y coordinate
        @return: if the axis param is set return x or y coordinate of the founded child
                if the axis param is empty return the founded child
                if no child is found return 0
        """
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
        """
        Count the number of children of type cell_type and return this number
        @param cell_type: the type of the desired child
        @return: the number of children of a specific type
        """
        nb = 0
        for item in self._children:
            if item.level == cell_type:
                nb += 1
        return nb

    def _update_deliverable(self, child):
        """
        update the x coordinate of the deliverable child passed in parameter
        @param child: the child to update
        """
        if self._find_first_child_of_type(child, "") == child:
            child.pos.x = self.pos.x + CellConst.PADDING_LEFT.value
        else:
            child.pos.x = self._find_last_child_of_type(child, "x") + CellConst.WIDTH.value + \
                          CellConst.PADDING_LEFT.value

    def _update_card(self, child):
        """
        update the x coordinate of the card child passed in parameter
        @param child: the child to update
        @return:
        """
        if self.level == CellType.DELIVERABLE:
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
        Loop through the children array and update each child depend on the child CellType
        """
        switcher = {
            CellType.DELIVERABLE: self._update_deliverable,
            CellType.CARD: self._update_card,
            CellType.INNER_CELL: self._update_inner_cell
        }
        for child in self._children:
            switcher.get(child.level)(child)

    def _add_child_component(self, child):
        """
        update the cell position and size depends on the child type
        @param child: the added child
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
