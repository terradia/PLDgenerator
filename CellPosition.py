"""
    Manage the cell position and size used in the Areas and Cell classes
"""
from dataclasses import dataclass
from Page import PageConst, CellConst, CellType


@dataclass
class Pos:
    """
        This dataclass provide a simple and more compact way
        to pass coordinates and sizes as parameter
    """
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0


class CellPosition:
    """
        Manage the cell position and size used in the Areas and Cell classes
    """
    def __init__(self, cell, pos=Pos()):
        """
            Define the cell position and size
            @param cell: Parent cell
            @param pos: dataclass that contain the x, y coord and the size of the object
        """
        self.cell = cell
        self._x = 0
        self._y = 0
        self._width = 0
        self._height = 0
        switcher = {
            "x": self._init_x,
            "y": self._init_y,
            "width": self._init_width,
            "height": self._init_height
        }
        pos_iter = vars(pos)
        for coord, value in pos_iter.items():
            switcher.get(coord)(cell.level, value)

    def _init_x(self, level, coord_value):
        """
            Init the x coordinate of the object
            @param level: type of the parent cell
            @param coord_value: value of the coordinate passed to the constructor by the Pos Dataclass
        """
        if coord_value == 0:
            if level == CellType.INNER_CELL:
                self._x = 0
            else:
                self._x = PageConst.WIDTH.value / 2 - CellConst.WIDTH.value / 2
        else:
            self._x = coord_value

    def _init_y(self, level, coord_value):
        """
            Init the y coordinate of the object
            @param level: type of the parent cell
            @param coord_value: value of the coordinate passed to the constructor by the Pos Dataclass
        """
        if coord_value == 0:
            if level == CellType.INNER_CELL:
                self._y = 0
            else:
                self._y = PageConst.HEIGHT.value / 4 - CellConst.HEIGHT.value / 2
        else:
            self._y = coord_value

    def _init_width(self, level, coord_value):
        """
            Init the width of the object
            @param level: type of the parent cell
            @param coord_value: value of the coordinate passed to the constructor by the Pos Dataclass
        """
        if coord_value == 0:
            if level == CellType.INNER_CELL:
                self._width = 200
            else:
                self._width = CellConst.WIDTH.value + (CellConst.PADDING_LEFT.value * 2)
        else:
            self._width = coord_value

    def _init_height(self, level, coord_value):
        """
            Init the height of the object
            @param level: type of the parent cell
            @param coord_value: value of the coordinate passed to the constructor by the Pos Dataclass
        """
        if coord_value == 0:
            if level == CellType.INNER_CELL:
                self._height = 80
            else:
                self._height = CellConst.HEIGHT.value + (CellConst.PADDING_TOP.value * 2)
        else:
            self._height = coord_value

    @property
    def x(self):
        """
        @return: x coordinate of the cell
        """
        return self._x

    @property
    def y(self):
        """
        @return: y coordinate of the cell
        """
        return self._y

    @property
    def width(self):
        """
        @return: width of the cell
        """
        return self._width

    @property
    def height(self):
        """
        @return: height of the cell
        """
        return self._height

    @x.setter
    def x(self, value):
        """
        set the new value of the x coordinate
        update the cell's children if the cell is a group
        rerender the cell in the xml tree
        @param value: the new x coordinate
        """
        self._x = value
        if self.cell.level == CellType.DELIVERABLE or self.cell.level == CellType.CARD:
            self.cell.update_children()
        self.cell.render()

    @y.setter
    def y(self, value):
        """
        set the new value of the y coordinate
        update the cell's children if the cell is a group
        rerender the cell in the xml tree
        @param value: the new y coordinate
        """
        self._y = value
        if self.cell.level == CellType.DELIVERABLE or self.cell.level == CellType.CARD:
            self.cell.update_children()
        self.cell.render()

    @width.setter
    def width(self, value):
        """
        set the new value of the width
        update the cell's children if the cell is a group
        rerender the cell in the xml tree
        @param value: the new width
        """
        self._width = value
        if self.cell.level == CellType.DELIVERABLE or self.cell.level == CellType.CARD:
            self.cell.update_children()
        self.cell.render()

    @height.setter
    def height(self, value):
        """
        set the new value of the height
        update the cell's children if the cell is a group
        rerender the cell in the xml tree
        @param value: the new height
        """
        self._height = value
        if self.cell.level == CellType.DELIVERABLE or self.cell.level == CellType.CARD:
            self.cell.update_children()
        self.cell.render()
