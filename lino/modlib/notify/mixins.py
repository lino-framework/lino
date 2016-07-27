# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.api import dd, rt, _
from lino.utils.xmlgen.html import E


class ChangeObservable(dd.Model):
    
    """
    Mixin for models which can "emit notifications" and define a list
    "observers" to be notified when an instance is modified.

    """

    class Meta(object):
        abstract = True

    def get_notify_subject(self, ar):
        return _("{user} modified {obj}").format(
            user=ar.get_user(), obj=self)

    def get_notify_body(self, ar):
        return E.tostring(E.p(
            _("{user} modified ").format(user=ar.get_user()),
            ar.obj2html(self),
            E.p("TODO: include a summary of the modifications.")))

    def get_notify_owner(self, ar):
        return self

    def get_change_observers(self):
        """Override this in subclasses to yield a list of users who are
        observing changes on this object.

        """
        return []

    # def emit_notification(self, ar, owner, subject, body):
    #     return super(ChangeObservable, self).emit_notification(
    #         ar, owner, subject, body, self.get_notify_observers())

    def after_ui_save(self, ar, cw):

        super(ChangeObservable, self).after_ui_save(ar, cw)

        subject = self.get_notify_subject(ar)
        body = self.get_notify_body(ar)
        owner = self.get_notify_owner(ar)
        # self.emit_notification(ar, owner, subject, body)
        emit = rt.models.notify.Notification.emit_notification
        emit(ar, owner, subject, body, self.get_change_observers())

        
