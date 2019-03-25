from bs4 import BeautifulSoup
import json
import requests
import re
import datetime

from send_email import send_email

from google_api import (
    GoogleCalendarAPI
)

API = GoogleCalendarAPI()

def get_event_id(start, end):
    return "quantico-noise-advisory-{}{}".format( start.strftime("%Y%m%d%H%M%S"), end.strftime("%Y%m%d%H%M%S") )

def parse_event(event):
    event = event.split(' - ')
    month_day = event[0].split(' ')
    month = month_day[0].replace('.', '')
    day = month_day[1].zfill(2)
    year = datetime.datetime.now().year

    def _get_time(string):
        hour_period = string.split(' ')
        hour = hour_period[0].zfill(2)

        period = re.sub( r'[^APM]+', '', hour_period[1].upper() )

        return (hour, period)

    time_range = event[1].split(' to ')
    start_hour, start_period = _get_time(time_range[0])

    end_hour, end_period = _get_time(time_range[1])

    start = datetime.datetime.strptime("{} {} {} {} {}".format(month, day, year, start_hour, start_period), "%b %d %Y %I %p")
    end = datetime.datetime.strptime("{} {} {} {} {}".format(month, day, year, end_hour, end_period), "%b %d %Y %I %p")

    description = event[2] if len(event) > 2 else "Very loud noise and noticeable ground vibrations may occur in the surrounding areas."

    eventId = get_event_id(start, end)

    return (start, end, description, eventId)

def get_advisories():

    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'}

    url = 'https://www.quantico.marines.mil/Advisories/Noise-Advisories/'

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    soup = soup.find("div", class_="livehtml")

    p = soup.find(text=re.compile('^Very loud noise')).parent.find_next('p')

    events = p.get_text().splitlines()

    for event in events:
        start, end, description, eventId = parse_event(event)
        result_message = API.add_event(start, end, description, eventId)
        print '\t* %s' % result_message

try:
    print '%s advisory script started...' % (datetime.datetime.now())
    get_advisories()
except BaseException, error:
    print 'ERROR: %s' % error.message
    send_email(error.message)

print '%s advisory script complete' % (datetime.datetime.now())
