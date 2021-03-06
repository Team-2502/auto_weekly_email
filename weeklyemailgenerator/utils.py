import datetime
import json
from dateutil.parser import isoparse
import os
from typing import List

import mistune

from weeklyemailgenerator.mdutils import emailLink
from weeklyemailgenerator import calendarutils
from weeklyemailgenerator import mdutils


class WeeklyEmail:
    SEPARATOR = "---"

    def __init__(self):
        self.sections = []
        self.header = ""

    def compile(self):
        return str(self.header).strip() + "\n\n" + \
               self._gen_overview() + "\n\n" + \
               ("\n\n" + WeeklyEmail.SEPARATOR + "\n\n").join(str(section) for section in self.sections)

    def _gen_overview(self):
        result = ""
        if len(self.sections) > 0:
            result = "## Schedule\n\n"
        for section in self.sections:
            if type(section) == Event:
                result += mdutils.b(section.heading)
                result += ": "
                for i, time in enumerate(section.times):
                    if len(section.times) > 1:
                        result += "\n\n - "
                    result += time
                    result += "\n\n"
        return result + WeeklyEmail.SEPARATOR

    def to_html(self):
        return mistune.markdown(self.compile())

    @staticmethod
    def get_n_spaces(n):
        return "".join(" " for _ in range(n))

    def __str__(self):
        return self.compile()


class Event:

    def __init__(self, event_dict):
        try:
            if "date" in event_dict["start"].keys():
                format_multi_day_time = "%Y-%m-%d"
                self.start = datetime.datetime.strptime(event_dict["start"]["date"], format_multi_day_time)
                self.end = datetime.datetime.strptime(event_dict["end"]["date"], format_multi_day_time)
                self.all_day = True
            elif "dateTime" in event_dict["start"].keys():
                self.start = isoparse(event_dict["start"]["dateTime"])
                self.end = isoparse(event_dict["end"]["dateTime"])
                self.all_day = False
            else:
                raise KeyError("Your event_dict does not seem to have a valid time marker; please check it.")

        except Exception as e:
            print(event_dict)
            raise e

        self.same_day = self.start.day == self.end.day or (self.end - self.start).days == 1

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
            self.times.extend(other.times)
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

    def _try_to_load_json_file(filename):
        filenames = [filename, "../" + filename]

        ret_json = None
        for fname in filenames:
            try:
                with open(fname) as f:
                    ret_json = json.load(f)
            except FileNotFoundError:
                pass

        if ret_json is not None:
            return ret_json
        else:
            raise FileNotFoundError

    try:
        if len(CAPTAINS) == 0:
            captains_json = None
            try:
                with open("../captains.json") as f:
                    captains_json = json.load(f)
            except FileNotFoundError:
                with open("captains.json") as f:
                    captains_json = json.load(f)

            for captain_dict in captains_json:
                CAPTAINS.append(Captain(captain_dict["name"], captain_dict["email"], captain_dict["phone_num"]))

        return CAPTAINS

    except FileNotFoundError:
        print("WARN: Could not find `captains.json`. Using sample captains list!\n")
        with open("../sample_captains.json") as f:
            captains_json = json.load(f)
        for captain_dict in captains_json:
            CAPTAINS.append(Captain(captain_dict["name"], captain_dict["email"], captain_dict["phone_num"]))
        return CAPTAINS


def gen_signature(captains: List[str] = None):
    """
    Generate a weekly email signature given a complete list of captains
    :param captains: List of Captains
    :return: A markdown-formatted email signature
    """
    result = ""
    if captains is None:
        captains = get_captains()
    for captain in captains:
        result += str(captain) + "\n\n\n"
    return result


def generate_email(days_in_past=0):
    """
    Generate the weekly email as an HTML File
    :param days_in_past: How many days ago we should pretend we are (adjusts for which week the email is for)
    :return: The absolute path to the HTML File
    """
    print("DEBUG: Started generate_email")

    monday, sunday, events = calendarutils.get_weeks_events(False, -days_in_past)

    header_format_string = "%B %dth"

    monday_text = monday.strftime(header_format_string)
    sunday_text = sunday.strftime(header_format_string)

    print("DEBUG: Figured out the dates of the email")
    email = WeeklyEmail()
    print("DEBUG: Constructed a WeeklyEmail()")

    open_room_times = None
    regular_events = []

    for event_dict in events:
        event_obj = Event(event_dict)
        print("DEBUG: Found an event -- {}".format(event_obj.heading.lower()))
        if event_obj.heading.lower() == "Captains Meeting".lower():
            continue  # Team does not need to know
        if event_dict["summary"].lower().find("open") > -1 and event_dict["summary"].lower().find("room") > -1:
            if open_room_times is None:
                open_room_times = event_obj
            else:
                open_room_times += event_obj
        else:
            found_similar_event = False
            for i, other_event_obj in enumerate(regular_events):
                if other_event_obj.heading.lower() == event_obj.heading.lower():
                    print("I have a duplicate event! Name:", event_obj.heading)
                    found_similar_event = True
                    break
            if found_similar_event:
                regular_events[i] += event_obj
            else:
                regular_events.append(event_obj)

    print("DEBUG: Finished iterating through events")

    email.header = "# " + monday_text + " to " + sunday_text
    if open_room_times is not None:
        email.sections.append(open_room_times)
    else:
        email.sections.append("### No open room scheduled for this week as of now.")

    print("DEBUG: Determined if there was open room this week")

    email.sections.extend(regular_events)
    email.sections.append(gen_signature())
    compiled_email = email.compile()

    print("DEBUG: Completed the email!")
    return mistune.markdown(compiled_email)
    # with open("weekly_email.html", "w") as f:
    #     f.write(mistune.markdown(compiled_email))
    #     f.close()
    #
    # return os.path.abspath("./weekly_email.html")
