"""
    The program start from here
"""
from AsanaWrapper import AsanaWrapper
from DiagramGenerator import DiagramGenerator


def main():
    """

    @return:
    """
    sprint = AsanaWrapper("")
    pld_json = sprint.get_sprint_tasks(["1116922404389120"])
    gen = DiagramGenerator()
    gen.create_xml_tree("Terradia", pld_json)
    gen.generate_svg_from_xml_tree()
    return 0


if __name__ == '__main__':
    main()
