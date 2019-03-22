GOOGLE_CALENDAR_ID = "primary"
TIME_ZONE = "America/New_York"
SCOPES = [
    "https://www.googleapis.com/auth/calendar", # read/write access to Calendars
]

REMINDERS = {
    'useDefault': False,
    'overrides': [
        {'method': 'email', 'minutes': 24 * 60},
    ],
}

'''
REMINDERS = { # Information about the event's reminders for the authenticated user.
    "overrides": [ # If the event doesn't use the default reminders, this lists the reminders specific to the event, or, if not set, indicates that no reminders are set for this event. The maximum number of override reminders is 5.
        {
            "minutes": 24*60, # Number of minutes before the start of the event when the reminder should trigger. Valid values are between 0 and 40320 (4 weeks in minutes).
            # Required when adding a reminder.
            "method": "A String", # The method used by this reminder. Possible values are:
            # - "email" - Reminders are sent via email.
            # - "sms" - Deprecated. Once this feature is shutdown, the API will no longer return reminders using this method. Any newly added SMS reminders will be ignored. See  Google Calendar SMS notifications to be removed for more information.
            # Reminders are sent via SMS. These are only available for G Suite customers. Requests to set SMS reminders for other account types are ignored.
            # - "popup" - Reminders are sent via a UI popup.
            # Required when adding a reminder.
        },
    ],
},
'''

# Add correct values to settings_local.py if you wish to receive an e-mail on script failure
SEND_EMAIL = False          # set to True to send e-mail
SENDER_EMAIL = None         # e.g. 'youraddress@gmail.com'
SENDER_EMAIL_HOST = None    # e.g. 'smtp.gmail.com'
SENDER_EMAIL_PORT = None    # e.g. 465
SENDER_PASSWORD = None
RECIPIENT_EMAIL = None      # e.g. 'youraddress@notgmail.com'
