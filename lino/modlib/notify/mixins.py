# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.api import dd, rt, _
from lino.utils.xmlgen.html import E


class Observable(dd.Model):
    
    """Mixin for models which can have observers to be notified about
    modifications in a database object.

    """

    class Meta(object):
        abstract = True

    def get_notify_observers(self):
        """Override this in subclasses to yield a list of users who are
        observing this object.

        """
        return []

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

        super(Observable, self).after_ui_save(ar, cw)

        others = set()
        for user in self.get_notify_observers():
            if user and user != ar.get_user():
                others.add(user)

        if len(others):
            subject = self.get_notify_subject(ar)
            body = self.get_notify_body(ar)
            owner = self.get_notify_owner(ar)
            dd.logger.info(
                "Notify %s users that %s", len(others), subject)
            notify = rt.models.notify.Notification.notify
            for user in others:
                notify(ar, user, owner, subject=subject, body=body)

        
