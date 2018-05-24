import webbrowser

import mistune
import os

import calendarutils
import utils

if __name__ == '__main__':
    events = calendarutils.get_weeks_events(False, 35)

    email = utils.WeeklyEmail()

    openroomtimes = []

    for event in events:
        email.sections.append(utils.Event(event))

    email.sections.append(utils.gen_signature())
    compiled_email = email.compile()
    print(compiled_email)
    with open("weekly_email.html", "w") as f:
        f.write(mistune.markdown(compiled_email))
        f.close()
