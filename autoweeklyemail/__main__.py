import mistune

import calendarutils
import utils

if __name__ == '__main__':
    events = calendarutils.get_weeks_events(False, -7)

    email = utils.WeeklyEmail()

    for event in events:
        try:
            email.sections.append(utils.WeeklyEmailSection(heading=event["summary"], text=event["description"]))
        except KeyError:
            email.sections.append(
                utils.WeeklyEmailSection(heading=event["summary"], text=None))

    email.sections.append(utils.gen_signature())
    compiled_email = email.compile()
    print(compiled_email)
    with open("weekly_email.html", "w") as f:
        f.write(mistune.markdown(compiled_email))