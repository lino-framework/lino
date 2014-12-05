# -*- coding: UTF-8 -*-
# Copyright 2010-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""

.. autosummary::

"""


# from django.contrib.contenttypes.models import *
from django.contrib.contenttypes.models import ContentType, models


from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.db.utils import DatabaseError
from django.db.models import FieldDoesNotExist

from lino import dd, rt
from lino.utils.xmlgen.html import E
from lino.utils import join_elems


from .mixins import Controllable


class ContentTypes(dd.Table):

    """
    Deserves more documentation.
    """
    model = 'contenttypes.ContentType'

    required = dd.required(user_level='manager')

    detail_layout = """
    id name app_label model base_classes
    HelpTextsByModel
    StaleControllablesByModel
    """

    @dd.displayfield(_("Base classes"))
    def base_classes(self, obj, ar):
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
                        ar.obj2html(ct, unicode(cl._meta.verbose_name)))
        if obj is not None:
            #~ add(obj.model_class())
            for b in obj.model_class().__bases__:
                add(b)
        return E.p(*join_elems(chunks, sep=', '))


class HelpText(dd.Model):

    class Meta:
        verbose_name = _("Help Text")
        verbose_name_plural = _("Help Texts")

    content_type = models.ForeignKey('contenttypes.ContentType',
                                     verbose_name=_("Model"))
    field = models.CharField(_("Field"), max_length=200)

    help_text = dd.RichTextField(_("HelpText"),
                                 blank=True, null=True, format='plain')

    def __unicode__(self):
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
            return "%s (%s)" % (unicode(de.verbose_name),
                                unicode(_("database field")))
        if isinstance(de, dd.VirtualField):
            return unicode(de.return_type.verbose_name)
        if isinstance(de, dd.Action):
            return unicode(de.label)
        return str(de)


class HelpTexts(dd.Table):
    required = dd.required(user_level='manager')
    model = 'contenttypes.HelpText'
    column_names = "field verbose_name help_text id content_type"


class HelpTextsByModel(HelpTexts):
    master_key = 'content_type'


class StaleControllables(dd.VirtualTable):

    label = _("Stale Controllables")

    column_names = "database_object owner_model owner_id"

    @classmethod
    def get_data_rows(self, ar):
        for M in rt.models_by_base(Controllable):
            for obj in M.objects.filter(owner_id__isnull=False):
                if obj.owner is None:
                    yield obj

    @dd.displayfield(_("Database object"))
    def database_object(self, obj, ar):
        return ar.obj2html(obj)

    @dd.virtualfield(models.IntegerField(_("Primary key")))
    def owner_id(self, obj, ar):
        return obj.owner_id

    @dd.displayfield(_("Controlling model"))
    def owner_model(self, obj, ar):
        ct = ContentType.objects.get_for_model(obj.__class__)
        return ar.obj2html(ct)
        # return dd.full_model_name(obj.__class__)


class StaleControllablesByModel(StaleControllables):
    master = 'contenttypes.ContentType'

    column_names = "database_object owner_id"

    @classmethod
    def get_data_rows(self, ar):
        rows = []
        mi = ar.master_instance
        # TODO: find them using a real database request
        if mi is not None:
            M = mi.model_class()
            if issubclass(M, Controllable):
                for obj in M.objects.filter(owner_id__isnull=False):
                    if obj.owner is None:
                        rows.append(obj)
        return rows

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

hook = dd.plugins.system


def setup_reports_menu(site, ui, profile, m):
    m = m.add_menu(hook.app_label, hook.verbose_name)
    m.add_action(site.modules.contenttypes.StaleControllables)


def setup_config_menu(site, ui, profile, m):
    m = m.add_menu(hook.app_label, hook.verbose_name)
    m.add_action(site.modules.contenttypes.HelpTexts)


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu(hook.app_label, hook.verbose_name)
    m.add_action(site.modules.contenttypes.ContentTypes)


@dd.receiver(dd.pre_ui_build)
def my_pre_ui_build(sender, **kw):
    try:
        HelpText = rt.modules.contenttypes.HelpText
        for ht in HelpText.objects.filter(help_text__isnull=False):
            #~ logger.info("20120629 %s.help_text", ht)
            try:
                dd.resolve_field(unicode(ht)).help_text = ht.help_text
            except FieldDoesNotExist as e:
                #~ logger.debug("No help texts : %s",e)
                pass
    except DatabaseError as e:
        dd.logger.debug("No help texts : %s", e)
        pass


# cause `fab mm` to generate translatable strings from Django's
# original module since those translations are not loaded.
_("content type")
_("content types")
