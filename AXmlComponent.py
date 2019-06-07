"""
    The AXmlComponent module define the base class for the xml used to create diagrams
"""
from abc import ABC, abstractmethod
from Page import CellType
from CellPosition import CellPosition


class AXmlComponent(ABC):
    """
        The AXmlComponent is an abstract class that define some variable and function for
        the Xml Component subclasses (RootArea, DeliverableArea, CardArea, Cell)
    """
    def __init__(self, page=None, level=CellType.UNDEFINED, hidden=False):
        """
            Setup some cell default information
            @param page: The related Page where the cell must be rendered
            @param level: Is an enum value from The CellType enum that represent the type of the cell
            @param hidden: A boolean that tell if the area must be displayed of just used for position processing
        """
        self.level = level
        self.node = None
        self.parent = page
        self.page = page
        self.pos = CellPosition(self)
        self._children = []
        self.index = 0
        self.hidden = hidden

    def __index__(self):
        """
            @return: self index position from the parent's children array
        """
        return self.index

    @abstractmethod
    def render(self):
        """
            erase the cell if it exist
            render the cell in the xml tree
        """
        pass

    def append_child(self, child):
        """
            append a child to the _children array
            render the cell and then update each of the cell's children
            @param child: the new child to append
        """
        self._children.append(child)
        child.index = len(self._children)
        if child.level == CellType.INNER_CELL:
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
            if current_child.level == child.level and child != current_child:
                if axis == "x":
                    return child.pos.x
                if axis == "y":
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
            if current_child.level == child.level and child != current_child:
                if axis == "x":
                    return child.pos.x
                if axis == "y":
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

    @abstractmethod
    def _update_deliverable(self, child):
        pass

    @abstractmethod
    def _update_card(self, child):
        pass

    @abstractmethod
    def _update_inner_cell(self, child):
        pass

    @abstractmethod
    def _add_child_component(self, child):
        pass
