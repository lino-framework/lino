#!/usr/bin/python
# Version 1.1
# This code is published under the FreeBSD license.

import os
import os.path
import re
import datetime
import time

SECONDS_PER_DAY=24*60*60
iCalFolder = os.path.expanduser("~/Library/Calendars")

class ICalReader:

    def __init__(self, calendarName = None):
        self.events = []
        if calendarName:
            self.iCalFiles = [calendarName]
        else:
            self.iCalFiles = os.listdir(iCalFolder)
            newList = []
            for file in self.iCalFiles:
                newList.append(iCalFolder+"/"+file)
            self.iCalFiles = newList
        self.readEvents()

    def calendars(self):
        return self.iCalFiles

    def readEvents(self):
        self.events = []
        for file in self.iCalFiles:
            lines = open(file).readlines()
            inEvent = False
            eventLines = []
            for line in lines:
                if re.match("^BEGIN:VEVENT", line):
                    inEvent = True
                    eventLines = []

                if inEvent:
                    eventLines.append(line)
                    if re.match("^END:VEVENT",line):
                        self.events.append(self.parseEvent(eventLines))

        return self.events

    def parseEvent(self, lines):
        event = ICalEvent()
        startDate = None
        rule = None
        endDate = None
        allDayEvent = False
        
        for line in lines:
            if re.match("^SUMMARY:(.*)", line):
                event.summary = re.match("^SUMMARY:(.*)", line).group(1)
            elif re.match("^DTSTART;.*:(.*).*", line):
                startDate = self.parseDate(re.match("^DTSTART;.*:(.*).*", line).group(1))
                allDayEvent = self.allDayEvent(re.match("^DTSTART;.*:(.*).*", line).group(1))
            elif re.match("^DTEND;.*:(.*).*", line):
                endDate = self.parseDate(re.match("^DTEND;.*:(.*).*", line).group(1))
            elif re.match("^EXDATE.*:(.*)", line):
                event.addExceptionDate(self.parseDate(re.match("^EXDATE.*:(.*)", line).group(1)))
            elif re.match("^RRULE:(.*)", line):
                rule = re.match("^RRULE:(.*)", line).group(1)

        event.allDayEvent = allDayEvent
        event.startDate = startDate
        event.endDate = endDate
        if rule:
            event.addRecurrenceRule(rule)
        return event

    def allDayEvent(self, dateStr):
        return len(dateStr) <= 9
        

    def parseDate(self, dateStr):
        year = int(dateStr[0:4])
        if year < 1970:
            year = 1970

        month = int(dateStr[4:4+2])
        day = int(dateStr[6:6+2])
        try:
            hour = int(dateStr[9:9+2])
            minute = int(dateStr[11:11+2])
        except:
            hour = 0
            minute = 0

        return datetime.datetime(year, month, day, hour, minute)

    def selectEvents(self, selectFunction):
        note = datetime.datetime.today()
        self.events.sort()
        events = filter(selectFunction, self.events)
        return events

    def todaysEvents(self, event):
        return event.startsToday()

    def tomorrowsEvents(self, event):
        return event.startsTomorrow()

    def eventsFor(self, date):
        note = datetime.datetime.today()
        self.events.sort()
        ret = []
        for event in self.events:
            if event.startsOn(date):
                ret.append(event)
        return ret


class ICalEvent:
    def __init__(self):
        self.exceptionDates = []
        self.dateSet = None
        self.allDayEvent = False

    def __str__(self):
        return self.summary

    def __eq__(self, otherEvent):
        return self.startDate == otherEvent.startDate

    def addExceptionDate(self, date):
        self.exceptionDates.append(date)

    def addRecurrenceRule(self, rule):
        self.dateSet = DateSet(self.startDate, self.endDate, rule)

    def startsToday(self):
        return self.startsOn(datetime.datetime.today())

    def startsTomorrow(self):
        tomorrow = datetime.datetime.fromtimestamp(time.time() + SECONDS_PER_DAY)
        return self.startsOn(tomorrow)

    def startsOn(self, date):
        if self.startDate:
            return (self.startDate.year == date.year and
                    self.startDate.month == date.month and
                    self.startDate.day == date.day or
                    (self.dateSet and self.dateSet.includes(date)))
        else:
            return (self.dateSet and self.dateSet.includes(date))

    def startTime(self):
        return self.startDate

class DateSet:
    def __init__(self, startDate, endDate, rule):
        self.startDate = startDate
        self.endDate = endDate
        self.frequency = None
        self.count = None
        self.untilDate = None
        self.byMonth = None
        self.byDate = None
        self.parseRecurrenceRule(rule)
    
    def parseRecurrenceRule(self, rule):
        if re.match("FREQ=(.*?);", rule) :
            self.frequency = re.match("FREQ=(.*?);", rule).group(1)
		
        if re.match("COUNT=(\d*)", rule) :
            self.count = int(re.match("COUNT=(\d*)", rule).group(1))
		
        if re.match("UNTIL=(.*?);", rule) :
            self.untilDate = DateParser.parse(re.match("UNTIL=(.*?);", rule).group(1))
		
        if re.match("INTERVAL=(\d*)", rule) :
            self.interval = int(re.match("INTERVAL=(\d*)", rule).group(1))

        if re.match("BYMONTH=(.*?);", rule) :
            self.byMonth = re.match("BYMONTH=(.*?);", rule).group(1)

        if re.match("BYDAY=(.*?);", rule) :
            self.byDay = re.match("BYDAY=(.*?);", rule).group(1)

        
    def includes(self, date):
        if date == self.startDate:
            return True

        if self.untilDate and date > self.untilDate:
            return False

        if self.frequency == 'DAILY':
            increment = 1
            if self.interval:
                increment = self.interval
            d = self.startDate
            counter = 0
            while(d < date):
                if self.count:
                    counter += 1
                    if counter >= self.count:
                        return False

                d = d.replace(day=d.day+1)

                if (d.day == date.day and
                    d.year == date.year and
                    d.month == date.month):
                    return True
            
        elif self.frequency == 'WEEKLY':
            if self.startDate.weekday() == date.weekday():
                return True
            else:
                if self.endDate:
                    for n in range(0, self.endDate.day - self.startDate.day):
                        newDate = self.startDate.replace(day=self.startDate.day+n)
                        if newDate.weekday() == date.weekday():
                            return True

        elif self.frequency == 'MONTHLY':
            pass

        elif self.frequency == 'YEARLY':
            pass

        return False
    

if __name__ == '__main__':
    reader = ICalReader()
    print "Today"
    print "====="
    for event in reader.selectEvents(reader.todaysEvents):
        print event
    print "Tomorrow"
    print "========"
    for event in reader.selectEvents(reader.tomorrowsEvents):
        print event
    print "02/14/2003 Events"
    print "================="
    for event in reader.eventsFor(datetime.date(2004, 02, 14)):
        print event
        
