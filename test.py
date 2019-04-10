import asana
import sys
import random
from enum import Enum
from datetime import datetime


BeginFile = '<mxGraphModel dx="1394" dy="824" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1.5" pageWidth="1169" pageHeight="827" background="#ffffff" math="0" shadow="0">\n    <root>\n        <mxCell id="0"/>\n        <mxCell id="1" parent="0"/>\n'
EndFile = '    </root>\n</mxGraphModel>\n'

CellId = 2

class CellType(Enum):
    ROOT = 0
    DELIVERABLE = 1
    CARD = 2


class GroupCell:
    def __init__(self, f, level = CellType.ROOT):
        global CellId
        self.padding = 20
        self.rand = lambda: random.randint(0, 255)
        self.ID = CellId
        CellId += 1
        if level == CellType.ROOT:
            self.color = "#AE4132"
            self.x = -105
            self.y = 0
            self.width = 200
            self.height = 80
        elif level == CellType.DELIVERABLE:
            self.color = "#10739E"
            self.x = -105
            self.y = 50
            self.width = 200
            self.height = 80
        elif level == CellType.CARD:
            self.color = '#{:02x}{:02x}{:02x}'.format(self.rand(), self.rand(), self.rand())
            self.x = 0
            self.y = 170
            self.width = 200
            self.height = 80
        self.render()

    def render(self):
        f.write('<mxCell id="{}" value="" style="fillColor={};strokeColor=none;opacity=30;" parent="1" vertex="1">\n'
                '   <mxGeometry x="{}" y="{}" width="{}" height="{}" as="geometry"/>\n'
                '</mxCell>\n'.format(self.ID, self.color, self.x, self.y, self.width, self.height))



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

# replace with your personal access token.
personal_access_token = ''

# Construct an Asana client
client = asana.Client.access_token(personal_access_token)
# Set things up to send the name of this script to us to show that you succeeded! This is optional.
client.options['client_name'] = "hello_world_python"

# Get your user info
diag = {}
PLD = client.get("", "")
for deliverable in PLD:
    card = client.get("/tasks/" + deliverable["gid"] + "/subtasks", "")
    cards = {}
    for tabs in card:
        tab = client.get("/tasks/" + tabs["gid"] + "/subtasks", "")
        subs = []
        for sub in tab:
            subs.append(sub["name"])
        cards[tabs["name"]] = subs
    diag[deliverable["name"]] = cards
dump(diag)
filename = "Deliverable " + str(datetime.now().month) + "-" + str(datetime.now().year) + ".xml"
f = open(filename, "w")
f.write(BeginFile)
GroupCell(f, CellType.ROOT)
f.write(EndFile)

