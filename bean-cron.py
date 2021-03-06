#!/usr/bin/python

# beancount-cron - automatically add automatic payments to a beancount file
# Copyright (C) 2018 Martin Hohenberg <me@martinhohenberg.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

def getNextDate(startDate, designator):

    endDate = startDate
    designator = designator.lower()
    multiplier = 1
    if (designator[0].isDigit()):
        multiplier = int(designator[0])
        designator = designator[1,]

    if (designator == "once"):
        return startDate

    if (designator == "yearly"):
        endDate = startDate.addYear(1*multiplier)        
        
    if (designator == "monthly"):
        endDate = startDate.addMonth(1*multiplier)       
        
    if (designator == "weekly"):
        days = 7*multiplier
        endDate = startDate.addDays(days)

    if (designator == "daily"):
        days = 1*multiplier
        endDate = startDate.addDays(days)

def readConfig():
    return []
        
# read the config file
configFields = readConfig()

# if backups are enabled
## delete old backups
## create a new backup subdir
## copy all the relevant files to the backup subdir

# read the cron file
cronEntries = file_read_contents(cronfile)


cronfile = ""
outfile = ""


for (entry in cronEntries):

    ## for each entry, check if the date is in the past
    list(date, schedule, amount, currency, fromAccount, toAccount, M, payee) = entry.split(" ")
    
    startDate = dateTime.parse(date)
    if (startDate <= dateTime.date.today()):
        ### if so: calculate the new date
        endDate = getNextDate(startDate, schedule)

        ### add a payment into the prepared outfile
        outFileEntry += startDate+" "+M+" "+payee+"\n"
        outFileEntry += "  "+fromAccount+"     -"+amount+" "+currency+" \n"
        outFileEntry += "  "+toAccount+" \n\n"
        
        ### then update the entry in the cronfile
        newCronLine =  endDate + " "
        newCronLine += schedule + " "
        newCronLine += amount + " "
        newCronLine += currency + " "
        newCronLine += fromAccount + " "
        newCronLine += toAccount + " "
        newCronLine += M + " "
        newCronLine += payee + "\n"
        
    else: 
        ### else: the new entry = the old entry
        newCronLine = entry

    print newCronLine

# attach the outfile to the the beancount-file
