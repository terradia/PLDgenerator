from GroupeCell import *
from Page import Page
from GetPLDConfig import *
from datetime import datetime
import xml.dom.minidom as dom


def XmlWriter(page):
    """

    @param page:
    @return:
    """
    filename = "Deliverable " + str(datetime.now().month) + "-" + str(datetime.now().year) + ".xml"
    f = open(filename, "w")
    f.truncate(0)
    xml_string = dom.parseString(Et.tostring(page.tree, encoding="unicode"))
    f.write(xml_string.toprettyxml())


def main():
    """

    @return:
    """
    AsanaSprint("")
    """page = Page()
    page.root_group_cell = GroupCell(page, CellType.ROOT)
    page.deliverable_group_cell = GroupCell(page, CellType.DELIVERABLE)
    card = GroupCell(page, CellType.CARD)
    page.deliverable_group_cell.append_child(card)
    card = GroupCell(page, CellType.CARD)
    page.deliverable_group_cell.append_child(card)
    XmlWriter(page)
    card = GroupCell(page, CellType.CARD)
    page.deliverable_group_cell.append_child(card)
    card = GroupCell(page, CellType.CARD)
    page.deliverable_group_cell.append_child(card)
    card = GroupCell(page, CellType.CARD)
    page.deliverable_group_cell.append_child(card)"""
    return 0


if __name__ == '__main__':
    main()
