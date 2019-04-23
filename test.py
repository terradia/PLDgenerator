import asana
import sys
import random
import xml.etree.ElementTree as et
from enum import Enum
from datetime import datetime
import xml.dom.minidom as dom


CellId = 2
Tree = et.Element('mxGraphModel',
                  {"dx": "1920",
                   "dy": "1080",
                   "grid": "1",
                   "gridSize": "10",
                   "guides": "1",
                   "tooltips": "1",
                   "connect": "1",
                   "arrows": "1",
                   "fold": "1",
                   "page": "1",
                   "pageScale": "1.5",
                   "pageWidth": "1920",
                   "pageHeight": "1080",
                   "background": "#ffffff",
                   "math": "0",
                   "shadow": "0"})
Doc = et.ElementTree(Tree)
Root = et.SubElement(Tree, 'root')
et.SubElement(Root, 'mxCell', {"id": "0"})
et.SubElement(Root, 'mxCell', {"id": "1", "parent": "0"})


class PageConst(Enum):
    HEIGHT = 1080
    WIDTH = 1920


class CellType(Enum):
    ROOT = 0
    DELIVERABLE = 1
    CARD = 2


class DeliverableConst(Enum):
    WIDTH = 200
    HEIGHT = 80
    PADDING_TOP = 20
    PADDING_LEFT = 20


class GroupCell:
    def __init__(self, level = CellType.ROOT):
        global CellId
        global Root
        global Tree
        self.padding = 20
        self.rand = lambda: random.randint(0, 255)
        self.ID = level.name
        self.x = PageConst.WIDTH.value / 2 - DeliverableConst.WIDTH.value / 2
        self.y = PageConst.HEIGHT.value / 4 - DeliverableConst.HEIGHT.value / 2
        self.width = DeliverableConst.WIDTH.value
        self.height = DeliverableConst.HEIGHT.value
        self.node = ""
        CellId += 1
        if level == CellType.ROOT:
            self.color = "#AE4132"
        elif level == CellType.DELIVERABLE:
            self.color = "#10739E"
            self.nbDeli = 0
            self.y += DeliverableConst.HEIGHT.value + DeliverableConst.PADDING_TOP.value
        elif level == CellType.CARD:
            self.color = '#{:02x}{:02x}{:02x}'.format(self.rand(), self.rand(), self.rand())
            self.nbCard = 0
            self.y += DeliverableConst.HEIGHT.value * 2 + DeliverableConst.PADDING_TOP.value
        self.render()

    def render(self):
        self.node = et.SubElement(Root, 'mxCell', {"id": str(self.ID),
                                                   "value": "",
                                                   "style": "fillColor=" + self.color + ";strokeColor=none;opacity=30;",
                                                   "parent": "1",
                                                   "vertex": "1"})
        et.SubElement(self.node, 'mxGeometry', {"x": str(self.x),
                                                "y": str(self.y),
                                                "width": str(self.width),
                                                "height": str(self.height),
                                                "as": "geometry"})

    def addcomponent(self):
        Root.remove(self.node)
        if self.ID == "DELIVERABLE":
            self.width += DeliverableConst.WIDTH.value + DeliverableConst.PADDING_LEFT.value
            self.nbDeli += 1
        if self.ID == "CARD":
            self.height += DeliverableConst.HEIGHT + DeliverableConst.PADDING_TOP
            self.nbCard += 1
        self.render()


def dump(obj, nested_level=0, output=sys.stdout):
    spacing = '   '
    if type(obj) == dict:
        print('%s{' % ((nested_level) * spacing))
        for k, v in obj.items():
            if hasattr(v, '__iter__') and type(v) != str:
                print('%s%s:' % ((nested_level + 1) * spacing, k))
                dump(v, nested_level + 1, output)
            else:
                print('%s%s: %s' % ((nested_level + 1) * spacing, k, v))
        print('%s}' % (nested_level * spacing))
    elif type(obj) == list:
        print('%s[' % ((nested_level) * spacing))
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v, nested_level + 1, output)
            else:
                print('%s%s' % ((nested_level + 1) * spacing, v))
        print('%s]' % ((nested_level) * spacing))
    else:
        print('%s%s' % (nested_level * spacing, obj))

"""# replace with your personal access token.
personal_access_token = ''

# Construct an Asana client
client = asana.Client.access_token(personal_access_token)
# Set things up to send the name of this script to us to show that you succeeded! This is optional.
client.options['client_name'] = "hello_world_python"

# Get your user info
diag = {}
PLD = client.get("/tasks//subtasks", "")
for deliverable in PLD:
    card = client.get("/tasks/" + deliverable["gid"] + "/subtasks", "")
    cards = {}
    print("deliverable: ", deliverable["name"])
    for tabs in card:
        tab = client.get("/tasks/" + tabs["gid"] + "/subtasks", "")
        subs = []
        for sub in tab:
            subs.append(sub["name"])
        cards[tabs["name"]] = subs
    diag[deliverable["name"]] = cards
dump(diag)"""

filename = "Deliverable " + str(datetime.now().month) + "-" + str(datetime.now().year) + ".xml"
f = open(filename, "w")
f.truncate(0)
RootGroup = GroupCell(CellType.ROOT)
DeliverableGroup = GroupCell(CellType.DELIVERABLE)
CardGroup = GroupCell(CellType.CARD)
xmlString = dom.parseString(et.tostring(Tree, encoding="unicode"))
f.write(xmlString.toprettyxml())
