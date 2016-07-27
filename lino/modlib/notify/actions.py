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
    """An action with a generic dialog window of three fields "Summary",
    "Description" and a checkbox "Don't send email notification".

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
        notify_body=fields.RichTextField(_("Description"), blank=True),
        notify_silent=models.BooleanField(
            _("Don't send email notification"), default=False),
    )

    params_layout = layouts.Panel("""
    notify_subject
    notify_body
    notify_silent
    """, window_size=(50, 15))

    def get_notify_owner(self, obj):
        return obj

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

    def get_notify_recipients(self, ar, owner):
        """Yield a list of users to be notified.

        """
        return []

    def action_param_defaults(self, ar, obj, **kw):
        kw = super(NotifyingAction, self).action_param_defaults(ar, obj, **kw)
        if obj is not None:
            s = self.get_notify_subject(ar, obj)
            if s is not None:
                kw.update(notify_subject=s)
            s = self.get_notify_body(ar, obj)
            if s is not None:
                kw.update(notify_body=s)
        return kw

    def run_from_ui(self, ar, **kw):
        ar.set_response(message=ar.action_param_values.notify_subject)
        ar.set_response(refresh=True)
        ar.set_response(success=True)
        if not ar.action_param_values.notify_silent:
            self.emit_notification(ar)

    def emit_notification(self, ar, **kw):
        # body = _("""%(user)s executed the following action:\n%(body)s
        # """) % dict(user=ar.get_user(),body=body)
        obj = ar.selected_rows[0]
        owner = self.get_notify_owner(obj)
        recipients = self.get_notify_recipients(ar, owner)
        rt.models.notify.Notification.emit_notification(
            ar, owner,
            ar.action_param_values.notify_subject,
            ar.action_param_values.notify_body, recipients)


