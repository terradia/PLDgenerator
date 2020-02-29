"""
    The program start from here
"""
import os
from src.AsanaWrapper import AsanaWrapper
from src.DiagramGenerator import DiagramGenerator
from src.UserStories import UserStories
from src.FileManager import FileManager
from src.dump import dump


def main():
    """

    @return:
    """
    sprint = AsanaWrapper(os.getenv("ASANA_KEY"))
    pld_json = sprint.get_sprint_tasks([os.getenv("TASK")])
    gen = DiagramGenerator()
    dump(pld_json)
    gen.create_xml_tree("Terradia", pld_json)
    FileManager().generate_svg_from_xml()
    return 0


if __name__ == '__main__':
    main()
