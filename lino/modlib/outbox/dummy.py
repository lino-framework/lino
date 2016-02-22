# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :term:`dummy module` for `outbox`, 
used by :func:`lino.core.utils.resolve_app`.
"""
from builtins import object
from lino.api import dd


class Mailable(object):
    pass

#~ class MailableType(object): pass


class MailableType(dd.Model):
    email_template = dd.DummyField()
    attach_to_email = dd.DummyField()

    class Meta(object):
        abstract = True

MailsByController = dd.DummyField()
