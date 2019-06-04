import xml.etree.ElementTree as Et
from CellPosition import CellPosition
from Page import CellType, CellConst
from PIL import ImageFont


class Cell:
    def __init__(self, page, parent_node, text):
        """
        Setup somme cell default information
        @param page: The related Page where the cell must be rendered
        @param parent_node: the group cell to which this cell is related
        @param text: The text to be displayed inside the cell
        """
        self.id = str(page.cell_id)
        self.level = CellType.INNER_CELL
        self.node = None
        self.parent = page
        self.page = page
        self.page.add_id()
        self.text = text
        self.font_size = self._get_wraped_font_size(15)
        self.index = 0
        self.pos = CellPosition(self, parent_node.pos.x + CellConst.PADDING_LEFT.value,
                                parent_node.pos.y + CellConst.PADDING_TOP.value)
        self.render()

    def __index__(self):
        """
        @return: self index position from the parent's children array
        """
        return self.index

    def _get_wraped_font_size(self, font_size):
        """
        process the displayed text in the desired font and font size to check if it fits inside the cell using the
        parameter font_size, if not decrease the font size
        @param font_size: default font size
        @return: the new font size
        """
        font = ImageFont.truetype('Montserrat-Regular.ttf', font_size)
        words = self.text.split()
        nb_lines = 1
        wraped = ""
        for word in words:
            wraped += word
            if font.getsize(wraped)[0] > 170:
                wraped = word
                nb_lines += 1
            if nb_lines > 4:
                font_size -= 1
                return self._get_wraped_font_size(font_size)
            wraped += " "
        return font_size

    def render(self):
        """
        erase the cell if it exist
        render the cell in the xml tree
        """
        if self.node is not None:
            self.page.root.remove(self.node)
        self.node = Et.SubElement(self.page.root, 'mxCell', {"id": str(self.id),
                                                             "value": self.text,
                                                             "style": "rounded=1;"
                                                                      "fillColor=#23445D;"
                                                                      "gradientColor=none;"
                                                                      "strokeColor=none;"
                                                                      "fontColor=#FFFFFF;"
                                                                      "fontStyle=1;"
                                                                      "fontFamily=Montserrat;"
                                                                      "whiteSpace=wrap;"
                                                                      "fontSize=" + str(self.font_size),
                                                             "parent": "2",
                                                             "vertex": "1"})
        Et.SubElement(self.node, "mxGeometry", {"x": str(self.pos.x),
                                                "y": str(self.pos.y),
                                                "width": str(self.pos.width),
                                                "height": str(self.pos.height),
                                                "as": "geometry"})
        return self
