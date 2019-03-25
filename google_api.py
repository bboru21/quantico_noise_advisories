# from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
import re
from base64 import b32encode

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

    def format_event_id(self, eventId):
        # base32hex encoding, lowercase letters a-v and digits 0-9
        encoded_string = b32encode(eventId)
        return re.sub(r'[^a-v0-9]', '', encoded_string.lower())

    def get_event(self, eventId):
        event = None
        try:
            event = self.service.events().get(calendarId=settings.GOOGLE_CALENDAR_ID, eventId=eventId).execute()
        except HttpError, error:
            # print error
            pass
        return event

    def delete_event(self, eventId):
        self.service.events().delete(calendarId=settings.GOOGLE_CALENDAR_ID, eventId=eventId).execute()
        return None

    def patch_event(self, eventId, body):
        return self.service.events().patch(calendarId=settings.GOOGLE_CALENDAR_ID, eventId=eventId, body=body).execute()

    def add_event(self, start, end, description, eventId):

        eventId = self.format_event_id(eventId)

        # check if event already exists
        event = self.get_event(eventId)

        if event:
            return 'advisory already exists from %s to %s' % (start.strftime("%m/%d/%Y %H:%M"), end.strftime("%m/%d/%Y %H:%M"))
        else:
            body = {
                'id': eventId,
                'summary': 'Quantico Noise Advisory',
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
                'reminders': settings.REMINDERS,
            }
            event = self.service.events().insert(calendarId=settings.GOOGLE_CALENDAR_ID, body=body).execute()
            return 'advisory added from %s to %s' % (start.strftime("%m/%d/%Y %H:%M"), end.strftime("%m/%d/%Y %H:%M"))

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
