# Quantico Noise Advisories
Script for scraping the Quantico Noise Advisories, and adding them to your Google Calendar.

## Installation
Run bash script to build Virtual Environment, install python packages and create local settings file:

`sh setup.sh`

## Setup Google Calendar API
https://developers.google.com/calendar/quickstart/python
Place credentials.json within the root directory.
Install Google Client Library:
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

## Running the Script

### Activate virtualenv:

`source virtualenv/bin/activate`

### Run Script:

`python get_advisories.py --settings=settings_local`
