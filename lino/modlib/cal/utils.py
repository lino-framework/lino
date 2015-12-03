# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Some calendar utilities

.. autosummary::


.. This is a tested document. You can test it using:

    $ python setup.py test -s tests.LibTests.test_cal_utils

..
  >>> import datetime
  >>> import lino
  >>> lino.startup('lino.projects.docs.settings.demo')
  >>> from lino.api.shell import *


"""

from __future__ import unicode_literals

import datetime

from dateutil.tz import tzlocal

from django.conf import settings
from django.utils.encoding import force_unicode

from lino.utils.format_date import format_date
from lino.utils.format_date import fds

from lino.api import rt


def aware(d):
    "Convert the given datetime into a timezone-aware datetime."
    return datetime.datetime(d.year, d.month, d.day, tzinfo=tzlocal())


def dt2kw(dt, name, **d):
    """Store given timestamp `dt` in a field dict.  `name` is the base
    name of the fields.

    Examples:
    
    >>> dt = datetime.datetime(2013,12,25,17,15,00)
    >>> dt2kw(dt,'foo')
    {u'foo_date': datetime.date(2013, 12, 25), u'foo_time': datetime.time(17, 15)}

    """
    if dt:
        if isinstance(dt, datetime.datetime):
            d[name + '_date'] = dt.date()
            if dt.time():
                d[name + '_time'] = dt.time()
            else:
                d[name + '_time'] = None
        elif isinstance(dt, datetime.date):
            d[name + '_date'] = dt
            d[name + '_time'] = None
        else:
            raise Exception("Invalid datetime value %r" % dt)
    else:
        d[name + '_date'] = None
        d[name + '_time'] = None
    return d


def setkw(obj, **kw):
    for k, v in kw.items():
        setattr(obj, k, v)


def when_text(d, t=None):
    """Return a string with a concise representation of the given date
    and time combination.

    Examples:

    >>> when_text(datetime.date(2013,12,25))
    u'Wed 12/25/13'
    
    >>> when_text(datetime.date(2013,12,25),datetime.time(17,15,00))
    u'Wed 12/25/13 (17:15)'
    
    >>> when_text(None)
    u''

    """
    if d is None:
        return ''
    # fmt = 'yyyy MMM dd (EE)'
    # txt = d.strftime(settings.SITE.date_format_strftime)
    txt = format_date(d, 'EE ')
    txt += fds(d)
    if t is not None:
        txt += ' (%s)' % t.strftime(settings.SITE.time_format_strftime)
    return txt


def update_auto_event(
        autotype, user, date, summary, owner, **defaults):
    return update_auto_component(
        rt.modules.cal.Event, autotype, user, date, summary, owner, **defaults)


def update_auto_task(
        autotype, user, date, summary, owner, **defaults):
    Task = rt.modules.cal.Task
    return update_auto_component(
        Task, autotype, user, date, summary, owner, **defaults)


def update_auto_component(
        model, autotype, user, date, summary, owner, **defaults):
    """
    Creates, updates or deletes the
    automatic :class:`calendar component <Component>`
    of the specified `auto_type` and `owner`.

    Specifying `None` for `date` means that
    the automatic component should be deleted.
    """
    #~ print "20120729 update_auto_component", model,autotype,user, date, settings.SITE.loading_from_dump
    #~ if SKIP_AUTO_TASKS: return
    if settings.SITE.loading_from_dump:
            #~ print "20111014 loading_from_dump"
        return None
    ContentType = rt.modules.contenttypes.ContentType
    ot = ContentType.objects.get_for_model(owner.__class__)
    if date and date >= settings.SITE.today() + datetime.timedelta(days=-7):
        #~ defaults = owner.get_auto_task_defaults(**defaults)
        #~ print "20120729 b"
        defaults.setdefault('user', user)
        obj, created = model.objects.get_or_create(
            defaults=defaults,
            owner_id=owner.pk,
            owner_type=ot,
            auto_type=autotype)
        if not obj.is_user_modified():
            original_state = dict(obj.__dict__)
            if obj.user != user:
                obj.user = user
            summary = force_unicode(summary)
            if obj.summary != summary:
                obj.summary = summary
            if obj.start_date != date:
                obj.start_date = date
            if created or obj.__dict__ != original_state:
                #~ obj.full_clean()
                obj.save()
        return obj
    else:
        #~ print "20120729 c"
        # delete task if it exists
        try:
            obj = model.objects.get(owner_id=owner.pk,
                                    owner_type=ot, auto_type=autotype)
        except model.DoesNotExist:
            pass
        else:
            if not obj.is_user_modified():
                obj.delete()


def update_reminder(type, owner, user, orig, msg, num, unit):
    """
    Shortcut for calling :func:`update_auto_task`
    for automatic "reminder tasks".
    A reminder task is a message about something that will
    happen in the future.
    """
    update_auto_task(
        type, user,
        unit.add_duration(orig, -num),
        msg,
        owner)

