# auto_weekly_email

Our team sends out a weekly email that describes what will be happening during the week (e.g when the workshop will be open,
when different subteam meetings are, fundraising opportunities, etc) in addition to communicating essential information to the
team (e.g registration for X competition is due by Y date!). In order to make the lives of our captains (the people who write
the emails) easier, we have automated the process of gathering events. We do so using the Google Calendar API, since our captains
also maintain a team calendar.


### It doesn't work!

You need to download `client-secret.json` from the Google Developers Console. You will need to log into `info@team2502.com` with
the password ;). It will go in the root folder. Then, the first time you run this, you will be asked to authenticate or something like that.
Select `info@team2502.com` in order for the calendar to be set properly.

You will also need to have a captains.json file in your root folder for the email signature to work. It must be formatted as follows:

```
[
  {
    "name": "my favorite captain"
    "email": "nice.person@team2502.com",
    "phone_num": "(123) 123-123"
  },
  {
    "name": "another captian",
    "email": "capncrunch@team2502.com",
    "phone_num": "(555) 666-7777"
  },
  {
    "name": "the robot",
    "email": "captains@team2502.com",
    "phone_num": ""
  }
]

```

You can have as many entries for captain as you like; however, you really only should have one per human captain and one for the robot.
