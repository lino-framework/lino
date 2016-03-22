# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.notifier`.

A notification is a message to be sent to a given user about a given
database object. Lino


.. xfile:: notifier/body.eml

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

from lino.utils.xmlgen.html import E
from lino.utils import join_elems


@dd.python_2_unicode_compatible
class Notification(UserAuthored, Controllable, Created):
    """A **notification** object represents the fact that a given user has
    been notified about a given database object.
    
    Use the class method :meth:`notify` to create a new notification
    (and to skip creation in case that user has already been notified
    about that object)

    .. attribute:: message
    
        The message to display. This should be a plain string which
        will be formatted (using standard string format) using the
        following context:

        :obj:  the object attached to this notification
        :user: the user who caused this notification

    .. attribute:: overview

        A display field which returns the parsed :attr:`message`.

    """
    class Meta(object):
        app_label = 'notifier'
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    seen = models.DateTimeField(_("seen"), null=True, editable=False)
    message = models.TextField(_("Message"), editable=False)

    def __str__(self):
        return _("About {0}").format(self.owner)
        # return self.message
        # return _("Notify {0} about change on {1}").format(
        #     self.user, self.owner)

    @classmethod
    def notify(cls, ar, owner, user, message):
        """Create a notification unless that user has already been notified
        about that object.


        """
        fltkw = gfk2lookup(cls.owner, owner)
        qs = cls.objects.filter(
            user=user, seen__isnull=True, **fltkw)
        if not qs.exists():
            # create a notification object and send email
            obj = cls(user=user, owner=owner, message=message)
            obj.full_clean()
            obj.save()
            obj.send_email(ar)

    @dd.displayfield()
    def overview(self, ar):
        if ar is None:
            return ''
        return self.get_overview(ar)

    def get_overview(self, ar):
        """Return the content to be displayed in the :attr:`overview` field.
        On interactive rendererers (extjs, bootstrap3) the `obj` and
        `user` are clickable.

        This is also used from the :xfile:`notifier/body.eml` template
        where they should just be surrounded by **double asterisks**
        so that Thunderbird displays them bold.

        """
        context = dict(
            obj=ar.obj2str(self.owner),
            user=ar.obj2str(self.user))
        return _(self.message).format(**context)
        # return E.p(
        #     ar.obj2html(self.owner), " ",
        #     _("was modified by {0}").format(self.user))

    @dd.action()
    def send_email(self, ar):
        if not self.user.email:
            dd.logger.info("User %s has no email address", self.user)
            return
        # dd.logger.info("20151116 %s %s", ar.bound_action, ar.actor)
        # ar = ar.spawn_request(renderer=dd.plugins.bootstrap3.renderer)
        sar = BaseRequest(
            # user=self.user, renderer=dd.plugins.bootstrap3.renderer)
            user=self.user, renderer=settings.SITE.kernel.text_renderer)
        tpl = dd.plugins.notifier.email_subject_template
        subject = tpl.format(obj=self)
        subject = settings.EMAIL_SUBJECT_PREFIX + subject
        template = rt.get_template('notifier/body.eml')
        context = dict(obj=self, E=E, rt=rt, ar=sar)
        body = template.render(**context)
        sender_email = ar.get_user().email or settings.SERVER_EMAIL
        sender = "{0} <{1}>".format(ar.get_user(), sender_email)
        rt.send_email(
            subject, sender, body, [self.user.email])
    
dd.update_field(Notification, 'user', verbose_name=_("User"))


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
            obj.seen = timezone.now()
            obj.save()
            # dd.logger.info("20151115 Marked %s as seen", obj)
        return super(Notifications, self).get_detail_title(ar, obj)


class AllNotifications(Notifications):
    required_roles = dd.required(SiteStaff)


class MyNotifications(My, Notifications):
    required_roles = dd.required()


def welcome_messages(ar):
    """Yield messages for the welcome page."""

    Notification = rt.modules.notifier.Notification
    qs = Notification.objects.filter(user=ar.get_user(), seen__isnull=True)
    if qs.count() > 0:
        chunks = [
            str(_("You have %d unseen notifications: ")) % qs.count()]
        chunks += join_elems([
            ar.obj2html(obj, str(obj.owner)) for obj in qs])
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
                return cls.model.objects.none()
            return cls.model.objects.filter(
                time__gte=mi.created,
                **gfk2lookup(cls.model.master, mi.owner))

else:

    ChangesByNotification = None


