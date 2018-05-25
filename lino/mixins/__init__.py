# -*- coding: UTF-8 -*-
# Copyright 2010-2018 Luc Saffre
# License: BSD (see file COPYING for details)

"""
This package contains model mixins, some of which are heavily used
by applications and the :ref:`xl`. But none of them is mandatory.

.. autosummary::
   :toctree:

    duplicable
    dupable
    sequenced
    human
    periods
    polymorphic
    uploadable
"""

from __future__ import unicode_literals
from builtins import str
from builtins import object

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import naturaltime

from lino.core import fields
from lino.core import model
from lino.core.workflows import ChangeStateAction
from lino.utils.mldbc.fields import LanguageField


class Contactable(model.Model):
    """
    Mixin for models that represent somebody who can be contacted by
    email.
    """
    class Meta(object):
        abstract = True

    email = models.EmailField(_('e-mail address'), blank=True)
    language = LanguageField(default=models.NOT_PROVIDED, blank=True)
    
    def get_as_user(self):
        """Return the user object representing this contactable.

        """
        raise NotImplementedError()
        

class Phonable(model.Model):
    """
    Mixin for models that represent somebody who can be contacted by
    phone.
    """

    class Meta(object):
        abstract = True

    url = models.URLField(_('URL'), blank=True)
    phone = models.CharField(_('Phone'), max_length=200, blank=True)
    gsm = models.CharField(_('GSM'), max_length=200, blank=True)
    fax = models.CharField(_('Fax'), max_length=200, blank=True)
    
    


class Registrable(model.Model):

    """
    Base class to anything that may be "registered" and "deregistered"
    (e.g. Invoices, Vouchers, Declarations, Reservations,...).
    "Registered" in general means "this object has been taken account of".
    Registered objects are not editable.

    .. attribute:: state

        The ChoiceList of the `state` field must have at least two items
        named "draft" and "registered".
        There may be additional states.
        Every state must have an extra attribute "editable".

    """
    class Meta(object):
        abstract = True

    workflow_state_field = 'state'

    _registrable_fields = None

    @classmethod
    def get_registrable_fields(cls, site):
        """Return a list of the fields which are *disabled* when this is
        *registered* (i.e. `state` is not `editable`).

        Usage example::

            class MyModel(dd.Registrable):

                @classmethod
                def get_registrable_fields(self, site):
                    for f in super(MyModel, self).get_registrable_fields(site):
                        yield f
                    yield 'user'
                    yield 'date'


        """
        return []
        # yield 'date'

    @classmethod
    def on_analyze(cls, site):
        super(Registrable, cls).on_analyze(site)
        cls._registrable_fields = set(cls.get_registrable_fields(site))

    def disabled_fields(self, ar):
        if not self.state.editable:
            return self._registrable_fields
        return super(Registrable, self).disabled_fields(ar)

    def get_row_permission(self, ar, state, ba):
        """Only rows in an editable state may be edited.

        Note that `ba` is the action being requested while
        `ar.bound_action` is the action from which the request was
        started.

        """
        # print "20150628 Registrable.get_row_permission %s %s : %s %s" \
        #     % (self, ba, state.editable, ba.action.readonly)
        if state and not state.editable and not isinstance(
                ba.action, ChangeStateAction):
            # if not ar.bound_action.action.readonly:
            if not ba.action.readonly:
                return False
        return super(Registrable, self).get_row_permission(ar, state, ba)

    def register(self, ar):
        """
        Register this object.  The base implementation just sets the state
        to "registered".

        Subclasses may override this to add custom behaviour.  Instead
        of subclassing you can also override :meth:`set_workflow_state
        <lino.core.model.Model.set_workflow_state>`,
        :meth:`before_state_change
        <lino.core.model.Model.before_state_change>` or
        :meth:`after_state_change
        <lino.core.model.Model.after_state_change>`.
        """

        # state_field = self._meta.get_field(self.workflow_state_field)
        state_field = self.workflow_state_field
        target_state = state_field.choicelist.registered
        self.set_workflow_state(ar, state_field, target_state)

    def deregister(self, ar):
        """
        Deregister this object.  The base implementation just sets the
        state to "draft".

        Subclasses may override this to add custom behaviour.  Instead
        of subclassing you can also override :meth:`set_workflow_state
        <lino.core.model.Model.set_workflow_state>`,
        :meth:`before_state_change
        <lino.core.model.Model.before_state_change>` or
        :meth:`after_state_change
        <lino.core.model.Model.after_state_change>`.
        """

        # state_field = self._meta.get_field(self.workflow_state_field)
        state_field = self.workflow_state_field
        target_state = state_field.choicelist.draft
        self.set_workflow_state(ar, state_field, target_state)

    # no longer needed after 20170826
    # @classmethod
    # def setup_parameters(cls, **fields):
    #     wsf = cls.workflow_state_field
    #     fields[wsf.name] = wsf.choicelist.field(blank=True, null=True)
    #     return super(Registrable, cls).setup_parameters(**fields)

    @classmethod
    def get_simple_parameters(cls):
        for p in super(Registrable, cls).get_simple_parameters():
            yield p
        yield cls.workflow_state_field.name


class Modified(model.Model):
    """
    Adds a a timestamp field which holds the last modification time of
    every individual database object.

    .. attribute:: modified

        The time when this database object was last modified.
    """

    auto_touch = True
    """
    Whether to touch objects automatically when saving them.

    If you set this to `False`, :attr:`modified` is updated only when
    you explicitly call :meth:`touch`.
    """
    
    class Meta(object):
        abstract = True

    modified = models.DateTimeField(_("Modified"), editable=False)

    def save(self, *args, **kwargs):
        if self.auto_touch and not settings.SITE.loading_from_dump:
            self.touch()
        super(Modified, self).save(*args, **kwargs)

    def touch(self):
        self.modified = timezone.now()


class Created(model.Model):
    """
    Adds a a timestamp field which holds the creation time of every
    individual database object.

    .. attribute:: created

        The time when this object was created.

        Does nut use Django's `auto_now` and `auto_now_add` features
        because their deserialization would be problematic.
    """
    class Meta(object):
        abstract = True

    created = models.DateTimeField(_("Created"), editable=False)

    @fields.displayfield(_('Created'))
    def created_natural(self, ar):
        return naturaltime(self.created)

    def save(self, *args, **kwargs):
        if self.created is None and not settings.SITE.loading_from_dump:
            self.created = timezone.now()
        super(Created, self).save(*args, **kwargs)


class CreatedModified(Created, Modified):

    """
    Adds two timestamp fields `created` and `modified`.

    """

    class Meta(object):
        abstract = True


class ProjectRelated(model.Model):

    """
    Mixin for models that are related to a "project". This adds a
    field named `project` and related default behaviour.

    A project in this context means what the users consider "the
    central most important model that is used to classify most other
    things".  For example in :ref:`avanti` the "project" is a Client
    while in :ref:`tera` it is a therapy.  The application's project
    model is specified in :attr:`lino.core.site.Site.project_model`.


    .. attribute:: project

        Pointer to the project to which this object is related.

        If the application's :attr:`project_model
        <lino.core.site.Site.project_model>` is empty, the
        :attr:`project` field will be a :class:`DummyField
        <lino.core.fields.DummyField>`.
    """

    class Meta(object):
        abstract = True

    if settings.SITE.project_model:
        project = fields.ForeignKey(
            settings.SITE.project_model,
            blank=True, null=True,
            related_name="%(app_label)s_%(class)s_set_by_project",
        )
    else:
        project = fields.DummyField('project')

    def get_related_project(self):
        if settings.SITE.project_model:
            return self.project

    def summary_row(self, ar, **kw):
        s = [ar.obj2html(self)]
        if settings.SITE.project_model:
            # if self.project and not dd.has_fk(rr,'project'):
            if self.project:
                # s += " (" + ui.obj2html(self.project) + ")"
                s += [" (", ar.obj2html(self.project), ")"]
        return s

    def update_owned_instance(self, controllable):
        """
        When a :class:`project-related <ProjectRelated>` object controls
        another project-related object, then the controlled
        automatically inherits the `project` of its controller.
        """
        if isinstance(controllable, ProjectRelated):
            controllable.project = self.project
        super(ProjectRelated, self).update_owned_instance(controllable)

    def get_mailable_recipients(self):
        if isinstance(self.project, settings.SITE.models.contacts.Partner):
            if self.project.email:
                yield ('to', self.project)
        for r in super(ProjectRelated, self).get_mailable_recipients():
            yield r

    def get_postable_recipients(self):
        if isinstance(self.project, settings.SITE.models.contacts.Partner):
            yield self.project
        for p in super(ProjectRelated, self).get_postable_recipients():
            yield p


class Referrable(model.Model):
    """
    Mixin for things that have a unique reference, i.e. an identifying
    name used by humans to refer to an individual object.

    A reference, unlike a primary key, can easily be changed.

    .. attribute:: ref

        The reference. This must be either empty or unique.
    """
    class Meta(object):
        abstract = True

    ref_max_length = 40
    """The maximum length of the :attr:`ref` field."""

    # ref = fields.NullCharField(_("Reference"),
    #                            max_length=ref_max_length,
    #                            blank=True, null=True,
    #                            unique=True)

    ref = models.CharField(
        _("Reference"), max_length=ref_max_length,
        blank=True, null=True, unique=True)

    def on_duplicate(self, ar, master):
        """
        Before saving a duplicated object for the first time, we must
        change the :attr:`ref` in order to avoid an IntegrityError.
        """
        if self.ref:
            self.ref += ' (DUP)'
        super(Referrable, self).on_duplicate(ar, master)

    @classmethod
    def get_by_ref(cls, ref, default=models.NOT_PROVIDED):
        """
        Return the object identified by the given reference.
        """
        try:
            return cls.objects.get(ref=ref)
        except cls.DoesNotExist:
            if default is models.NOT_PROVIDED:
                raise cls.DoesNotExist(
                    "No %s with reference %r" % (str(cls._meta.verbose_name), ref))
            return default

    @classmethod
    def quick_search_filter(cls, search_text, prefix=''):
        """Overrides the default behaviour defined in
        :meth:`lino.core.model.Model.quick_search_filter`. For
        Referrable objects, when quick-searching for a text containing
        only digits, the user usually means the :attr:`ref` and *not*
        the primary key.

        """
        #if search_text.isdigit():
        if search_text.startswith('*'):
            return models.Q(**{prefix+'ref__icontains': search_text[1:]})
        return super(Referrable, cls).quick_search_filter(search_text, prefix)



from lino.mixins.duplicable import Duplicable, Duplicate
from lino.mixins.sequenced import Sequenced, Hierarchical
from lino.mixins.periods import DateRange
from lino.mixins.periods import ObservedDateRange, Yearly, Monthly, Today
from lino.mixins.polymorphic import Polymorphic
from lino.mixins.uploadable import Uploadable

from lino.utils.mldbc.fields import BabelCharField, BabelTextField
from lino.utils.mldbc.mixins import BabelNamed, BabelDesignated

from lino.mixins.human import Human, Born

