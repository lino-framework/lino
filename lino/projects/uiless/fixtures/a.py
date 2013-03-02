# -*- coding: UTF-8 -*-
"""
This is a `Python dump <http://lino-framework.org/topics/dumpy.html>`_.
"""
from __future__ import unicode_literals
SOURCE_VERSION = '1.5.8'
from decimal import Decimal
from datetime import datetime as dt
from datetime import time,date
from lino.utils import babel
from lino.utils.mti import create_child
from lino.dd import resolve_model
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
    Needed if `lino.Lino.languages` changed between dumpdata and loaddata
    """
    return babel.babel_values(fieldname,en=values[0])
    
admin_LogEntry = resolve_model("admin.LogEntry")
auth_Group = resolve_model("auth.Group")
auth_Permission = resolve_model("auth.Permission")
auth_User = resolve_model("auth.User")
contenttypes_ContentType = resolve_model("contenttypes.ContentType")
polls_Choice = resolve_model("polls.Choice")
polls_Poll = resolve_model("polls.Poll")
sessions_Session = resolve_model("sessions.Session")
sites_Site = resolve_model("sites.Site")

def create_django_admin_log(id, action_time, user_id, content_type_id, object_id, object_repr, action_flag, change_message):
    kw = dict()
    kw.update(id=id)
    kw.update(action_time=action_time)
    kw.update(user_id=user_id)
    content_type_id = new_content_type_id(content_type_id)
    kw.update(content_type_id=content_type_id)
    kw.update(object_id=object_id)
    kw.update(object_repr=object_repr)
    kw.update(action_flag=action_flag)
    kw.update(change_message=change_message)
    return admin_LogEntry(**kw)

def create_auth_group(id, name):
    kw = dict()
    kw.update(id=id)
    kw.update(name=name)
    return auth_Group(**kw)

def create_auth_permission(id, name, content_type_id, codename):
    kw = dict()
    kw.update(id=id)
    kw.update(name=name)
    content_type_id = new_content_type_id(content_type_id)
    kw.update(content_type_id=content_type_id)
    kw.update(codename=codename)
    return auth_Permission(**kw)

def create_auth_user(id, username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined):
    kw = dict()
    kw.update(id=id)
    kw.update(username=username)
    kw.update(first_name=first_name)
    kw.update(last_name=last_name)
    kw.update(email=email)
    kw.update(password=password)
    kw.update(is_staff=is_staff)
    kw.update(is_active=is_active)
    kw.update(is_superuser=is_superuser)
    kw.update(last_login=last_login)
    kw.update(date_joined=date_joined)
    return auth_User(**kw)

def create_django_content_type(id, name, app_label, model):
    kw = dict()
    kw.update(id=id)
    kw.update(name=name)
    kw.update(app_label=app_label)
    kw.update(model=model)
    return contenttypes_ContentType(**kw)

def create_polls_choice(id, poll_id, choice_text, votes):
    kw = dict()
    kw.update(id=id)
    kw.update(poll_id=poll_id)
    kw.update(choice_text=choice_text)
    kw.update(votes=votes)
    return polls_Choice(**kw)

def create_polls_poll(id, question, pub_date):
    kw = dict()
    kw.update(id=id)
    kw.update(question=question)
    kw.update(pub_date=pub_date)
    return polls_Poll(**kw)

def create_django_session(session_key, session_data, expire_date):
    kw = dict()
    kw.update(session_key=session_key)
    kw.update(session_data=session_data)
    kw.update(expire_date=expire_date)
    return sessions_Session(**kw)

def create_django_site(id, domain, name):
    kw = dict()
    kw.update(id=id)
    kw.update(domain=domain)
    kw.update(name=name)
    return sites_Site(**kw)



def django_site_objects():
    yield create_django_site(1,u'example.com',u'example.com')

def polls_poll_objects():
    yield create_polls_poll(1,u'What is your preferred colour?',dt(2013,2,11,0,0,0))
    yield create_polls_poll(2,u'Do you like Django?',dt(2013,2,11,0,0,0))
    yield create_polls_poll(3,u'Do you like ExtJS?',dt(2013,2,11,0,0,0))

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

def auth_permission_objects():
    yield create_auth_permission(19,u'Can add log entry',admin_LogEntry,u'add_logentry')
    yield create_auth_permission(20,u'Can change log entry',admin_LogEntry,u'change_logentry')
    yield create_auth_permission(21,u'Can delete log entry',admin_LogEntry,u'delete_logentry')
    yield create_auth_permission(1,u'Can add group',auth_Group,u'add_group')
    yield create_auth_permission(4,u'Can change group',auth_Group,u'change_group')
    yield create_auth_permission(7,u'Can delete group',auth_Group,u'delete_group')
    yield create_auth_permission(2,u'Can add permission',auth_Permission,u'add_permission')
    yield create_auth_permission(5,u'Can change permission',auth_Permission,u'change_permission')
    yield create_auth_permission(8,u'Can delete permission',auth_Permission,u'delete_permission')
    yield create_auth_permission(3,u'Can add user',auth_User,u'add_user')
    yield create_auth_permission(6,u'Can change user',auth_User,u'change_user')
    yield create_auth_permission(9,u'Can delete user',auth_User,u'delete_user')
    yield create_auth_permission(10,u'Can add content type',contenttypes_ContentType,u'add_contenttype')
    yield create_auth_permission(11,u'Can change content type',contenttypes_ContentType,u'change_contenttype')
    yield create_auth_permission(12,u'Can delete content type',contenttypes_ContentType,u'delete_contenttype')
    yield create_auth_permission(22,u'Can add choice',polls_Choice,u'add_choice')
    yield create_auth_permission(24,u'Can change choice',polls_Choice,u'change_choice')
    yield create_auth_permission(26,u'Can delete choice',polls_Choice,u'delete_choice')
    yield create_auth_permission(23,u'Can add poll',polls_Poll,u'add_poll')
    yield create_auth_permission(25,u'Can change poll',polls_Poll,u'change_poll')
    yield create_auth_permission(27,u'Can delete poll',polls_Poll,u'delete_poll')
    yield create_auth_permission(13,u'Can add session',sessions_Session,u'add_session')
    yield create_auth_permission(14,u'Can change session',sessions_Session,u'change_session')
    yield create_auth_permission(15,u'Can delete session',sessions_Session,u'delete_session')
    yield create_auth_permission(16,u'Can add site',sites_Site,u'add_site')
    yield create_auth_permission(17,u'Can change site',sites_Site,u'change_site')
    yield create_auth_permission(18,u'Can delete site',sites_Site,u'delete_site')

def auth_user_objects():
    yield create_auth_user(1,u'root',u'',u'',u'root@example.com',u'pbkdf2_sha256$10000$HjAs4ueOXJ3m$Z/Dv/71uKIaXy9z2rqirkN3gyIhAc5mpsk0bfKl2AOM=',True,True,True,dt(2013,2,11,7,40,47),dt(2013,2,11,7,40,47))


def objects():
    yield django_site_objects()
    yield polls_poll_objects()
    yield polls_choice_objects()
    yield auth_permission_objects()
    yield auth_user_objects()

settings.SITE.install_migrations(globals())
