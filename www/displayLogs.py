#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

from modules import logFile, webPageFooter, webPageHeader, pageNav
import cgi
import cgitb

cgitb.enable()  # for troubleshooting

def pageLinks():
    print('\n<br><a href="index.py">Home</a>')


def pageBody():
    print("\n<br>")

    for fileName in (logFile, "/home/pi/bin/piSchoolBell/gpio-watch.log"):
        print("\n<br>"
              + "\n<br>File name: %s" % fileName
              + "\n<hr>")

        with open(fileName) as f:
            content = f.readlines()

        content = [x.strip() for x in content]

        if content:
            for line in content:
                print("\n<br>%s" % line)
        else:
            print("\n<br>------ No entries in %s -----" % fileName)


if __name__ == "__main__":
    webPageHeader()
    pageNav()
    pageBody()
    webPageFooter()