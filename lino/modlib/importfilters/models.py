# Copyright 2009-2015 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.importfilter`.

"""
from builtins import str
from builtins import object


import logging
logger = logging.getLogger(__name__)
#~ from lino.utils import dblogger

from django.conf import settings
from django.contrib.contenttypes import models as contenttypes
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text


from django.db import models
from django.utils.translation import ugettext_lazy as _


from lino.api import dd, rt

from lino.utils.instantiator import Instantiator


class FieldSeparators(dd.ChoiceList):
    pass


class Filter(dd.Model):
    name = models.CharField(_("Name"), max_length=200)
    content_type = dd.ForeignKey(contenttypes.ContentType,
                                 verbose_name=_("Model"))
    field_sep = models.CharField(_("Field separator"), max_length=10)
    help_text = dd.RichTextField(_("HelpText"),
                                 blank=True, null=True, format='plain')


class Filters(dd.Table):
    model = Filter
    column_names = "name content_type *"
    detail_layout = """
    name content_type field_sep
    help_text
    importfilters.ItemsByFilter
    """


class Item(mixins.Sequenced):

    class Meta(object):
        verbose_name = _("Import Filter Item")
        verbose_name_plural = _("Import Filter Items")

    filter = dd.ForeignKey(Filter)
    field = models.CharField(_("Field"), max_length=200)
    column = models.IntegerField(_("Column"))

    help_text = dd.RichTextField(_("HelpText"),
                                 blank=True, null=True, format='plain')

    @dd.chooser(simple_values=True)
    def field_choices(cls, filter):
        l = []
        if filter is not None:
            model = filter.content_type.model_class()
            meta = model._meta
            for f in meta.fields:
                if not getattr(f, '_lino_babel_field', False):
                    l.append(f.name)
            l.sort()
        return l


class Items(dd.Table):
    model = Item
    column_names = "column field help_text *"


class ItemsByFilter(Items):
    master_key = 'filter'
    column_names = "column field help_text workflow_buttons *"


class Import(dd.VirtualTable):
    column_names = 'description obj2unicode'
    parameters = dict(
        filter=dd.ForeignKey(Filter),
        data=dd.RichTextField(_("Data to import"),
                              blank=True, null=True,
                              format='plain'))

    @classmethod
    def get_data_rows(self, ar):
        flt = ar.param_values.filter
        build = Instantiator(flt.content_type.model_class()).build
        for ln in ar.param_values.data.splitlines():
            ln = ln.strip()
            if ln:
                kw = dict()
                cells = flt.field_sep.split(ln)
                for item in flt.item_set.all():
                    if item.column:
                        kw[item.field] = cells[item.column-1]
                yield build(**kw)

    @dd.displayfield(_("Description"))
    def description(cls, obj, ar):
        kw = dict()
        flt = ar.param_values.filter
        for item in flt.item_set.all():
            kw[item.field] = getattr(obj, item.field)
        return str(kw)

    @dd.displayfield(_("obj2unicode"))
    def obj2unicode(cls, obj, ar):
        return dd.obj2unicode(obj)


