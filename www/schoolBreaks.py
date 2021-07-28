#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Encoding: UTF-8

from modules import (
    htmlFormEscape,
    validateDate,
    webPageFooter,
    webPageHeader,
    pageNav,
    db_connect,
    db_create_cursor,
    db_close_cursor,
    db_disconnect,
    db_query,
)
from datetime import datetime
import cgi
import MySQLdb
import re
import cgitb

cgitb.enable()  # for troubleshooting


addSchoolBreak = False  # will display form to add break

editSchoolBreakId = ""  # this break will be edited

newSchoolBreakName = ""  # new break will be inserted
newStartDate = ""
newEndDate = ""

updateSchoolBreakId = ""  # this break will be updated
updateSchoolBreakName = ""
updateStartDate = ""
updateEndDate = ""

deleteSchoolBreakId = ""  # this break will be deleted

verbose = False

fs = cgi.FieldStorage()

# connect to database
cnx = db_connect(verbose)

# create cursor
cursor = db_create_cursor(cnx, verbose)

# handle inputs
for key in fs.keys():
    if key == "deleteSchoolBreakId":  # delete break
        deleteSchoolBreakId = fs[key].value

    elif key == "editSchoolBreakId":  # display form to edit break
        editSchoolBreakId = fs[key].value

    elif (
        key == "addSchoolBreak" and fs[key].value == "1"
    ):  # display form to add new break
        addSchoolBreak = True

    elif key == "newSchoolBreakName":  # add break
        newSchoolBreakName = fs[key].value
    elif key == "newStartDate":
        newStartDate = fs[key].value
    elif key == "newEndDate":
        newEndDate = fs[key].value

    elif key == "updateSchoolBreakId":  # update break
        updateSchoolBreakId = fs[key].value
    elif key == "updateSchoolBreakName":
        updateSchoolBreakName = fs[key].value
    elif key == "updateStartDate":
        updateStartDate = fs[key].value
    elif key == "updateEndDate":
        updateEndDate = fs[key].value

# get current time
dateTimeNow = datetime.now()
dateNow = str(dateTimeNow.strftime("%Y-%m-%d"))

if deleteSchoolBreakId:  # delete break
    query = "DELETE FROM breaks WHERE breakId = '%s'" % deleteSchoolBreakId
    try:
        result, rowCount = db_query(cursor, query, verbose)  # run query
    except MySQLdb.Error as e:
        print ("\n<br>Error: Could not delete break \n<br>%s" % e
            + "\n<br>SQL: %s" % query)
    else:
        if rowCount:
            print ("\n<br>Deleted break with id = %s" % deleteSchoolBreakId)

elif newSchoolBreakName:  # add break
    if newEndDate == "":  # no end date stated
        newEndDate = newStartDate

    if not re.match("^[a-zA-Z0-9,. ]{1,100}$", newSchoolBreakName):
        print(
            "\n<br>Error: \n<br>Illegal characters in name - "
            + newSchoolBreakName
            + " "
            "\n<br>No special characters (including Swedish etc.) allowed "
            "\n<br>Only characters, digits, spaces and ,. allowed "
            "\n<br>Max 100 characters"
        )
    elif not re.match("^[0-9-]{1,10}$", newStartDate) or not validateDate(
        newStartDate, verbose
    ):
        print(
            "\n<br>Error: \n<br>Illegal date, characters or length in start date - "
            + newStartDate
            + " "
            "\n<br>Must be in the form YY-MM-DD"
            "\n<br>Only digits, spaces and - allowed "
            "\n<br>Max 100 characters"
        )
    elif not re.match("^[0-9-]{1,10}$", newEndDate) or not validateDate(
        newEndDate, verbose
    ):
        print(
            "\n<br>Error: \n<br>Illegal date, characters or length in end date - "
            + newEndDate
            + " "
            "\n<br>Must be in the form YY-MM-DD"
            "\n<br>Only digits, spaces and - allowed "
            "\n<br>Max 100 characters"
        )
    elif newEndDate < dateNow:
        print(
            "\n<br>Error: \n<br>End date occurs earlier than today - "
            + newEndDate
            + " < "
            + dateNow
            + " "
        )
    elif newEndDate < newStartDate:
        print(
            "\n<br>Error: \n<br>End date occurs earlier than start date - "
            + newEndDate
            + " < "
            + newStartDate
            + " "
        )
    elif newEndDate < dateNow:
        print(
            "\n<br>Error: \n<br>End date occurs earlier than today - "
            + newEndDate
            + " < "
            + dateNow
            + " "
        )
    else:
        query = (
            "INSERT INTO breaks "
            "(breakName, startDate, endDate) "
            "VALUES "
            "('" + newSchoolBreakName + "', "
            "'" + newStartDate + "', "
            "'" + newEndDate + "')"
        )
        try:  # insert break in to db
            result, rowCount = db_query(cursor, query, verbose)  # run query
        except (MySQLdb.IntegrityError) as e:  # break name already in database
            print(
                "Error: \n<br>There was already a break with that name. "
                "\n<br>    Pattern not added "
                "\n<br>%s" % e
            )
        except MySQLdb.Error as e:
            print ("\n<br>Error: Could not add break \n<br>%s" % e
                + "\n<br>SQL: %s" % query)
        else:
            print ("\n<br>Added new break")

elif updateSchoolBreakId:  # update break
    if updateEndDate == "":  # no end date stated
        updateEndDate = updateStartDate
    if not re.match("^[a-zA-Z0-9,. ]{1,100}$", updateSchoolBreakName):
        print(
            "Error: \n<br>Illegal characters in name - " + updateSchoolBreakName + " "
            "\n<br>No special characters (including Swedish etc.) allowed "
            "\n<br>Only characters, digits, spaces and ,. allowed "
            "\n<br>Max 100 characters!"
        )
    elif not re.match("^[0-9-]{1,10}$", updateStartDate) or not validateDate(
        updateStartDate, verbose
    ):
        print(
            "Error: \n<br>Illegal date, characters or length in start date - "
            + updateStartDate
            + " "
            "\n<br>Must be in the form YY-MM-DD"
            "\n<br>Only digits, spaces and , allowed "
            "\n<br>Max 100 characters!"
        )
    elif not re.match("^[0-9-]{1,10}$", updateEndDate) or not validateDate(
        updateEndDate, verbose
    ):
        print(
            "Error: \n<br>Illegal date, characters or length in end date - "
            + updateEndDate
            + " "
            "\n<br>Must be in the form YY-MM-DD"
            "\n<br>Only digits, spaces and , allowed "
            "\n<br>Max 100 characters!"
        )
    elif updateEndDate < dateNow:
        print(
            "\n<br>Error: \n<br>End date occurs earlier than today - "
            + updateEndDate
            + " < "
            + dateNow
            + " "
        )
    elif updateEndDate < updateStartDate:
        print(
            "\n<br>Error: \n<br>End date occurs earlier than start date - "
            + updateEndDate
            + " < "
            + updateStartDate
            + " "
        )
    elif updateEndDate < dateNow:
        print(
            "\n<br>Error: \n<br>End date occurs earlier than today - "
            + updateEndDate
            + " < "
            + dateNow
            + " "
        )
    else:
        query = (
            "UPDATE breaks SET "
            "breakName = '" + updateSchoolBreakName + "', "
            "startDate = '" + updateStartDate + "', "
            "endDate = '" + updateEndDate + "' "
            "WHERE "
            "breakId = '%s'" % updateSchoolBreakId
        )
        try:  # update break
            result, rowCount = db_query(cursor, query, verbose)  # run query
        except (MySQLdb.IntegrityError) as e:  # break name already in database
            print(
                "Error: \n<br>There was already a break with that name. "
                "\n<br>Pattern not updated "
                "\n<br>%s>" % e
            )
        except MySQLdb.Error as e:
            print ("\n<br>Error: Could not update break \n<br>%s" % e
                + "\n<br>SQL: %s" % query)
        else:
            if rowCount:
                print ("\n<br>Updated break with id = %s" % updateSchoolBreakId)

def pageBody():

    # get breaks
    query = "SELECT breakId, breakName, startDate, endDate FROM breaks ORDER BY startDate ASC"

    result, rowCount = db_query(cursor, query, verbose)  # run query
    if rowCount:  # display breaks in a table
        print ("\n<br>\n<br>"
            + '<a class="addNew" href="schoolBreaks.py?addSchoolBreak=1">Add New Break</a>'
            + "\n<br>\n<br>"
            + '<table>'
            + "<tr>"
            + "<th>Break name</th>"
            + "<th>Start date</th>"
            + "<th>End date</th>"
            + "<th></th>"
            + "</tr>")

        for row in result:
            schoolBreakId = row[0]
            schoolBreakName = row[1]
            startDate = row[2]
            endDate = row[3]

            if editSchoolBreakId == str(
                schoolBreakId
            ):  # this is the schoolBreak we are about to edit
                editSchoolBreakName = schoolBreakName
                editStartDate = startDate
                editEndDate = endDate

            print ("<tr>"
                + "<td>%s</td>" % schoolBreakName
                + "<td>%s</td>" % startDate
                + "<td>%s</th>" % endDate
                + '<td><a class="delete" href="schoolBreaks.py?deleteSchoolBreakId=%s">Delete</a>' % schoolBreakId
                + '<a class="edit" href="schoolBreaks.py?editSchoolBreakId=%s">Edit</a></td>' % schoolBreakId
                + "</tr>")

        print ("</table")

    if editSchoolBreakId:
        print ("\n<br><br>"
            + "<h3>Edit break</h3>"
            + '<form action="/schoolBreaks.py">'
            + "Pattern id:<br>"
            + '<input type="text" name="updateSchoolBreakId" value="%s">' % editSchoolBreakId
            + "<br><br><br>"
            + "Break name:<br>"
            + '<input type="text" name="updateSchoolBreakName" value="%s">' % editSchoolBreakName
            +(
                "State a name for your break. <br><br>"
                "\nMax 100 characters. <br>"
                )
            + "<br><br>"
            + "Start date:<br>"
            + '<input type="text" name="updateStartDate" value="%s">' % editStartDate
            + (
                "State date in the form: YY-MM-DD. <br><br>"
                "\nOnly digits and - are allowed. <br>"
                )
            + "<br><br>"
            + "End date:<br>"
            + '<input type="text" name="updateEndDate" value="%s">' % editEndDate
            + (
                "State date in the form: YY-MM-DD. <br><br>"
                "\nOnly digits and - are allowed. <br>"
                )
            + "<br><br>"
            + '<input type="submit" value="Submit">'
            + "</form>")

    if addSchoolBreak:  # display form to add break
        print ("\n<br><br>"
            + "<h3>Add break</h3>"
            + '<form action="/schoolBreaks.py">'
            + "Break name:<br>"
            + '<input type="text" name="newSchoolBreakName" value="Break name">'
            + ("State a name for your break. <br><br>" "\nMax 100 characters. <br>"))
        dateTimeNow = datetime.now()
        dateNow = str(dateTimeNow.strftime("%Y-%m-%d"))
        print ("<br><br>"
            + "Start date:<br>"
            + '<input type="text" name="newStartDate" value="%s">' % dateNow
            + (
                "State date in the form: YY-MM-DD. <br><br>"
                "\nOnly digits and - are allowed. <br>"
                )
            + "<br><br>"
            + "End date:<br>"
            + '<input type="text" name="newEndDate" value="%s">' % dateNow
            +(
                "State date in the form: YY-MM-DD. <br><br>"
                "\nOnly digits and - are allowed. <br>"
                )
            + "<br><br>"
            + '<input type="submit" value="Submit">'
            + "</form>")

if __name__ == "__main__":
    webPageHeader()
    pageNav()
    pageBody()
    webPageFooter()

# close cursor
db_close_cursor(cnx, cursor, verbose)

# close db
db_disconnect(cnx, verbose)

print ("""
</body>
</html>
""")