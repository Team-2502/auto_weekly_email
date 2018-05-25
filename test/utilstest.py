import unittest

from autoweeklyemail.utils import get_captains, Captain, Event


def fun(x):
    return x + 1


class UtilsTest(unittest.TestCase):
    def test_get_captains(self):
        captains = get_captains()
        self.assertGreater(len(captains), 0)

    def test_captains_tostr(self):
        captain = Captain("Grant", "grant@yahoo.com", "(555) 555-5555")
        self.assertEqual(str(captain), "Grant: [grant@yahoo.com](mailto:grant@yahoo.com), (555) 555-5555")


class EventTest(unittest.TestCase):
    def setUp(self):
        self.all_event_dicts = [
            {'location': 'Town Name High School, 1234 Street St, Small Town, MN, USA',
             'end': {'dateTime': '2018-05-29T20:00:00-05:00'}, 'summary': 'End of the Year Banquet',
             'start': {'dateTime': '2018-05-29T18:00:00-05:00'}},
            {'originalStartTime': {'timeZone': 'America/Chicago', 'dateTime': '2018-06-01T21:00:00-05:00'},
             'location': 'Restaurant Establishment, 5678 Road Blvd, Small Town, MN, USA',
             'description': 'This is where team members get to together, hang out, and eat ice cream. There is not necessarily a mentor present at this event.',
             'end': {'timeZone': 'America/Chicago', 'dateTime': '2018-06-01T22:30:00-05:00'}, 'summary': 'DQ Social',
             'start': {'timeZone': 'America/Chicago', 'dateTime': '2018-06-01T21:00:00-05:00'}}]

        self.all_event_objs = [Event(event) for event in self.all_event_dicts]

    def test_get_time_string(self):
        self.assertEqual("Tuesday, May 29th from 06:00 PM to 08:00 PM",
                         self.all_event_objs[0].get_time_string().strip())
        self.assertEqual("Friday, June 01th from 09:00 PM to 10:30 PM",
                         self.all_event_objs[1].get_time_string().strip())

    def test_str(self):
        expected_str_first = "## End of the Year Banquet\n\n" \
                             "**Location: **Town Name High School, 1234 Street St, Small Town, MN, USA\n\n"
        actual_str_first = str(self.all_event_objs[0])

        expected_str_second = "## DQ Social\n\n" \
                              "**Location: **Restaurant Establishment, 5678 Road Blvd, Small Town, MN, USA\n\n" \
                              "This is where team members get to together, hang out, and eat ice cream. There is not necessarily a mentor present at this event."
        actual_str_second = str(self.all_event_objs[1])
        print(actual_str_first)
        self.assertEqual(expected_str_first.strip(), actual_str_first.strip())
        self.assertEqual(expected_str_second.strip(), actual_str_second.strip())

    def test_add_similar_event(self):
        og_icecream_social_obj = Event(self.all_event_dicts[1])

        another_icecream_social_dict = {
            'originalStartTime': {'timeZone': 'America/Chicago', 'dateTime': '2018-06-01T21:00:00-05:00'},
            'location': 'Restaurant Establishment, 5678 Road Blvd, Small Town, MN, USA',
            'description': 'This is where team members get to together, hang out, and eat ice cream. There is not necessarily a mentor present at this event.',
            'end': {'timeZone': 'America/Chicago', 'dateTime': '2018-06-08T22:30:00-05:00'}, 'summary': 'DQ Social',
            'start': {'timeZone': 'America/Chicago', 'dateTime': '2018-06-08T21:00:00-05:00'}}

        another_icecream_social_obj = Event(another_icecream_social_dict)

        og_icecream_social_obj.add_similar_event(another_icecream_social_obj)

        expected_str = "## DQ Social\n\n" \
                       "**Location: **Restaurant Establishment, 5678 Road Blvd, Small Town, MN, USA\n\n" \
                       "This is where team members get to together, hang out, and eat ice cream. There is not necessarily a mentor present at this event.\n\n"

        self.assertEqual(expected_str.strip(), str(og_icecream_social_obj).strip())


if __name__ == '__main__':
    unittest.main()
