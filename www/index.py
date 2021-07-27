#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

from modules import (
    nextRing,
    webPageFooter,
    webPageHeader,
    db_connect,
    db_create_cursor,
    db_close_cursor,
    db_disconnect,
    db_query,
    bellRelayGpio,
    displayOnLCD,
)
from time import sleep
from datetime import datetime
import cgi
import cgitb

cgitb.enable()  # for troubleshooting


try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!")


ringSchoolBell = False

verbose = False

fs = cgi.FieldStorage()

print("Content-type: text/html")

print("""
<html>
<head><title>School Bell</title></head>
<body>
<h3>School Bell</h3>
""")

for key in fs.keys():
    if (key == "ringSchoolBell" and fs[key].value == "1"):
        ringSchoolBell = True

if ringSchoolBell:
    bellRelayState = False
    LCDMessage = "Ringing Bell......"
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(bellRelayGpio, GPIO.OUT, initial=GPIO.LOW)
    displayOnLCD("", LCDMessage, verbose)
    bellRelayState = True
    GPIO.output(bellRelayGpio, bellRelayState)
    sleep(1)
    GPIO.output(bellRelayGpio, False)
    GPIO.cleanup(bellRelayGpio)
    LCDMessage = ""
    displayOnLCD("", LCDMessage, verbose)

# connect to database
cnx = db_connect(verbose)

# create cursor
cursor = db_create_cursor(cnx, verbose)

# get current time
dateTimeNow = datetime.now()

dateNow = dateTimeNow.strftime("%Y-%m-%d")

timeNow = dateTimeNow.strftime("%H:%M")


def pageLinks():

    print('<a href="index.py?ringSchoolBell=1"><strong>RING THE BELL</strong></a>'
        + '\n<br>\n<br>\n<br><a href="ringTimes.py">Times</a>'
        + "\n<br>"
        + '\n<br><a href="schoolBreaks.py">Breaks</a>'
        + "\n<br>"
        + '\n<br><a href="ringPatterns.py">Patterns</a>'
        + "\n<br>"
        + '\n<br><a href="status.py">Status</a>'
        + '\n<br>')


def pageFooter():
    webPageFooter


def pageBody():

    # find next time for ring
    (
        nextRingDay,
        nextRingDate,
        nextRingTime,
        ringTimeName,
        ringPatternName,
        ringPattern,
    ) = nextRing(cursor, dateNow, timeNow, verbose)
    nextRingDate = datetime.strftime(nextRingDate, "%Y-%m-%d")

    print("\n<br>Current date and Time"
        + "\n<br>&emsp;%s \n<br>&emsp;%s" % (dateNow, timeNow)
        + "\n<br>"
        + "\n<br>Next bell:"
        + "\n<br>&emsp;%s, %s" % (nextRingDate, nextRingDay)
        + "\n<br>&emsp;&emsp;%s, %s" % (nextRingTime, ringTimeName)
        + "\n<br>")


if __name__ == "__main__":
    webPageHeader()
    pageLinks()
    pageBody()
    webPageFooter()

# close cursor
db_close_cursor(cnx, cursor, verbose)

# close db
db_disconnect(cnx, verbose)

print("""
</body>
</html>
""")
