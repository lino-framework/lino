# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.notifier`.

A notification is a message to be sent to a given user about a given
database object. Lino

"""

import datetime

from django.db import models
from django.conf import settings

from lino.api import dd, rt, _


from lino.core.utils import gfk2lookup

from lino.mixins import Created
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.users.mixins import UserAuthored, My

from lino.utils.xmlgen.html import E
from lino.utils import join_elems


class Notification(UserAuthored, Controllable, Created):
    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    seen = models.DateTimeField(_("seen"), null=True, editable=False)
    message = models.TextField(_("Message"), editable=False)

    def __unicode__(self):
        return _("About {0}").format(self.owner)
        # return self.message
        # return _("Notify {0} about change on {1}").format(
        #     self.user, self.owner)

    @classmethod
    def notify(cls, ar, owner, user, message):
        fltkw = gfk2lookup(cls.owner, owner)
        qs = cls.objects.filter(
            user=user, seen__isnull=True, **fltkw)
        if not qs.exists():
            # create a notification object and send email
            obj = cls(user=user, owner=owner, message=message)
            obj.full_clean()
            obj.save()
            obj.send_email(ar)

    @dd.action()
    def send_email(self, ar):
        if not self.user.email:
            dd.logger.info("User %s has no email address", self.user)
            return
        tpl = dd.plugins.notifier.email_subject_template
        subject = tpl.format(obj=self)
        subject = settings.EMAIL_SUBJECT_PREFIX + subject
        template = rt.get_template('notifier/body.eml')
        context = dict(obj=self, E=E, rt=rt)
        body = template.render(**context)
        sender = ar.get_user().email or settings.SERVER_EMAIL
        rt.send_email(
            subject, sender, body, [self.user.email])
    

class Notifications(dd.Table):
    """Shows the gobal list of all notifications.

    """
    model = 'notifier.Notification'
    column_names = "created overview user seen *"

    detail_layout = """
    overview
    notifier.ChangesByNotification
    """

    @classmethod
    def get_detail_title(self, ar, obj):
        if obj.seen is None and obj.user == ar.get_user():
            obj.seen = datetime.datetime.now()
            obj.save()
            dd.logger.info("20151115 Marked %s as seen", obj)
        return super(Notifications, self).get_detail_title(ar, obj)

    @dd.displayfield()
    def overview(cls, self, ar):
        context = dict(
            obj=E.tostring(ar.obj2html(self.owner)),
            user=E.tostring(ar.obj2html(self.user)))
        return _(self.message).format(**context)
        # return E.p(
        #     ar.obj2html(self.owner), " ",
        #     _("was modified by {0}").format(self.user))


class MyNotifications(My, Notifications):
    pass


def welcome_messages(ar):
    """Yield messages for the welcome page."""

    Notification = rt.modules.notifier.Notification
    qs = Notification.objects.filter(user=ar.get_user(), seen__isnull=True)
    if qs.count() > 0:
        chunks = [
            unicode(_("You have %d unseen notifications: ")) % qs.count()]
        chunks += join_elems([
            ar.obj2html(obj, unicode(obj.owner)) for obj in qs])
        yield E.span(*chunks)

dd.add_welcome_handler(welcome_messages)


if dd.is_installed('changes'):

    from lino.modlib.changes.models import ChangesByMaster

    class ChangesByNotification(ChangesByMaster):

        master = 'notifier.Notification'

        @classmethod
        def get_request_queryset(cls, ar):
            mi = ar.master_instance
            if mi is None:
                return cls.model.objects.null()
            return cls.model.objects.filter(
                time__gte=mi.created,
                **gfk2lookup(cls.model.master, mi.owner))

else:

    ChangesByNotification = None


