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

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

from lino import dd
from lino import mixins


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
        verbose_name=_("Default for"),
        null=True, blank=True,
        unique=True,
        help_text=_("The model for which this is the default \
        attestation type."))

    @dd.chooser(simple_values=True)
    def body_template_choices(cls):
        return settings.SITE.list_templates(
            '.body.html', cls.get_templates_group())


class AttestationTypes(dd.Table):

    """
    Displays all rows of :class:`AttestationType`.
    """
    model = 'attestations.AttestationType'
    required = dd.required(user_level='admin', user_groups='office')
    column_names = 'name build_method template content_type *'
    order_by = ["name"]

    insert_layout = """
    name
    build_method
    """

    detail_layout = """
    id name
    build_method template body_template email_template attach_to_email
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
    # icon_name = 'email_add'
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
        try:
            akw.update(type=AttestationType.objects.get(content_type=ct))
        except AttestationType.DoesNotExist:
            pass
    
        a = obj.create_attestation(ar, **akw)

        a.full_clean()
        a.save()
        
        if True:  # issue_directly
            a.do_print.run_from_ui(ar, **kw)
        else:
            js = ar.renderer.instance_handler(ar, a)
            kw.update(eval_js=js)
            ar.success(**kw)


class Attestable(dd.Model):

    """Mixin for models that provide a "Create attestation" button.  A
    Mailable model must also inherit
    :class:`lino.mixins.printable.BasePrintable` or some subclass
    thereof.

    """
    class Meta:
        abstract = True

    issue_attestation = CreateAttestation()

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

    """
    An attestation is a document that describes some aspect of the current
    situation.
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

    def __unicode__(self):
        return u'%s #%s' % (self._meta.verbose_name, self.pk)

    def get_mailable_type(self):
        return self.type

    def get_print_language(self):
        return self.language

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
    outbox.MailsByController
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

