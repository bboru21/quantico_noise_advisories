# Quantico Noise Advisories
Script for scraping the Quantico Noise Advisories, and adding them to your Google Calendar.

## Installation
Run bash script to build Virtual Environment, install python packages and create local settings file:

`sh setup.sh`

## Setup Google Calendar API
Follow Google's directions for usage of their Calendar API: https://developers.google.com/calendar/quickstart/python

Place `credentials.json` within the root directory. Don't worry about it showing up in version control, as all of Google's files should be ignored by .git.

Google Client python packages should already have been installed via `setup.sh`, so you should not have to install them again.

Once the process is complete, delete the `token.pickel` file found within the root directory. The boilerplate `GoogleCalendarAPI` class will recreate one with correct scopes for read/write Calendar priveledges.

## Running the Script

### Activate virtualenv:

`source virtualenv/bin/activate`

### Run Script:

`python get_advisories.py --settings=settings_local`
