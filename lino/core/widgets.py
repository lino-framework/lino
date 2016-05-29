# -*- coding: UTF-8 -*-
# Copyright 2009-2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""Defines widgets ("layout elements") and a :class:`WidgetFactory`.


"""

from __future__ import unicode_literals
from builtins import str
from builtins import object

import threading

from django.conf import settings
from django.db import models
from django.db.models.fields import NOT_PROVIDED

from django.db.models.fields.related import \
    ReverseOneToOneDescriptor as SingleRelatedObjectDescriptor
from django.db.models.fields.related import \
    ReverseManyToOneDescriptor as ForeignRelatedObjectsDescriptor
from django.db.models.fields.related import \
    ManyToManyDescriptor as ManyRelatedObjectsDescriptor
from django.db.models.fields.related import ManyToManyRel, ManyToOneRel


from lino.core import layouts
from lino.core import constants
from lino.core import fields
from lino.core.gfks import GenericRelation
from lino.core.gfks import GenericForeignKey
from lino.core.layouts import DummyPanel
from lino.core.permissions import Permittable
from lino.core.layouts import (FormLayout, ParamsLayout,
                               ColumnsLayout, ActionParamsLayout)

from lino.utils import join_elems
from lino.utils import curry
from lino.utils.mldbc.fields import BabelCharField, BabelTextField
from lino.utils.ranges import constrain
from lino.utils.xmlgen.html import E
from lino.utils.html2xhtml import html2xhtml
from lino.core.permissions import make_view_permission_handler

user_profile_rlock = threading.RLock()
_for_user_profile = None


def with_user_profile(profile, func, *args, **kwargs):
    """Run the given callable `func` with the given user profile `profile`
    activated. Optional args and kwargs are forwarded to the callable,
    and the return value is returned.

    """
    global _for_user_profile

    with user_profile_rlock:
        old = _for_user_profile
        _for_user_profile = profile
        return func(*args, **kwargs)
        _for_user_profile = old


def get_user_profile():
    return _for_user_profile


def is_hidden_babel_field(fld):
    lng = getattr(fld, '_babel_language', None)
    if lng is None:
        return False
    if _for_user_profile is None:
        return False
    if _for_user_profile.hidden_languages is None:
        return False
    if lng in _for_user_profile.hidden_languages:
        return True
    return False


class Widget(Permittable):
    name = None
    vflex = False
    hflex = True
    width = None
    height = None
    preferred_width = 10
    preferred_height = 1
    hidden = False
    editable = False
    label = None
    label_width = 0
    parent = None  # will be set by Container

    def __init__(self, layout_handle, name, **kwargs):
        self.layout_handle = layout_handle
        self.name = name
        # new since 20121130. theoretically better
        if 'required_roles' in kwargs:
            assert isinstance(kwargs['required_roles'], set)
        else:
            required = set()
            required |= self.required_roles
            kwargs.update(required_roles=required)

        # install `allow_read` permission handler:
        self.install_permission_handler()
        self.setup(**kwargs)

    def __repr__(self):
        return "{0} {2} in {1}".format(
            self.__class__.__name__, self.layout_handle, self.name)

    def __str__(self):
        "This shows how the widget is specified"
        name = self.name
        if self.width is None:
            return name
        if self.height is None:
            return name + ":%d" % self.width
        return name + ":%dx%d" % (self.width, self.height)

    def setup(self, width=None, height=None, label=None,
              preferred_width=None,
              # help_text=None,
              required_roles=NOT_PROVIDED, **ignored):
        if preferred_width is not None:
            self.preferred_width = preferred_width
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if label is not None:
            self.label = label
        if required_roles is not NOT_PROVIDED:
            if not isinstance(required_roles, set):
                raise Exception(
                    "20150628 %s has required_roles %s" % (
                        self, required_roles))
            self.required_roles = required_roles
        # if help_text is not None:
        #     self.help_text = help_text
        return ignored

    def install_permission_handler(self):
        self.allow_read = curry(make_view_permission_handler(
            self, True,
            self.debug_permissions,
            self.required_roles), self)

    def is_visible(self):
        if self.hidden:
            return False
        return self.is_permitted()

    def is_permitted(self):
        return self.get_view_permission(_for_user_profile)

    def get_view_permission(self, profile):
        return self.allow_read(profile)

    # def walk(self):
    #     if self.is_visible():
    #         yield self

    def set_parent(self, parent):
        self.parent = parent
        if self.label:
            if isinstance(parent, Panel):
                if parent.label_align == layouts.LABEL_ALIGN_LEFT:
                    self.preferred_width += len(self.label)

    def add_requirements(self, *args):
        super(Widget, self).add_requirements(*args)
        self.install_permission_handler()

    def unused_loosen_requirements(self, actor):
        """Retain only those requirements of `self` which are
        also in `actor`.

        For example an InsertFormPanel has initially the requirements
        of the actor who defines it. That actor may not be visible to
        the current user.  But the panel may be used by other actors
        which are visible because they have less requirements.

        """
        if self.layout_handle.layout._datasource == actor:
            return  # nothing to loosen

        s1 = self.required_roles
        self.required_roles = self.required_roles & actor.required_roles
        # NB: don't change above line to the shorter syntax:
        # self.required_roles &= actor.required_roles
        # Because then the following wouldn't work:
        loosened = s1 != self.required_roles

        if loosened:
            # tpl = "20150716 loosened requirements of {0} from {1}"
            # msg = tpl.format(self, actor)
            # #logger.info(msg)
            # raise Exception(msg)
            self.install_permission_handler()

    def ext_options(self, **options):
        return options

    def as_plain_html(self, ar, obj):
        yield E.p("cannot handle %s" % self.__class__)


class Panel(Widget):
    def __init__(self, lh, name, vertical, *widgets, **kwargs):
        self.vertical = vertical
        # self.widgets = widgets
        self.widgets = self.columns = widgets
        super(Panel, self).__init__(lh, name, **kwargs)


class DetailMainPanel(Panel):
    pass


class ParamsPanel(Panel):
    pass


class ActionParamsPanel(Panel):
    pass


class TabPanel(Panel):
    pass


class ConstantWidget(Widget):
    vflex = True

    def __init__(self, lh, fld, **kw):
        Widget.__init__(self, lh, fld.name, **kw)
        self.html = fld.text_fn(lh.layout._datasource)

    def as_plain_html(self, ar, obj):
        return self.html


class FieldWidget(Widget):
    """
    Base class for all Widgets on some filed-like data element.
    """
    stored = True
    filter_type = None  # 'auto'
    active_change_event = 'change'
    zero = 0

    def __init__(self, layout_handle, field, **kw):
        if not getattr(field, 'name', None):
            raise Exception("Field '%s' in %s has no name!" %
                            (field, layout_handle))
        self.field = field
        self.editable = field.editable  # and not field.primary_key

        kw.setdefault('label', field.verbose_name)
        self.add_default_value(kw)

        Widget.__init__(self, layout_handle, field.name, **kw)

    def add_default_value(self, kw):
        if self.field.has_default():
            dv = self.field.default
            if callable(dv):
                return
                # dv = dv()
            kw.update(value=dv)

    def value_from_object(self, obj, ar):
        """
        Wrapper around Django's `value_from_object`.
        But for virtual fields it also forwards the action request `ar`.
        """
        return self.field.value_from_object(obj)

    def as_plain_html(self, ar, obj):
        value = self.value_from_object(obj, ar)
        text = str(value)
        if not text:
            text = " "
        # yield E.p(unicode(elem.field.verbose_name),':',E.br(),E.b(text))
        yield E.label(str(self.field.verbose_name))
        yield E.input(type="text", value=text)

    def cell_html(self, ui, row):
        return getattr(row, self.field.name)

    def value2html(self, ar, v, **cellattrs):
        """Return an etree element representing of the given value.  The
        possible return values may be:

        - an xml.etree.ElementTree.Element

        The default implementation returns an HTML element obtained
        from :meth:`format_value`.

        """
        if self.field.primary_key:
            url = ar.renderer.pk2url(ar, v)
            if url is not None:
                return E.td(E.a(self.format_value(
                    ar, v), href=url), **cellattrs)
        return E.td(self.format_value(ar, v), **cellattrs)

    def format_value(self, ar, v):
        return self.field._lino_atomizer.format_value(ar, v)

    def sum2html(self, ar, sums, i, **cellattrs):
        return E.td(self.format_sum(ar, sums, i), **cellattrs)

    def format_sum(self, ar, sums, i):
        """Return a string or an html element which expresses a sum of this
        column.

        :ar: the action request
        :sums: a list of sum values for all columns of this `ar`
        :i: the index of this field in `sums`

        """
        if i == 0:
            return E.b(ar.get_sum_text())
        if sums[i]:
            return E.b(self.format_value(ar, sums[i]))
        return ''

    def value2num(self, v):
        # print "20120426 %s value2num(%s)" % (self,v)
        return 0


class TextFieldWidget(FieldWidget):
    vflex = True
    # width = 60
    preferred_width = 60
    preferred_height = 5
    format = 'plain'

    def __init__(self, lh, field, **kw):
        self.format = getattr(field, 'textfield_format', None) \
            or settings.SITE.textfield_format
        FieldWidget.__init__(self, lh, field, **kw)

    def as_plain_html(self, ar, obj):
        value = self.field.value_from_object(obj)
        text = str(value)
        if not text:
            text = " "
        # yield E.p(unicode(elem.field.verbose_name),':',E.br(),E.b(text))
        yield E.label(str(self.field.verbose_name))
        yield E.textarea(text, rows=str(self.preferred_height))

    def value2html(self, ar, v, **cellattrs):
        if self.format == 'html' and v:
            v = html2xhtml(v)
            top = E.fromstring(v)
        else:
            top = self.format_value(ar, v)
        return E.td(top, **cellattrs)


class DisplayWidget(FieldWidget):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('value', '<br/>')  # see blog/2012/0527
        kwargs.update(always_enabled=True)
        FieldWidget.__init__(self, *args, **kwargs)
        self.preferred_height = self.field.preferred_height
        self.preferred_width = self.field.preferred_width
        if self.field.max_length:
            self.preferred_width = self.field.max_length


class RecurrenceWidget(DisplayWidget):
    pass


class ForeignKeyWidget(FieldWidget):
    preferred_width = 20

    def cell_html(self, ui, row):
        obj = getattr(row, self.field.name)
        if obj is None:
            return ''
        return ui.obj2html(obj)

    def value2html(self, ar, v, **cellattrs):
        return E.td(ar.obj2html(v), **cellattrs)


class GenericForeignKeyWidget(DisplayWidget):

    def __init__(self, layout_handle, field, **kw):
        self.field = field
        self.editable = False
        kw.update(label=getattr(field, 'verbose_name', None) or field.name)
        # kw.update(label=field.verbose_name)
        Widget.__init__(self, layout_handle, field.name, **kw)

    def add_default_value(self, kw):
        pass


class HtmlBoxWidget(DisplayWidget):
    preferred_height = 5
    vflex = True


class SlaveSummaryPanel(HtmlBoxWidget):
    """The panel used to display a slave table whose `slave_grid_format`
is 'summary'.

    """
    def __init__(self, lh, actor, **kw):
        box = fields.HtmlBox(actor.label, help_text=actor.help_text)
        fld = fields.VirtualField(box, actor.get_slave_summary)
        fld.name = actor.__name__
        fld.lino_resolve_type()
        super(SlaveSummaryPanel, self).__init__(lh, fld, **kw)


class GridWidget(Panel):
    vflex = True
    xtype = None
    preferred_height = 5

    def __init__(self, layout_handle, name, rpt, *columns, **kw):
        self.actor = rpt
        if len(columns) == 0:
            self.rh = rpt.get_handle()
            if not hasattr(self.rh, 'list_layout'):
                raise Exception("%s has no list_layout" % self.rh)
            columns = self.rh.list_layout.main.columns
            # columns = self.rh.list_layout._main.elements
        w = 0
        for e in columns:
            w += (e.width or e.preferred_width)
        self.preferred_width = constrain(w, 10, 120)
        self.columns = columns

        kw.setdefault('label', rpt.label)

        super(GridWidget, self).__init__(layout_handle, name, True, **kw)

    def headers2html(self, ar, columns, headers, **cellattrs):
        assert len(headers) == len(columns)
        for i, e in enumerate(columns):
            txt = headers[i]
            # print 20131015, txt
            txt = join_elems(txt.split('\n'), sep=E.br)
            if ar.renderer.is_interactive:  # and ar.master_instance is None:
                # print 20130527, ar.order_by
                if e.sortable and ar.order_by != [e.name]:
                    kw = {constants.URL_PARAM_SORT: e.name}
                    url = ar.renderer.get_request_url(ar, **kw)
                    if url is not None:
                        txt = [E.a(*txt, href=url)]

            # logger.info("20130119 headers2html %s %s",fields,headers)
            th = E.th(*txt, **cellattrs)
            # th = E.th(txt,**cellattrs)
            e.apply_cell_format(th)
            yield th

    def as_plain_html(self, ar, obj):
        from lino.modlib.bootstrap3.views import table2html
        sar = ar.spawn(self.actor.default_action, master_instance=obj)
        yield table2html(sar, as_main=(self.name == "main"))
        # yield sar.as_bootstrap_html(as_main=(self.name == "main"))


class CharFieldWidget(FieldWidget):
    def __init__(self, *args, **kw):
        FieldWidget.__init__(self, *args, **kw)
        self.preferred_width = 1 + min(
            20, max(3, self.field.max_length or 0))


class PasswordFieldWidget(CharFieldWidget):
    pass


class FileFieldWidget(CharFieldWidget):
    pass


class URLFieldWidget(CharFieldWidget):
    preferred_width = 40


class IncompleteDateFieldWidget(CharFieldWidget):
    preferred_width = 10


class QuantityFieldWidget(CharFieldWidget):
    def value2num(self, v):
        return v


class DateFieldWidget(FieldWidget):
    preferred_width = 13


class DateTimeFieldWidget(FieldWidget):
    preferred_width = 16


class TimeFieldWidget(FieldWidget):
    preferred_width = 6


class MonthFieldWidget(DateFieldWidget):
    pass


class DatePickerFieldWidget(FieldWidget):
    pass


class NumberFieldWidget(FieldWidget):

    def apply_cell_format(self, e):
        # e.set('align','right')
        e.attrib.update(align='right')
        # logger.info("20130119 apply_cell_format %s",etree.tostring(e))

    def format_sum(self, ar, sums, i):
        return E.b(self.format_value(ar, sums[i]))

    def value2num(self, v):
        return v

    # def apply_cell_format(self,e):
        # e.set('align','right')

    def sum2html(self, ar, sums, i, **cellattrs):
        cellattrs.update(align="right")
        return super(NumberFieldWidget, self).sum2html(
            ar, sums, i, **cellattrs)


class IntegerFieldWidget(NumberFieldWidget):
    preferred_width = 5


class AutoFieldWidget(NumberFieldWidget):
    preferred_width = 5

    def value2num(self, v):
        return 0

    def format_sum(self, ar, sums, i):
        return ''


class DecimalFieldWidget(NumberFieldWidget):
    pass


class BooleanFieldWidget(FieldWidget):
    pass


class WidgetFactory(object):

    _FIELD2ELEM = (
        # (dd.Constant, ConstantElement),
        (fields.RecurrenceField, RecurrenceWidget),
        (fields.HtmlBox, HtmlBoxWidget),
        (fields.DisplayField, DisplayWidget),
        (fields.QuantityField, QuantityFieldWidget),
        (fields.IncompleteDateField, IncompleteDateFieldWidget),
        # (dd.LinkedForeignKey, LinkedForeignKeyElement),
        (models.URLField, URLFieldWidget),
        (models.FileField, FileFieldWidget),
        (models.EmailField, CharFieldWidget),
        # (dd.HtmlTextField, HtmlTextFieldElement),
        # (dd.RichTextField, RichTextFieldElement),
        (models.TextField, TextFieldWidget),  # also dd.RichTextField
        (fields.PasswordField, PasswordFieldWidget),
        (models.CharField, CharFieldWidget),
        (fields.MonthField, MonthFieldWidget),
        (models.DateTimeField, DateTimeFieldWidget),
        (fields.DatePickerField, DatePickerFieldWidget),
        (models.DateField, DateFieldWidget),
        (models.TimeField, TimeFieldWidget),
        (models.IntegerField, IntegerFieldWidget),
        (models.DecimalField, DecimalFieldWidget),
        (models.AutoField, AutoFieldWidget),
        (models.BooleanField, BooleanFieldWidget),
        # TODO: Lino currently renders NullBooleanField like BooleanField
        (models.NullBooleanField, BooleanFieldWidget),
        # (models.ManyToManyField, M2mGridElement),
        (models.ForeignKey, ForeignKeyWidget),
    )

    def get_data_elem(self, lh, name):

        if settings.SITE.catch_layout_exceptions:
            try:
                de = lh.get_data_elem(name)
            except Exception as e:
                # logger.exception(e) removed 20130422 because it caused
                # disturbing output when running tests
                de = None
                name += " (" + str(e) + ")"
        else:
            de = lh.get_data_elem(name)

        if de is None:
            # If the plugin has been hidden, we want the element to simply
            # disappear, similar as if the user had no view permission.
            s = name.split('.')
            if len(s) == 2:
                if settings.SITE.is_hidden_app(s[0]):
                    return (de, None)
            # ctx = (lh.layout.__class__, name, ', '.join(dir(lh.layout)))
            # raise Exception(
            #     "Instance of %s has no data element '%s' (names are %s)" % ctx)
            raise Exception("{0} has no data element '{1}'".format(
                lh.layout, name))
        return de
       
    def create_main_panel(self, lh, name, vertical, *elems, **pkw):
        if isinstance(lh.layout, ColumnsLayout):
            return GridWidget(
                lh, name, lh.layout._datasource, *elems, **pkw)
        elif isinstance(lh.layout, ActionParamsLayout):
            return ActionParamsPanel(lh, name, vertical, *elems, **pkw)
        elif isinstance(lh.layout, ParamsLayout):
            return ParamsPanel(lh, name, vertical, *elems, **pkw)
        elif isinstance(lh.layout, FormLayout):
            if len(elems) == 1 or vertical:
                return DetailMainPanel(lh, name, vertical, *elems, **pkw)
            else:
                return TabPanel(lh, name, *elems, **pkw)
        raise Exception("No element class for layout %r" % lh.layout)

        # return Panel(lh, name, vertical, *widgets, **kwargs)
        
    def create_layout_panel(self, lh, name, vertical, elems, **kwargs):
        if name == 'main':
            return self.create_main_panel(
                lh, name, vertical, *elems, **kwargs)
        return Panel(lh, name, vertical, *elems, **kwargs)

    def create_layout_element(self, lh, name, **kw):
        """
        Create a layout element from the named data element.
        """
        de = self.get_data_elem(lh, name)

        return self.create_widget(de, lh, name)

    def create_widget(self, de, lh, name, **kwargs):

        if isinstance(de, type) and issubclass(de, fields.Dummy):
            return None

        if isinstance(de, DummyPanel):
            return None

        if isinstance(de, GenericRelation):
            return None

        if isinstance(de, fields.DummyField):
            lh.add_store_field(de)
            return None

        if isinstance(de, models.Field):
            if isinstance(de, (BabelCharField, BabelTextField)):
                if len(settings.SITE.BABEL_LANGS) > 0:
                    elems = [self.create_field_element(lh, de, **kwargs)]
                    for lang in settings.SITE.BABEL_LANGS:
                        bf = lh.get_data_elem(name + lang.suffix)
                        elems.append(self.create_field_element(
                            lh, bf, **kwargs))
                    return elems
            return self.create_field_element(lh, de, **kwargs)

        if isinstance(de, fields.RemoteField):
            return self.create_field_element(lh, de, **kwargs)

        if isinstance(de, fields.VirtualField):
            return self.create_vurt_element(lh, name, de, **kwargs)

        if callable(de):
            rt = getattr(de, 'return_type', None)
            if rt is not None:
                return self.create_meth_element(lh, name, de, rt, **kwargs)
        return self.create_other_widget(de, lh, name, **kwargs)

    def create_other_widget(self, de, lh, name, **kw):

        from lino.core import tables

        if isinstance(de, fields.Constant):
            return ConstantWidget(lh, de, **kw)

        if isinstance(de, SingleRelatedObjectDescriptor):
            return Widget(lh, de.related, **kw)

        if isinstance(de, (
                ManyRelatedObjectsDescriptor,
                ForeignRelatedObjectsDescriptor)):
            e = Widget(lh, de.related, **kw)
            lh.add_store_field(e.field)
            return e

        if isinstance(de, models.ManyToManyField):
            e = Widget(lh, de.related, **kw)
            lh.add_store_field(e.field)
            return e

        if isinstance(de, (ManyToManyRel, ManyToOneRel)):
            e = Widget(lh, de, **kw)
            lh.add_store_field(e.field)
            return e

        if isinstance(de, GenericForeignKey):
            # create a horizontal panel with 2 comboboxes
            de.primary_key = False  # for ext_store.Store()
            lh.add_store_field(de)
            return GenericForeignKeyWidget(lh, de, **kw)

        if isinstance(de, type) and issubclass(de, tables.AbstractTable):

            if isinstance(lh.layout, FormLayout):
                # When a table is specified in the layout of a
                # DetailWindow, then it will be rendered as a panel that
                # displays a "summary" of that table. The panel will have
                # a tool button to "open that table in its own
                # window". The format of that summary is defined by the
                # `slave_grid_format` of the table. `slave_grid_format` is
                # a string with one of the following values:

                if de.slave_grid_format == 'grid':
                    return GridWidget(lh, name, de, **kw)

                elif de.slave_grid_format == 'html':
                    field = fields.HtmlBox(verbose_name=de.label)
                    field.name = de.__name__
                    field.help_text = de.help_text
                    field._return_type_for_method = de.slave_as_html_meth()
                    lh.add_store_field(field)
                    e = HtmlBoxWidget(lh, field, **kw)
                    e.add_requirements(*de.required_roles)
                    return e

                elif de.slave_grid_format == 'summary':
                    e = SlaveSummaryPanel(lh, de, **kw)
                    lh.add_store_field(e.field)
                    return e
                else:
                    raise Exception(
                        "Invalid slave_grid_format %r" % de.slave_grid_format)

            else:
                e = SlaveSummaryPanel(lh, de, **kw)
                lh.add_store_field(e.field)
                return e

        # Build an error message.

        if hasattr(lh, 'rh'):
            msg = "Unknown element '%s' (%r) referred in layout <%s of %s>."
            msg = msg % (name, de, lh.layout, lh.rh.actor)
            l = [wde.name for wde in lh.rh.actor.wildcard_data_elems()]
            # VirtualTables don't have a model
            model = getattr(lh.rh.actor, 'model', None)
            if getattr(model, '_lino_slaves', None):
                l += [str(rpt) for rpt in model._lino_slaves.values()]
            msg += " Possible names are %s." % ', '.join(l)
        else:
            msg = "Unknown element '%s' (%r) referred in layout <%s>." % (
                name, de, lh.layout)
            # if de is not None:
            #     msg += " Cannot handle %r" % de
        raise KeyError(msg)

    def field2elem(self, lh, field, **kwargs):

        selector_field = field
        if isinstance(field, fields.RemoteField):
            selector_field = field.field
        if isinstance(selector_field, fields.VirtualField):
            selector_field = selector_field.return_type
        # remember the case of RemoteField to VirtualField

        if isinstance(selector_field, fields.CustomField):
            e = selector_field.create_layout_elem(lh, field, **kwargs)
            if e is not None:
                return e

        for df, cl in self._FIELD2ELEM:
            if isinstance(selector_field, df):
                return cl(lh, field, **kwargs)

        if isinstance(field, fields.VirtualField):
            raise NotImplementedError(
                "No LayoutElement for VirtualField %s on %s in %s" % (
                    field.name, field.return_type.__class__,
                    lh.layout))
        if isinstance(field, fields.RemoteField):
            raise NotImplementedError(
                "No LayoutElement for RemoteField %s to %s" % (
                    field.name, field.field.__class__))
        raise NotImplementedError(
            "No LayoutElement for %s (%s) in %s" % (
                field.name, field.__class__, lh.layout))

        # e = Widget(lh, field.name, **kwargs)
        # e.field = field
        # return e
    
    def create_vurt_element(self, lh, name, vf, **kw):
        e = self.create_field_element(lh, vf, **kw)
        if not vf.is_enabled(lh):
            e.editable = False
        return e

    def create_meth_element(self, lh, name, meth, rt, **kw):
        rt.name = name
        rt._return_type_for_method = meth
        if meth.__code__.co_argcount < 2:
            raise Exception(
                "Method %s has %d arguments (must have at least 2)" %
                (meth, meth.__code__.co_argcount))
        return self.create_field_element(lh, rt, **kw)

    def create_field_element(self, lh, field, **kw):
        e = self.field2elem(lh, field, **kw)
        if e.field is None:
            raise Exception("e.field is None for %s.%s" % (lh.layout, kw))
        lh.add_store_field(e.field)
        return e
