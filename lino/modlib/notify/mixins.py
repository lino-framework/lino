# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

from builtins import str
from django.conf import settings
from lino.api import dd, rt, _
from lino.utils.xmlgen.html import E


class ChangeObservable(dd.Model):
    """Mixin for models which can emit notifications to a list of
    "observers" when an instance is modified.

    """

    class Meta(object):
        abstract = True

    def get_change_subject(self, ar, cw):
        ctx = dict(user=ar.get_user())
        if cw is None:
            msg = _("has been created by {user}").format(**ctx)
            return "{} {}".format(self, msg)
        if len(list(cw.get_updates())) == 0:
            return
        msg = _("has been modified by {user}").format(**ctx)
        return "{} {}".format(self, msg)
            
            
    def get_change_body(self, ar, cw):
        """Returns the text of the notification message to emit.

        The default implementation returns a message of style
        "{object} has been modified by {user}" followed by a summary
        of the changes.  

        Application code can override this. Returning None or an empty
        string means to suppress notification.

        """
        if cw is None:
            elems = [E.p(
                ar.obj2memo(self),
                ' ', _("has been created by {user}").format(
                    user=ar.get_user()))]
        else:
            items = list(cw.get_updates_html())
            if len(items) == 0:
                return
            elems = [E.p(
                ar.obj2memo(self),
                ' ', _("has been modified by {user}").format(
                    user=ar.get_user()),
                ":")]
            elems.append(E.ul(*items))
        return E.tostring(E.div(*elems))

    def get_change_owner(self, ar):
        """Return the owner (the database object we are talking about) of the
        notification to emit. When a user has already an unseen
        notification about a given owner, then Lino ignores all
        subsequent notifications with that owner.

        For example
        :class:`lino_welfare.modlib.pcsw.coaching.Coaching` returns
        the coaching's client as owner in order to avoid multiple
        messages.

        """
        return self

    def get_change_observers(self):
        """Return or yield a list of `(user, mail_mode)` tuples who are
        observing changes on this object.

        Should be implemented in subclasses. The default
        implementation returns an empty list, i.e. nobody gets
        notified.

        """
        return []

    def after_ui_save(self, ar, cw):
        """Emits notification about the change to every watcher."""
        super(ChangeObservable, self).after_ui_save(ar, cw)

        def msg(user, mm):
            subject = self.get_change_subject(ar, cw)
            if not subject:
                return None
            return (subject, self.get_change_body(ar, cw))
            
        owner = self.get_change_owner(ar)
        mt = rt.actors.notify.MessageTypes.change
        rt.models.notify.Message.emit_message(
            ar, owner, mt, msg, self.get_change_observers())
