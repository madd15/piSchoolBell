#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import os
import sys
import socket
from modules import (
    nextRing,
    getUptime,
    isRingDay,
    findRingTimes,
    webPageFooter,
    webPageHeader,
    pageNav,
    countEntriesInDatabase,
    db_connect,
    db_create_cursor,
    db_close_cursor,
    db_disconnect,
    db_query,
)
import netifaces as ni
from datetime import datetime, timedelta
import cgi
import cgitb

cgitb.enable()  # for troubleshooting

verbose = False

# connect to database
cnx = db_connect(verbose)

# create cursor
cursor = db_create_cursor(cnx, verbose)

# get current time
dateTimeNow = datetime.now()

dateNow = dateTimeNow.strftime("%Y-%m-%d")

timeNow = dateTimeNow.strftime("%H:%M")

weekNumberNow = datetime.strptime(dateNow, "%Y-%m-%d").strftime("%W")

dayNumberNow = int(datetime.strptime(dateNow, "%Y-%m-%d").strftime("%w")) - 1
if dayNumberNow == -1:
    dayNumberNow = 6


def countRingTimes(iMax):
    ringCount = 0
    schoolDayCount = 0

    date = dateNow

    oldWeekNumber = 0

    i = 0

    while True:
        isWorkDay, isNotOnBreak, weekNumber, dayNumber, breakName = isRingDay(
            date, oldWeekNumber, cursor, verbose
        )

        if isNotOnBreak or isWorkDay:
            schoolDayCount += 1

        if isNotOnBreak:
            ringTimes = findRingTimes(date, dayNumber, cursor, verbose)
            if ringTimes:
                for ringTime in ringTimes:
                    ringCount += 1

        i += 1

        if i >= iMax:
            break
        else:
            # convert to time object
            date = datetime.strptime(date, "%Y-%m-%d")
            date = date + timedelta(days=1)  # add one day
            date = datetime.strftime(date, "%Y-%m-%d")  # convert to string

    return ringCount, schoolDayCount


def pageLinks():

    print ('\n<br><a href="displayLogs.py">Log files</a>')

def pageBody():

    print ("\n<br>")

    # time and date
    print(
        "\n<br>Date: \n<br>&nbsp;&nbsp;&nbsp;&nbsp;%s "
        "\n<br>Time: \n<br>&nbsp;&nbsp;&nbsp;&nbsp;%s "
        "\n<br>\n<br>Week number: \n<br>&nbsp;&nbsp;&nbsp;&nbsp;%s "
        "\n<br>Day number: \n<br>&nbsp;&nbsp;&nbsp;&nbsp;%s "
        % (dateNow, timeNow, weekNumberNow, dayNumberNow)
    )

    # uptime
    uptimeSeconds = getUptime()
    uptime = str(timedelta(seconds=uptimeSeconds))

    print ("\n<br>"
        + "\n<br>Uptime: \n<br>&nbsp;&nbsp;&nbsp;&nbsp;%s" % uptime
        + "\n<br>"
        + "\n<br>Database:")

    for tableName in ("ringTimes", "breaks", "ringPatterns"):
        entries = countEntriesInDatabase(tableName, cursor, verbose)
        if entries:
            print ("\n<br>&nbsp;&nbsp;&nbsp;&nbsp%s entries: %s" % (tableName, entries))
        else:
            print ("\n<br>&nbsp;&nbsp;&nbsp;&nbspError retriveing %s" % tableName)

    print ("\n<br>")

    # last break
    query = "SELECT endDate FROM breaks ORDER BY endDate DESC LIMIT 1"
    result, rowCount = db_query(cursor, query, verbose)  # run query
    if rowCount:
        for row in result:
            lastBreakEnds = row[0]
        print ("\n<br>&nbsp;&nbsp;&nbsp;&nbspLast break ends: %s" % lastBreakEnds)
    else:
        print ("\n<br>&nbsp;&nbsp;&nbsp;&nbspError retrieving last break: No breaks in database")
    print ("\n<br>")

    # system
    print ("\n<br>"
        + "\n<br>System:"
        + "\n<br>&nbsp;&nbsp;&nbsp;&nbspHostname: %s" % socket.gethostname())

    # ip info
    # find this devices ip address
    interfaceIPs = []
    interfaces = ni.interfaces()
    print ("\n<br>"
        + "\n<br>&nbsp;&nbsp;&nbsp;&nbspNet interfaces with IP:")
    i = 0
    for interface in interfaces:
        try:
            ip = ni.ifaddresses(interface)[ni.AF_INET][0]["addr"]
        except:
            ip = "No IP assigned"
        interfaceIPs.append({"interface%s" % i: interface, "ip%s" % i: ip})
        i += 1
    i = 0
    for interfaceIP in interfaceIPs:
        if (
            not interfaceIP["ip%s" % i].startswith("127")
            and not interfaceIP["ip%s" % i].startswith("169")
            and not interfaceIP["ip%s" % i] == "NA"
        ):
            print(
                "\n<br>&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp%s: %s"
                % (interfaceIP["interface%s" % i], interfaceIP["ip%s" % i])
            )
        i += 1


if __name__ == "__main__":
    webPageHeader()
    pageNav()
    pageLinks()
    pageBody()
    webPageFooter()

print ("""
</body>
</html>
""")