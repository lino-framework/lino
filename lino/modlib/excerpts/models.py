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
The :xfile:`models.py` file for :mod:`ml.excerpts`.
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
from django.utils import translation

from lino import dd
from lino import mixins
from lino.mixins.printable import model_group

from lino.utils.xmlgen.html import E

outbox = dd.resolve_app('outbox')
postings = dd.resolve_app('postings')
contacts = dd.resolve_app('contacts')


class ExcerptType(
        dd.BabelNamed,
        mixins.PrintableType,
        outbox.MailableType):

    templates_group = 'excerpts/Excerpt'

    class Meta:
        abstract = dd.is_abstract_model('excerpts.ExcerptType')
        verbose_name = _("Excerpt Type")
        verbose_name_plural = _("Excerpt Types")

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
        related_name='excerpt_types',
        # null=True, blank=True,
        help_text=_("The model that can issue printouts of this type."))

    primary = models.BooleanField(
        _("Primary"),
        default=False,
        help_text=_("""There's at most one primary type per model. \
        Enabling this field will automatically make the other \
        types non-primary."""))

    skip_dialog = models.BooleanField(
        _("Skip dialog"),
        default=False,
        help_text=_("""Check this to define a "quick printout" type."""))

    @dd.chooser(simple_values=True)
    def body_template_choices(cls, content_type):
        tplgroup = model_group(content_type.model_class())
        return settings.SITE.list_templates('.body.html', tplgroup)

    # @dd.chooser(simple_values=True)
    # def body_template_choices(cls):
    #     return settings.SITE.list_templates(
    #         '.body.html', cls.get_templates_group())

    def after_ui_save(self, ar):
        super(ExcerptType, self).after_ui_save(ar)
        if self.primary:
            for o in self.content_type.excerpt_types.exclude(id=self.id):
                if o.primary:
                    o.primary = False
                    o.save()
                    ar.set_response(refresh_all=True)


class ExcerptTypes(dd.Table):

    """
    Displays all rows of :class:`ExcerptType`.
    """
    model = 'excerpts.ExcerptType'
    required = dd.required(user_level='admin', user_groups='office')
    column_names = 'content_type name build_method template primary *'
    order_by = ["name"]

    insert_layout = """
    name
    content_type primary skip_dialog
    build_method template body_template
    """

    detail_layout = """
    id name
    content_type primary skip_dialog
    build_method template body_template
    email_template attach_to_email
    remark:60x5
    excerpts.ExcerptsByType
    """

    @classmethod
    def get_choices_text(self, obj, request, field):
        if field.name == 'content_type':
            return "%s (%s)" % (
                dd.full_model_name(obj.model_class()),
                obj)
        return obj.get_choices_text(request, self, field)


class CreateExcerpt(dd.Action):
    """Creates a Excerpt and displays it.

    """
    parameters = dict(
        excerpt_type=dd.ForeignKey('excerpts.ExcerptType'),
        user=dd.ForeignKey('users.User'),
        owner_type=dd.ForeignKey(ContentType, editable=False),
    )
    params_layout = """
    excerpt_type
    user
    owner_type
    """
    url_action_name = 'create_excerpt'
    icon_name = 'script_add'
    help_text = _('Create a new excerpt using this data record.')
    label = _('Create Excerpt')
    sort_index = 49  # immediately before "Print"

    def action_param_defaults(self, ar, obj, **kw):
        kw = super(CreateExcerpt, self).action_param_defaults(
            ar, obj, **kw)
        if obj is not None:
            ct = ContentType.objects.get_for_model(obj.__class__)
            kw.update(owner_type=ct)
            try:
                at = ExcerptType.objects.get(
                    content_type=ct, primary=True)
                kw.update(excerpt_type=at)
            except ExcerptType.MultipleObjectsReturned:
                pass
            except ExcerptType.DoesNotExist:
                pass
        kw.update(user=ar.get_user())
        return kw

    @dd.chooser()
    def excerpt_type_choices(cls, owner_type):
        logger.info("20140515 excerpt_type_choices(%r)", owner_type)
        return ExcerptType.objects.filter(content_type=owner_type)

    def get_action_permission(self, ar, obj, state):
        # if not ar.get_user().email:
        #     return False
        if obj is not None:
            if not obj.is_attestable():
                return False
        return super(CreateExcerpt,
                     self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        at = ar.action_param_values.excerpt_type
        akw = dict(
            user=ar.action_param_values.user,
            excerpt_type=at,
            owner=obj)
        akw = obj.get_excerpt_options(ar, **akw)
        a = dd.modules.excerpts.Excerpt(**akw)

        a.full_clean()
        a.save()

        if at.skip_dialog:
            # print directly without dialog
            a.do_print.run_from_ui(ar, **kw)
        else:
            # open detail window on the created excerpt
            # js = ar.renderer.instance_handler(ar, a)
            # kw.update(eval_js=js)
            ar.success(**kw)
            ar.goto_instance(a)


class Excerpt(dd.TypedPrintable,
              dd.UserAuthored,
              dd.Controllable,
              contacts.ContactRelated,
              dd.ProjectRelated,
              outbox.Mailable,
              postings.Postable):

    """An excerpt is a printable document that describes some aspect
    of the current situation.

    """

    manager_level_field = 'office_level'

    class Meta:
        abstract = dd.is_abstract_model('excerpts.Excerpt')
        verbose_name = _("Excerpt")
        verbose_name_plural = _("Excerpts")

    # date = models.DateField(
    #     verbose_name=_('Date'), default=datetime.date.today)

    excerpt_type = dd.ForeignKey(
        'excerpts.ExcerptType',
        blank=True, null=True)

    language = dd.LanguageField()

    mails_by_owner = dd.ShowSlaveTable('outbox.MailsByController')

    def __unicode__(self):
        return u'%s #%s' % (self._meta.verbose_name, self.pk)

    def get_mailable_type(self):
        return self.excerpt_type

    def get_printable_type(self):
        return self.excerpt_type

    def on_create(self, ar):
        """When creating an Excerpt by double clicking in
        ExcerptsByProject, then the `project` field gets filled
        automatically, but we also want to set the `owner` field to
        the project.

        """
        super(Excerpt, self).on_create(ar)
        if not self.owner_id:
            if self.project:
                self.owner = self.project

    @dd.chooser()
    def excerpt_type_choices(cls, owner):
        # logger.info("20140513 %s", owner)
        qs = ExcerptType.objects.order_by('name')
        if owner is None:
            return qs.filter(content_type__isnull=True)
        ct = ContentType.objects.get_for_model(owner.__class__)
        return qs.filter(content_type=ct)

    @property
    def date(self):
        "Used in templates"
        if self.build_time:
            return self.build_time.date()
        return datetime.date.today()

    def get_print_language(self):
        """Returns the language to be selected when rendering this
        Excerpt. Default implementation returns the content of
        `self.language`.

        """
        return self.language

    @dd.virtualfield(dd.HtmlBox(_("Preview")))
    def preview(self, ar):
        with translation.override(self.get_print_language()):
            ctx = self.get_printable_context(ar)
            return '<div class="htmlText">%s</div>' % ctx['body']

    def get_printable_context(self, ar, **kw):
        kw = super(Excerpt, self).get_printable_context(ar, **kw)
        atype = self.excerpt_type
        if atype and atype.body_template:
            tplname = atype.body_template
            tplgroup = model_group(atype.content_type.model_class())
            tplname = tplgroup + '/' + tplname
            # tplname = atype.get_templates_group() + '/' + tplname
            saved_renderer = ar.renderer
            ar.renderer = settings.SITE.ui.plain_renderer
            template = settings.SITE.jinja_env.get_template(tplname)
            kw.update(body=template.render(**kw))
            ar.renderer = saved_renderer
        else:
            kw.update(body='')
        kw.update(obj=self.owner)
        # if self.owner is not None:
        #     kw.update(self=self.owner)
        #     kw.update(this=self.owner)
        #     kw.update(doc=self)
        return kw

    @classmethod
    def on_analyze(cls, lino):
        cls.PRINTABLE_FIELDS = dd.fields_list(
            cls,
            'project company contact_person contact_role \
            excerpt_type language \
            user build_method')
        super(Excerpt, cls).on_analyze(lino)

    def disabled_fields(self, ar):
        if not self.build_time:
            return set()
        return self.PRINTABLE_FIELDS


dd.update_field(Excerpt, 'company',
                verbose_name=_("Recipient (Organization)"))
dd.update_field(Excerpt, 'contact_person',
                verbose_name=_("Recipient (Person)"))


class ExcerptDetail(dd.FormLayout):
    main = """
    id excerpt_type:25 project
    company contact_person contact_role
    user:10 language:8 owner build_method build_time
    preview
    """


class Excerpts(dd.Table):
    required = dd.required(user_groups='office', user_level='admin')
    label = _("Excerpts history")
    icon_name = 'script'

    model = 'excerpts.Excerpt'
    detail_layout = ExcerptDetail()
    insert_layout = """
    excerpt_type project
    company language
    """
    column_names = "id build_time user excerpt_type project *"
    order_by = ["id"]


class MyExcerpts(mixins.ByUser, Excerpts):
    required = dd.required(user_groups='office')
    column_names = "build_time excerpt_type project *"
    order_by = ["build_time"]


class ExcerptsByType(Excerpts):
    master_key = 'excerpt_type'
    column_names = "build_time user *"
    order_by = ["build_time"]


class ExcerptsByX(Excerpts):
    required = dd.required(user_groups='office')
    column_names = "build_time excerpt_type user *"
    order_by = ["-build_time"]

if settings.SITE.project_model is not None:

    class ExcerptsByProject(ExcerptsByX):
        master_key = 'project'


class ExcerptsByOwner(ExcerptsByX):
    master_key = 'owner'
    column_names = "build_time excerpt_type user *"
    help_text = _("History of excerpts based on this data record.")


class ExcerptsByCompany(ExcerptsByX):
    master_key = 'company'
    column_names = "build_time excerpt_type user *"


class ExcerptsByPerson(ExcerptsByX):
    master_key = 'contact_person'
    column_names = "build_time excerpt_type user *"


system = dd.resolve_app('system')


def setup_main_menu(site, ui, profile, m):
    m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
    m.add_action('excerpts.MyExcerpts')


def setup_config_menu(site, ui, profile, m):
    m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
    m.add_action('excerpts.ExcerptTypes')


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu("office", system.OFFICE_MODULE_LABEL)
    m.add_action('excerpts.Excerpts')


@dd.receiver(dd.pre_analyze)
def set_excerpts_actions(sender, **kw):
    # logger.info("20140401 %s.set_attest_actions()", __name__)
    # in case ExcerptType is overridden
    ExcerptType = sender.modules.excerpts.ExcerptType
    ctypes = set()
    try:
        for atype in ExcerptType.objects.all():
            ct = atype.content_type
            if not ct is None and not ct in ctypes:
                ctypes.add(ct)
                m = ct.model_class()
                m.define_action(create_excerpt=CreateExcerpt())
                m.define_action(
                    show_excerpts=dd.ShowSlaveTable(
                        'excerpts.ExcerptsByOwner'
                    ))
                # logger.info("20140401 %s is attestable", m)
    except Exception as e:
        logger.info("Failed to load excerpts_actions : %s", e)

    # An attestable model must also inherit
    # :class:`lino.mixins.printable.BasePrintable` or some subclass
    # thereof.
