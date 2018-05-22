import json
import mistune

import mdutils
from mdutils import emailLink


class WeeklyEmail:
    SEPARATOR = "\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-"

    def __init__(self):
        self.sections = []

    def compile(self):
        return ("\n\n" + WeeklyEmail.SEPARATOR + "\n\n").join(str(section) for section in self.sections)

    def to_html(self):
        return mistune.markdown(self.compile())

    def __str__(self):
        return self.compile()


class WeeklyEmailSection:

    def __init__(self, heading=None, text=None):
        self.heading = heading
        self.text = text

    def __str__(self):
        result = ""
        if self.heading is not None:
            result += "## " + self.heading
        if self.text is not None:
            result += "\n\n" + self.text

        return result


class Captain:
    """
    Contains info for a captain, such as name, email, and phone number
    """

    def __init__(self, name, email, phone_num):
        """
        Make a new captain
        :param name: Their name
        :param email: Their email
        :param phone_num: Their phone number
        """
        self.name = name
        self.email = email
        self.phone_num = phone_num

    def __str__(self):
        return self.name + ": " + emailLink(self.email) + ", " + self.phone_num


CAPTAINS = []


def get_captains():
    """
    Get the list of captains, and read them fresh from the json if there are none
    :return: A list of Captains
    """
    if len(CAPTAINS) == 0:
        captains_json = None
        try:
            captains_json = json.load(open("../captains.json"))
        except FileNotFoundError:
            captains_json = json.load(open("captains.json"))

        for captain_dict in captains_json:
            CAPTAINS.append(Captain(captain_dict["name"], captain_dict["email"], captain_dict["phone_num"]))

    return CAPTAINS


def gen_signature(captains=get_captains()):
    """
    Generate a weekly email signature given a complete list of captains
    :param captains: List of Captains
    :return: A markdown-formatted email signature
    """
    result = ""
    for captain in captains:
        result += str(captain) + "\n\n\n"
    return result
