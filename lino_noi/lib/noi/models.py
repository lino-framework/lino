# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""The :xfile:`models.py` module for :mod:`lino_noi`.

Defines a handler for :data:`lino.modlib.smtpd.signals.mail_received`.

"""

from email.parser import Parser

from lino.api import dd
from lino.modlib.smtpd.signals import mail_received


@dd.receiver(dd.post_analyze)
def my_details(sender, **kw):
    sender.modules.system.SiteConfigs.set_detail_layout("""
    site_company next_partner_id:10
    default_build_method
    max_auto_events default_event_type site_calendar
    """)


@dd.receiver(mail_received)
def process_message(sender=None, peer=None, mailfrom=None,
                    rcpttos=None, data=None, **kwargsg):
    print 'Receiving message from:', peer
    print 'Message addressed from:', mailfrom
    print 'Message addressed to  :', rcpttos
    print 'Message length        :', len(data)
    msg = Parser().parsestr(data)
    print 'To: %s' % msg['to']
    print 'From: %s' % msg['from']
    print 'Subject: %s' % msg['subject']
    return None



