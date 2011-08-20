# -*- coding: UTF-8 -*-
## Copyright 2011 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
Starts a daemon (or, if daemons are not supported, a nomal console process) 
that watches for changes in remote calendars.
See also :doc:`/tickets/47`

"""

import os
import sys
import codecs
import time
import datetime
#~ import signal
import atexit

#~ import logging
#~ logger = logging.getLogger(__name__)

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ValidationError


from django.conf import settings


from django.db.utils import DatabaseError
from django.db import models
# OperationalError
from django.utils import simplejson
#~ from django.contrib.auth import models as auth
from lino.modlib.users import models as auth

import lino

from lino.tools import resolve_model
from lino.modlib.contacts.utils import name2kw, street2kw, join_words

from lino.utils import confirm
from lino.utils import dblogger
from lino.tools import obj2str

from lino.utils.daemoncommand import DaemonCommand

#~ from datetime import datetime, timedelta

import caldav
from caldav.elements import dav, cdav
#~ from lino.modlib.cal.models import Calendar, Event

Calendar = resolve_model('cal.Calendar')
Event = resolve_model('cal.Event')

REQUEST = dblogger.PseudoRequest('watch_calendars')

# dblogger.log_changes(REQUEST,obj)




def watch():
    "Deserves more documentation."
    for dbcal in Calendar.objects.all():
        if not dbcal.url_template: 
            continue
        url = dbcal.get_url()
        dblogger.info("Get calendar %s from %s",dbcal.name, url)
        
        client = caldav.DAVClient(url)
        principal = caldav.Principal(client, url)
        #~ print "url.username:", principal.url.username
        #~ print "url.hostname:", principal.url.hostname

        calendars = principal.calendars()
        if len(calendars) == 0:
            dblogger.info("--> Sorry, no calendar")
        elif len(calendars) > 1:
            #~ print "WARNING: more than 1 calendar"
            dblogger.warning("--> More than 1 calendar")
        else:
            touched = set()
            count_update = 0
            count_new = 0
            count_deleted = 0
            calendar = calendars[0]
            #~ print "Using calendar", calendar

            props = calendar.get_properties([dav.DisplayName()])
            dbcal.name = props[dav.DisplayName().tag]
            dbcal.save()
            
            from_date = dbcal.start_date 
            if not from_date:
                from_date = datetime.datetime.now() - datetime.timedelta(days=365)
            until_date = datetime.datetime.now() + datetime.timedelta(days=365)

            results = calendar.date_search(from_date,until_date)
            if results:
                for comp in results:
                    if comp.instance.vevent:
                        summary = comp.instance.vevent.summary.value
                        uid = comp.instance.vevent.uid.value
                        dtstart = comp.instance.vevent.dtstart.value
                        dtend = comp.instance.vevent.dtend.value
                        try:
                            obj = Event.objects.get(uid=uid)
                            count_update += 1
                        except Event.DoesNotExist, e:
                        #~ except Exception, e:
                            obj = Event(uid=uid)
                            obj.user = dbcal.user
                            count_new += 1
                        obj.summary = summary
                        #~ print type(dtstart)
                        #~ print repr(dtstart)
                        if dtstart:
                            if isinstance(dtstart,datetime.datetime):
                                obj.start_date = dtstart.date()
                                obj.start_time = dtstart.time()
                            elif isinstance(dtstart,datetime.date):
                                obj.start_date = dtstart
                            else:
                                dblogger.warning(
                                    "Invalid value for dtstart: %r",
                                    dtstart)
                        if dtend:
                            if isinstance(dtend,datetime.datetime):
                                obj.end_date = dtstart.date()
                                obj.end_time = dtend.time()
                            elif isinstance(dtend,datetime.date):
                                obj.end_date = dtend
                            else:
                                dblogger.warning(
                                    "Invalid value for dtend: %r",
                                    dtstart)
                        obj.full_clean()
                        dblogger.log_changes(REQUEST,obj)
                        obj.save()
                        touched.add(obj.pk)
                    else:
                        raise Exception(
                            "Got unhandled component %s" 
                            % comp.instance.prettyPrint())
                        #~ print "children:", [c for c in comp.instance.getChildren()]
                    
                    #~ raise StopIteration
            qs = dbcal.event_set.exclude(id__in=touched)
            count_deleted = qs.count()
            qs.delete() # doesn't call delete methods of individual objects
            #~ for obj in qs:
                #~ obj.delete()
            dblogger.info(
                "--> Created %d, updated %d, deleted %s events", 
                count_new, count_update,count_deleted)

        
        

def main(*args,**options):
    msg = "Started watch_calendars %s..."
    dblogger.info(msg,lino.__version__)
        
    def goodbye():
        msg = "Stopped watch_calendars %s ..."
        dblogger.info(msg,lino.__version__)
    atexit.register(goodbye)
    
    while True:
        watch()
        #~ try:
            #~ watch()
        #~ except Exception,e:
            #~ dblogger.exception(e)
        time.sleep(60) # sleep for a minute

class Command(DaemonCommand):
  
    help = __doc__
    
    preserve_loggers = [dblogger.logger]
    
    def handle_daemon(self, *args, **options):
        #~ models.get_models() # trigger django.db.models.loading.cache._populate()
        settings.LINO.setup()
        main(*args,**options)


