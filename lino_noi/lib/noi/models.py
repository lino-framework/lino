# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
#
# This file is part of Lino Noi.
#
# Lino Noi is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Noi is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Noi.  If not, see
# <http://www.gnu.org/licenses/>.

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



