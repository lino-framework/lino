# -*- coding: UTF-8 -*-

from django.db import models

from lino.api import dd, rt, _
from lino.core import actions


class NotifyingAction(actions.Action):
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
        return None

    def get_notify_body(self, ar, obj):
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
        mt = self.get_notify_message_type()
        if mt is None:
            return
        pv = ar.action_param_values
        
        m = getattr(obj, 'emit_system_note', None)
        if m is not None:
            m(ar, subject=pv.notify_subject, body=pv.notify_body)
        
        recipients = self.get_notify_recipients(ar, obj)
        def msg(user, mm):
            if not pv.notify_subject:
                return None
            return (pv.notify_subject, pv.notify_body)
        rt.models.notify.Message.emit_notification(
            ar, owner, mt, msg, recipients)

    def get_notify_message_type(self):
        return rt.models.notify.MessageTypes.change
    
    def get_notify_owner(self, ar, obj):
        return None

    def get_notify_recipients(self, ar, obj):
        return []

        
