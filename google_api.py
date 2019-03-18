# from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import os
from simple_settings import settings

class GoogleCalendarAPI(object):

    service = None

    def __init__(self):

        creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', settings.SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)

    def add_event(self, start, end, description):

        event = {
            'location': 'Quantico Military Base, Quantico Virginia',
            'description': description,
            'start': {
                'dateTime': start.strftime("%Y-%m-%dT%H:%M:%S"), # '2015-05-28T17:00:00-07:00'
                'timeZone': settings.TIME_ZONE,
            },
            'end': {
                'dateTime': end.strftime("%Y-%m-%dT%H:%M:%S"), # '2015-05-28T17:00:00-07:00'
                'timeZone': settings.TIME_ZONE,
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                ],
            },
        }

        event = self.service.events().insert(calendarId=settings.GOOGLE_CALENDAR_ID, body=event).execute()

        return event

    def get_events(self, max_results=10):
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        events_result = self.service.events().list(calendarId=settings.GOOGLE_CALENDAR_ID, timeMin=now,
                                        maxResults=max_results, singleEvents=True,
                                        orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events

    def get_calendars(self):
        result = self.service.calendarList().list().execute()
        calendars = result.get('items', [])
        return calendars
