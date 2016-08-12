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
from __future__ import unicode_literals
from builtins import str
from builtins import object

from django.db import models
from django.conf import settings
from django.utils import timezone

from lino.api import dd, rt, _

from lino.core.roles import SiteStaff
from lino.core.gfks import gfk2lookup
from lino.core.requests import BaseRequest

from lino.mixins import Created, ObservedPeriod
from lino.modlib.gfks.mixins import Controllable
from lino.modlib.users.mixins import UserAuthored, My
from .utils import body_subject_to_elems

from lino.utils.xmlgen.html import E
from lino.utils import join_elems

from datetime import timedelta


class MarkSeen(dd.Action):
    label = _("Seen")
    show_in_bbar = False
    show_in_workflow = True
    button_text = "✓"  # u"\u2713"

    def get_action_permission(self, ar, obj, state):
        if obj.seen:
            return False
        return super(MarkSeen, self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar):
        for obj in ar.selected_rows:
            obj.seen = timezone.now()
            obj.save()
        ar.success(refresh_all=True)
        

# @dd.python_2_unicode_compatible
class Notification(UserAuthored, Controllable, Created):
    """A **notification** object represents the fact that a given user has
    been notified about a given database object.
    
    Use the class method :meth:`create_notification` to create a new
    notification (and to skip creation in case that user has already
    been notified about that owner)

    .. attribute:: subject
    .. attribute:: body
    .. attribute:: user
    .. attribute:: owner
 
       The database object this message is about.
       This field is labelled `About`.

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
    def emit_notification(cls, ar, owner, subject, body, recipients):
        """Create one notification for every recipient."""
        # dd.logger.info("20160717 %s emit_notifications()", self)
        others = set()
        for user in recipients:
            if user and user != ar.user:
                others.add(user)

        if len(others):
            dd.logger.info(
                "Notify %s users that %s", len(others), subject)
            for user in others:
                cls.create_notification(
                    ar, user, owner, subject=subject, body=body)

    @classmethod
    def create_notification(cls, ar, user, owner=None, **kwargs):
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
            # debug level because we don't want to see this message
            # every 10 seconds:
            dd.logger.debug("User %s has no email address", self.user)
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
    
    @dd.action(label=_("Send e-mail"),
               show_in_bbar=False, show_in_workflow=True,
               button_text="✉")  # u"\u2709"
    def do_send_email(self, ar):
        self.send_email()

    # @dd.action(label=_("Seen"),
    #            show_in_bbar=False, show_in_workflow=True,
    #            button_text="✓")  # u"\u2713"
    # def mark_seen(self, ar):
    #     self.seen = timezone.now()
    #     self.save()
    #     ar.success(refresh_all=True)

    mark_seen = MarkSeen()


dd.update_field(Notification, 'user',
                verbose_name=_("Recipient"), editable=False)
Notification.update_controller_field(
    null=True, blank=True, verbose_name=_("About"))


class Notifications(dd.Table):
    "Base for all tables of notifications."
    model = 'notify.Notification'
    column_names = "created subject user seen sent *"

    detail_layout = dd.DetailLayout("""
    created user seen sent owner
    overview
    """, window_size=(50, 15))

    parameters = ObservedPeriod(
        user=dd.ForeignKey(
            settings.SITE.user_model,
            blank=True, null=True),
        show_seen=dd.YesNo.field(_("Seen"), blank=True),
    )

    params_layout = "user show_seen start_date end_date"

    @classmethod
    def get_simple_parameters(cls):
        s = super(Notifications, cls).get_simple_parameters()
        s.add('user')
        return s

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Notifications, self).get_request_queryset(ar)
        pv = ar.param_values

        if pv.show_seen == dd.YesNo.yes:
            qs = qs.filter(seen__isnull=False)
        elif pv.show_seen == dd.YesNo.no:
            qs = qs.filter(seen__isnull=True)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Notifications, self).get_title_tags(ar):
            yield t
        pv = ar.param_values
        if pv.show_seen:
            yield unicode(pv.show_seen)

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
    # label = _("My notifications")
    required_roles = dd.required()
    column_names = "created subject owner sent workflow_buttons *"
    order_by = ['created']
    # filter = models.Q(seen__isnull=True)

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyNotifications, self).param_defaults(ar, **kw)
        kw.update(show_seen=dd.YesNo.no)
        return kw

    @classmethod
    def get_welcome_messages(cls, ar, **kw):
        sar = ar.spawn(cls)
        count = sar.get_total_count()
        if count > 0:
            msg = _("You have %d unseen notifications.") % count
            yield ar.href_to_request(sar, msg)


# def welcome_messages(ar):
#     """Yield messages for the welcome page."""

#     Notification = rt.models.notify.Notification
#     qs = Notification.objects.filter(user=ar.get_user(), seen__isnull=True)
#     if qs.count() > 0:
#         chunks = [
#             str(_("You have %d unseen notifications: ")) % qs.count()]
#         chunks += join_elems([
#             ar.obj2html(obj, obj.subject) for obj in qs])
#         yield E.span(*chunks)

# dd.add_welcome_handler(welcome_messages)


@dd.schedule_often()
def send_pending_emails():
    h = settings.EMAIL_HOST
    if not h or h.endswith('example.com'):
        dd.logger.debug(
            "Won't send pending notifications because EMAIL_HOST is %r",
            h)
        return
    Notification = rt.models.notify.Notification
    qs = Notification.objects.filter(sent__isnull=True)
    if qs.count() > 0:
        dd.logger.debug(
            "Send out emails for %d notifications.", qs.count())
        for obj in qs:
            obj.send_email()
    else:
        dd.logger.debug("No unsent notifications.")


@dd.schedule_daily()
def clear_seen_notifications():
    """Delete notifications older than 24 hours that have been seen.

    """
    remove_after = 24
    Notification = rt.models.notify.Notification
    qs = Notification.objects.filter(
        seen__isnull=False,
        seen__lt=timezone.now()-timedelta(hours=remove_after))
    if qs.count() > 0:
        dd.logger.info(
            "Removing %d notifications older than %d hours.",
            qs.count(), remove_after)
        qs.delete()

