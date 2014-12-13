# -*- coding: UTF-8 -*-
# Copyright 2010-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""This package contains Model mixins, some of which are heavily used
by :mod:`lino.modlib`. None of them is mandatory for a Lino
application.

.. autosummary::
   :toctree:

    duplicable
    sequenced
    human
    periods
    polymorphic
    printable
    uploadable


"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


import datetime

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.humanize.templatetags.humanize import naturaltime


from lino.modlib.users.mixins import UserLevels
from lino.core.choicelists import ChoiceList, Choice
from lino.core import actions
from lino.core import fields
from lino.core import dbtables
from lino.core import model
from lino.core.dbutils import navinfo
from lino.utils import AttrDict
from lino.core.perms import AnonymousUser


class UserAuthored(model.Model):

    """
    Mixin for models that have a `user` field which is automatically
    set to the requesting user.
    Also defines a `ByUser` base table which fills the master instance
    from the web request.
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

AutoUser = UserAuthored  # backwards compatibility


if settings.SITE.user_model:

    class ByUser(dbtables.Table):
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
            #~ logger.info("mixins.ByUser.setup_request")
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

else:

    # dummy Table for userless sites
    class ByUser(dbtables.Table):
        pass


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
            actions.AuthorAction, self).get_action_permission(ar, obj, state)


class Registrable(model.Model):

    """
    Base class to anything that may be "registered" and "deregistered"
    (e.g. Invoices, Vouchers, Declarations, Reservations,...).
    "Registered" in general means "this object has been taken account of".
    Registered objects are not editable.
    The ChoiceList of the `state` field must have at least two items
    named "draft" and "registered".
    There may be additional states.
    Every state must have an extra attribute "editable".
    """
    class Meta:
        abstract = True

    workflow_state_field = 'state'

    _registrable_fields = None

    @classmethod
    def get_registrable_fields(cls, site):
        """
        Return a list of the fields which are *disabled* when this is
        *registered* (i.e. `state` is not `editable`).
        """
        return []
        #~ yield 'date'

    @classmethod
    def on_analyze(cls, site):
        super(Registrable, cls).on_analyze(site)
        cls._registrable_fields = set(cls.get_registrable_fields(site))
        #~ logger.info("20130128 %s %s",cls,cls._registrable_fields)

    def disabled_fields(self, ar):
        if not self.state.editable:
            return self._registrable_fields
        return super(Registrable, self).disabled_fields(ar)

    def get_row_permission(self, ar, state, ba):
        """
        Only rows in an editable state may be edited.
        """
        #~ if isinstance(ba.action,actions.DeleteSelected):
            #~ logger.info("20130128 Registrable.get_row_permission %s %s %s %s",
                #~ self,state,ba.action,ar.bound_action.action.readonly)
        if state and not state.editable:
            if not ar.bound_action.action.readonly:
                return False
        return super(Registrable, self).get_row_permission(ar, state, ba)

    def register(self, ar):
        """
        Register this item.
        The base implementation just sets the state to "registered".
        Subclasses may override this to add custom behaviour.
        """

        state_field = self._meta.get_field(self.workflow_state_field)
        target_state = state_field.choicelist.registered
        self.set_workflow_state(ar, state_field, target_state)


    #~ def deregister(self,ar):
        #~ """
        #~ Deregister this item.
        #~ The base implementation just sets the state to "draft".
        #~ Subclasses may override this to add custom behaviour.
        #~ """
        #~ state_field = self._meta.get_field('state')
        #~ self.state = state_field.choicelist.draft

    #~ def before_printable_build(self,bm):
        #~ state_field = self._meta.get_field('state')
        #~ if self.state != state_field.choicelist.registered:
            #~ self.register(None)
            #~ self.save()

class Modified(model.Model):

    class Meta:
        abstract = True

    modified = models.DateTimeField(_("Modified"), editable=False)

    def save(self, *args, **kwargs):
        if not settings.SITE.loading_from_dump:
            self.modified = datetime.datetime.now()
        super(Modified, self).save(*args, **kwargs)


class Created(model.Model):

    class Meta:
        abstract = True

    created = models.DateTimeField(_("Created"), editable=False)

    @fields.displayfield(_('Created'))
    def created_natural(self, ar):
        return naturaltime(self.created)

    def save(self, *args, **kwargs):
        if self.created is None and not settings.SITE.loading_from_dump:
            self.created = datetime.datetime.now()
        super(Created, self).save(*args, **kwargs)


class CreatedModified(Created, Modified):

    """Adds two timestamp fields `created` and `modified`.

    We don't use Django's `auto_now` and `auto_now_add` features
    because their deserialization (restore from a python dump) would
    be problematic.

    """

    class Meta:
        abstract = True


class ProjectRelated(model.Model):

    """Mixin for Models that are automatically related to a "project".  A
    project means here "the central most important thing that is used
    to classify most other things".  

    Whether an application has such a concept of "project",
    and which model has this privileged status,
    is set in :attr:`ad.Site.project_model`.

    For example in :ref:`welfare` the "project" is a Client.

    """

    class Meta:
        abstract = True

    if settings.SITE.project_model:
        project = models.ForeignKey(
            settings.SITE.project_model,
            blank=True, null=True,
            related_name="%(app_label)s_%(class)s_set_by_project",
        )
    else:
        project = fields.DummyField()

    def get_related_project(self, ar):
        if settings.SITE.project_model:
            return self.project

    #~ def summary_row(self,ui,rr,**kw):
    def summary_row(self, ar, **kw):
        s = [ar.obj2html(self)]
        if settings.SITE.project_model:
            #~ if self.project and not dd.has_fk(rr,'project'):
            if self.project:
                #~ s += " (" + ui.obj2html(self.project) + ")"
                s += [" (", ar.obj2html(self.project), ")"]
        return s

    def update_owned_instance(self, controllable):
        """
        When a :class:`project-related <ProjectRelated>`
        object controls another project-related object,
        then the controlled automatically inherits
        the `project` of its controller.
        """
        if isinstance(controllable, ProjectRelated):
            controllable.project = self.project
        super(ProjectRelated, self).update_owned_instance(controllable)

    def get_mailable_recipients(self):
        if isinstance(self.project, settings.SITE.modules.contacts.Partner):
            if self.project.email:
                yield ('to', self.project)
        for r in super(ProjectRelated, self).get_mailable_recipients():
            yield r

    def get_postable_recipients(self):
        if isinstance(self.project, settings.SITE.modules.contacts.Partner):
            yield self.project
        for p in super(ProjectRelated, self).get_postable_recipients():
            yield p


class Referrable(model.Model):

    """
    Mixin for things that have a unique `ref` field and a `get_by_ref` method.
    """
    class Meta:
        abstract = True

    ref = fields.NullCharField(_("Reference"),
                               max_length=40,
                               blank=True, null=True,
                               unique=True)

    @classmethod
    def get_by_ref(cls, ref, default=models.NOT_PROVIDED):
        try:
            return cls.objects.get(ref=ref)
        except cls.DoesNotExist:
            if default is models.NOT_PROVIDED:
                raise cls.DoesNotExist(
                    "No %s with reference %r" % (unicode(cls._meta.verbose_name), ref))
            return default

    #~ def __unicode__(self):
        #~ return self.ref or unicode(_('(Root)'))

    def __unicode__(self):
        return super(Referrable, self).__unicode__() + " (" + self.ref + ")"



from lino.mixins.printable import (Printable, PrintableType,
                                   CachedPrintable, TypedPrintable,
                                   DirectPrintAction, CachedPrintAction)

from lino.mixins.duplicable import Duplicable, Duplicate
from lino.mixins.sequenced import Sequenced, Hierarizable
from lino.mixins.periods import DatePeriod
from lino.mixins.polymorphic import Polymorphic
from lino.mixins.uploadable import Uploadable

from lino.utils.mldbc.fields import BabelCharField, BabelTextField
from lino.utils.mldbc.mixins import BabelNamed

from lino.mixins.human import Human, Born

# from lino.core.report import Report
