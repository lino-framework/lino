# -*- coding: UTF-8 -*-
# Copyright 2011-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals
from builtins import object

from django.db import models

from django.utils.translation import ugettext_lazy as _
# from django.utils.translation import pgettext_lazy as pgettext
from django.utils.text import format_lazy
from django.conf import settings

from lino.api import dd, rt

from lino.core.exceptions import ChangedAPI
from lino.core import model
from lino.core import actions
from lino.core import dbtables
from lino.core.roles import SiteStaff
from lino.modlib.printing.mixins import Printable

from .roles import Helper, AuthorshipTaker



class Authored(Printable):
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
        if ar and ar.user:
            self.set_author(ar.user)
        super(Authored, self).on_duplicate(ar, master)

    def get_row_permission(self, ar, state, ba):
        """Only "managers" can edit other users' work.

        See also :attr:`manager_roles_required`.

        """
        if not super(Authored, self).get_row_permission(ar, state, ba):
            return False
        if ar and ba.action.select_rows:
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
        inserts the *real* user, not subst_user.
        This is important for cal.Event.
        """
        if ar and self.user_id is None:
            u = ar.user
            if u is not None:
                self.user = u
        super(UserAuthored, self).on_create(ar)

    def get_time_zone(self):
        """Return the author's timezone. Used by
        :class:`lino_xl.lib.cal.mixins.Started`.

        """
        if self.user_id is None:
            # return settings.TIME_ZONE
            return rt.models.about.TimeZones.default
        return self.user.time_zone or rt.models.about.TimeZones.default
        # return self.user.timezone or settings.TIME_ZONE



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
        # return self._label or \
        #     _("My %s") % self.model._meta.verbose_name_plural
        return self._label or \
            format_lazy(_("My {}"), self.model._meta.verbose_name_plural)

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(My, self).param_defaults(ar, **kw)
        # kw.update(user=ar.get_user())
        # k = self.author_field_name or self.model.author_field_name
        # kw[k] = ar.get_user()
        # kw[self.model.author_field_name] = ar.get_user()
        kw['user'] = ar.get_user()
        return kw

class StartPlan(dd.Action):
    show_in_bbar = False
    # icon_name = 'basket'
    sort_index = 52
    select_rows = False
    http_method = 'POST'
    update_after_start = False

    def get_button_label(self, actor):
        return self.label or actor.model._meta.verbose_name
        # return format_lazy(
        #     pgettext("singular", "My {}"), actor.model._meta.verbose_name)
        
    # def attach_to_actor(self, owner, name):
    #     self.label = format_lazy(
    #         _("Start new {}"), owner.model._meta.verbose_name)
    #     # self.label = owner.model._meta.verbose_name
    #     print("20180905 {} on {} {}".format(name, owner, self.label))
    #     return super(StartPlan, self).attach_to_actor(owner, name)
    
    def get_options(self, ar):
        return {}

    def get_plan_model(self):
        return self.defining_actor.model
        # return ar.actor.model
    
    def run_from_ui(self, ar, **kw):
        options = self.get_options(ar)
        pm = self.get_plan_model()
        plan = pm.run_start_plan(ar.get_user(), **options)
        # plan = self.defining_actor.model.run_start_plan(
        #     ar.get_user(), **options)
        if self.update_after_start:
            plan.run_update_plan(ar)
        ar.goto_instance(plan)


class UpdatePlan(dd.Action):
    label = _("Update plan")
    icon_name = 'lightning'
    sort_index = 53

    def run_from_ui(self, ar, **kw):
        for plan in ar.selected_rows:
            plan.run_update_plan(ar)
        ar.success(refresh=True)


class UserPlan(UserAuthored):
    class Meta:
        abstract = True

    today = models.DateField(_("Today"), default=dd.today)
    
    update_plan = UpdatePlan()
    start_plan = StartPlan()
    
    @classmethod
    def run_start_plan(cls, user, **options):
        try:
            plan = cls.objects.get(user=user)
            changed = False
            for k, v in options.items():
                if getattr(plan, k) != v:
                    changed = True
                    setattr(plan, k, v)
            if 'today' not in options:
                if plan.today != dd.today():
                    plan.today = dd.today()
                    changed = True
            if changed:
                plan.reset_plan()
        except cls.DoesNotExist:
            plan = cls(user=user, **options)
        plan.full_clean()
        plan.save()
        return plan

    def run_update_plan(self, ar):
        raise NotImplementedError()

    def reset_plan(self):
        """Delete all cached data for this plan.
        """
        pass

   
class AssignToMe(dd.Action):
    """Set yourself as assigned user.

    This will ask for confirmation and then set
    :attr:`Assignable.assigned_to`.

    """
    label = _("Assign to me")
    show_in_workflow = True
    show_in_bbar = False  # added 20180515 for noi. possible side
                          # effects in welfare.
    
    # readonly = False
    required_roles = dd.login_required(Helper)

    # button_text = u"\u2698"  # FLOWER (⚘)
    # button_text = u"\u26d1"  # ⛑
    # button_text = u"\u261D"  # ☝
    button_text = u"\u270B"  # ✋
    
    # help_text = _("You become assigned to this.")

    def get_action_permission(self, ar, obj, state):
        if obj.assigned_to_id:
            return False
        # user = ar.get_user()
        # if obj.assigned_to == user:
        #     return False
        # if user == obj.get_author():
        #     return False
        return super(AssignToMe,
                     self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]

        def ok(ar):
            obj.assigned_to = ar.get_user()
            obj.save()
            ar.set_response(refresh=True)

        ar.confirm(ok, _("You become assigned to this."),
                   _("Are you sure?"))


class TakeAuthorship(dd.Action):
    """
    You declare to become the fully responsible user for this database
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

    disable_author_assign = True
    """
    Set this to False if you want that the author of an object can
    also assign themselves.

    In Lino Noi you can be author of a ticket and then assign it to
    yourself, but e.g. in group calendar management we don't want this
    behaviour.
    """

    def disabled_fields(self, ar):
        s = super(Assignable, self).disabled_fields(ar)
        user = ar.get_user()
        if self.assigned_to == user:
            s.add('assign_to_me')
        
        if self.disable_author_assign and user == self.get_author():
            s.add('assign_to_me')
            s.add('take')
        return s
    

    def on_create(self, ar):
        # 20130722 e.g. CreateClientEvent sets assigned_to it explicitly
        if self.assigned_to is None:
            self.assigned_to = ar.subst_user
        super(Assignable, self).on_create(ar)
    
