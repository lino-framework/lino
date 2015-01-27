# -*- coding: UTF-8 -*-
# Copyright 2012 Luc Saffre
# License: BSD (see file COPYING for details)

"""
code changes must be documented in *one central place 
per developer*, not per module.
"""

import os
import datetime
from django.conf import settings
from lino.utils import i2d, i2t
from lino.utils.restify import restify, doc2rst

from lino.api import dd, rt
blogs = dd.resolve_app('blogs')
tickets = dd.resolve_app('tickets')


class Blogger(object):

    def __init__(self, user=None):
        self.objects_list = []
        self.date = None
        self.user = user
        self.current_project = None

    def set_date(self, d):
        self.date = i2d(d)

    def set_project(self, project):
        self.current_project = project

    def set_user(self, username):
        self.user = settings.SITE.user_model.objects.get(username=username)

    def add_object(self, obj):
        self.objects_list.append(obj)
        return obj

    def project(self, ref, title, body, raw_html=False, **kw):
        if not raw_html:
            body = restify(doc2rst(body))
        kw.update(ref=ref)
        kw.update(description=body)
        kw.update(name=title)
        if self.project:
            kw.setdefault('parent', self.current_project)
        return self.add_object(tickets.Project(**kw))

    def milestone(self, ref, date, body=None, raw_html=False, **kw):
        if not raw_html:
            body = restify(doc2rst(body))
        kw.update(ref=ref)
        #~ kw.update(checkin=checkin)
        #~ kw.update(description=body)
        if self.project:
            kw.setdefault('project', self.current_project)
        return self.add_object(tickets.Milestone(**kw))

    #~ def change(self,time,title,body,module=None,tags=None,issue=None,raw_html=False):
    def entry(self, ticket, time, title, body, raw_html=False, **kw):
        if isinstance(time, (basestring, int)):
            time = i2t(time)
        kw.update(created=datetime.datetime.combine(self.date, time))
        if not raw_html:
            body = restify(doc2rst(body))
        kw.update(user=self.user)
        kw.update(body=body)
        kw.update(title=title)
        kw.update(ticket=ticket)
        return self.add_object(blogs.Entry(**kw))

    def follow(self, prev, time, body, raw_html=False, **kw):
        return self.entry(
            prev.ticket, time, prev.title + " (continued)", body,
            raw_html=raw_html, **kw)

    def ticket(self, project_ref, title, body, raw_html=False, **kw):
        if not raw_html:
            body = restify(doc2rst(body))
        kw.update(description=body)
        kw.update(summary=title)
        project = tickets.Project.get_by_ref(project_ref)
        #~ try:
            #~ project=tickets.Project.objects.get(ref=project_ref)
        #~ except tickets.Project.DoesNotExist,e:
            #~ raise Exception("No project with reference %r" % project_ref)
        kw.update(project=project)
        #~ kw.update(project=tickets.Project.objects.get(ref=project_ref))
        return self.add_object(tickets.Ticket(**kw))

    def flush(self):
        for o in self.objects_list:
            yield o
        self.objects_list = []

#~ ENTRY_TYPE_CHANGE = 1
#~ ENTRY_TYPE_ISSUE = 2

#~ class Entry(object):
    #~ raw_html = False
    #~ def __init__(self,date,title,body,module=None,tags=None,issue=None):
    # ~ # def __init__(self,module,date,tags,body):
        #~ self.title = title
        #~ self.date = i2d(date)
        #~ self.tags = tags
        #~ self.body = restify(doc2rst(body))
        #~ self.module = module
        #~ self.issue = issue

    #~ def __unicode__(self):
        #~ return "(%s %s) : [%s] %s" % (self.date,self.title,self.tags,self.body)

#~ class CodeChange(Entry): pass
#~ class Issue(Entry): pass


#~ def build_blog_entries(**kw):
    #~ from lino.modlib.blog import models import Entry
    #~ global ENTRIES_LIST
    #~ for e in ENTRIES_LIST:
        #~ if not e.raw_html:
            #~ body = restify(doc2rst(e.body))
        #~ yield blogs.Entry(created=e.date,title=e.title,e.body,**kw)
    #~ ENTRIES_LIST = []


#~ blogger = Blogger()
