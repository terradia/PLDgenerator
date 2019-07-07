"""
    This module provide the class that generate the xml for the cell
"""
import xml.etree.ElementTree as Et
from PIL import ImageFont
from src.CellPosition import CellPosition, Pos
from src.Page import CellType, CellConst
from src.AXmlComponent import AXmlComponent


class Cell(AXmlComponent):
    """
        The Cell class is used to create cell that contain text in the diagram
    """
    def __init__(self, page, parent_node, text):
        """
            Setup some cell default information
            @param page: The related Page where the cell must be rendered
            @param parent_node: the group cell to which this cell is related
            @param text: The text to be displayed inside the cell
        """
        super().__init__(page, CellType.INNER_CELL)
        self.text = text
        self.font_size = self._get_wrapped_font_size(15)
        self.pos = CellPosition(self, Pos(x=parent_node.pos.x + CellConst.PADDING_LEFT.value,
                                          y=parent_node.pos.y + CellConst.PADDING_TOP.value))
        self.render()

    def _get_wrapped_font_size(self, font_size):
        """
            process the displayed text in the desired font and font size to check if it fits inside the cell using the
            parameter font_size, if not decrease the font size
            @param font_size: default font size
            @return: the new font size
        """
        font = ImageFont.truetype('../assets/Montserrat-Regular.ttf', font_size)
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
                return self._get_wrapped_font_size(font_size)
            wraped += " "
        return font_size

    def render(self):
        """
            erase the cell if it exist
            render the cell in the xml tree
        """
        if self.node is not None:
            self.page.root.remove(self.node)
        self.node = Et.SubElement(self.page.root, 'mxCell', {"id": str(id(self)),
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

    def _update_deliverable(self, child):
        pass

    def _update_card(self, child):
        pass

    def _update_inner_cell(self, child):
        pass

    def _add_child_component(self, child):
        pass
