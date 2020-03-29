# -*- coding: UTF-8 -*-
# Copyright 2010-2020 Rumma & Ko Ltd
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
    ref
    registrable

"""

from builtins import object

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.text import format_lazy
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import naturaltime

from lino.core import fields
from lino.core import model
from lino.core.workflows import ChangeStateAction
from lino.utils.mldbc.fields import LanguageField
from lino.core.exceptions import ChangedAPI


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

    modified = models.DateTimeField(_("Modified"), editable=False, null=True)

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

    project = fields.ForeignKey(
        settings.SITE.project_model,
        blank=True, null=True,
        related_name="%(app_label)s_%(class)s_set_by_project")

    def get_related_project(self):
        if settings.SITE.project_model:
            return self.project

    # def on_create(self, ar):
    #     super(ProjectRelated, self).on_create(ar)
    #     print(20200327, ar.actor.master_key, ar.master_instance)
    #     if ar.actor.master_key and ar.actor.master_key == "project":
    #         self.project = ar.master_instance

    def summary_row(self, ar, **kwargs):
        s = list(super(ProjectRelated, self).summary_row(ar, **kwargs))
        # s = [ar.obj2html(self)]
        if settings.SITE.project_model:
            if self.project and not ar.is_obvious_field("project"):
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

    @classmethod
    def get_simple_parameters(cls):
        for p in super(ProjectRelated, cls).get_simple_parameters():
            yield p
        # if settings.SITE.project_model:
        yield 'project'

    # @classmethod
    # def setup_parameters(cls, params):
    #     super(ProjectRelated, cls).setup_parameters(params)
    #     if settings.SITE.project_model:
    #         params['project'].help_text = format_lazy(
    #             _("Show only entries having this {project}."),
    #             project=settings.SITE.project_model._meta.verbose_name)


class Story(model.Model):
    class Meta:
        abstract = True

    def get_story(self, ar):
        return []

    @fields.virtualfield(fields.HtmlBox())
    def body(self, ar):
        if ar is None:
            return ''
        # ar.master_instance = self
        html = ar.renderer.show_story(
            ar, self.get_story(ar), header_level=1)
        return ar.html_text(html)
        # return ar.html_text(ar.story2html(
        #     self.get_story(ar), header_level=1))

    def as_appy_pod_xml(self, apr):
        chunks = tuple(apr.story2odt(
            self.get_story(apr.ar), master_instance=self))
        return str('').join(chunks)  # must be utf8 encoded




from .ref import Referrable, StructuredReferrable
from .registrable import Registrable, RegistrableState
from lino.mixins.duplicable import Duplicable, Duplicate
from lino.mixins.sequenced import Sequenced, Hierarchical
from lino.mixins.periods import DateRange
from lino.mixins.periods import ObservedDateRange, Yearly, Monthly, Today
from lino.mixins.polymorphic import Polymorphic
from lino.mixins.uploadable import Uploadable

from lino.utils.mldbc.fields import BabelCharField, BabelTextField
from lino.utils.mldbc.mixins import BabelNamed, BabelDesignated

from lino.mixins.human import Human, Born
