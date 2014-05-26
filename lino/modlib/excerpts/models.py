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

from django.core.exceptions import ValidationError

from lino import dd
from lino import mixins
from lino.mixins.printable import model_group

from lino.utils.xmlgen.html import E

outbox = dd.resolve_app('outbox')
postings = dd.resolve_app('postings')
contacts = dd.resolve_app('contacts')

from .mixins import Certifiable


class ExcerptType(
        dd.BabelNamed,
        mixins.PrintableType,
        outbox.MailableType):

    # templates_group = 'excerpts/Excerpt'

    class Meta:
        abstract = dd.is_abstract_model('excerpts.ExcerptType')
        verbose_name = _("Excerpt Type")
        verbose_name_plural = _("Excerpt Types")

    certifying = models.BooleanField(
        verbose_name=_("Certifying"),
        default=False,
        help_text=_("Whether an excerpt of this type is a unique printout."))

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

    backward_compat = models.BooleanField(
        _("Backward compatible"),
        default=False,
        help_text=_("Check this to have `this` in template context "
                    "point to owner instead of excerpt."))

    @dd.chooser(simple_values=True)
    def template_choices(cls, build_method, content_type):
        tplgroups = [model_group(content_type.model_class()), 'excerpts']
        return cls.get_template_choices(build_method, tplgroups)

    @dd.chooser(simple_values=True)
    def body_template_choices(cls, content_type):
        tplgroups = [model_group(content_type.model_class()), 'excerpts']
        return settings.SITE.list_templates('.body.html', tplgroups)

    # @dd.chooser(simple_values=True)
    # def body_template_choices(cls):
    #     return settings.SITE.list_templates(
    #         '.body.html', cls.get_templates_group())

    def full_clean(self, *args, **kwargs):
        if self.certifying:
            if not self.primary:
                raise ValidationError(
                    _("Cannot set %(c)s without %(p)s") % dict(
                        c=_("Certifying"), p=_("Primary")))
            mc = self.content_type.model_class()
            if not issubclass(mc, Certifiable):
                raise ValidationError(
                    _("Cannot set %(c)s for non.certifiable "
                      "model %(m)s") % dict(
                        c=_("Certifying"), m=mc.meta.verbose_name))
        super(ExcerptType, self).full_clean(*args, **kwargs)

    def after_ui_save(self, ar):
        super(ExcerptType, self).after_ui_save(ar)
        if self.primary:
            for o in self.content_type.excerpt_types.exclude(id=self.id):
                if o.primary:
                    o.primary = False
                    o.save()
                    ar.set_response(refresh_all=True)

    @classmethod
    def get_template_groups(cls):
        raise Exception("""20140520 Not used by ExcerptType. We
        override everything else to not call the class method.""")


class ExcerptTypes(dd.Table):

    """
    Displays all rows of :class:`ExcerptType`.
    """
    model = 'excerpts.ExcerptType'
    required = dd.required(user_level='admin', user_groups='office')
    column_names = ("content_type primary certifying name build_method "
                    "template *")
    order_by = ["content_type", "name"]

    insert_layout = """
    name
    content_type primary certifying
    build_method template body_template
    """

    detail_layout = """
    id name
    content_type:15 build_method:15 template:15 \
    body_template:15 email_template:15
    primary certifying backward_compat attach_to_email
    # remark:60x5
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
    icon_name = 'printer'
    help_text = _('Print this data record.')
    label = _('Print')
    sort_index = 50  # like "Print"
    combo_group = "creacert"

    def __init__(self, etype, *args, **kwargs):
        self.excerpt_type = etype
        super(CreateExcerpt, self).__init__(*args, **kwargs)

    def run_from_ui(self, ar, **kw):
        Excerpt = dd.modules.excerpts.Excerpt
        obj = ar.selected_rows[0]
        qs = Excerpt.objects.filter(
            excerpt_type=self.excerpt_type,
            owner_id=obj.pk,
            owner_type=ContentType.objects.get_for_model(obj.__class__))
        qs = qs.order_by('id')
        if qs.count() == 0:
            akw = dict(
                user=ar.get_user(),
                owner=obj,
                excerpt_type=self.excerpt_type)
            akw = obj.get_excerpt_options(ar, **akw)
            a = Excerpt(**akw)
            a.full_clean()
            a.save()
        else:
            a = qs[0]

        if self.excerpt_type.certifying:
            obj.printed_by = a
            obj.full_clean()
            obj.save()

        a.do_print.run_from_ui(ar, **kw)


class ClearPrinted(dd.Action):
    sort_index = 51
    label = _('Clear printed')
    icon_name = 'printer_delete'
    help_text = _("Mark this object as not printed.")

    def get_action_permission(self, ar, obj, state):
        if obj.printed_by_id is None:
            return False
        return super(ClearPrinted, self).get_action_permission(
            ar, obj, state)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        if obj.printed_by_id is None:
            ar.error(_("Oops."))
            return

        def ok(ar2):
            obj.clear_cache()
            ar2.success(_("Printedness has been undone."), refresh=True)
        if False:
            ar.confirm(
                ok,
                _("Going to undo the printedness of %s") % dd.obj2unicode(obj))
        else:
            ok(ar)


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

    excerpt_type = dd.ForeignKey('excerpts.ExcerptType')

    language = dd.LanguageField()

    mails_by_owner = dd.ShowSlaveTable('outbox.MailsByController')

    def __unicode__(self):
        if self.build_time:
            return unicode(self.build_time)
        return _("Unprinted %s #%d") % (self._meta.verbose_name, self.pk)

    def get_mailable_type(self):
        return self.excerpt_type

    def get_template_groups(self):
        ptype = self.get_printable_type()
        if ptype is None:
            raise Exception("20140520 Must have excerpt_type.")
        grp = model_group(ptype.content_type.model_class())
        return [grp, 'excerpts']

    def filename_root(self):
        # mainly because otherwise we would need to move files around on
        # existing sites
        et = self.excerpt_type
        if et is None or not et.certifying:
            return super(Excerpt, self).filename_root()
        o = self.owner
        return o._meta.app_label + '.' + o.__class__.__name__ + '-' + str(o.pk)

    def get_printable_type(self):
        return self.excerpt_type

    def get_print_language(self):
        """Returns the language to be selected when rendering this
        Excerpt. Default implementation returns the content of
        `self.language`.

        """
        return self.language

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

    @dd.virtualfield(dd.HtmlBox(_("Preview")))
    def preview(self, ar):
        with translation.override(self.get_print_language()):
            ctx = self.get_printable_context(ar)
            return '<div class="htmlText">%s</div>' % ctx['body']

    def get_printable_context(self, ar, **kw):
        kw = super(Excerpt, self).get_printable_context(ar, **kw)
        kw.update(obj=self.owner)
        # kw.update(excerpt=self)
        body = ''
        if self.excerpt_type_id is not None:
            atype = self.excerpt_type
            if atype.backward_compat:
                kw.update(this=self.owner)

            if atype.body_template:
                tplname = atype.body_template
                tplgroup = model_group(atype.content_type.model_class())
                tplname = tplgroup + '/' + tplname
                saved_renderer = ar.renderer
                ar.renderer = settings.SITE.ui.plain_renderer
                template = settings.SITE.jinja_env.get_template(tplname)
                body = template.render(**kw)
                ar.renderer = saved_renderer
        kw.update(body=body)
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
    column_names = ("id build_time owner excerpt_type user project "
                    "company contact_person *")
    order_by = ["id"]


class MyExcerpts(mixins.ByUser, Excerpts):
    required = dd.required(user_groups='office')
    column_names = "build_time excerpt_type project *"
    order_by = ["-build_time"]


class ExcerptsByX(Excerpts):
    required = dd.required(user_groups='office')
    column_names = "build_time excerpt_type owner *"
    order_by = ['-build_time', 'id']
    auto_fit_column_widths = True


class ExcerptsByType(ExcerptsByX):
    master_key = 'excerpt_type'


class ExcerptsByOwner(ExcerptsByX):
    master_key = 'owner'
    help_text = _("History of excerpts based on this data record.")
    # hidden_columns = 'owner'

if settings.SITE.project_model is not None:

    class ExcerptsByProject(ExcerptsByX):
        master_key = 'project'


class ExcerptsByCompany(ExcerptsByX):
    master_key = 'company'


class ExcerptsByPerson(ExcerptsByX):
    master_key = 'contact_person'


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
    try:
        for atype in ExcerptType.objects.all():
            ct = atype.content_type
            if ct is not None:
                m = ct.model_class()
                an = 'create_excerpt'
                if not atype.primary:
                    an += str(atype.pk)
                m.define_action(**{an: CreateExcerpt(
                    atype, unicode(atype))})
                if atype.primary:
                    if atype.certifying:
                        m.define_action(
                            clear_printed=ClearPrinted())
                    else:
                        m.define_action(
                            show_excerpts=dd.ShowSlaveTable(
                                'excerpts.ExcerptsByOwner'
                            ))
                # logger.info("20140401 %s is attestable", m)
    except Exception as e:
        logger.info("Failed to set excerpts actions : %s", e)

    # An attestable model must also inherit
    # :class:`lino.mixins.printable.BasePrintable` or some subclass
    # thereof.
