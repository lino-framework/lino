# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.
"""
The :xfile:`models.py` file for :mod:`lino.modlib.attestations`.
"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

import datetime

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from lino import dd
from lino import mixins

from lino.utils.xmlgen.html import E

outbox = dd.resolve_app('outbox')
postings = dd.resolve_app('postings')
contacts = dd.resolve_app('contacts')


class AttestationType(
        dd.BabelNamed,
        mixins.PrintableType,
        outbox.MailableType):

    templates_group = 'attestations/Attestation'

    class Meta:
        verbose_name = _("Attestation Type")
        verbose_name_plural = _("Attestation Types")

    important = models.BooleanField(
        verbose_name=_("important"),
        default=False)
    remark = models.TextField(verbose_name=_("Remark"), blank=True)

    body_template = models.CharField(
        max_length=200,
        verbose_name=_("Body template"),
        blank=True, help_text="The body template to be used when \
        rendering a printable of this type. This is a list of files \
        with extension `.body.html`.")

    content_type = dd.ForeignKey(
        'contenttypes.ContentType',
        verbose_name=_("Model"),
        related_name='attestation_types',
        null=True, blank=True,
        help_text=_("The model that can issue attestations of this type."))

    primary = models.BooleanField(
        _("Primary"),
        default=False,
        help_text=_("""There's at most one primary type per model. \
        Enabling this field will automatically make the other \
        types non-primary."""))

    skip_dialog = models.BooleanField(
        _("Skip dialog"),
        default=False,
        help_text=_("""Check this to define a "quick attestation" type."""))

    @dd.chooser(simple_values=True)
    def body_template_choices(cls):
        return settings.SITE.list_templates(
            '.body.html', cls.get_templates_group())

    def after_ui_save(self, ar):
        super(AttestationType, self).after_ui_save(ar)
        if self.primary:
            for o in self.content_type.attestation_types.exclude(id=self.id):
                if o.primary:
                    o.primary = False
                    o.save()
                    ar.response.update(refresh_all=True)


class AttestationTypes(dd.Table):

    """
    Displays all rows of :class:`AttestationType`.
    """
    model = 'attestations.AttestationType'
    required = dd.required(user_level='admin', user_groups='office')
    column_names = 'name build_method template content_type primary *'
    order_by = ["name"]

    insert_layout = """
    name
    build_method
    """

    detail_layout = """
    id name
    content_type primary skip_dialog
    build_method template body_template
    email_template attach_to_email
    remark:60x5
    attestations.AttestationsByType
    """

    @classmethod
    def get_choices_text(self, obj, request, field):
        if field.name == 'content_type':
            return "%s (%s)" % (
                dd.full_model_name(obj.model_class()),
                obj)
        return obj.get_choices_text(request, self, field)


class CreateAttestation(dd.Action):

    """
    Creates an attestation and displays it.
    """
    url_action_name = 'attst'
    icon_name = 'script_add'
    help_text = _('Create an attestation from this')
    label = _('Create attestation')

    def get_action_permission(self, ar, obj, state):
        if not ar.get_user().email:
            return False
        if obj is not None:
            if not obj.is_attestable():
                return False
        return super(CreateAttestation,
                     self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        akw = dict(
            user=ar.get_user(),
            owner=obj)
        ct = ContentType.objects.get_for_model(obj.__class__)
        primary_type = None

        try:
            primary_type = AttestationType.objects.get(
                content_type=ct, primary=True)
            akw.update(type=primary_type)
        except AttestationType.MultipleObjectsReturned:
            pass
        except AttestationType.DoesNotExist:
            pass
            # atypes = AttestationType.objects.filter(content_type=ct)
            # n = atypes.count()
            # if n == 1:
            #     akw.update(type=atypes[0])

        a = obj.create_attestation(ar, **akw)

        a.full_clean()
        a.save()
        
        if primary_type is None or not primary_type.skip_dialog:
            # open detail window on the created attestation
            js = ar.renderer.instance_handler(ar, a)
            kw.update(eval_js=js)
            ar.success(**kw)
        else:  # print directly without dialog
            a.do_print.run_from_ui(ar, **kw)


class Attestable(dd.Model):

    """Mixin for models that provide a "Create attestation" button.  A
    Mailable model must also inherit
    :class:`lino.mixins.printable.BasePrintable` or some subclass
    thereof.

    """
    class Meta:
        abstract = True

    issue_attestation = CreateAttestation()
    
    # Note every Attestable wants a "show attestations" button
    # show_attestations = dd.ShowSlaveTable('attestations.AttestationsByOwner')

    def is_attestable(self):
        return True

    def create_attestation(self, ar, **kw):
        return dd.modules.attestations.Attestation(**kw)


class Attestation(dd.TypedPrintable,
                  dd.UserAuthored,
                  dd.Controllable,
                  contacts.ContactRelated,
                  dd.ProjectRelated,
                  outbox.Mailable,
                  postings.Postable):

    """An attestation is a printable document that describes some aspect
    of the current situation.

    """

    manager_level_field = 'office_level'

    class Meta:
        abstract = settings.SITE.is_abstract_model('attestations.Attestation')
        verbose_name = _("Attestation")
        verbose_name_plural = _("Attestations")

    # date = models.DateField(
    #     verbose_name=_('Date'), default=datetime.date.today)

    type = models.ForeignKey(
        AttestationType,
        blank=True, null=True,
        verbose_name=_('Attestation Type'))

    language = dd.LanguageField()

    mails_by_owner = dd.ShowSlaveTable('outbox.MailsByController')

    def __unicode__(self):
        return u'%s #%s' % (self._meta.verbose_name, self.pk)

    def get_mailable_type(self):
        return self.type

    def on_create(self, ar):
        """When creating an Attestation by double clicking in
        AttestationsByProject, then the `project` field gets filled
        automatically, but we also want to set the `owner` field to
        the project.

        """
        super(Attestation, self).on_create(ar)
        if not self.owner_id:
            if self.project:
                self.owner = self.project

    @dd.chooser()
    def type_choices(cls, owner):
        qs = AttestationType.objects.order_by('name')
        if owner is None:
            return qs.filter(content_type__isnull=True)
        print(20140210, owner)
        ct = ContentType.objects.get_for_model(owner.__class__)
        return qs.filter(content_type=ct)

    @property
    def date(self):
        "Used in templates"
        if self.build_time:
            return self.build_time.date()
        return datetime.date.today()

    def get_print_language(self):
        return self.language

    @dd.virtualfield(dd.HtmlBox(_("Preview")))
    def preview(self, ar):
        ctx = self.get_printable_context(ar)
        return '<div class="htmlText">%s</div>' % ctx['body']

    def get_printable_context(self, ar, **kw):
        kw = super(Attestation, self).get_printable_context(ar, **kw)
        if self.type and self.type.body_template:
            tplname = self.type.body_template
            tplname = self.type.get_templates_group() + '/' + tplname
            saved_renderer = ar.renderer
            ar.renderer = settings.SITE.ui.plain_renderer
            template = settings.SITE.jinja_env.get_template(tplname)
            kw.update(body=template.render(**kw))
            ar.renderer = saved_renderer
        else:
            kw.update(body='')
        # if self.owner is not None:
        #     kw.update(self=self.owner)
        #     kw.update(this=self.owner)
        #     kw.update(doc=self)
        return kw


dd.update_field(Attestation, 'company',
                verbose_name=_("Recipient (Organization)"))
dd.update_field(Attestation, 'contact_person',
                verbose_name=_("Recipient (Person)"))


class AttestationDetail(dd.FormLayout):
    main = """
    id type:25 project
    company contact_person contact_role
    user:10 language:8 owner build_time
    preview
    """


class Attestations(dd.Table):
    required = dd.required(user_groups='office', user_level='admin')

    model = 'attestations.Attestation'
    detail_layout = AttestationDetail()
    insert_layout = """
    type project
    company language
    """
    column_names = "id build_time user type project *"
    order_by = ["id"]


class MyAttestations(mixins.ByUser, Attestations):
    required = dd.required(user_groups='office')
    column_names = "build_time type project *"
    order_by = ["build_time"]


class AttestationsByType(Attestations):
    master_key = 'type'
    column_names = "build_time user *"
    order_by = ["build_time"]


class AttestationsByX(Attestations):
    required = dd.required(user_groups='office')
    column_names = "build_time type user *"
    order_by = ["-build_time"]

if settings.SITE.project_model is not None:

    class AttestationsByProject(AttestationsByX):
        master_key = 'project'


class AttestationsByOwner(AttestationsByX):
    master_key = 'owner'
    column_names = "build_time type user *"


class AttestationsByCompany(AttestationsByX):
    master_key = 'company'
    column_names = "build_time type user *"


class AttestationsByPerson(AttestationsByX):
    master_key = 'contact_person'
    column_names = "build_time type user *"


system = dd.resolve_app('system')


def setup_main_menu(site, ui, profile, m):
    m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
    m.add_action('attestations.MyAttestations')


def setup_config_menu(site, ui, profile, m):
    m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
    m.add_action('attestations.AttestationTypes')


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
    m.add_action('attestations.Attestations')

