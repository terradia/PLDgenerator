"""
    Manage the cell position and size used in the GroupCell and Cell class
"""
from Page import PageConst, CellConst, CellType


class CellPosition:
    """
    Manage the cell position and size used in the GroupCell and Cell class
    """
    def __init__(self, cell, x=0, y=0, width=0, height=0):
        """
        Define the cell position and size
        @param cell: Parent cell
        @param x: x coordinate of the cell
        @param y: y coordiante of the cell
        @param width: width of the cell
        @param height: height of the cell
        """
        self.cell = cell
        if x == 0:
            if cell.level == CellType.INNER_CELL:
                self._x = 0
            else:
                self._x = PageConst.WIDTH.value / 2 - CellConst.WIDTH.value / 2
        else:
            self._x = x
        if y == 0:
            if cell.level == CellType.INNER_CELL:
                self._y = 0
            else:
                self._y = PageConst.HEIGHT.value / 4 - CellConst.HEIGHT.value / 2
        else:
            self._y = y
        if width == 0:
            if cell.level == CellType.INNER_CELL:
                self._width = 200
            else:
                self._width = CellConst.WIDTH.value + (CellConst.PADDING_LEFT.value * 2)
        else:
            self._width = width
        if height == 0:
            if cell.level == CellType.INNER_CELL:
                self._height = 80
            else:
                self._height = CellConst.HEIGHT.value + (CellConst.PADDING_TOP.value * 2)
        else:
            self._height = height

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
