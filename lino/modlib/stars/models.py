# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.stars`.

"""

import datetime

from django.db import models
from django.conf import settings

from lino.api import dd, rt, _


from lino.core.utils import gfk2lookup

from lino.modlib.gfks.mixins import Controllable
from lino.modlib.users.mixins import UserAuthored, ByUser


class Star(UserAuthored, Controllable):
    """Represents the fact that a given database object is starred by a
    given User.

    .. attribute:: owner

        The starred database object

    .. attribute:: user

        The starring user (pointer to :class:lino.modlib.users.models.User`

    """

    controller_is_optional = False

    class Meta:
        verbose_name = _("Star")
        verbose_name_plural = _("Stars")

    @classmethod
    def for_obj(cls, obj, **kwargs):
        """Return a queryset of :class:`Star` instances for the given database
        object.

        """
        return cls.objects.filter(**gfk2lookup(cls.owner, obj, **kwargs))


def get_favourite(obj, user):
    if user.authenticated:
        qs = rt.modules.stars.Star.for_obj(obj, user=user)
        if qs.count() == 0:
            return None
        return qs[0]


class Stars(dd.Table):
    model = 'stars.Star'


class MyStars(Stars, ByUser):
    pass


class Notification(dd.Model):
    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    star = dd.ForeignKey('stars.Star', editable=False)
    change = dd.ForeignKey('changes.Change', editable=False)
    seen = models.DateTimeField(
        _("seen"), null=True, editable=False)

    def __unicode__(self):
        return _("Notify {0} about change on {1}").format(
            self.star.user, self.star.owner)

    def send_email(self, ar):
        subject = unicode(self)
        template = rt.get_template('stars/Notification/body.eml')
        context = dict(ar=ar, obj=self, E=E)
        body = template.render(**context)
        sender = self.star.user.email or settings.SERVER_EMAIL
        rt.send_email(
            subject, sender, body, [self.star.user.email])
    

class Notifications(dd.Table):
    """Shows the gobal list of all notifications.
    
    """
    model = 'stars.Notification'
    column_names = "overview change__time star__user seen"

    detail_layout = """
    overview
    stars.ChangesByNotification
    """

    @classmethod
    def get_detail_title(self, ar, obj):
        if obj.seen is None and obj.star.user == ar.get_user():
            obj.seen = datetime.datetime.now()
            obj.save()
            dd.logger.info("20151115 marked %s as seen", obj)
        return super(Notifications, self).get_detail_title(ar, obj)

    @dd.displayfield()
    def overview(cls, self, ar):
        return E.p(
            ar.obj2html(self.star.owner), " ",
            _("was modified by {0}").format(self.change.user))


class StarObject(dd.Action):
    sort_index = 100
    # label = "*"
    label = u"☆"  # 2606
    help_text = _("Star this database object.")
    show_in_workflow = True
    show_in_bbar = False
    required_roles = dd.login_required()

    def get_action_permission(self, ar, obj, state):
        star = get_favourite(obj, ar.get_user())
        if star is not None:
            return False
        return super(StarObject, self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        Star = rt.modules.stars.Star
        Star(owner=obj, user=ar.get_user()).save()
        ar.success(
            _("{0} is now starred.").format(obj), refresh_all=True)


class UnstarObject(dd.Action):
    sort_index = 100
    # label = "-"
    label = u"★"  # 2605

    help_text = _("Unstar this database object.")
    show_in_workflow = True
    show_in_bbar = False

    def get_action_permission(self, ar, obj, state):
        star = get_favourite(obj, ar.get_user())
        if star is None:
            return False
        return super(UnstarObject, self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        star = get_favourite(obj, ar.get_user())
        star.delete()
        ar.success(
            _("{0} is no longer starred.").format(obj), refresh_all=True)


dd.Model.star_object = StarObject()
dd.Model.unstar_object = UnstarObject()


from lino.utils.xmlgen.html import E
from lino.utils import join_elems


def welcome_messages(ar):
    """Yield messages for the welcome page."""
    # Star = rt.modules.stars.Star
    # qs = Star.objects.filter(user=ar.get_user())
    # if qs.count() > 0:
    #     chunks = [unicode(_("Your stars are "))]
    #     chunks += join_elems([ar.obj2html(obj.owner) for obj in qs])
    #     yield E.span(*chunks)

    Notification = rt.modules.stars.Notification
    qs = Notification.objects.filter(
        star__user=ar.get_user(), seen__isnull=True)
    if qs.count() > 0:
        chunks = [
            unicode(_("You have %d unseen notifications: ")) % qs.count()]
        chunks += join_elems([
            ar.obj2html(obj, unicode(obj.star.owner)) for obj in qs])
        yield E.span(*chunks)

dd.add_welcome_handler(welcome_messages)


from lino.modlib.changes.models import Change, ChangesByMaster
from django.db.models.signals import post_save


class ChangesByNotification(ChangesByMaster):

    master = 'stars.Notification'

    # @classmethod
    # def get_master_instance(self, ar, master, pk):
    #     notification = super(self).get_master_instance(ar, master, pk)
    #     if notification is None:
    #         return
    #     return notification.
        
    @classmethod
    def get_request_queryset(cls, ar):
        mi = ar.master_instance
        if mi is None:
            return cls.model.objects.null()
        return cls.model.objects.filter(
            time__gte=mi.change.time,
            **gfk2lookup(cls.model.master, mi.star.owner))


@dd.receiver(post_save, sender=Change)
def notify_handler(sender, instance=None, **kwargs):
    Notification = rt.modules.stars.Notification
    self = instance  # a Change object
    others = rt.modules.stars.Star.for_obj(self.master).exclude(user=self.user)
    ar = rt.login(self.user, renderer=settings.SITE.kernel.default_ui.renderer)
    for star in others:
        fltkw = dict()
        for k, v in gfk2lookup(Change.master, self.master).items():
            fltkw['change__'+k] = v
        qs = Notification.objects.filter(
            star=star, seen__isnull=True, **fltkw)
        if not qs.exists():
            # create a notification object and send email
            obj = Notification(change=self, star=star)
            obj.full_clean()
            obj.save()
            obj.send_email(ar)

