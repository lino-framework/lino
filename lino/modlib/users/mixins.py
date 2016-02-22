# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Model mixins for :mod:`lino.modlib.users`.

.. autosummary::

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
from lino.core.roles import SiteUser, SiteStaff, login_required

from .utils import AnonymousUser


class TimezoneHolder(models.Model):
    """Mixin for database models which have a :attr:`timezone` field.

    .. attribute:: timezone
    
        The timezone.

    """
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


class UserAuthored(model.Model):
    """Model mixin for database objects that have a `user` field which
    points to the "author" of this object. The default user is
    automatically set to the requesting user.

    .. attribute:: user

        The author of this object.
        A pointer to :class:`lino.modlib.users.models.User`.

    """

    class Meta(object):
        abstract = True

    manager_roles_required = login_required(SiteStaff)
    """The list of required roles for getting permission to edit other
    users' work.

    By default, only :class:`SiteStaff <lino.core.roles.SiteStaff>`
    users can edit other users' work.

    An application can set :attr:`manager_roles_required` to some
    other user role class or a tuple of such classes.

    Setting :attr:`manager_roles_required` to ``[]`` will **disable**
    this behaviour (i.e. everybody can edit the work of other users).

    This is going to be passed to :meth:`has_required_roles
    <lino.core.users.choicelists.UserProfile.has_required_roles>` of
    the requesting user's profile.

    Usage examples see :class:`lino_xl.lib.notes.models.Note` or
    :class:`lino_xl.lib.cal.models.Component`.

    """

    workflow_owner_field = 'user'
    user = dd.ForeignKey(
        'users.User',
        verbose_name=_("Author"),
        related_name="%(app_label)s_%(class)s_set_by_user",
        blank=True, null=True)

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

    def on_duplicate(self, ar, master):
        """The default behaviour after duplicating is to change the author to
        the user who requested the duplicate.

        """
        if ar.user is not None:
            self.user = ar.user
        super(UserAuthored, self).on_duplicate(ar, master)

    def get_row_permission(self, ar, state, ba):
        """Only "managers" or "editors" can edit other users' work.

        See also :attr:`manager_roles_required`.

        """
        if not super(UserAuthored, self).get_row_permission(ar, state, ba):
            return False
        user = ar.get_user()
        if self.user != ar.user \
           and (ar.subst_user is None or self.user != ar.subst_user) \
           and not user.profile.has_required_roles(
               self.manager_roles_required):
            return ba.action.readonly
        return True

    @classmethod
    def on_analyze(cls, site):
        if hasattr(cls, 'manager_level_field'):
            raise ChangedAPI("{0} has a manager_level_field".format(cls))
        super(UserAuthored, cls).on_analyze(site)

    @classmethod
    def get_parameter_fields(cls, **fields):
        """Adds the :attr:`user` filter parameter field."""
        fields.setdefault(
            'user', models.ForeignKey(
                'users.User', verbose_name=_("Author"),
                blank=True, null=True))
        return super(UserAuthored, cls).get_parameter_fields(**fields)

    @classmethod
    def get_simple_parameters(cls):
        s = super(UserAuthored, cls).get_simple_parameters()
        s.add('user')
        return s

AutoUser = UserAuthored  # old name for backwards compatibility


class My(dbtables.Table):
    """Table mixin for tables on :class:`UserAuthored`.

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
        kw.update(user=ar.get_user())
        return kw


class ByUser(dbtables.Table):
    """Base table which fills the master instance from the web request.

    """
    master_key = 'user'
    #~ details_of_master_template = _("%(details)s of %(master)s")
    details_of_master_template = _("%(details)s")

    @classmethod
    def get_actor_label(self):
        if self.model is None:
            return self._label or self.__name__
        return self._label or \
            _("My %s") % self.model._meta.verbose_name_plural

    @classmethod
    def setup_request(self, ar):
        #~ logger.info("ByUser.setup_request")
        if ar.master_instance is None:
            u = ar.get_user()
            if not isinstance(u, AnonymousUser):
                ar.master_instance = u
        super(ByUser, self).setup_request(ar)

    @classmethod
    def get_view_permission(self, profile):
        if not profile.has_required_roles([SiteUser]):
            return False
        return super(ByUser, self).get_view_permission(profile)

if settings.SITE.user_model is None:

    # dummy Table for userless sites
    ByUser = dbtables.Table


class AuthorAction(actions.Action):
    """
    """
    manager_roles_required = login_required(SiteStaff)

    def get_action_permission(self, ar, obj, state):
        user = ar.get_user()
        if obj.user != user and \
           not user.profile.has_required_roles(self.manager_roles_required):
            return self.readonly
        return super(
            AuthorAction, self).get_action_permission(ar, obj, state)
