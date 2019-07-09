"""
    The program start from here
"""
import os
from src.AsanaWrapper import AsanaWrapper
from src.DiagramGenerator import DiagramGenerator
from src.UserStories import UserStories


def main():
    """

    @return:
    """
    UserStories().gen_user_stories({"StorieName": "1.1 Modification du BMC",
                 "CustomerType": "CBO (Chief Business Officer)",
                 "Need": "BMC qui définit bien le projet",
                 "Description": "Le BMC permet de dresser l’état des lieux du modèle économique d’une entreprise. Il est donc important qu’il soit précis",
                 "DoD": "-	Remplir le BMC\n"
                        "-	Effectuer les modifications sur les parties principales\n"
                        "-	Définir précisément les cibles avec les critères de segmentation\n"
                        "-	Modification sur les parties Channels et Customer Relationship\n"
                        "-	Faire une petite étude de la consommation moyenne pour définir les cibles\n"
                        "-	Faire des recherches sur les catégories socio-professionnelles",
                 "TimeCharge": "1 Jour(s) / Homme"})
    """sprint = AsanaWrapper(os.getenv("ASANA_KEY"))
    pld_json = sprint.get_sprint_tasks([os.getenv("TASK")])
    gen = DiagramGenerator()
    gen.create_xml_tree("Terradia", pld_json)
    gen.generate_svg_from_xml_tree()"""
    return 0


if __name__ == '__main__':
    main()
