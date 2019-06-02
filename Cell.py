import xml.etree.ElementTree as Et
from CellPosition import CellPosition
from Page import CellType, CellConst
from PIL import ImageFont


class Cell:
    def __init__(self, page, parent_node, text):
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
        return self.index

    def _get_wraped_font_size(self, font_size):
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
