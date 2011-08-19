import sys
from datetime import datetime, timedelta
import caldav
from caldav.elements import dav, cdav

# Principal url
#~ url = "https://user:pass@hostname/user/Calendar"
username = 'luc.saffre@gmail.com'
pwd = raw_input("Please enter password for %s: " % username)

loc = '/calendar/dav/%s/' % username
url = "https://%s:%s@www.google.com%s" % (username,pwd,loc)

vcal = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VEVENT
UID:1234567890
DTSTAMP:20100510T182145Z
DTSTART:20100512T170000Z
DTEND:20100512T180000Z
SUMMARY:This is an event
END:VEVENT
END:VCALENDAR
"""

# the above raw data can be done using vobject:

import vobject
mycal = vobject.iCalendar()
mycal.add('vevent')
mycal.vevent.add('uid').value = "1234567890"
mycal.vevent.add('dtstamp').value = datetime(2010,5,10,18,21,45)
#~ mycal.vevent.add('dtstamp').value = datetime.now()
mycal.vevent.add('dtstart').value = datetime(2010,5,12,17,0,0)
mycal.vevent.add('dtend').value = datetime(2010,5,12,18,0,0)
mycal.vevent.add('summary').value = "This is still my event"
vcal = mycal.serialize()


client = caldav.DAVClient(url)
principal = caldav.Principal(client, url)
#~ print "url.username:", principal.url.username
#~ print "url.hostname:", principal.url.hostname

calendars = principal.calendars()
if len(calendars) == 0:
    print "Sorry, no calendar"
    print principal.children()
    sys.exit()
    
if len(calendars) > 1:
    print "WARNING: more than 1 calendar"
    
calendar = calendars[0]
print "Using calendar", calendar

print "Renaming (works, but is deactivated)"
if False:
    calendar.set_properties([dav.DisplayName("Test calendar"),])
print calendar.get_properties([dav.DisplayName(),])

#~ event = caldav.Event(client, data = vcal, parent = calendar).save()
#~ print "Event", event, "created"

d = datetime(2010, 5, 12)
print "Looking for events on ", d
results = calendar.date_search(d,d+timedelta(days=1))
for event in results:
    print "Found", event.instance.prettyPrint()

d = datetime(2011, 8, 20)
print "Looking for events after", d
results = calendar.date_search(d,d+timedelta(days=4))
for event in results:
    print "Found", event.instance.prettyPrint()
    
