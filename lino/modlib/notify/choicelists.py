# -*- coding: UTF-8 -*-
# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Choicelists for this plugin.

"""
from __future__ import unicode_literals
# from builtins import str

from lino.api import dd, _, pgettext


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

    .. attribute:: silent

        Disable notifications for this user.

    .. attribute:: never

        Notify in Lino but never send email.


    """
    verbose_name = _("Notification mode")
    verbose_name_plural = _("Notification modes")
    
add = MailModes.add_item
add('silent', _("Silent"), 'silent')
add('never', _("No mails"), 'never')
# add('immediately', _("Immediately"), 'immediately')  # obsolete
add('often', _("Mail often"), 'often')
add('daily', _("Daily email digest"), 'daily')
add('weekly', _("Weekly email digest"), 'weekly')  # not yet implemented
