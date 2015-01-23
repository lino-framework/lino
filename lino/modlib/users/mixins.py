# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Model mixins for :mod:`lino.modlib.users`.

.. autosummary::

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.conf import settings


from lino.core import fields
from lino.core import model
from lino.core import actions
from lino.core import dbtables

from .choicelists import UserLevels
from .utils import AnonymousUser


class UserAuthored(model.Model):
    """Model mixin for database objects that have a `user` field which
    points to the "author" of this object. The default user is
    automatically set to the requesting user.

    """
    required = dict(auth=True)

    class Meta:
        abstract = True

    if settings.SITE.user_model:

        workflow_owner_field = 'user'

        user = models.ForeignKey(
            settings.SITE.user_model,
            verbose_name=_("Author"),
            related_name="%(app_label)s_%(class)s_set_by_user",
            blank=True, null=True
        )

    else:

        user = fields.DummyField()

    def on_create(self, ar):
        """
        Adds the requesting user to the `user` field.

        When acting as another user, the default implementation
        still inserts the real user, not subst_user.
        This is important for cal.Event.
        """
        if self.user_id is None:
            #~ u = ar.get_user()
            u = ar.user
            if u is not None:
                self.user = u
        super(UserAuthored, self).on_create(ar)

    manager_level_field = 'level'
    """Only system managers can edit other users' work.  But if the
    application defines customized UserGroups, then we may want to
    permit it also to department managers.  If an application defines
    a UserGroup `foo`, then it can set this attribute to `'foo_level'`
    on a model to specify that a manager level for the foo department
    is enough to get edit permission on other users' instances.
    
    Usage examples see
    :class:`lino.modlib.notes.models.Note`
    or
    :class:`lino.modlib.cal.models.Component`.

    """

    def get_row_permission(self, ar, state, ba):
        """
        Only system managers can edit other users' work.
        """
        if not super(UserAuthored, self).get_row_permission(ar, state, ba):
            #~ logger.info("20120919 no permission to %s on %s for %r",action,self,user)
            return False
        user = ar.get_user()
        if self.user != ar.user and \
           (ar.subst_user is None or self.user != ar.subst_user) \
           and getattr(user.profile, self.manager_level_field) < \
           UserLevels.manager:
            return ba.action.readonly
        return True

AutoUser = UserAuthored  # old name for backwards compatibility


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
        if not profile.authenticated:
            return False
        return super(ByUser, self).get_view_permission(profile)

if settings.SITE.user_model is None:

    # dummy Table for userless sites
    ByUser = dbtables.Table


class AuthorAction(actions.Action):
    """
    """
    manager_level_field = 'level'

    def get_action_permission(self, ar, obj, state):
        user = ar.get_user()
        if obj.user != user and getattr(
                user.profile, self.manager_level_field) < UserLevels.manager:
            return self.readonly
        return super(
            AuthorAction, self).get_action_permission(ar, obj, state)


