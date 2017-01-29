# -*- coding: UTF-8 -*-

import logging

logger = logging.getLogger(__name__)

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt
from lino.core import layouts
from lino.core import fields
from lino.core import actions


class NotifyingAction(actions.Action):
    """An action which pops up a dialog window of three fields "Summary",
    "Description" and a checkbox "Don't notify others" to optionally
    suppress notification.

    Screenshot of a notifying action:

    .. image:: /images/screenshots/reception.CheckinVisitor.png
        :scale: 50

    Dialog fields:

    .. attribute:: subject
    .. attribute:: body
    .. attribute:: silent

    """
    custom_handler = True

    parameters = dict(
        notify_subject=models.CharField(
            _("Summary"), blank=True, max_length=200),
        notify_body=dd.RichTextField(_("Description"), blank=True),
        notify_silent=models.BooleanField(
            _("Don't notify others"), default=False),
    )

    params_layout = dd.Panel("""
    notify_subject
    notify_body
    notify_silent
    """, window_size=(50, 15))

    def get_notify_subject(self, ar, obj):
        """
        Return the default value of the `notify_subject` field.
        """
        return None

    def get_notify_body(self, ar, obj):
        """
        Return the default value of the `notify_body` field.
        """
        return None

    def action_param_defaults(self, ar, obj, **kw):
        kw = super(NotifyingAction, self).action_param_defaults(ar, obj, **kw)
        if obj is None:
            raise Exception("2017129 called without obj")
        if obj is not None:
            s = self.get_notify_subject(ar, obj)
            if s is not None:
                kw.update(notify_subject=s)
            s = self.get_notify_body(ar, obj)
            if s is not None:
                kw.update(notify_body=s)
        return kw

    def run_from_ui(self, ar, **kw):
        # raise Exception("20170128a {}".format(ar.action_param_values))
        ar.set_response(message=ar.action_param_values.notify_subject)
        ar.set_response(refresh=True)
        ar.set_response(success=True)
        if not ar.action_param_values.notify_silent:
            for obj in ar.selected_rows:
                self.emit_message(ar, obj)

    def emit_message(self, ar, obj, **kw):
        owner = self.get_notify_owner(ar, obj)
        recipients = self.get_notify_recipients(ar, obj)
        mt = rt.models.notify.MessageTypes.action
        pv = ar.action_param_values
        def msg(user, mm):
            if not pv.notify_subject:
                return None
            return (pv.notify_subject, pv.notify_body)
        rt.models.notify.Message.emit_message(
            ar, owner, mt, msg, recipients)

    def get_notify_owner(self, ar, obj):
        """Expected to return the :attr:`owner
        lino.modlib.notify.models.Message.owner>` of the message.

        The default returns `None`.

        `ar` is the action request, `obj` the object on which the
        action is running,

        """
        return None

    def get_notify_recipients(self, ar, obj):
        """Yield a list of users to be notified.

        `ar` is the action request, `obj` the object on which the
        action is running, 

        """
        return []

        
