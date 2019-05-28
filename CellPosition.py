from Page import PageConst, CellConst, CellType


class CellPosition:
    def __init__(self, cell, x=0, y=0, width=0, height=0):
        """

        @param cell:
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
        if self.cell.level == CellType.DELIVERABLE or self.cell.level == CellType.CARD:
            self.cell.update_children()
        self.cell.render()

    @y.setter
    def y(self, value):
        """

        @param value:
        @return:
        """
        self._y = value
        if self.cell.level == CellType.DELIVERABLE or self.cell.level == CellType.CARD:
            self.cell.update_children()
        self.cell.render()

    @width.setter
    def width(self, value):
        """

        @param value:
        @return:
        """
        self._width = value
        if self.cell.level == CellType.DELIVERABLE or self.cell.level == CellType.CARD:
            self.cell.update_children()
        self.cell.render()

    @height.setter
    def height(self, value):
        """

        @param value:
        @return:
        """
        self._height = value
        if self.cell.level == CellType.DELIVERABLE or self.cell.level == CellType.CARD:
            self.cell.update_children()
        self.cell.render()
