#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

from modules import (
    nextRing,
    webPageFooter,
    webPageHeader,
    pageNav,
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

for key in fs.keys():
    if (key == "ringSchoolBell" and fs[key].value == "1"):
        ringSchoolBell = True

if ringSchoolBell:
    LCDMessage = "Ringing Bell......"
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(bellRelayGpio, GPIO.OUT, initial=GPIO.LOW)
    displayOnLCD("", LCDMessage, verbose)
    GPIO.output(bellRelayGpio, True)
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

    print('<div class="bellButton"><a href="index.py?ringSchoolBell=1" class="mybutton"><strong>RING THE BELL</strong></a></div>')


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

    print("\nNext bell:"
        + "\n<br>&emsp;%s, %s" % (nextRingDate, nextRingDay)
        + "\n<br>&emsp;&emsp;%s, %s" % (nextRingTime, ringTimeName)
        + "\n<br>")

if __name__ == "__main__":
    webPageHeader()
    pageNav()
    pageLinks()
    pageBody()
    webPageFooter()

# close cursor
db_close_cursor(cnx, cursor, verbose)

# close db
db_disconnect(cnx, verbose)