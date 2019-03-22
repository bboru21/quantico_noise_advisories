#!/bin/sh

MAILTO=""

source virtualenv/bin/activate
python get_advisories.py --settings=settings_local