import mistune

import calendarutils
import utils

if __name__ == '__main__':
    events = calendarutils.get_weeks_events(False, -7)

    email = utils.WeeklyEmail()

    open_room_times = None
    regular_events = []

    for event in events:
        if event["summary"].lower().find("open") > -1 and event["summary"].lower().find("room") > -1:
            if open_room_times is None:
                open_room_times = utils.Event(event)
            else:
                open_room_times += utils.Event(event)
        else:
            regular_events.append(utils.Event(event))

    email.sections.append(open_room_times)
    email.sections.extend(regular_events)
    email.sections.append(utils.gen_signature())
    compiled_email = email.compile()
    print(compiled_email)
    with open("weekly_email.html", "w") as f:
        f.write(mistune.markdown(compiled_email))
        f.close()
