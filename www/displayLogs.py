#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

from modules import logFile, webPageFooter
import cgi
import cgitb

cgitb.enable()  # for troubleshooting


print("Content-type: text/html")

print("""
<html>
<head><title>School Bell - Log Files</title></head>
<body> 
<h3> School Bell - Log Files</h3>
""")

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
    pageLinks()
    pageBody()
    webPageFooter()

print("""
</body>
</html>
""")
