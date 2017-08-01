# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Choicelists for this plugin.

"""
from __future__ import unicode_literals
# from builtins import str
from builtins import object
import json

from django.db import models
from django.conf import settings
from django.utils import timezone

from lino.api import dd, rt, _, pgettext

from lino.core.roles import SiteStaff
from lino.core.gfks import gfk2lookup
from lino.core.requests import BaseRequest
from lino.core.site import html2text

from lino.mixins import Created, ObservedDateRange
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.users.mixins import UserAuthored, My
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino.mixins.bleached import body_subject_to_elems

from lino.utils.xmlgen.html import E
from lino.utils import join_elems

class MessageTypes(dd.ChoiceList):
    """
    The list of possible choices for the `message_type` field
    of a :class:`Message`.
    """
    verbose_name = _("Message Type")
    verbose_name_plural = _("Message Types")


add = MessageTypes.add_item
add('100', _("System event"), 'system')
add('200', pgettext("message type", "Change"), 'change')
add('300', _("Action"), 'action')
# add('300', _("Warning"), 'warning')
# add('400', _("Note"), 'note')
# add('900', _("Notification"), 'notification')



class MailModes(dd.ChoiceList):
    """How the system should send email notifications to a user.

    """
    verbose_name = _("Email notification mode")
    verbose_name_plural = _("Email notification modes")
    
add = MailModes.add_item
add('never', _("Never"), 'never')
# add('immediately', _("Immediately"), 'immediately')  # obsolete
add('often', _("Often"), 'often')
add('daily', _("Daily"), 'daily')
add('weekly', _("Weekly"), 'weekly')  # not yet implemented
