# -*- coding: UTF-8 -*-
# Copyright 2010-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from django import VERSION
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.utils import DatabaseError
from django.db.models import FieldDoesNotExist
from django.contrib.contenttypes.models import ContentType, models

from lino.core.roles import SiteStaff
from lino.api import dd, rt
from etgen.html import E
from lino.utils import join_elems

from lino.core.utils import get_models


if VERSION[0] > 2:
    # restore Django 2 behaviour
    def old__ct_str(self):
        return self.name
    ContentType.__str__ = old__ct_str


class ContentTypes(dd.Table):
    model = 'contenttypes.ContentType'

    required_roles = dd.login_required(SiteStaff)

    detail_layout = """
    id app_label model base_classes
    HelpTextsByModel
    BrokenGFKsByModel
    """

    @dd.displayfield(_("Base classes"))
    def base_classes(self, obj, ar):
        if obj is None:
            return ""
        chunks = []

        def add(cl):
            for b in cl.__bases__:
                add(b)
            # :
            if issubclass(cl, dd.Model) and cl is not dd.Model \
               and cl._meta.managed:
                if getattr(cl, '_meta', False) and not cl._meta.abstract:
                    #~ logger.info("20120205 adding(%r)",cl)
                    ct = ContentType.objects.get_for_model(cl)
                    chunks.append(
                        ar.obj2html(ct, str(cl._meta.verbose_name)))
        #~ add(obj.model_class())
        cl = obj.model_class()
        # e.g. if database is nor synchronized
        if cl is not None:
            for b in cl.__bases__:
                add(b)
        return E.p(*join_elems(chunks, sep=', '))



class HelpText(dd.Model):
    class Meta(object):
        app_label = 'gfks'
        verbose_name = _("Help Text")
        verbose_name_plural = _("Help Texts")

    content_type = dd.ForeignKey('contenttypes.ContentType',
                                 verbose_name=_("Model"))
    field = models.CharField(_("Field"), max_length=200)

    help_text = dd.RichTextField(_("HelpText"),
                                 blank=True, null=True, format='plain')

    def __str__(self):
        return self.content_type.app_label + '.' \
            + self.content_type.model + '.' + self.field

    @dd.chooser(simple_values=True)
    def field_choices(cls, content_type):
        l = []
        if content_type is not None:
            model = content_type.model_class()
            meta = model._meta
            for f in meta.fields:
                if not getattr(f, '_lino_babel_field', False):
                    l.append(f.name)
            for f in meta.many_to_many:
                l.append(f.name)
            for f in meta.virtual_fields:
                l.append(f.name)
            for a in model.get_default_table().get_actions():
                l.append(a.action.action_name)
            l.sort()
        return l

    #~ def get_field_display(cls,fld):
        #~ return fld

    @dd.virtualfield(models.CharField(_("Verbose name"), max_length=200))
    def verbose_name(self, request):
        m = self.content_type.model_class()
        de = m.get_default_table().get_data_elem(self.field)
        if isinstance(de, models.Field):
            return "%s (%s)" % (str(de.verbose_name),
                                str(_("database field")))
        if isinstance(de, dd.VirtualField):
            return str(de.return_type.verbose_name)
        if isinstance(de, dd.Action):
            return str(de.label)
        return str(de)


class HelpTexts(dd.Table):
    required_roles = dd.login_required(SiteStaff)
    model = 'gfks.HelpText'
    column_names = "field verbose_name help_text id content_type"


class HelpTextsByModel(HelpTexts):
    master_key = 'content_type'


class BrokenGFKs(dd.VirtualTable):
    label = _("Broken GFKs")
    required_roles = dd.login_required(SiteStaff)

    column_names = "database_model database_object message todo"

    @classmethod
    def get_data_rows(self, ar):
        f = settings.SITE.kernel.get_broken_generic_related
        for model in get_models(include_auto_created=True):
            for obj in f(model):
                yield obj

    @dd.displayfield(_("Database object"))
    def database_object(self, obj, ar):
        return ar.obj2html(obj)

    @dd.displayfield(_("Message"))
    def message(self, obj, ar):
        return obj._message

    @dd.displayfield(_("Action"))
    def todo(self, obj, ar):
        return obj._todo

    @dd.displayfield(_("Database model"))
    def database_model(self, obj, ar):
        ct = ContentType.objects.get_for_model(obj.__class__)
        return ar.obj2html(ct)


class BrokenGFKsByModel(BrokenGFKs):
    master = 'contenttypes.ContentType'

    column_names = "database_object message todo"

    @classmethod
    def get_data_rows(self, ar):
        mi = ar.master_instance
        f = settings.SITE.kernel.get_broken_generic_related
        if mi is not None:
            for obj in f(mi.model_class()):
                yield obj

    @classmethod
    def get_pk_field(self):
        return settings.SITE.site_config._meta.get_field('id')

    @classmethod
    def get_row_by_pk(self, ar, pk):
        mi = ar.master_instance
        if mi is None:
            return None
        M = mi.model_class()
        try:
            return M.objects.get(pk=pk)
        except ValueError:
            return None
        except M.DoesNotExist:
            return None

    @classmethod
    def get_row_permission(cls, obj, ar, state, ba):
        return True


if False:  # disabled 20160712

  @dd.receiver(dd.pre_ui_build)
  def my_pre_ui_build(sender, **kw):
    try:
        HelpText = rt.models.gfks.HelpText
        for ht in HelpText.objects.filter(help_text__isnull=False):
            # dd.logger.info("20120629 %s.help_text", ht)
            try:
                dd.resolve_field(str(ht)).help_text = ht.help_text
            except FieldDoesNotExist as e:
                #~ logger.debug("No help texts : %s",e)
                pass
    except DatabaseError as e:
        dd.logger.debug("No help texts : %s", e)
        pass


# cause `inv mm` to generate translatable strings from Django's
# original module since those translations are not loaded.
_("content type")
_("content types")
