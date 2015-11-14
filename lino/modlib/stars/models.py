# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.stars`.

"""

from django.db import models
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
        verbose_name = _("Star")
        verbose_name_plural = _("Stars")

    star = dd.ForeignKey('stars.Star', editable=False)
    change = dd.ForeignKey('changes.Change', editable=False)
    seen = models.DateTimeField(
        _("seen"), null=True, editable=False)


class Notifications(dd.Table):
    model = 'stars.Notification'


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
    Star = rt.modules.stars.Star

    qs = Star.objects.filter(user=ar.get_user())
    if qs.count() > 0:
        chunks = [unicode(_("Your stars are "))]
        chunks += join_elems([ar.obj2html(obj.owner) for obj in qs])
        yield E.span(*chunks)

dd.add_welcome_handler(welcome_messages)


from lino.modlib.changes.models import Change
from django.db.models.signals import post_save


@dd.receiver(post_save, sender=Change)
def notify_handler(sender, **kwargs):
    self = sender
    star = rt.modules.stars.Star.objects.get(user=self.user, owner=self.owner)
    Notification = rt.modules.stars.Notification
    qs = Notification.objects.filter(
        change__owner=self.owner, star=star, seen__isnull=True)
    if not qs.exists():
        Notification(change=self, star=star, seen=False).save()
    
