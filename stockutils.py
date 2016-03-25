#!/usr/bin/python

"""Utility functions"""
import datetime
import unittest

import configdb

DB_FILE="db/holdings.db"
timeFormat = fmt="%Y-%m-%d %H:%M:%S"

#Helper for messing with timezones
def parseOffset(offset):
    hours = int(offset[0:3])
    minutes = int(offset[3:])
    return datetime.timedelta(hours=hours, minutes=minutes)

def toUTC(time, offset):
    return time - parseOffset(offset)

def nowUTC():
    offset = configdb.getConfig('server_utcoffset')
    now_utc=toUTC(datetime.datetime.now(), offset)
    return now_utc.strftime(timeFormat)

class TestUtils(unittest.TestCase):
    def testNowUTC(self):
        print nowUTC()

if __name__=="__main__":
    unittest.main()
