import os
import webbrowser

import mistune

import calendarutils
import utils

if __name__ == '__main__':
    monday, sunday, events = calendarutils.get_weeks_events(False, -7)

    header_format_string = "%B %dth"

    monday_text = monday.strftime(header_format_string)
    sunday_text = sunday.strftime(header_format_string)

    email = utils.WeeklyEmail()

    open_room_times = None
    regular_events = []

    for event_dict in events:
        event_obj = utils.Event(event_dict)
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

    email.header = "# " + monday_text + " to " + sunday_text
    if open_room_times is not None:
        email.sections.append(open_room_times)
    else:
        email.sections.append("### No open room scheduled for this week as of now.")
    email.sections.extend(regular_events)
    email.sections.append(utils.gen_signature())
    compiled_email = email.compile()

    with open("weekly_email.html", "w") as f:
        f.write(mistune.markdown(compiled_email))
        f.close()

    webbrowser.open("file://" + os.path.abspath("./weekly_email.html"))
