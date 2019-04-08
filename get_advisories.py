# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import json
import requests
import re
import datetime
import dateparser

from send_email import send_email

from google_api import (
    GoogleCalendarAPI
)

API = GoogleCalendarAPI()

def get_event_id(start, end, description):
    return "qna-{}{}{}".format( re.sub(r'\W','',description), start.strftime("%Y%m%d%H%M%S"), end.strftime("%Y%m%d%H%M%S") )

MONTH_DAY_PATTERN = re.compile(
    r'(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\D+\d{1,2}',
    flags=re.IGNORECASE,
)
TIME_PATTERN = r'\d{1,2}(:\d{1,2})?\W+(am|a\.m\.|pm|p\.m\.)'
TIME_RANGE_PATTERN = re.compile(
    r'{0}\Wto\W{0}'.format(TIME_PATTERN),
    flags=re.IGNORECASE,
)

def prepare_string(string):
    string = re.sub(r'[^a-z0-9:\/\-\.\s]', ' ', string, flags=re.IGNORECASE)
    string = ' '.join(string.split())
    string = re.sub(r'\snoon\s', ' 12 pm ', string, flags=re.IGNORECASE)
    string = re.sub(r'\smidnight\s', ' 11:59 pm ', string, flags=re.IGNORECASE)
    return string


def parse_event(_string, previous_month_day):

    start = None
    end = None
    description = None

    string = prepare_string(_string)

    # pase month and day
    match = re.search(MONTH_DAY_PATTERN, string)
    if match:
        month_day = match.group(0)
    elif previous_month_day:
        month_day = previous_month_day

    # parse time range

    time_range = re.search(TIME_RANGE_PATTERN, string).group(0)
    start_time, end_time = [ t.strip() for t in time_range.split('to') ]

    # use dateparser package to translate flexible date format
    start = dateparser.parse('{} {}'.format(month_day, start_time))
    end = dateparser.parse('{} {}'.format(month_day, end_time))

    # parse description
    _description = string
    _description = re.sub(MONTH_DAY_PATTERN, '', _description)
    _description = re.sub(TIME_RANGE_PATTERN, '', _description)
    _description = re.sub(r'[^a-z0-9\/\-\.\s]', '', _description, flags=re.IGNORECASE)
    description = _description.strip()

    if len(description) < 2:
        description = "Very loud noise and noticeable ground vibrations may occur in the surrounding areas."

    eventId = get_event_id(start, end, description)

    return (start, end, description, eventId)


def get_advisories():

    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'}

    url = 'https://www.quantico.marines.mil/Advisories/Noise-Advisories/'

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    soup = soup.find("div", class_="livehtml")

    p = soup.find(text=re.compile('^Very loud noise')).parent.find_next('p')

    events = p.get_text().splitlines()

    previous_month_day = None

    for event_string in events:
        start, end, description, eventId = parse_event(event_string, previous_month_day)
        previous_month_day = start.strftime("%B %d")
        result_message = API.add_event(start, end, description, eventId)
        print '\t* %s' % result_message

try:
    print '%s advisory script started...' % (datetime.datetime.now())
    get_advisories()
except BaseException, error:
    print 'ERROR: %s' % error.message
    send_email(error.message)

print '%s advisory script complete' % (datetime.datetime.now())
