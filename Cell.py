import xml.etree.ElementTree as Et
from CellPosition import CellPosition
from Page import CellType, CellConst

"""
    <mxCell id="2" value="Head of Development" style="rounded=1;fillColor=#23445D;gradientColor=none;strokeColor=none;fontColor=#FFFFFF;fontStyle=1;fontFamily=Tahoma;fontSize=14" parent="1" vertex="1">
      <mxGeometry x="670" y="240" width="190" height="80" as="geometry"/>
    </mxCell>
"""


class Cell:
    def __init__(self, page, parent_node, text):
        self.id = str(page.cell_id)
        self.level = CellType.INNER_CELL
        self.node = None
        self.parent = page
        self.page = page
        self.page.add_id()
        self.text = text
        self.index = 0
        self.pos = CellPosition(self, parent_node.pos.x + CellConst.PADDING_LEFT.value,
                                parent_node.pos.y + CellConst.PADDING_TOP.value)
        self.render()

    def __index__(self):
        return self.index

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
                                                                      "fontFamily=Tahoma;"
                                                                      "whiteSpace=wrap;"
                                                                      "fontSize=15",
                                                             "parent": "2",
                                                             "vertex": "1"})
        Et.SubElement(self.node, "mxGeometry", {"x": str(self.pos.x),
                                                "y": str(self.pos.y),
                                                "width": str(self.pos.width),
                                                "height": str(self.pos.height),
                                                "as": "geometry"})
        return self
