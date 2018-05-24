import datetime
import json

import mistune

import mdutils
from mdutils import emailLink


class WeeklyEmail:
    SEPARATOR = "---"

    def __init__(self):
        self.sections = []

    def compile(self):
        return ("\n\n" + WeeklyEmail.SEPARATOR + "\n\n").join(str(section) for section in self.sections)

    def to_html(self):
        return mistune.markdown(self.compile())

    def __str__(self):
        return self.compile()

    def add_room_times(self, open_room_times):
        pass


class Event:

    def __init__(self, event_dict):
        try:
            if "date" in event_dict["start"].keys():
                format_multi_day_time = "%Y-%m-%d"
                self.start = datetime.datetime.strptime(event_dict["start"]["date"], format_multi_day_time)
                self.end = datetime.datetime.strptime(event_dict["end"]["date"], format_multi_day_time)
                self.all_day = True
            elif "dateTime" in event_dict["start"].keys():
                format_single_day_time = "%Y-%m-%dT%H:%M:%S-05:00"
                self.start = datetime.datetime.strptime(event_dict["start"]["dateTime"], format_single_day_time)
                self.end = datetime.datetime.strptime(event_dict["end"]["dateTime"], format_single_day_time)
                self.all_day = False
            else:
                raise KeyError("Your event_dict does not seem to have a valid time marker; please check it.")

        except Exception as e:
            print(event_dict)
            raise e

        self.same_day = self.start.day == self.end.day

        self.heading = event_dict["summary"]

        if "description" in event_dict.keys():
            self.text = event_dict["description"]
        else:
            self.text = None

        if "location" in event_dict.keys():
            self.location = event_dict["location"]
        else:
            self.location = None

        self.times = [self.get_time_string()]

    def __str__(self):
        result = ""
        if self.heading is not None:
            result += "## " + self.heading + "\n\n"

        time_str = self.get_time_string()
        if len(self.times) > 1:
            result += "#### Times\n\n"
            for occurence in self.times:
                result += occurence

        elif time_str is not None:
            result += mdutils.b("Time: ") + time_str

        if self.location is not None:
            result += mdutils.b("Location: ") + str(self.location) + "\n\n"

        if self.text is not None:
            result += self.text

        return result

    def get_time_string(self):
        if self.same_day:
            if self.all_day:
                time = self.start.strftime("%A, %B %dth all day")
            else:
                time = self.start.strftime("%A, %B %dth from %I:%M %p") + self.end.strftime(" to %I:%M %p")
        else:
            if self.all_day:
                time = self.start.strftime("%A, %B %dth to ") + self.end.strftime("%A, %B %dth")
            else:
                time = self.start.strftime("%A, %B %dth from %I:%M %p") + self.end.strftime(
                    " to %A, %B %dth at %I:%M %p")
        if time is not None:
            return str(time) + "\n\n"
        return None

    def add_similar_event(self, other):
        if type(other) == Event:
            self.times.append(other.get_time_string())
            return self
        else:
            raise ValueError("You tried to add an Event to something that was not an event")

    def __add__(self, other):
        return self.add_similar_event(other)


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
