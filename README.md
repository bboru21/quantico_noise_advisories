# Quantico Noise Advisories
Script for scraping the Quantico Noise Advisories, and adding them to your Google Calendar.

## Installation
Run bash script to build Virtual Environment, install python packages and create local settings file:

`sh setup.sh`

## Setup Google Calendar API
Follow Google's directions for usage of their Calendar API: https://developers.google.com/calendar/quickstart/python

Place `credentials.json` within the root directory. Don't worry about it showing up in version control, as all of Google's files should be ignored by .git.

Google Client python packages should already have been installed via `setup.sh`, so you should not have to install them again.

Once the process is complete, delete the `token.pickel` file found within the root directory. The `get_advisories.py` script will recreate one with correct scopes for read/write Calendar priveledges.

## Setup Local Settings
This script utilizes a local settings file `settings_local.py` which is ignored by git. This file imports all values from the base settings file `settings_base.py`. If you wish to override any of these base settings (such as `GOOGLE_CALENDAR_ID` whose default value is "primary") you may do so within the `settings_local.py` file.

## Running the Script

### Activate virtualenv:

`source virtualenv/bin/activate`

### Run Script:

`python get_advisories.py --settings=settings_local`
