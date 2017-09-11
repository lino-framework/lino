# -*- coding: UTF-8 -*-
# Copyright 2011-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""Model mixins for this plugin.

"""

from __future__ import unicode_literals
from builtins import object

import logging
logger = logging.getLogger(__name__)

from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from lino.api import dd

from lino.core.exceptions import ChangedAPI
from lino.core import model
from lino.core import actions
from lino.core import dbtables
from lino.core.roles import SiteUser, SiteStaff

from .roles import Helper, AuthorshipTaker


class TimezoneHolder(models.Model):
    class Meta(object):
        abstract = True

    if settings.USE_TZ:
        timezone = models.CharField(_("Time zone"), max_length=15, blank=True)
    else:
        timezone = dd.DummyField()

    @dd.chooser(simple_values=True)
    def timezone_choices(cls, partner):
        import pytz
        if partner and partner.country:
            return pytz.country_timezones[partner.country.isocode]
        return pytz.common_timezones


class Authored(dd.Model):
    class Meta(object):
        abstract = True

    # author_field_name = None
    
    manager_roles_required = dd.login_required(SiteStaff)

    def get_author(self):
        return self.user
        # return getattr(self, self.author_field_name)
    
    def set_author(self, user):
        raise NotImplementedError()
    
    def on_duplicate(self, ar, master):
        """The default behaviour after duplicating is to change the author to
        the user who requested the duplicate.

        """
        if ar.user is not None:
            self.set_author(ar.user)
        super(Authored, self).on_duplicate(ar, master)

    def get_row_permission(self, ar, state, ba):
        """Only "managers" can edit other users' work.

        See also :attr:`manager_roles_required`.

        """
        if not super(Authored, self).get_row_permission(ar, state, ba):
            return False
        user = ar.get_user()
        author = self.get_author()
        if author != ar.user \
           and (ar.subst_user is None or author != ar.subst_user) \
           and not user.user_type.has_required_roles(
               self.manager_roles_required):
            return ba.action.readonly
        return True

    @classmethod
    def on_analyze(cls, site):
        if hasattr(cls, 'manager_level_field'):
            raise ChangedAPI("{0} has a manager_level_field".format(cls))
        super(Authored, cls).on_analyze(site)

    # no longer needed after 20170826
    # @classmethod
    # def setup_parameters(cls, **fields):
    #     """Adds the :attr:`user` filter parameter field."""
    #     fld = cls._meta.get_field('user')
    #     fields.setdefault(
    #         'user', models.ForeignKey(
    #             'users.User', verbose_name=fld.verbose_name,
    #             blank=True, null=True))
    #     return super(Authored, cls).setup_parameters(**fields)

    @classmethod
    def get_simple_parameters(cls):
        for p in super(Authored, cls).get_simple_parameters():
            yield p
        yield 'user'  # cls.author_field_name)

    def get_print_language(self):
        u = self.get_author()
        if u is None or not u.language:
            return super(Authored, self).get_print_language()
        return u.language

    
class UserAuthored(Authored):
    class Meta(object):
        abstract = True

    workflow_owner_field = 'user'
    # author_field_name = 'user'    
    user = dd.ForeignKey(
        'users.User',
        verbose_name=_("Author"),
        related_name="%(app_label)s_%(class)s_set_by_user",
        blank=True, null=True)

    def set_author(self, user):
        self.user = user
        # setattr(self, self.author_field_name, user)
        
    def on_create(self, ar):
        """
        Adds the requesting user to the `user` field.

        When acting as another user, the default implementation
        still inserts the real user, not subst_user.
        This is important for cal.Event.
        """
        if self.user_id is None:
            u = ar.user
            if u is not None:
                self.user = u
        super(UserAuthored, self).on_create(ar)

    def get_timezone(self):
        """Return the author's timezone. Used by
        :class:`lino_xl.lib.cal.mixins.Started`.

        """
        if self.user_id is None:
            return settings.TIME_ZONE
        return self.user.timezone or settings.TIME_ZONE


AutoUser = UserAuthored  # old name for backwards compatibility


class My(dbtables.Table):
    """Mixin for tables on :class:`Authored` which sets the requesting
    user as default value for the :attr:`author` filter parameter.

    If the table's model does *not* inherit from :class:`Authored`,
    then it must define a parameter field named 'user' and a model
    attribute `user`.  This feature is used by
    :class:`lino_xl.lib.reception.models.MyWaitingVisitors`.

    Used by
    :mod:`lino_xl.lib.excerpts` and
    :mod:`lino_xl.lib.reception`.

    """

    @classmethod
    def get_actor_label(self):
        if self.model is None:
            return self._label or self.__name__
        return self._label or \
            _("My %s") % self.model._meta.verbose_name_plural

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(My, self).param_defaults(ar, **kw)
        # kw.update(user=ar.get_user())
        # k = self.author_field_name or self.model.author_field_name
        # kw[k] = ar.get_user()
        # kw[self.model.author_field_name] = ar.get_user()
        kw['user'] = ar.get_user()
        return kw


# class ByUser(dbtables.Table):
#     """Deprecated mixin for slave tables whose master is the requesting
#     user.

#     """
#     master_key = 'user'
#     #~ details_of_master_template = _("%(details)s of %(master)s")
#     details_of_master_template = _("%(details)s")

#     @classmethod
#     def get_actor_label(self):
#         if self.model is None:
#             return self._label or self.__name__
#         return self._label or \
#             _("My %s") % self.model._meta.verbose_name_plural

#     @classmethod
#     def setup_request(self, ar):
#         #~ logger.info("ByUser.setup_request")
#         if ar.master_instance is None:
#             u = ar.get_user()
#             if not isinstance(u, AnonymousUser):
#                 ar.master_instance = u
#         super(ByUser, self).setup_request(ar)

#     @classmethod
#     def get_view_permission(self, user_type):
#         if not user_type.has_required_roles([SiteUser]):
#             return False
#         return super(ByUser, self).get_view_permission(user_type)

# if settings.SITE.user_model is None:

#     # dummy Table for userless sites
#     ByUser = dbtables.Table


# class AuthorAction(actions.Action):
#     """Mixin for actions that are reserved to the author of the database
#     object.

#     """
#     manager_roles_required = dd.login_required(SiteStaff)

#     def get_action_permission(self, ar, obj, state):
#         user = ar.get_user()
#         if obj.user != user and \
#            not user.user_type.has_required_roles(self.manager_roles_required):
#             return self.readonly
#         return super(
#             AuthorAction, self).get_action_permission(ar, obj, state)

   
class AssignToMe(dd.Action):
    """Set yourself as assigned user.

    This will ask for confirmation and then set
    :attr:`Assignable.assigned_to`.

    """
    label = _("Assign to me")
    show_in_workflow = True
    # readonly = False
    required_roles = dd.login_required(Helper)

    # button_text = u"\u2698"  # FLOWER (⚘)
    # button_text = u"\u26d1"  # ⛑
    # button_text = u"\u261D"  # ☝
    button_text = u"\u270B"  # ✋
    
    # help_text = _("You become assigned to this.")

    # def get_action_permission(self, ar, obj, state):
    #     user = ar.get_user()
    #     if obj.assigned_to == user:
    #         return False
    #     if user == obj.get_author():
    #         return False
    #     return super(AssignToMe,
    #                  self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]

        def ok(ar):
            obj.assigned_to = ar.get_user()
            obj.save()
            ar.set_response(refresh=True)

        ar.confirm(ok, _("You become assigned to this."),
                   _("Are you sure?"))


class TakeAuthorship(dd.Action):
    """You declare to become the fully responsible user for this database
    object.

    Accordingly, this action is available only when you are not
    already fully responsible. You are fully responsible when (1)
    :attr:`Assignable.user` is set to *you* **and** (2)
    :attr:`Event.assigned_to` is *not empty*.

    Basically anybody can take any event, even if it is not assigned
    to them.

    New since 20160814 : I think that the Take action has never been
    really used. The original use case is when a user creates an
    apointment for their colleague: that colleague goes to assigned_to
    and is invited to "take" the appointment which has been agreed for
    him.

    """
    label = _("Take")
    show_in_workflow = True
    show_in_bbar = False
    
    # This action modifies the object, but we don't tell Lino about it
    # because we want that even non-manager users can run it on
    # objects authored by others.
    # readonly = False
    
    required_roles = dd.login_required(AuthorshipTaker)

    button_text = u"\u2691"

    # def get_action_permission(self, ar, obj, state):
    #     # new since 20160814
    #     if obj.get_author() == ar.get_user():
    #         return False
    #     # if obj.assigned_to != ar.get_user():
    #     #     return False
    #     # if obj.get_author() == ar.get_user():
    #     #     if obj.assigned_to is None:
    #     #         return False
    #     # elif obj.assigned_to != ar.get_user():
    #     #     return False
    #     return super(TakeAuthorship,
    #                  self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        # obj is an Assignable

        def ok(ar):
            obj.set_author(ar.get_user())
            # obj.user = ar.get_user()
            obj.assigned_to = None
            #~ kw = super(TakeAuthorship,self).run(obj,ar,**kw)
            obj.save()
            ar.set_response(refresh=True)

        ar.confirm(ok,
                   _("You take responsibility for {}.").format(obj),
                   _("Are you sure?"))


class Assignable(Authored):
    """.. attribute:: assigned_to

        This field is usually empty.  Setting it to another user means
        "I am not fully responsible for this item".

        This field is cleared when somebody calls
        :class:`TakeAuthorship` on the object.

    """

    class Meta(object):
        abstract = True

    assigned_to = dd.ForeignKey(
        settings.SITE.user_model,
        verbose_name=_("Assigned to"),
        related_name="%(app_label)s_%(class)s_set_assigned",
        blank=True, null=True)

    take = TakeAuthorship()
    assign_to_me = AssignToMe()

    def disabled_fields(self, ar):
        s = super(Assignable, self).disabled_fields(ar)
        user = ar.get_user()
        if self.assigned_to == user:
            s.add('assign_to_me')
        if user == self.get_author():
            s.add('assign_to_me')
            s.add('take')
        return s
    

    def on_create(self, ar):
        # 20130722 e.g. CreateClientEvent sets assigned_to it explicitly
        if self.assigned_to is None:
            self.assigned_to = ar.subst_user
        super(Assignable, self).on_create(ar)
    
