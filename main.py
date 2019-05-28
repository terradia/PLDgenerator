from GroupeCell import *
from Cell import Cell
from Page import Page
from GetPLDConfig import *
from datetime import datetime
import xml.dom.minidom as dom
import os
from Naked.toolshed.shell import execute_js


def XmlWriter(page):
    """

    @param page:
    @return:
    """
    filename = "Deliverable_" + str(datetime.now().month) + "_" + str(datetime.now().year) + ".xml"
    f = open(filename, "wb")
    f.truncate(0)
    xml_string = dom.parseString(Et.tostring(page.tree, encoding="UTF-8"))
    print(xml_string.actualEncoding)
    f.write(xml_string.toprettyxml(encoding="utf-8"))
    return filename


def create_xml(page, pld_dict):
    for deliverable, cards in sorted(pld_dict.items()):
        cell = Cell(page, page.deliverable_group_cell, deliverable)
        page.deliverable_group_cell.append_child(cell)
        card_group = GroupCell(page, CellType.CARD)
        page.deliverable_group_cell.append_child(card_group)
        for card in sorted(cards):
            cell = Cell(page, card_group, card)
            card_group.append_child(cell)
    return page


def init_xml(sprint):
    pld_json = sprint.get_sprint_tasks([""])
    page = Page()
    page.root_group_cell = GroupCell(page, CellType.ROOT)
    cell = Cell(page, page.root_group_cell, "Terradia")
    page.root_group_cell.append_child(cell)
    page.deliverable_group_cell = GroupCell(page, CellType.DELIVERABLE)
    return page, pld_json


def main():
    """

    @return:
    """
    sprint = AsanaSprint("")
    page, pld_dict = init_xml(sprint)
    filename = XmlWriter(create_xml(page, pld_dict))
    print(os.path.splitext(filename)[0]+'.svg')
    return execute_js('./drawio-batch-master/drawio-batch.js', filename + " " + os.path.splitext(filename)[0]+'.svg')


if __name__ == '__main__':
    main()
