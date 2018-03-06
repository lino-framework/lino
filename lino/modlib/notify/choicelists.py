# -*- coding: UTF-8 -*-
# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Choicelists for this plugin.

"""
from __future__ import unicode_literals
# from builtins import str

from atelier.utils import isidentifier

from lino.api import dd, _, pgettext


class MessageType(dd.Choice):
    #required_roles = set({})
    
    def __init__(self, value, text, **kwargs):
        if not isidentifier(value):
            raise Exception("{} not a valid identifier".format(value))
        super(MessageType, self).__init__(value, text, value, **kwargs)
        
    # def add_requirements(self, *args):
    #     """
    #     Add the specified user roles as requirements to this message type.
    #     """
    #     self.required_roles |= set(args)

class MessageTypes(dd.ChoiceList):
    """
    The list of possible choices for the `message_type` field
    of a :class:`Message`.
    """
    verbose_name = _("Message Type")
    verbose_name_plural = _("Message Types")
    item_class = MessageType

    # @classmethod
    # def register_type(cls, name, *args, **kwargs):
    #     cls.add_item_lazy(name, *args, **kwargs)


add = MessageTypes.add_item
add('system', _("System event"))
add('change', pgettext("message type", "Change"))
# add('300', _("Action"), 'action')
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
