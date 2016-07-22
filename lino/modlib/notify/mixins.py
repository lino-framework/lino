# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.api import dd, rt, _
from lino.utils.xmlgen.html import E


class Observable(dd.Model):
    """Mixin for models which can "emit notifications" and define a list
    "observers" to be notified when a notification is emitted.

    """

    class Meta(object):
        abstract = True

    def get_notify_observers(self):
        """Override this in subclasses to yield a list of users who are
        observing this object.

        """
        return []

    def emit_notification(self, ar, owner, subject, body):
        """Create one notification for every observer."""
        # dd.logger.info("20160717 %s emit_notifications()", self)
        others = set()
        for user in self.get_notify_observers():
            if user and user != ar.user:
                others.add(user)

        if len(others):
            dd.logger.info(
                "Notify %s users that %s", len(others), subject)
            notify = rt.models.notify.Notification.create_notification
            for user in others:
                notify(ar, user, owner, subject=subject, body=body)


class ChangeObservable(Observable):
    
    """An :class:`Observable` which automatically emits notifications when
    a database object is modified.

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

    def after_ui_save(self, ar, cw):

        super(ChangeObservable, self).after_ui_save(ar, cw)

        subject = self.get_notify_subject(ar)
        body = self.get_notify_body(ar)
        owner = self.get_notify_owner(ar)
        self.emit_notification(ar, owner, subject, body)

        
