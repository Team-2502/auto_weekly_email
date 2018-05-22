from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

# Setup the Calendar API

# Authentication scope
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

# Where our OAuth2 Tokens are stored
store = file.Storage('credentials.json')

# Load em
creds = store.get()

# If they're old / don't exist
if not creds or creds.invalid:
    # Get some
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)

# Set up our API caller thing
service = build('calendar', 'v3', http=creds.authorize(Http()))


def get_weeks_events(this_week=True, days_in_future=7):
    # Get current time
    now = None
    if this_week:
        now = datetime.datetime.now()
    else:
        now = datetime.datetime.now() + datetime.timedelta(days=days_in_future)
    days_ago = datetime.datetime.utcnow().isoweekday() - 1
    time_delta_to_monday = datetime.timedelta(days=days_ago, hours=now.hour, minutes=now.minute)
    time_delta_to_sunday = datetime.timedelta(days=6 - days_ago, hours=24 - now.hour, minutes=60 - now.minute)

    monday = now - time_delta_to_monday
    sunday = now + time_delta_to_sunday

    # Call calendar/v3/calendars/calendarId/events
    events_result = service.events().list(calendarId='primary', timeMin=monday.isoformat() + 'Z',
                                          timeMax=sunday.isoformat() + 'Z', singleEvents=True,
                                          orderBy='startTime').execute()
    return events_result.get('items', [])


if __name__ == '__main__':
    get_weeks_events()
