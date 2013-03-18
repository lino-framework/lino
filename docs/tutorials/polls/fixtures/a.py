# -*- coding: UTF-8 -*-
"""
This is a `Python dump <http://north.lino-framework.org>`_
created using Python 2.7.3, Django 1.4.5, djangosite 0.1.0, North 0.1.0, Lino 1.6.3, Jinja 2.6, Sphinx 1.1.3, python-dateutil 2.1, OdfPy ODFPY/0.9.6, docutils 0.10, suds 0.4, PyYaml 3.10, Appy 0.8.3 (2013/02/22 15:29).

"""
from __future__ import unicode_literals
SOURCE_VERSION = '2.7.3'
from decimal import Decimal
from datetime import datetime as dt
from datetime import time,date
from north.dpy import create_mti_child
from north.dbutils import resolve_model
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

            
def new_content_type_id(m):
    if m is None: return m
    # if not fmn: return None
    # m = resolve_model(fmn)
    ct = ContentType.objects.get_for_model(m)
    if ct is None: return None
    return ct.pk
    

def bv2kw(fieldname,values):
    """
    Needed if `Site.languages` changed between dumpdata and loaddata
    """
    return settings.SITE.babelkw(fieldname,en_US=values[0])
    
polls_Choice = resolve_model("polls.Choice")
polls_Poll = resolve_model("polls.Poll")
ui_SiteConfig = resolve_model("ui.SiteConfig")

def create_polls_choice(id, poll_id, choice, votes):
    kw = dict()
    kw.update(id=id)
    kw.update(poll_id=poll_id)
    kw.update(choice=choice)
    kw.update(votes=votes)
    return polls_Choice(**kw)

def create_polls_poll(id, question, hidden, pub_date):
    kw = dict()
    kw.update(id=id)
    kw.update(question=question)
    kw.update(hidden=hidden)
    kw.update(pub_date=pub_date)
    return polls_Poll(**kw)

def create_ui_siteconfig(id, default_build_method):
    kw = dict()
    kw.update(id=id)
    kw.update(default_build_method=default_build_method)
    return ui_SiteConfig(**kw)



def ui_siteconfig_objects():
    yield create_ui_siteconfig(1,u'appyodt')

def polls_poll_objects():
    yield create_polls_poll(1,u'What is your preferred colour?',False,dt(2013,3,18,0,0,0))
    yield create_polls_poll(2,u'Do you like Django?',False,dt(2013,3,18,0,0,0))
    yield create_polls_poll(3,u'Do you like ExtJS?',False,dt(2013,3,18,0,0,0))

def polls_choice_objects():
    yield create_polls_choice(1,1,u'Blue',0)
    yield create_polls_choice(2,1,u'Red',0)
    yield create_polls_choice(3,1,u'Yellow',0)
    yield create_polls_choice(4,1,u'other',0)
    yield create_polls_choice(5,2,u'Yes',0)
    yield create_polls_choice(6,2,u'No',0)
    yield create_polls_choice(7,2,u'Not yet decided',0)
    yield create_polls_choice(8,3,u'Yes',0)
    yield create_polls_choice(9,3,u'No',0)
    yield create_polls_choice(10,3,u'Not yet decided',0)


def objects():
    yield ui_siteconfig_objects()
    yield polls_poll_objects()
    yield polls_choice_objects()

settings.SITE.install_migrations(globals())
