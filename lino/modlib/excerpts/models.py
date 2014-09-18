# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)
"""
The :xfile:`models.py` file for :mod:`ml.excerpts`.
"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from os.path import join, dirname

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

outbox = dd.require_app_models('outbox')
postings = dd.require_app_models('postings')

davlink = dd.resolve_plugin('davlink')

from .mixins import Certifiable


class ExcerptType(
        dd.BabelNamed,
        mixins.PrintableType,
        outbox.MailableType):

    # templates_group = 'excerpts/Excerpt'

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'ExcerptType')
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

    print_directly = models.BooleanField(_("Print directly"), default=True)

    @dd.chooser(simple_values=True)
    def template_choices(cls, build_method, content_type):
        tplgroups = [model_group(content_type.model_class()), 'excerpts']
        return cls.get_template_choices(build_method, tplgroups)

    @dd.chooser(simple_values=True)
    def body_template_choices(cls, content_type):
        # 20140617 don't remember why the "excerpts" group was useful here
        # tplgroups = [model_group(content_type.model_class()), 'excerpts']
        # return settings.SITE.list_templates('.body.html', *tplgroups)

        tplgroup = model_group(content_type.model_class())
        return settings.SITE.list_templates('.body.html', tplgroup)

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

    def update_siblings(self):
        updated = 0
        if self.primary:
            for o in self.content_type.excerpt_types.exclude(id=self.id):
                if o.primary:
                    o.primary = False
                    o.save()
                    updated += 1
        return updated

    def save(self, *args, **kwargs):
        # It is important to ensure that there is really only one
        # primary ExcerptType per model because
        # :func:`set_excerpts_actions` will install these as action on
        # the model.
        super(ExcerptType, self).save(*args, **kwargs)
        self.update_siblings()
        
    def after_ui_save(self, ar):
        super(ExcerptType, self).after_ui_save(ar)
        if self.primary:
        # if self.update_siblings():
            ar.set_response(refresh_all=True)

    @classmethod
    def get_template_groups(cls):
        raise Exception("""20140520 Not used by ExcerptType. We
        override everything else to not call the class method.""")

    def get_body_template_filename(self):
        if not self.body_template:
            return
        tplgroup = model_group(self.content_type.model_class())
        return settings.SITE.find_config_file(
            self.body_template, tplgroup)

    def get_body_template_name(self):
        if not self.body_template:
            return None
        tplgroup = model_group(self.content_type.model_class())
        return tplgroup + '/' + self.body_template

    @classmethod
    def update_for_model(cls, model, **kw):
        ct = ContentType.objects.get_for_model(dd.resolve_model(model))
        obj = cls.objects.get(primary=True, content_type=ct)
        for k, v in kw.items():
            setattr(obj, k, v)
        obj.full_clean()
        obj.save()

    def get_or_create_excerpt(self, ar):
        obj = ar.selected_rows[0]
        Excerpt = dd.modules.excerpts.Excerpt
        ex = None
        if self.certifying:
            qs = Excerpt.objects.filter(
                excerpt_type=self,
                owner_id=obj.pk,
                owner_type=ContentType.objects.get_for_model(obj.__class__))
            qs = qs.order_by('id')
            if qs.count() > 0:
                ex = qs[0]
        if ex is None:
            akw = dict(
                user=ar.get_user(),
                owner=obj,
                excerpt_type=self)
            akw = obj.get_excerpt_options(ar, **akw)
            ex = Excerpt(**akw)
            ex.full_clean()
            ex.save()

        if self.certifying:
            obj.printed_by = ex
            obj.full_clean()
            obj.save()

        return ex


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
    primary print_directly certifying backward_compat attach_to_email
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
    label = _('Print')
    help_text = _('Create an excerpt in order to print this data record.')
    sort_index = 50  # like "Print"
    combo_group = "creacert"

    def __init__(self, etype, *args, **kwargs):
        self.excerpt_type = etype
        super(CreateExcerpt, self).__init__(*args, **kwargs)

    def run_from_ui(self, ar, **kw):
        ex = self.excerpt_type.get_or_create_excerpt(ar)
        # logger.info("20140812 excerpts.CreateExcerpt %s", self.excerpt_type)
        if self.excerpt_type.print_directly:
            ex.do_print.run_from_ui(ar, **kw)
        else:
            ar.goto_instance(ex)


class ClearPrinted(dd.Action):
    sort_index = 51
    label = _('Clear print cache')
    icon_name = 'printer_delete'
    help_text = _("Mark this object as not printed. A subsequent "
                  "call to print will generate a new cache file.")

    def get_action_permission(self, ar, obj, state):
        if obj.printed_by_id is None:
            return False
        return super(ClearPrinted, self).get_action_permission(
            ar, obj, state)

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        if obj.printed_by is None:
            ar.error(_("Oops."))
            return

        def ok(ar2):
            obj.clear_cache()
            ar2.success(_("Print cache file has been cleared."), refresh=True)
        if False:
            ar.confirm(
                ok,
                _("Going to clear the print cache file of %s") %
                dd.obj2unicode(obj))
        else:
            ok(ar)


class BodyTemplateContentField(dd.VirtualField):

    editable = True

    def __init__(self, *args, **kw):
        if settings.SITE.confdirs.LOCAL_CONFIG_DIR is None:
            self.editable = False  # No local config dir
        rt = dd.RichTextField(*args, **kw)
        dd.VirtualField.__init__(self, rt, None)

    def value_from_object(self, obj, ar):
        fn = obj.excerpt_type.get_body_template_filename()
        if not fn:
            return "(%s)" % _(
                "Excerpt type \"%s\" has no body_template") % obj.excerpt_type
        return file(fn).read()

    def set_value_in_object(self, ar, obj, value):
        fn = obj.excerpt_type.get_body_template_name()
        if not fn:
            return
            # raise Warning(
            #     "No `body_template_name` while saving to %s" % dd.obj2str(obj))

        lcd = settings.SITE.confdirs.LOCAL_CONFIG_DIR
        if lcd is None:
            raise Warning("No local config directory. "
                          "Contact your system administrator.")
        local_file = join(lcd.name, fn)
        settings.SITE.makedirs_if_missing(dirname(local_file))
        value = value.encode('utf-8')
        logger.info("Wrote body_template_content %s", local_file)
        file(local_file, "w").write(value)


class Excerpt(dd.TypedPrintable,
              dd.UserAuthored,
              dd.Controllable,
              dd.ProjectRelated,
              outbox.Mailable,
              postings.Postable):

    manager_level_field = 'office_level'

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Excerpt')
        verbose_name = _("Excerpt")
        verbose_name_plural = _("Excerpts")

    excerpt_type = dd.ForeignKey('excerpts.ExcerptType')
    body_template_content = BodyTemplateContentField(_("Body template"))

    if dd.is_installed('outbox'):
        mails_by_owner = dd.ShowSlaveTable('outbox.MailsByController')

    def disabled_fields(self, ar):
        rv = super(Excerpt, self).disabled_fields(ar)
        rv = rv | set(['excerpt_type', 'project'])
        if self.build_time:
            rv |= self.PRINTABLE_FIELDS
        return rv

    def __unicode__(self):
        if self.build_time:
            return unicode(self.build_time)
        return _("Unprinted %s #%d") % (self._meta.verbose_name, self.pk)

    def get_mailable_type(self):
        return self.excerpt_type

    @property
    def recipient(self):
        return self.owner.get_print_recipient()

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
        return self.owner.get_print_language()

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
        return settings.SITE.today()

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

            tplname = atype.get_body_template_name()
            if tplname:
                saved_renderer = ar.renderer
                ar.renderer = settings.SITE.plugins.bootstrap3.renderer
                # ar.renderer = settings.SITE.ui.plain_renderer
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
    def on_analyze(cls, site):
        cls.PRINTABLE_FIELDS = dd.fields_list(
            cls,
            'project excerpt_type  \
            body_template_content \
            user build_method')
        super(Excerpt, cls).on_analyze(site)


if davlink:

    class ExcerptDetail(dd.FormLayout):
        window_size = (80, 15)
        main = "general config"
        general = dd.Panel(
            """
            id excerpt_type:25 project
            user:10 build_method
            owner build_time
            # preview
            """, label=_("General"))
        config = dd.Panel(
            "body_template_content",
            label=_("Configure"),
            required=dd.required(user_level="admin"))

else:

    class ExcerptDetail(dd.FormLayout):
        window_size = (80, 'auto')
        main = """
        id excerpt_type:25 project
        user:10 build_method
        owner build_time
        # preview
        """


class Excerpts(dd.Table):
    required = dd.required(user_groups='office', user_level='admin')
    # label = _("Excerpts history")
    icon_name = 'script'

    model = 'excerpts.Excerpt'
    detail_layout = ExcerptDetail()
    insert_layout = """
    excerpt_type 
    project
    """
    column_names = ("id build_time owner excerpt_type user project *")
    order_by = ["id"]

    allow_create = False


class MyExcerpts(mixins.ByUser, Excerpts):
    required = dd.required(user_groups='office')
    column_names = "build_time excerpt_type project *"
    order_by = ["-build_time"]


class ExcerptsByX(Excerpts):
    required = dd.required(user_groups='office')
    column_names = "build_time excerpt_type owner *"
    order_by = ['-build_time', 'id']
    auto_fit_column_widths = True
    # window_size = (70, 20)


class ExcerptsByType(ExcerptsByX):
    master_key = 'excerpt_type'


class ExcerptsByOwner(ExcerptsByX):
    master_key = 'owner'
    help_text = _("History of excerpts based on this data record.")
    label = _("Existing excerpts")

    slave_grid_format = 'summary'

    @classmethod
    def get_slave_summary(self, obj, ar):
        sar = self.request(master_instance=obj)
        items = []
        for ex in sar:
            items.append(E.li(ar.obj2html(ex)))
        if len(items) == 0:
            items.append(_("No excerpts."))

        # actions = []

        # def add_action(btn):
        #     if btn is None:
        #         return False
        #     actions.append(btn)
        #     return True

        # for lt in addable_link_types:
        #     sar = ar.spawn(Links, known_values=dict(type=lt, parent=obj))
        #     if add_action(sar.insert_button(
        #             lt.as_parent(obj), icon_name=None)):
        #         if not lt.symmetric:
        #             actions.append('/')
        #             sar = ar.spawn(
        #                 Links, known_values=dict(type=lt, child=obj))
        #             add_action(sar.insert_button(
        #                 lt.as_child(obj), icon_name=None))
        #         actions.append(' ')

        # elems += [E.br(), _("Create relationship as ")] + actions
        return E.div(*items)


if settings.SITE.project_model is not None:

    class ExcerptsByProject(ExcerptsByX):
        master_key = 'project'


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
        etypes = [(obj, obj.content_type)
                  for obj in ExcerptType.objects.all()]
    except Exception as e:
        etypes = []
        logger.warning("Failed to set excerpts actions : %s", e)

    for atype, ct in etypes:
        if ct is not None:
            m = ct.model_class()
            if atype.primary:
                an = 'do_print'
            else:
                an = 'create_excerpt' + str(atype.pk)
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
            # logger.info(
            #     "20140618 %s.define_action('%s') from %s ", ct, an, atype)

    # An attestable model must also inherit
    # :class:`lino.mixins.printable.BasePrintable` or some subclass
    # thereof.
