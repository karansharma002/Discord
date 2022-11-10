# DATETIME TO SECONDS / MINUTES / HOURS CONVERTER
# SOFIA 24 JUNE 2020

import datetime
from dateutil import parser

def date_sec(val):
	t3 = parser.parse(str(val))
	t4 = parser.parse(str(datetime.datetime.now()))
	c = t3 - t4
	d = round(c.total_seconds())
	return d

def date_min(val):
	t3 = parser.parse(str(val))
	t4 = parser.parse(str(datetime.datetime.now()))
	c = t3 - t4
	d = d = round(c.total_seconds() / 60)
	return d

def date_hour(val):
	t3 = parser.parse(str(val))
	t4 = parser.parse(str(datetime.datetime.now()))
	c = t3 - t4
	d = d = round(c.total_seconds() / 3600)
	return d