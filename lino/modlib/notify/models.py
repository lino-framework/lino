# -*- coding: UTF-8 -*-
# Copyright 2011-2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for this plugin.

A notification is a message to be sent to a given user about a given
database object. Lino


.. xfile:: notify/body.eml

    The Jinja template to use for generating the body of the
    notification email.

    Available context variables:

    :obj:  The :class:`Notification` object
    :E:    The html namespace :mod:`lino.utils.xmlgen.html`
    :rt:   The runtime API :mod:`lino.api.rt`
    :ar:   The action request which caused the notification. a
           :class:`BaseRequest <lino.core.requests.BaseRequest>`)

"""
from builtins import str
from builtins import object

from django.db import models
from django.conf import settings
from django.utils import timezone

from lino.api import dd, rt, _

from lino.core.roles import SiteStaff
from lino.core.gfks import gfk2lookup
from lino.core.requests import BaseRequest

from lino.mixins import Created
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.users.mixins import UserAuthored, My
from .utils import body_subject_to_elems

from lino.utils.xmlgen.html import E
from lino.utils import join_elems

from datetime import timedelta
try:
    import schedule
except ImportError as e:
    dd.logger.warning("schedule not installed (%s)", e)
    schedule = False


# @dd.python_2_unicode_compatible
class Notification(UserAuthored, Controllable, Created):
    """A **notification** object represents the fact that a given user has
    been notified about a given database object.
    
    Use the class method :meth:`notify` to create a new notification
    (and to skip creation in case that user has already been notified
    about that object)

    .. attribute:: subject
    .. attribute:: body
    .. attribute:: user
    .. attribute:: owner
    .. attribute:: created
    .. attribute:: sent
    .. attribute:: seen
    
    """
    class Meta(object):
        app_label = 'notify'
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    seen = models.DateTimeField(_("seen"), null=True, editable=False)
    sent = models.DateTimeField(_("sent"), null=True, editable=False)
    # message = models.TextField(_("Message"), editable=False)
    subject = models.CharField(_("Subject"), max_length=250, editable=False)
    body = models.TextField(_("Body"), editable=False)

    # def __str__(self):
    #     return _("About {0}").format(self.owner)
        # return self.message
        # return _("Notify {0} about change on {1}").format(
        #     self.user, self.owner)

    @classmethod
    def notify(cls, ar, user, owner=None, **kwargs):
        """Create a notification unless that user has already been notified
        about that object.

        Does not send an email because that might skiw down response
        time.

        """
        fltkw = gfk2lookup(cls.owner, owner)
        qs = cls.objects.filter(
            user=user, seen__isnull=True, **fltkw)
        if not qs.exists():
            obj = cls(user=user, owner=owner, **kwargs)
            obj.full_clean()
            obj.save()

    @dd.displayfield()
    def overview(self, ar):
        if ar is None:
            return ''
        return self.get_overview(ar)

    def get_overview(self, ar):
        """Return the content to be displayed in the :attr:`overview` field.
        On interactive rendererers (extjs, bootstrap3) the `obj` and
        `user` are clickable.

        This is also used from the :xfile:`notify/body.eml` template
        where they should just be surrounded by **double asterisks**
        so that Thunderbird displays them bold.

        """
        elems = body_subject_to_elems(ar, self.subject, self.body)
        return E.div(*elems)
        # context = dict(
        #     obj=ar.obj2str(self.owner),
        #     user=ar.obj2str(self.user))
        # return _(self.message).format(**context)
        # return E.p(
        #     ar.obj2html(self.owner), " ",
        #     _("was modified by {0}").format(self.user))

    def send_email(self):
        """"""
        if not self.user.email:
            dd.logger.info("User %s has no email address", self.user)
            return
        # dd.logger.info("20151116 %s %s", ar.bound_action, ar.actor)
        # ar = ar.spawn_request(renderer=dd.plugins.bootstrap3.renderer)
        # sar = BaseRequest(
        #     # user=self.user, renderer=dd.plugins.bootstrap3.renderer)
        #     user=self.user, renderer=settings.SITE.kernel.text_renderer)
        # tpl = dd.plugins.notify.email_subject_template
        # subject = tpl.format(obj=self)
        subject = settings.EMAIL_SUBJECT_PREFIX + self.subject
        # template = rt.get_template('notify/body.eml')
        # context = dict(obj=self, E=E, rt=rt, ar=sar)
        # body = template.render(**context)

        template = rt.get_template('notify/body.eml')
        context = dict(obj=self, E=E, rt=rt)
        body = template.render(**context)

        sender = settings.SERVER_EMAIL
        rt.send_email(subject, sender, body, [self.user.email])
        self.sent = timezone.now()
        self.save()
    
    @dd.action()
    def do_send_email(self, ar):
        self.send_email()

dd.update_field(Notification, 'user',
                verbose_name=_("Recipient"), editable=False)
Notification.update_controller_field(null=True, blank=True)


class Notifications(dd.Table):
    "Base for all tables of notifications."
    model = 'notify.Notification'
    column_names = "created subject user seen sent *"

    detail_layout = dd.DetailLayout("""
    created user seen sent
    overview
    """, window_size=(50, 15))

    # detail_layout = """
    # overview
    # notify.ChangesByNotification
    # """

    @classmethod
    def get_detail_title(self, ar, obj):
        if obj.seen is None and obj.user == ar.get_user():
            obj.seen = timezone.now()
            obj.save()
            # dd.logger.info("20151115 Marked %s as seen", obj)
        return super(Notifications, self).get_detail_title(ar, obj)


class AllNotifications(Notifications):
    """The gobal list of all notifications.

    """
    required_roles = dd.required(SiteStaff)


class MyNotifications(My, Notifications):
    required_roles = dd.required()


def welcome_messages(ar):
    """Yield messages for the welcome page."""

    Notification = rt.models.notify.Notification
    qs = Notification.objects.filter(user=ar.get_user(), seen__isnull=True)
    if qs.count() > 0:
        chunks = [
            str(_("You have %d unseen notifications: ")) % qs.count()]
        chunks += join_elems([
            ar.obj2html(obj, obj.subject) for obj in qs])
        yield E.span(*chunks)

dd.add_welcome_handler(welcome_messages)


if schedule:

    def send_pending_emails():
        Notification = rt.models.notify.Notification
        qs = Notification.objects.filter(sent__isnull=True)
        if qs.count() > 0:
            dd.logger.info(
                "Send out emails for %d notifications.", qs.count())
            for obj in qs:
                obj.send_email()
        # else:
        #     dd.logger.info("No unsent notifications.")

    if settings.EMAIL_HOST and not settings.EMAIL_HOST.endswith('example.com'):
        dd.logger.debug(
            "Send pending notifications via %s", settings.EMAIL_HOST)
        schedule.every(10).seconds.do(send_pending_emails)
    else:
        dd.logger.debug(
            "Won't send pending notifications because EMAIL_HOST is empty")

    def clear_seen_notifications():
        """Delete notifications older than 24 hours that have been seen.

        """
        remove_after = 24
        Notification = rt.models.notify.Notification
        qs = Notification.objects.filter(
            seen__isnull=False,
            seen_lt=timezone.now()-timedelta(hours=remove_after))
        if qs.count() > 0:
            dd.logger.info(
                "Removing %d notifications older than %d hours.",
                qs.count(), remove_after)
            qs.delete()

    schedule.every().day.do(clear_seen_notifications)


