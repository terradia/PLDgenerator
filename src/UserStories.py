import re
from string import Template
from datetime import datetime
from src.DiagramGenerator import DiagramGenerator


class UserStories:
    def __init__(self, stories_name, customer_type, need, description, dod, charge):
        self.substitution = dict(
            StorieName=stories_name,
            CustomerType=customer_type,
            Need=need,
            Description=description,
            DoD=dod,
            TimeCharge=charge
        )
        self.gen_date = "_" + str(datetime.now().month) + "_" + str(
            datetime.now().year)
        self.open_template()

    @staticmethod
    def _get_valid_filename(filename):
        """
            This function is from the django framework:
                (https://github.com/django/django/blob/master/django/utils/text.py):
            Return the given string converted to a string that can be used for a clean
            filename. Remove leading and trailing spaces; convert other spaces to
            underscores; and remove anything that is not an alphanumeric, dash,
            underscore, or dot.
            @param filename: filename string to process
            @return: The converted string
        """
        filename = str(filename).strip().replace(' ', '_')
        return re.sub(r'(?u)[^-\w.]', '', filename)

    def open_template(self):
        stream = open("../assets/UserStorieTemplate.xml", "r")
        template = Template(stream.read())
        user_stories = template.substitute(self.substitution)
        stream.close()
        filename = self._get_valid_filename(self.substitution.get("StorieName")) + self.gen_date + ".xml"
        stream = open("../xml/" + filename, "wb")
        stream.write(user_stories.encode('utf-8'))
        stream.close()
        DiagramGenerator.generate_svg_from_xml_tree()
