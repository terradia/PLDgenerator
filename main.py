from GroupeCell import *
from Cell import Cell
from Page import Page
from GetPLDConfig import *
from datetime import datetime
import xml.dom.minidom as dom
import re
import os
from Naked.toolshed.shell import execute_js


def XmlWriter(page, file_type):
    """

    @param page:
    @return:
    """
    filename = get_valid_filename(file_type) + "_" + str(datetime.now().month) + "_" + str(datetime.now().year) + ".xml"
    if not os.path.isdir('./xml'):
        os.makedirs('./xml')
    if not os.path.isdir('./svg'):
        os.makedirs('./svg')
    f = open("./xml/" + filename, "wb")
    xml_string = dom.parseString(Et.tostring(page.tree, encoding="UTF-8"))
    f.write(xml_string.toprettyxml(encoding="utf-8"))
    f.close()


def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def create_xml(root_name, json_dict):
    page = init_xml(root_name)
    for deliverable, cards in sorted(json_dict.items()):
        cell = Cell(page, page.deliverable_group_cell, deliverable)
        page.deliverable_group_cell.append_child(cell)
        card_group = GroupCell(page, CellType.CARD)
        page.deliverable_group_cell.append_child(card_group)
        if isinstance(cards, dict):
            create_xml(deliverable, cards)
        for card in sorted(cards):
            cell = Cell(page, card_group, card)
            card_group.append_child(cell)
    XmlWriter(page, root_name)
    return page


def init_xml(root_name):
    page = Page()
    page.root_group_cell = GroupCell(page, CellType.ROOT)
    cell = Cell(page, page.root_group_cell, root_name)
    page.root_group_cell.append_child(cell)
    page.deliverable_group_cell = GroupCell(page, CellType.DELIVERABLE)
    return page


def main():
    """

    @return:
    """
    sprint = AsanaSprint("0/3f3fdafe316d91ca6951530ea0419b9d")
    pld_json = sprint.get_sprint_tasks(["1116922404389120"])
    create_xml("Terradia", pld_json)
    for filename in os.listdir('xml'):
        execute_js('./drawio-batch-master/drawio-batch.js',
               "./xml/" + filename + " ./svg/" + os.path.splitext(filename)[0] + '.svg')
    return 0


if __name__ == '__main__':
    main()
