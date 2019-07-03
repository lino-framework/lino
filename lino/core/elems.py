# -*- coding: UTF-8 -*-
# Copyright 2009-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Defines "layout elements" (widgets).

"""

from __future__ import unicode_literals, print_function
from builtins import str
import six

import logging

logger = logging.getLogger(__name__)

from cgi import escape
import decimal

from django.db import models
from django.utils.translation import ugettext as _
from django.utils.text import format_lazy
from django.conf import settings
from django.db.models.fields.related import \
    ReverseOneToOneDescriptor as SingleRelatedObjectDescriptor
from django.db.models.fields.related import \
    ReverseManyToOneDescriptor as ForeignRelatedObjectsDescriptor
from django.db.models.fields.related import \
    ManyToManyDescriptor as ManyRelatedObjectsDescriptor

from django.db.models.fields.related import ManyToManyRel, ManyToOneRel
from django.db.models.fields import NOT_PROVIDED

from lino.core import layouts
from lino.core import fields
from lino.core.actions import Action, Permittable
from lino.core import constants
from lino.core.gfks import GenericRelation
from lino.modlib.bootstrap3.views import table2html

from lino.utils.ranges import constrain
from lino.utils import jsgen
from lino.utils import mti
from lino.core import choicelists
from lino.utils.jsgen import py2js, js_code
from lino.utils.html2xhtml import html2xhtml

from lino.utils import join_elems
from lino.core.actors import qs2summary

from lino.core.layouts import (FormLayout, ParamsLayout,
                               ColumnsLayout, ActionParamsLayout,
                               DummyPanel)

from lino.utils.mldbc.fields import BabelCharField, BabelTextField
from lino.core import tables
from lino.core.gfks import GenericForeignKey
from lino.utils.format_date import fds

from etgen import etree
from etgen.html import E, forcetext, tostring
from lino.utils import is_string

from lino.core.site import html2text
from etgen.html2rst import html2rst

from lino.modlib.users.utils import get_user_profile

EXT_CHAR_WIDTH = 9
EXT_CHAR_HEIGHT = 22

# FULLWIDTH = '100%'
# FULLHEIGHT = '100%'

FULLWIDTH = '-20'
FULLHEIGHT = '-10'

# USED_NUMBER_FORMATS = dict()

DEFAULT_PADDING = 2


def form_field_name(f):
    if isinstance(f, models.ForeignKey) \
            or (isinstance(f, models.Field) and f.choices):
        return f.name + constants.CHOICES_HIDDEN_SUFFIX
    else:
        return f.name


def has_fk_renderer(fld):
    return isinstance(fld, models.ForeignKey)


def py2html(obj, name):
    for n in name.split('.'):
        obj = getattr(obj, n, "N/A")
    if callable(obj):
        obj = obj()
    if getattr(obj, '__iter__', False):
        obj = list(obj)
    return escape(str(obj))


class GridColumn(jsgen.Component):
    """
    The component that generates the JS of a grid column.
    """
    declare_type = jsgen.DECLARE_INLINE

    def __init__(self, layout_handle, index, editor, **kw):
        self.editor = editor
        # 20171227 taken from extjs6
        if editor.grid_column_template is not None:
            self.value_template = editor.grid_column_template
        # kw.setdefault('sortable', True)
        kw.update(sortable=editor.sortable)
        # 20171227 in extjs6, editable was not set here:
        kw.update(editable=editor.editable)

        kw.update(colIndex=index)
        if editor.hidden:
            kw.update(hidden=True)
        if settings.SITE.use_filterRow and layout_handle.ui.renderer.extjs_version is not None:
            if editor.filter_type:
                if index == 0:
                    # first column used to show clear filter icon in this
                    # column
                    kw.update(clearFilter=True)
                # else:
                # print index, "is not 1"
                if self.layout_handle.ui.renderer.extjs_version == 3:
                    js = 'new Ext.form.TextField()'
                else:
                    js = "Ext.create('Ext.form.TextField',{})"
                kw.update(filterInput=js_code(js))
                kw.update(filterOptions=[
                    # dict(value='startwith', text='Start With'),
                    # dict(value='endwith', text='End With'),
                    dict(value='empty', text='Is empty'),
                    dict(value='notempty', text='Is not empty'),
                    dict(value='contains', text='Contains'),
                    dict(value='doesnotcontain', text='Does not contain')
                ])

        if settings.SITE.use_gridfilters and editor.gridfilters_settings:
            if isinstance(editor, FieldElement) \
                    and not isinstance(editor.field, fields.VirtualField):
                kw = editor.get_gridfilters_settings(kw)
                # kw.update(filter=editor.gridfilters_settings)
        if isinstance(editor, FieldElement):
            if settings.SITE.use_quicktips:
                # 20171227 taken from extjs6:
                layout_handle.ui.renderer.add_help_text(kw,
                              # GridColumn tooltips don't support html
                              self.editor.field.help_text if self.editor.field.help_text and "<" not in self.editor.field.help_text else "",
                              "",  # Title
                              layout_handle.layout._datasource,
                              self.editor.field.name)

            def fk_renderer(fld, name):
                # FK fields are clickable only if their target has a
                # detail view
                rpt = fld.remote_field.model.get_default_table()
                if rpt.detail_action is not None:
                    if rpt.detail_action.get_view_permission(
                            get_user_profile()):
                        return "Lino.fk_renderer('%s','Lino.%s')" % (
                            name + constants.CHOICES_HIDDEN_SUFFIX,
                            rpt.detail_action.full_name())

            rend = None
            # if isinstance(editor.field, models.AutoField):
            #     rend = 'Lino.id_renderer'
            # elif isinstance(editor.field, dd.DisplayField):
            #     rend = 'Lino.raw_renderer'
            # elif isinstance(editor.field, models.TextField):
            #     rend = 'Lino.text_renderer'
            # if isinstance(editor.field, fields.CustomField):
            #     rend = editor.field.get_column_renderer()
            if has_fk_renderer(editor.field):
                rend = fk_renderer(editor.field, editor.field.name)
            elif isinstance(editor.field, fields.VirtualField):
                # kw.update(sortable=False)
                if has_fk_renderer(editor.field.return_type):
                    rend = fk_renderer(
                        editor.field.return_type, editor.field.name)
            if rend:
                kw.update(renderer=js_code(rend))
            kw.update(editable=editor.editable)
            if editor.editable and not isinstance(editor, BooleanFieldElement):
                kw.update(editor=editor)
        else:
            kw.update(editable=False)
        kw.update(editor.get_column_options())
        jsgen.Component.__init__(self, editor.name, **kw)
        # if self.name == 'requested':
        #     print("20170214 {}".format(editor.sortable))

    def ext_options(self, **kw):
        kw = jsgen.Component.ext_options(self, **kw)
        if self.editor.field is not None:
            if is_hidden_babel_field(self.editor.field):
                kw.update(hidden=True)
        return kw


class Toolbar(jsgen.Component):
    value_template = "new Ext.Toolbar(%s)"


class ComboBox(jsgen.Component):
    value_template = 'new Ext.form.ComboBox(%s)'


# todo: rename this to Panel, and Panel to PanelElement or sth else


class ExtPanel(jsgen.Component):
    value_template = "new Ext.Panel(%s)"


class Calendar(jsgen.Component):
    value_template = "new Lino.CalendarPanel(%s)"


from lino.utils.jsgen import VisibleComponent


class LayoutElement(VisibleComponent):
    stored = False
    ext_name = None
    ext_suffix = ""
    # data_type = None
    filter_type = None
    gridfilters_settings = None
    parent = None  # will be set by Container

    # label = None
    # label_width = 0
    editable = False
    sortable = False
    xtype = None  # set by subclasses
    grid_column_template = None
    collapsible = False
    active_child = True
    refers_to_ww = False

    input_classes = None
    oui5_field_template = "openui5/elems/field/FieldElement.xml"

    def __init__(self, layout_handle, name, **kw):
        # logger.debug("LayoutElement.__init__(%r,%r)", layout_handle.layout,name)
        # self.parent = parent
        # name = layout_handle.layout._actor_name + '_' + name
        # if 'hide_sum' in kw:
        #     raise Exception("20180210")
        assert isinstance(layout_handle, layouts.LayoutHandle)
        opts = layout_handle.layout._element_options.get(name, {})
        for k, v in opts.items():
            if not hasattr(self, k):
                raise Exception("%s has no attribute %s" % (self, k))
            setattr(self, k, v)

        # new since 20121130. theoretically better
        if 'required_roles' in kw:
            assert isinstance(kw['required_roles'], set)
        else:
            required = set()
            # required |= layout_handle.layout._datasource.required_roles
            required |= self.required_roles
            kw.update(required_roles=required)

        VisibleComponent.__init__(self, name, **kw)
        # if opts:
        # print "20120525 apply _element_options", opts, 'to', self.__class__, self
        self.layout_handle = layout_handle
        # if layout_handle is not None:
        # layout_handle.setup_element(self)
        # if isinstance(layout_handle.layout, FormLayout):
        # if self.name.startswith('history_tab'):
        # if isinstance(self, TabPanel):
        # if isinstance(self, TabPanel):  # self.required_roles:
        # self.name == 'history_tab':
        # logger.info(
        #     "20160908 LayoutElement %r required_roles %r, kw was %r, opts was %r",
        #   self, self.required_roles, kw, opts)

    # def submit_fields(self):
    # return []

    def add_requirements(self, *args):
        super(LayoutElement, self).add_requirements(*args)
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

    def __repr__(self):
        return "<%s %s in %s>" % (
            self.__class__.__name__, self.name, self.layout_handle.layout)

    def get_property(self, name):
        v = getattr(self, name, None)
        if self.parent is None or v is not None:
            return v
        return self.parent.get_property(name)

    def get_column_options(self, **kw):
        return kw

    def get_gridfilters_settings(self, kw):  # 20171227 taken from extjs6
        if self.gridfilters_settings:
            kw.update(filter=dict(self.gridfilters_settings))
        return kw

    def set_parent(self, parent):
        # if self.parent is not None:
        # raise Exception("%s : parent is already %s, cannot set it to %s" % (self,self.parent,parent))
        self.parent = parent
        # if isinstance(parent,FieldSetPanel):
        # self.label = None
        # self.update(label = None)
        label = self.get_label()
        if label:
            if isinstance(parent, Panel):
                if self.layout_handle.layout.label_align == layouts.LABEL_ALIGN_LEFT:
                    self.preferred_width += len(label)

    def ext_options(self, **kw):
        if self.hidden:
            kw.update(hidden=True)
        if isinstance(self.parent, TabPanel):
            label = self.get_label()
            if not label:
                raise Exception(
                    "Item %s of tabbed %s has no label!" % (
                        self, self.layout_handle))
            ukw = dict(title=label)
            ukw.update(
                listeners=dict(activate=js_code("Lino.on_tab_activate")))
            # add_help_text(
            #     ukw, self.help_text, 'title',
            #     self.layout_handle.layout._datasource, self.name)
            self.update(**ukw)
        if self.xtype is not None:
            self.update(xtype=self.xtype)
        if self.collapsible:
            self.update(collapsible=True)
        kw = VisibleComponent.ext_options(self, **kw)
        return kw

    def as_plain_html(self, ar, obj):
        yield E.p("cannot handle %s" % self.__class__)


class ConstantElement(LayoutElement):
    declare_type = jsgen.DECLARE_INLINE
    # declare_type = jsgen.DECLARE_THIS
    # declare_type = jsgen.DECLARE_VAR
    xtype = 'label'
    vflex = True

    def __init__(self, lh, fld, **kw):
        # kw.update(html=fld.text_fn(lh.layout._datasource,lh.ui))
        kw.update(html=fld.text_fn(lh.layout._datasource))
        # kw.update(html=fld.text)
        # kw.update(autoHeight=True)
        LayoutElement.__init__(self, lh, fld.name, **kw)
        # self.text = text

    # def ext_options(self,**kw):
    # kw = LayoutElement.ext_options(self,**kw)
    # kw.update(html=self.text.text)
    # return kw

    def as_plain_html(self, ar, obj):
        return self.value.get('html')


class ButtonElement(LayoutElement):
    declare_type = jsgen.DECLARE_INLINE
    # xtype = 'label'
    xtype = 'button'

    def __init__(self, lh, name, a, **kwargs):
        # kwargs.update(html='<a href="#" onclick="javascript:{js}">{text}</a>'.format(
        #     text=a.label, js=a.js_handler))
        kwargs.update(
            text=a.label,
            handler=js_code(a.js_handler),
            scope=js_code('this'))
        LayoutElement.__init__(self, lh, name, **kwargs)


class Spacer(LayoutElement):
    declare_type = jsgen.DECLARE_INLINE
    # xtype = 'label'
    value_template = "new Ext.Spacer(%s)"


def add_help_text(kw, help_text, title, datasource, fieldname):
    if settings.SITE.use_quicktips:
        if settings.SITE.show_internal_field_names:
            ttt = "(%s.%s) " % (datasource, fieldname)
        else:
            ttt = ''
        if help_text:
            ttt = format_lazy(u"{}{}",ttt, help_text)
        if ttt:
            # kw.update(qtip=self.field.help_text)
            # kw.update(toolTipText=self.field.help_text)
            # kw.update(tooltip=self.field.help_text)
            kw.update(listeners=dict(render=js_code(
                "Lino.quicktip_renderer(%s,%s)" % (
                    py2js(title),
                    py2js(ttt)))
            ))


def is_hidden_babel_field(fld):
    lng = getattr(fld, '_babel_language', None)
    if lng is None:
        return False
    ut = get_user_profile()
    if ut is None:
        return False
    if ut.hidden_languages is None:
        return False
    if lng in ut.hidden_languages:
        return True
    return False


class FieldElement(LayoutElement):
    """
    Base class for all Widgets on some filed-like data element.
    """
    # declare_type = jsgen.DECLARE_INLINE
    # declare_type = jsgen.DECLARE_THIS
    declare_type = jsgen.DECLARE_VAR
    stored = True
    filter_type = None  # 'auto'
    active_change_event = 'change'
    # declaration_order = 3
    # ext_suffix = "_field"wrapper
    zero = 0
    hide_sum = False

    oui5_column_template = "openui5/elems/column/FieldElement.xml"
    oui5_field_template = "openui5/elems/field/FieldElement.xml"

    def __init__(self, layout_handle, field, hide_sum=False, **kw):
        if not getattr(field, 'name', None):
            raise Exception("Field '%s' in %s has no name!" %
                            (field, layout_handle))
        self.field = field
        self.editable = field.editable  # and not field.primary_key
        self.hide_sum = hide_sum

        if 'listeners' not in kw:
            if not isinstance(layout_handle.layout, ColumnsLayout):
                layout_handle.ui.renderer.add_help_text(
                    kw, self.field.help_text, self.field.verbose_name,
                    layout_handle.layout._datasource, self.field.name)

        # http://www.rowlands-bcs.com/extjs/tips/tooltips-form-fields
        # if self.field.__doc__:
        # kw.update(toolTipText=self.field.__doc__)
        # label = field.verbose_name
        # if not self.field.blank:
        # label = string_concat('<b>',label,'</b>')
        # label = string_concat(label,' [*]')
        # kw.update(style=dict(padding=DEFAULT_PADDING))
        # kw.update(style=dict(marginLeft=DEFAULT_PADDING))
        # kw.update(style='padding: 10px')
        # logger.info("20120931 %s %s",layout_handle,field.name)
        # if field.name == "detail_pointer":
        #     logger.info("20170905 using verbose_name %s",
        #                 field.verbose_name)

        # kw.setdefault('label',string_concat('<b>',field.verbose_name,'</b>'))
        # kw.setdefault('label',
        # ~ string_concat('<span class="ttdef"><a class="tooltip" href="#">',
        # field.verbose_name,
        # '<span class="classic">This is a test...</span></a></span>'))
        # kw.setdefault('label',
        # ~ string_concat('<div class="ttdef"><a class="tooltip" href="#">',
        # field.verbose_name,
        # '<span class="classic">This is a test...</span></a></div>'))

        self.add_default_value(kw)

        LayoutElement.__init__(self, layout_handle, field.name, **kw)

        # if self.field.__class__.__name__ == "DcAmountField":
        # print 20130911, self.field, self.editable

        if isinstance(field, fields.FakeField) and field.sortable_by:
            self.sortable = True

    def get_label(self):
        if self._label is None:
            return self.field.verbose_name
        return self._label

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
        if self.layout_handle.layout.label_align == layouts.LABEL_ALIGN_TOP:
            yield E.br()
        input_classes = "form-control " + self.input_classes if self.input_classes is not None else "form-control"
        yield E.input(type="text", value=text, **{'class': input_classes})
        # if self.field.help_text:
        # yield E.span(unicode(text),class_="help-block")
        # yield E.p(unicode(elem.field.verbose_name),':',E.br(),E.b(text))

    def cell_html(self, ui, row):
        return getattr(row, self.field.name)

    def add_default_value(self, kw):
        if self.field.has_default():
            dv = self.field.default
            if callable(dv):
                return
                # dv = dv()
            kw.update(value=dv)

    def get_column_options(self, **kw):
        # raise "get_column_options() %s" % self.__class__
        # kw.update(xtype='gridcolumn')
        # kw.update(dataIndex=self.field.name)
        kw.update(dataIndex=self.name)
        label = self.get_label()

        if self.field.help_text is not None:
            help_text = format_lazy(u"{}",self.field.help_text)
        elif settings.SITE.show_internal_field_names:
            help_text = format_lazy("(%s.%s) " % ( self.layout_handle.layout._datasource, self.field.name))
        else:
            help_text = ''
        kw.update(tooltip=help_text)

        if label is None:
            kw.update(header=self.name)
        else:
            kw.update(header=label)
        # if self.label is None:
        #     kw.update(header=self.name)
        # elif self.label:
        #     kw.update(header=self.label)
        # else:
        #     kw.update(header=self.label)

        # 20171227 taken from extjs6:
        if not self.editable:
            kw.update(editable=False)
        if not self.sortable:
            kw.update(sortable=False)

        w = self.width or self.preferred_width
        # kw.update(width=w*EXT_CHAR_WIDTH)
        kw.update(width=js_code("Lino.chars2width(%d)" % (w + 1)))
        """
        We add 1 character (9 pixels) to the theoretic width.
        e.g. the columns "16-24" etc in `courses.PendingCourseRequests`
        has w=5 and should be rendered so that the header is visible.
        """
        return kw

    def get_field_options(self, **kw):
        if self.xtype:
            kw.update(xtype=self.xtype)

        if is_hidden_babel_field(self.field):
            kw.update(hidden=True)

        # since 20171227:
        if self.layout_handle.ui.renderer.extjs_version != 3:
            kw.update(labelAlign=self.layout_handle.layout.label_align)

        # When used as editor of an EditorGridPanel, don't set the
        # name attribute because it is not needed for grids and might
        # conflict with fields of a surrounding detail form. See ticket
        # #38 (`/blog/2011/0408`).  Also don't set a label then.
        if isinstance(self.layout_handle.layout, ColumnsLayout):
            # ticket#1964 : Omit the 'Hidden' value for the column editor even if the field is hidden
            # kw.update(hidden=False)
            # above line removed 20180103 because it caused hidden
            # babel fields to not get hidden in use_django_forms
            # and because there are changces that it is no longer
            # needed for #1964
            pass
        else:
            kw.update(name=self.field.name)
            label = self.get_label()
            if label:
                if self.field.help_text:
                    if settings.SITE.use_css_tooltips:
                        label = format_lazy(u"{}{}{}{}{}",
                                            '<a class="tooltip" href="#">',
                                            label,
                                            '<span class="classic">',
                                            self.field.help_text,
                                            '</span></a>')
                    elif settings.SITE.use_quicktips:
                        label = format_lazy(u"{}{}{}",
                                            '<span style="border-bottom: 1px dotted #000000;">',
                                            label,
                                            '</span>')

                kw.update(fieldLabel=label)
        if self.editable:
            if not self.field.blank:
                kw.update(allowBlank=False)
            kw.update(selectOnFocus=True)
        else:
            kw.update(disabled=True)
            # kw.update(readOnly=True)
        return kw

    def ext_options(self, **kw):
        kw = LayoutElement.ext_options(self, **kw)
        kw.update(self.get_field_options())
        return kw

    def apply_cell_format(self, e):
        pass

    def value2html(self, ar, v, **cellattrs):
        """Return a `<td>` html etree element representing the given value.

        The default implementation returns an HTML element obtained
        from :meth:`format_value`.

        """
        if self.field.primary_key:
            # print(20170301, ar.renderer)
            url = ar.renderer.get_detail_url(ar.actor, v)
            # 20171227 in extjs6 above line was:
            # url = ar.pk2url(v)
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
        if i == ar.actor.sum_text_column:
            return E.b(*forcetext(ar.get_sum_text(sums)))
        if self.hide_sum:
            return ''
        v = sums[self.name]
        if v:
            return E.b(self.format_value(ar, v))
        return ''

    def value2num(self, v):
        # print "20120426 %s value2num(%s)" % (self,v)
        return 0


class TextFieldElement(FieldElement):
    # xtype = 'textarea'
    filter_type = 'string'
    gridfilters_settings = dict(type='string')
    vflex = True
    # value_template = "new Ext.form.TextArea(%s)"
    xtype = None
    # width = 60
    preferred_width = 60
    preferred_height = 5
    # collapsible = True
    separate_window = False
    active_child = False
    format = 'plain'
    oui5_field_template = "/openui5/elems/field/TextFieldElement.xml"

    def __init__(self, layout_handle, field, **kw):
        self.format = getattr(field, 'textfield_format', None) \
                      or settings.SITE.textfield_format

        if layout_handle.ui.renderer.extjs_version == 3:
            self.value_template = "new Ext.form.TextArea(%s)"
        else:
            self.value_template = "Ext.create('Ext.form.TextArea',%s)"

        if self.format == 'html':
            if settings.SITE.is_installed('tinymce'):
                if layout_handle.ui.renderer.extjs_version == 3:
                    self.value_template = "new Lino.RichTextPanel(%s)"
                else:
                    self.value_template = "Ext.create('Lino.RichTextPanel',%s)"

                self.active_child = True
                # if self.label:
                # kw.update(title=unicode(self.label))
                self.separate_window = True
                # we don't call FieldElement.__init__ but do almost the same:
                self.field = field
                self.editable = field.editable  # and not field.primary_key
                # 20111126 kw.update(ls_url=rpt2url(layout_handle.rh.report))
                # kw.update(master_panel=js_code("this"))
                if layout_handle.ui.renderer.extjs_version is not None:
                    kw.update(containing_panel=js_code("this"))
                # kw.update(title=unicode(field.verbose_name)) 20111111
                kw.update(label=self.get_label())
                kw.update(title=field.verbose_name)
                return LayoutElement.__init__(
                    self, layout_handle, field.name, **kw)
            else:
                if layout_handle.ui.renderer.extjs_version == 3:
                    self.value_template = "new Ext.form.HtmlEditor(%s)"
                else:
                    self.value_template = "Ext.create('Ext.form.HtmlEditor',%s)"
                if settings.SITE.use_vinylfox:
                    kw.update(plugins=js_code('Lino.VinylFoxPlugins()'))
        elif self.format == 'plain':
            kw.update(
                growMax=2000,
                # defaultAutoCreate = dict(
                # tag="textarea",
                # autocomplete="off"
                # )
            )
            # Using a text editor in a grid is irritating because the
            # grid editor doesn't react "normally" to ENTER. We might
            # use enterIsSpecial, but then users have no chance at all
            # to insert a newline character.
            if False:
                if isinstance(layout_handle.layout, ColumnsLayout):
                    kw.update(enterIsSpecial=True)

        else:
            raise Exception(
                "Invalid textfield format %r for field %s.%s" % (
                    self.format, field.model.__name__, field.name))
        FieldElement.__init__(self, layout_handle, field, **kw)

    def as_plain_html(self, ar, obj):
        value = self.field.value_from_object(obj)
        text = str(value)
        if not text:
            text = " "
        # yield E.p(unicode(elem.field.verbose_name),':',E.br(),E.b(text))
        # 20171227 in extjs there was no E.div() around them.
        yield E.div(
            E.label(str(self.get_label())),
            E.textarea(text, rows=str(self.preferred_height),
                       **{'class': "form-control"}),
            **{'class': "form-group"}
        )

    def value2html(self, ar, v, **cellattrs):
        # if self.format == 'html' and v:
        if v and v.startswith("<"):
            from lxml import html
            top = html.fromstring(v)
            # xv = html2xhtml(v)
            # # v = v.decode('utf-8')
            # # top = E.fromstring(v)
            # # top = E.raw(v)
            # from lxml import etree
            # if False:
            #     top = etree.fromstring(xv)
            # else:
            #     try:
            #         top = etree.fromstring(xv)
            #     except Exception as e:
            #         top = str(e)
            #         msg = "{} while trying to parse XML\n" \
            #         "{!r}\n(from html {!r})".format(e, xv, v)
            #         logger.warning(msg)
        else:
            top = self.format_value(ar, v)
        return E.td(top, **cellattrs)

    def format_value(self, ar, v):  # new since 20161120
        if self.format == 'html' and v:
            if etree.iselement(v):
                return html2rst(v)
            return html2text(v)
        return super(TextFieldElement, self).format_value(ar, v)


class CharFieldElement(FieldElement):
    filter_type = 'string'
    gridfilters_settings = dict(type='string')
    value_template = "new Ext.form.TextField(%s)"
    sortable = True
    xtype = None

    def __init__(self, *args, **kw):
        FieldElement.__init__(self, *args, **kw)
        # See 20180828 and 20181014 
        self.preferred_width = 1 + min(20, max(3, self.field.max_length or 0))

    def get_field_options(self, **kw):
        kw = FieldElement.get_field_options(self, **kw)
        kw.update(maxLength=self.field.max_length)
        if self.field.max_length is not None:
            if self.field.max_length <= 10:
                kw.update(boxMinWidth=js_code('Lino.chars2width(%d)' %
                                              self.field.max_length))

        for lino_name, extjs_name in (
                ('regex', 'regex'),
                ('mask_re', 'maskRe'),
                ('strip_chars_re', 'stripCharsRe'),
        ):
            v = getattr(self.field, lino_name, None)
            if v is not None:
                kw[extjs_name] = js_code(v)

        # kw.update(style=dict(padding=DEFAULT_PADDING))
        # kw.update(margins='10px')
        return kw


class PasswordFieldElement(CharFieldElement):

    def get_field_options(self, **kw):
        kw = super(PasswordFieldElement, self).get_field_options(**kw)
        kw.update(inputType='password')
        return kw


class FileFieldElement(CharFieldElement):
    # xtype = 'fileuploadfield'
    # value_template = "new Lino.FileField(%s)"
    value_template = "Lino.file_field_handler(this,%s)"
    # value_template = "%s"

    # def __init__(self,layout_handle,*args,**kw):
    # CharFieldElement.__init__(self,layout_handle,*args,**kw)
    # layout_handle.has_upload = True

    # def get_field_options(self,**kw):
    # kw = CharFieldElement.get_field_options(self,**kw)
    # kw.update(emptyText=_('Select a document to upload...'))
    # ~ # kw.update(buttonCfg=dict(iconCls='upload-icon'))
    # return kw


class ComboFieldElement(FieldElement):
    # value_template = "new Ext.form.ComboBox(%s)"
    # sortable = True
    xtype = None
    filter_type = 'string'
    gridfilters_settings = dict(type='string')

    # oui5_field_template = "openui5/elems/field/ComboElement.xml"
    oui5_field_template = "openui5/elems/field/ComboElement.xml"

    def get_field_options(self, **kw):
        kw = FieldElement.get_field_options(self, **kw)
        # When used as editor of an EditorGridPanel, don't set the name attribute
        # because it is not needed for grids and might conflict with fields of a
        # surronding detail form. See ticket #38 (`/blog/2011/0408`).
        # Also, Comboboxes with simple values may never have a hiddenName
        # option.
        if not isinstance(self.layout_handle.layout, ColumnsLayout) \
                and not isinstance(self, SimpleRemoteComboFieldElement):
            kw.update(hiddenName=self.field.name +
                                 constants.CHOICES_HIDDEN_SUFFIX)
        return kw


class ChoicesFieldElement(ComboFieldElement):
    value_template = "new Lino.ChoicesFieldElement(%s)"

    def get_field_options(self, **kw):
        kw = ComboFieldElement.get_field_options(self, **kw)
        kw.update(store=tuple(self.field.choices))
        # kw.update(hiddenName=self.field.name+constants.CHOICES_HIDDEN_SUFFIX)
        return kw


class ChoiceListFieldElement(ChoicesFieldElement):
    """Like :class:`ChoicesFieldElement`, but we use the fact that
    choicelists are actors to define them once and refer to them.
    Special case are choicelist fields with blank=True: these must
    dynamicaly add a blank choice to the the choicelist.
    """

    oui5_field_template = "openui5/elems/field/ChoiceListFieldElement.xml"
    filter_type = 'list'
    gridfilters_settings = dict(type='list')

    def __init__(self, layout_handle, field, **kw):
        pw = field.choicelist.preferred_foreignkey_width
        if pw is not None:
            kw.setdefault('preferred_width', pw)
        FieldElement.__init__(self, layout_handle, field, **kw)

    def get_field_options(self, **kw):
        kw = ComboFieldElement.get_field_options(self, **kw)
        # kw.update(store=js_code('Lino.%s.choices' % self.field.choicelist.actor_id))
        if self.layout_handle.ui.renderer.extjs_version is not None:
            js = 'Lino.%s' % self.field.choicelist.actor_id
            if self.field.blank:
                js = "[['','<br>']].concat(%s)" % js
                # 20171227 in extjs6 it was:
                # js = "[['','']].concat(%s)" % js
        else:# react only
            js = self.field.choicelist.actor_id
            if self.field.blank:
                kw.update(blank=self.field.blank)
        kw.update(store=js_code(js))
        return kw

    def get_gridfilters_settings(self, kw):
        kw = super(ChoicesFieldElement, self).get_gridfilters_settings(kw)
        kw['filter'].update(options=[str(c[1]) for c in self.field.choices])
        return kw


class RemoteComboFieldElement(ComboFieldElement):
    value_template = "new Lino.RemoteComboFieldElement(%s)"

    def store_options(self, **kw):
        # ~ kw.update(baseParams=js_code('this.get_base_params()')) # 20120202
        if self.editable:
            url = self.layout_handle.get_choices_url(self.field, **kw)
            if self.layout_handle.ui.renderer.extjs_version is not None:
                if self.layout_handle.ui.renderer.extjs_version == 3:
                    proxy = dict(url=url, method='GET')
                    js = "new Ext.data.HttpProxy(%s)"
                else:
                    reader = dict(
                        type='json', rootProperty='rows',
                        totalProperty='count',
                        idProperty='this.ls_id_property',
                        keepRawData='true')
                    proxy = dict(url=url, method='GET', reader=reader)
                    js = "Ext.create('Ext.data.HttpProxy',%s)"
                kw.update(proxy=js_code(js % py2js(proxy)))
        # a JsonStore without explicit proxy sometimes used method POST
        return kw

    def get_field_options(self, **kw):
        kw = ComboFieldElement.get_field_options(self, **kw)
        if self.editable:
            sto = self.store_options()
            # print repr(sto)
            if self.layout_handle.ui.renderer.extjs_version == 3:
                kw.update(
                    store=js_code(
                        "new Lino.ComplexRemoteComboStore(%s)" %
                        py2js(sto)))
            else:
                kw.update(
                    store=js_code(
                        "Ext.create('Lino.ComplexRemoteComboStore',%s)" %
                        py2js(sto)))
        return kw


class SimpleRemoteComboFieldElement(RemoteComboFieldElement):
    value_template = "new Lino.SimpleRemoteComboFieldElement(%s)"
    # def get_field_options(self,**kw):
    # todo : store
    # ~ # Do never add a hiddenName
    # return FieldElement.get_field_options(self,**kw)


class ComplexRemoteComboFieldElement(RemoteComboFieldElement):
    # value_template = "new Lino.ComplexRemoteComboFieldElement(%s)"

    def unused_get_field_options(self, **kw):
        kw = RemoteComboFieldElement.get_field_options(self, **kw)
        kw.update(hiddenName=self.field.name + constants.CHOICES_HIDDEN_SUFFIX)
        return kw


# class LinkedForeignKeyElement(ComplexRemoteComboFieldElement):
# pass

def action_name(a):
    if a is None:
        return 'null'
    return 'Lino.' + a.full_name()


class ForeignKeyElement(ComplexRemoteComboFieldElement):
    oui5_field_template = "openui5/elems/field/ForeignKeyElement.xml"

    preferred_width = 20

    def get_field_options(self, **kw):
        kw = super(ForeignKeyElement, self).get_field_options(**kw)
        if not self.field.remote_field:
            raise Exception("20171210 %r" % self.field.__class__)
        if isinstance(self.field.remote_field.model, six.string_types):
            raise Exception("20130827 %s.remote_field.model is %r" %
                            (self.field, self.field.remote_field.model))
        pw = self.field.remote_field.model.preferred_foreignkey_width
        if pw is not None:
            kw.setdefault('preferred_width', pw)
        actor = self.field.remote_field.model.get_default_table()
        if not isinstance(self.layout_handle.layout, ColumnsLayout):
            if self.layout_handle.ui.renderer.extjs_version is not None:
                if actor is None:
                    raise Exception("20181229 {!r} {}".format(self,
                                                              self.field.remote_field.model))
                a1 = actor.detail_action
                a2 = actor.insert_action
                if a1 is not None or a2 is not None:
                    if self.layout_handle.ui.renderer.extjs_version == 3:
                        self.value_template = "new Lino.TwinCombo(%s)"
                    else:
                        self.value_template = "Ext.create('Lino.TwinCombo',%s)"
                    js = "function(e){ Lino.show_fk_detail(this,%s,%s)}" % (
                        action_name(a1), action_name(a2))
                    kw.update(onTrigger2Click=js_code(js))
        kw.update(related_actor_id=actor.actor_id)

        kw.update(pageSize=actor.page_length)
        if actor.model is not None:
            kw.update(emptyText=_('Select a %s...') %
                                actor.model._meta.verbose_name)
        return kw

    def cell_html(self, ui, row):
        obj = getattr(row, self.field.name)
        if obj is None:
            return ''
        return ui.obj2html(obj)

    def value2html(self, ar, v, **cellattrs):
        txt = self.format_value(ar, v)
        return E.td(ar.obj2html(v, txt), **cellattrs)

class TimeFieldElement(FieldElement):
    value_template = "new Lino.TimeField(%s)"
    # xtype = 'timefield'
    # ~ data_type = 'time' # for store column
    sortable = True
    preferred_width = 8
    # filter_type = 'time'
    input_classes = "TimeField"

    oui5_field_template = "openui5/elems/field/TimeFieldElement.xml"

    def get_field_options(self, **kwargs):
        kwargs = FieldElement.get_field_options(self, **kwargs)
        if settings.SITE.calendar_start_hour:
            kwargs['minValue'] = '{}:00'.format(
                settings.SITE.calendar_start_hour)
            # kwargs['minValue'] = settings.SITE.calendar_start_hour
        eh = settings.SITE.calendar_end_hour
        if eh:
            if eh > 12:
                kwargs['maxValue'] = '{}:00 PM'.format(eh-12)
            else:
                kwargs['maxValue'] = '{}:00'.format(eh)
            # kwargs['maxValue'] = settings.SITE.calendar_end_hour
            # kwargs['maxValue'] = '9:00 PM'
        return kwargs


class DateTimeFieldElement(FieldElement):
    # value_template = "new Lino.DateTimeField(%s)"
    value_template = "new Ext.form.DisplayField(%s)"
    # ~ data_type = 'date' # for store column
    sortable = True
    preferred_width = 16
    # filter_type = 'date'

    oui5_field_template = "openui5/elems/field/DateTimeFieldElement.xml"

    def __init__(self, layout_handle, field, **kw):
        if self.editable:
            if layout_handle.ui.renderer.extjs_version == 3:
                self.value_template = "new Lino.DateTimeField(%s)"
            else:
                self.value_template = "Ext.create('Lino.DateTimeField',%s)"
        else:
            kw.update(value="<br>")
            if layout_handle.ui.renderer.extjs_version == 3:
                self.value_template = "new Ext.form.DisplayField(%s)"
            else:
                self.value_template = "Ext.create('Ext.form.DisplayField',%s)"

        FieldElement.__init__(self, layout_handle, field, **kw)

    def value2html(self, ar, v, **cellattrs):
        if v is None:
            v = ''
        else:
            v = fds(v) + " " + v.strftime(
                settings.SITE.time_format_strftime)
        return E.td((v), **cellattrs)


class DatePickerFieldElement(FieldElement):
    input_classes = "DatePickerField"

    value_template = "new Lino.DatePickerField(%s)"

    def get_column_options(self, **kw):
        raise Exception("not allowed in grid")


class DateFieldElement(FieldElement):
    input_classes = "DatePickerField"
    if settings.SITE.use_spinner:
        raise Exception("20130114")
        value_template = "new Lino.SpinnerDateField(%s)"
    else:
        value_template = "new Lino.DateField(%s)"
        # value_template = "new Lino.DatePickerField(%s)"
    # xtype = 'datefield'
    # ~ data_type = 'date' # for store column
    sortable = True
    # ~ preferred_width = 8 # 20131022
    preferred_width = 13
    filter_type = 'date'
    gridfilters_settings = dict(
        type='date', dateFormat=settings.SITE.date_format_extjs)
    # todo: DateFieldElement.preferred_width should be computed from Report.date_format
    # ~ grid_column_template = "new Ext.grid.DateColumn(%s)"

    # def __init__(self,layout_handle,field,**kw):
    # ~ if False: # getattr(field,'picker',False):
    # self.value_template = "new Lino.DatePickerField(%s)"
    # FieldElement.__init__(self,layout_handle,field,**kw)

    # def get_field_options(self,**kw):
    # kw = FieldElement.get_field_options(self,**kw)
    # kw.update(format=self.layout_handle.rh.actor.date_format)
    # return kw

    oui5_field_template = "openui5/elems/field/DateFieldElement.xml"

    def get_column_options(self, **kw):
        kw = FieldElement.get_column_options(self, **kw)
        kw.update(xtype='datecolumn')
        # kw.update(format=self.layout_handle.rh.actor.date_format)
        kw.update(format=settings.SITE.date_format_extjs)
        # ~ kw.update(boxMinWidth=js_code('Lino.chars2width(%d)' % 12)) # experimental value.
        return kw


class MonthFieldElement(DateFieldElement):

    def get_field_options(self, **kw):
        kw = DateFieldElement.get_field_options(self, **kw)
        kw.update(format='m/Y')
        kw.update(plugins='monthPickerPlugin')
        return kw


class URLFieldElement(CharFieldElement):
    sortable = True
    preferred_width = 40
    value_template = "new Lino.URLField(%s)"

    # def get_field_options(self,**kw):
    # kw = FieldElement.get_field_options(self,**kw)
    # ~ kw.update(vtype='url') #,vtypeText=
    # return kw


class IncompleteDateFieldElement(CharFieldElement):
    """
    Widget for :class:`lino.core.fields.IncompleteDate` fields.
    """
    preferred_width = 10
    value_template = "new Lino.IncompleteDateField(%s)"

    # def __init__(self,*args,**kw):
    # FieldElement.__init__(self,*args,**kw)

    def get_field_options(self, **kw):
        # skip CharFieldElement.get_field_options because
        # boxMinWidth and maxLength are set by Lino.IncompleteDateField
        kw = FieldElement.get_field_options(self, **kw)
        # kw.update(maxLength=10)
        return kw


class NumberFieldElement(FieldElement):
    """
    Base class for integers, decimals, RequestField,...
    """
    filter_type = 'numeric'
    gridfilters_settings = dict(type='numeric')
    value_template = "new Ext.form.NumberField(%s)"
    sortable = True
    number_format = '0'

    def apply_cell_format(self, e):
        # e.set('align', 'right')
        e.set('class', 'number-cell')
        # e.attrib.update(align='right')
        # logger.info("20130119 apply_cell_format %s",etree.tostring(e))

    def format_sum(self, ar, sums, i):
        if self.hide_sum:
            if i == ar.actor.sum_text_column:
                return E.b(*forcetext(ar.get_sum_text(sums)))
            return ''
        return E.b(self.format_value(ar, sums[self.name]))

    def value2num(self, v):
        if self.hide_sum:
            return 0
        return v

    # def apply_cell_format(self,e):
    # e.set('align','right')

    def sum2html(self, ar, sums, i, **cellattrs):
        cellattrs['class'] = 'number-cell'
        # cellattrs.update(align="right")
        return super(NumberFieldElement, self).sum2html(
            ar, sums, i, **cellattrs)

    # 20130119b
    # def value2html(self,ar,v,**cellattrs):
    # cellattrs.update(align="right")
    # return E.td(self.format_value(ar,v),**cellattrs)

    def get_column_options(self, **kw):
        kw = FieldElement.get_column_options(self, **kw)
        kw.update(align='right')

        # if self.number_format != settings.SITE.default_number_format_extjs:
        #     kw.update(format=self.number_format)
        if self.number_format:
            kw.update(xtype='numbercolumn')
            kw.update(format=self.number_format)
        # n = USED_NUMBER_FORMATS.get(self.number_format, 0)
        # USED_NUMBER_FORMATS[self.number_format] = n + 1
        # ~ kw.update(format='') # 20130125
        # ~ kw.update(renderer=js_code('Lino.nullnumbercolumn_renderer')) # 20130125
        return kw


class DecimalFieldElement(NumberFieldElement):
    zero = decimal.Decimal(0)

    # value_template = "new Ext.form.NumberField(%s)"
    # filter_type = 'numeric'
    # gridfilters_settings = dict(type='numeric')
    # xtype = 'numberfield'
    # sortable = True
    # data_type = 'float'

    def __init__(self, *args, **kw):
        FieldElement.__init__(self, *args, **kw)
        self.preferred_width = max(5, self.field.max_digits) \
                               + self.field.decimal_places
        # fmt = '0,000'
        # fmt = '0.0'
        # if self.field.decimal_places > 0:
        #     fmt += ',' + ("0" * self.field.decimal_places)
        if len(settings.SITE.decimal_group_separator):
            # Ext.utils.format.number() is not able to specify
            # anything else than '.' or ',' as group separator,
            if settings.SITE.decimal_separator == ',':
                fmt = "0.000"
            else:
                fmt = "0,000"
        else:
            fmt = "0"
        if self.field.decimal_places > 0:
            fmt += settings.SITE.decimal_separator
            fmt += "0" * self.field.decimal_places
        if settings.SITE.decimal_separator == ',':
            fmt += "/i"
        self.number_format = fmt

    def get_field_options(self, **kw):
        kw = FieldElement.get_field_options(self, **kw)
        if self.field.decimal_places:
            kw.update(decimalPrecision=self.field.decimal_places)
            # kw.update(decimalPrecision=-1)
            kw.update(decimalSeparator=settings.SITE.decimal_separator)
        else:
            kw.update(allowDecimals=False)
        if self.editable:
            kw.update(allowBlank=self.field.blank)
        return kw


class IntegerFieldElement(NumberFieldElement):
    preferred_width = 5
    # data_type = 'int'


class AutoFieldElement(NumberFieldElement):
    preferred_width = 5

    # data_type = 'int'

    def value2num(self, v):
        return 0

    def format_sum(self, ar, sums, i):
        return ''


class RequestFieldElement(IntegerFieldElement):

    def value2num(self, v):
        if self.hide_sum:
            return 0
        # logger.info("20131114 value2num %s",v)
        return v.get_total_count()

    def value_from_object(self, obj, ar):
        # logger.info("20131114 value_from_object %s",v)
        return self.field.value_from_object(obj, ar)

    def value2html(self, ar, v, **cellattrs):
        # logger.info("20121116 value2html(%s)", v)
        n = v.get_total_count()
        if n == 0:
            return E.td(**cellattrs)
        url = ar.renderer.request_handler(v)
        if url is None:
            return E.td(str(n), **cellattrs)
        return E.td(E.a(str(n), href='javascript:' + url), **cellattrs)

    def format_value(self, ar, v):
        # logger.info("20121116 format_value(%s)", v)
        # raise Exception("20130131 %s" % v)
        if v is None:
            raise Exception("Got None value for %s" % self)
        n = v.get_total_count()
        if True:
            if n == 0:
                return ''
        # if n == 12:
        # logger.info("20120914 format_value(%s) --> %s",v,n)
        return ar.href_to_request(v, str(n))

    def format_sum(self, ar, sums, i):
        if self.hide_sum:
            return ''
        # return self.format_value(ar,sums[i])
        return E.b(str(sums[self.name]))


class QuantityFieldElement(CharFieldElement):

    def get_column_options(self, **kw):
        # print 20130125, self.field.name
        kw = super(QuantityFieldElement, self).get_column_options(**kw)
        # kw.update(xtype='numbercolumn')
        kw.update(align='right')
        kw.update(format='')  # 20130125
        # ~ kw.update(renderer=js_code('Lino.nullnumbercolumn_renderer')) # 20130125
        return kw

    def value2num(self, v):
        if self.hide_sum:
            return 0
        return v


class DisplayElement(FieldElement):
    """ExtJS element to be used for :class:`DisplayFields
    <lino.core.fields.DisplayField>`.

    """
    # preferred_width = 30
    # preferred_height = 3
    ext_suffix = "_disp"
    # declare_type = jsgen.DECLARE_THIS
    declare_type = jsgen.DECLARE_VAR
    value_template = "new Ext.form.DisplayField(%s)"
    oui5_column_template = "openui5/elems/column/DisplayElement.xml"
    oui5_field_template = "openui5/elems/field/DisplayElement.xml"

    def __init__(self, *args, **kw):
        kw.setdefault('value', '<br/>')  # see blog/2012/0527
        kw.update(always_enabled=True)
        FieldElement.__init__(self, *args, **kw)
        self.preferred_height = self.field.preferred_height
        self.preferred_width = self.field.preferred_width
        if self.field.max_length is not None:  # might be explicit 0
            self.preferred_width = self.field.max_length
        # if self.field.name == "overview":
        #     print("20181022", self.field, self.field.verbose_name)

    def value_from_object(self, obj, ar):
        return self.field.value_from_object(obj, ar)

    def value2html(self, ar, v, **cellattrs):
        try:
            if etree.iselement(v) and v.tag == 'div':
                # if etree.iselement(v):
                #     if v.tag == 'div':
                #         return E.td(*[child for child in v], **cellattrs)
                #     if v.tag == 'td':
                #         return v
                return E.td(*[child for child in v], **cellattrs)
            return E.td(v, **cellattrs)
        except Exception as e:
            logger.error(e)
            return E.td(str(e), **cellattrs)

    def format_value(self, ar, v):
        if etree.iselement(v):
            return html2rst(v)
        return self.field._lino_atomizer.format_value(ar, v)

    def as_plain_html(self, ar, obj):
        # Todo make part of a panel or something so it's aligned with the other elements.
        value = self.value_from_object(obj, ar)
        if etree.iselement(value):
            yield value
        else:
            for x in super(DisplayElement, self).as_plain_html(ar, obj):
                yield x


class BooleanDisplayElement(DisplayElement):
    preferred_width = 20
    preferred_height = 1

    def __init__(self, *args, **kw):
        # do not call DisplayElement.__init__()
        # ~ kw.setdefault('value','<br/>') # see blog/2012/0527
        # kw.update(always_enabled=True)
        FieldElement.__init__(self, *args, **kw)


class BooleanFieldElement(FieldElement):
    value_template = "new Ext.form.Checkbox(%s)"
    # xtype = 'checkbox'
    # data_type = 'boolean'
    filter_type = 'boolean'
    gridfilters_settings = dict(type='boolean')
    # def __init__(self,*args,**kw):
    # FieldElement.__init__(self,*args,**kw)
    # active_change_event = 'check'

    oui5_field_template = "openui5/elems/field/CheckBoxFieldElement.xml"

    def set_parent(self, parent):
        FieldElement.set_parent(self, parent)
        # if isinstance(parent,Panel) and parent.hideCheckBoxLabels:
        if parent.hideCheckBoxLabels:
            self.update(hideLabel=True)

    def add_default_value(self, kw):
        if self.field.has_default():
            dv = self.field.default
            if callable(dv):
                return
                # dv = dv()
            kw.update(checked=dv)
            # kw.update(value=dv)
            # self.remove('value')

    def get_field_options(self, **kw):
        kw = FieldElement.get_field_options(self, **kw)
        if not isinstance(self.layout_handle.layout, ColumnsLayout):
            if 'fieldLabel' in kw:
                del kw['fieldLabel']
            # kw.update(hideLabel=True)

            label = self.get_label()

            if isinstance(self.field, mti.EnableChild):
                # no longer used since 20150131
                rpt = self.field.child_model.get_default_table()
                if rpt.detail_action is not None:
                    js = "Lino.show_mti_child('%s',Lino.%s)" % (
                        self.field.name,
                        rpt.detail_action.full_name())
                    label += """ (<a href="javascript:%s">%s</a>)""" % (
                        js, _("show"))

            # self.verbose_name = \
            # 'is a <a href="javascript:Lino.enable_child_label()">%s</a>' % self.field.child_model.__name__
            # 'is a <a href="foo">[%s]</a>' % self.child_model._meta.verbose_name

            kw.update(boxLabel=label)

        return kw

    def get_column_options(self, **kw):
        kw = FieldElement.get_column_options(self, **kw)
        kw.update(xtype='checkcolumn')
        return kw

    def get_from_form(self, instance, values):
        """
        standard HTML submits checkboxes of a form only when they are checked.
        So if the field is not contained in values, we take False as value.
        """
        instance[self.field.name] = values.get(self.field.name, False)


class SingleRelatedObjectElement(DisplayElement):
    """The widget used to render a `SingleRelatedObjectDescriptor`,
    i.e. the other side of a `OneToOneField`.

    """

    def __init__(self, lh, relobj, **kw):
        """
        :lh: the LayoutHandle
        :relobj: the RelatedObject instance
        """
        # print(20130202, relobj.parent_model, relobj.model, relobj.field)
        self.relobj = relobj
        self.editable = False
        # kw.update(
        #     label=str(getattr(relobj.model._meta, 'verbose_name', None))
        #           or relobj.var_name)
        # DisplayElement.__init__(self,lh,relobj.field,**kw)

        # ~ kw.setdefault('value','<br/>') # see blog/2012/0527
        # kw.update(always_enabled=True)
        FieldElement.__init__(self, lh, relobj.field, **kw)
        # self.preferred_height = self.field.preferred_height
        # self.preferred_width = self.field.preferred_width
        # if self.field.max_length:
        # self.preferred_width = self.field.max_length

    def get_label(self):
        return self._label or self.relobj.model._meta.verbose_name \
            or self.relobj.var_name

    def add_default_value(self, kw):
        pass


class GenericForeignKeyElement(DisplayElement):
    """
    A :class:`DisplayElement` specially adapted to a :term:`GFK` field.
    """

    def __init__(self, layout_handle, field, **kw):
        self.field = field
        self.editable = False
        # kw.update(label=getattr(field, 'verbose_name', field.name))
        # kw.update(label=field.verbose_name)
        LayoutElement.__init__(self, layout_handle, field.name, **kw)

    def add_default_value(self, kw):
        pass

    def value_from_object(self, obj, ar):
        # logger.info("20180712 GFK.value_from_object() %s %s", self, obj)
        # needed for as_plain_html()
        return getattr(obj, self.field.name)


class RecurrenceElement(DisplayElement):
    value_template = "new Ext.ensible.cal.RecurrenceField(%s)"


class HtmlBoxElement(DisplayElement):
    """Element that renders to a `Lino.HtmlBoxPanel`.

    """
    ext_suffix = "_htmlbox"
    value_template = "new Lino.HtmlBoxPanel(%s)"
    preferred_height = 5
    vflex = True
    filter_type = 'string'
    gridfilters_settings = dict(type='string')
    refers_to_ww = True

    def get_field_options(self, **kw):
        # kw.update(master_panel=js_code("this"))
        kw.update(name=self.field.name)
        if self.layout_handle.ui.renderer.extjs_version is not None:
            kw.update(containing_panel=js_code("this"))
        kw.update(layout='fit')
        # kw.update(autoScroll=True)

        # hide horizontal scrollbar
        # for this trick thanks to Vladimir
        # <http://forums.ext.net/showthread.php?1513-CLOSED-Autoscroll-on-ext-panel>
        # kw.update(bodyStyle="overflow-x:hidden !important;")
        kw.update(bodyStyle="overflow-x:hidden;")

        # ~ if self.field.drop_zone: # testing with drop_zone 'FooBar'
        # kw.update(listeners=dict(render=js_code('initialize%sDropZone' % self.field.drop_zone)))
        if self.layout_handle.ui.renderer.extjs_version is not None:
            html = self.field.default
            if self.layout_handle.ui.renderer.extjs_version == 3:
                js1 = "new Ext.BoxComponent("
            else:
                js1 = "Ext.create('Ext.Component',"
            if html is NOT_PROVIDED:
                js = js1 + "{autoScroll:true})"
            else:
                if callable(html):
                    html = html()
                js = js1 + "{autoScroll:true, html:%s})"
                js = js % py2js(html)
            kw.update(items=js_code(js))
        label = self.get_label()
        if label:
            kw.update(title=label)
        return kw

    def value2html(self, ar, v, **cellattrs):
        # added 20181102, expecting  side effects.
        if is_string(v) and v.startswith("<"):
            from lxml import html
            v = html.fromstring(v)
        return super(HtmlBoxElement, self).value2html(ar, v, **cellattrs)

    def as_plain_html(self, ar, obj):
        value = self.value_from_object(obj, ar)
        if value is fields.NOT_PROVIDED:
            value = str(ar.no_data_text)
        if is_string(value) and value.startswith("<"):
            from lxml import html
            value = html.fromstring(value)
            # try:
            #     value = E.fromstring(value)
            # except Exception:
            #     # logger.warning("20180114 Failed to parse %s", value)
            #     pass
                # panel = E.fromstring('<div class="panel panel-default"><div class="panel-body">' + value + "</div></div>")
        if etree.iselement(value):
            panel = E.div(
                E.div(value, **{'class': "panel-body"}),
                **{'class': "panel panel-default"})

            yield panel


class SlaveSummaryPanel(HtmlBoxElement):
    """
    The panel used to display a slave table whose `display_mode` is
    'summary'.  

    Note that this creates an automatic VirtualField which is a bit
    special because it is created during :func:`create_layout_element`
    after the startup analysis.
    """

    oui5_field_template = "openui5/elems/field/SlaveSummaryElement.xml"

    def __init__(self, lh, actor, **kw):
        box = fields.HtmlBox(actor.label, help_text=actor.help_text)
        # def getter(*args, **kwargs):
        #     print("20181121 SlaveSummaryPanel getter", actor)
        #     return actor.get_table_summary(*args, **kwargs)
        fld = fields.VirtualField(box, actor.get_table_summary)
        # fld.name = actor.__module__ + '_' + actor.__name__
        fld.name = actor.actor_id.replace('.', '_')
        fld.model = lh.layout._datasource  # 20181023 experimental
        # actor.virtual_fields[fld.name] = fld
        # fld.lino_resolve_type()
        super(SlaveSummaryPanel, self).__init__(lh, fld, **kw)


class ManyRelatedObjectElement(HtmlBoxElement):

    def __init__(self, lh, relobj, **kw):
        name = relobj.field.remote_field.related_name

        def f(obj, ar):
            return qs2summary(ar, getattr(obj, name).all())

        box = fields.HtmlBox(name)
        fld = fields.VirtualField(box, f)
        fld.name = name
        fld.model = self
        # fld.lino_resolve_type()
        super(ManyRelatedObjectElement, self).__init__(lh, fld, **kw)


class ManyToManyElement(HtmlBoxElement):

    def __init__(self, lh, relobj, **kw):
        name = relobj.field.name

        def f(obj, ar):
            return qs2summary(ar, getattr(obj, name).all())

        box = fields.HtmlBox(relobj.field.verbose_name)
        fld = fields.VirtualField(box, f)
        fld.name = name
        fld.model = self
        # fld.lino_resolve_type()
        super(ManyToManyElement, self).__init__(lh, fld, **kw)


class Wrapper(VisibleComponent):
    """
    """
    # label = None
    oui5_field_template = "openui5/elems/field/WrappedElement.xml"

    def __init__(self, e, **kw):
        kw.update(layout='form')
        if not isinstance(e, TextFieldElement):
            kw.update(autoHeight=True)
        kw.update(labelAlign=e.layout_handle.layout.label_align)
        kw.update(items=e, xtype='panel')
        VisibleComponent.__init__(self, e.name + "_ct", **kw)
        self.wrapped = e
        for n in ('width', 'height', 'preferred_width', 'preferred_height',
                  # 'loosen_requirements'
                  'vflex'):
            setattr(self, n, getattr(e, n))

        if e.vflex:
            e.update(anchor=FULLWIDTH + ' ' + FULLHEIGHT)
        else:
            e.update(anchor=FULLWIDTH)
            e.update(autoHeight=True)  # 20130924

    def is_visible(self):
        return self.wrapped.is_visible()

    def get_view_permission(self, user_type):
        return self.wrapped.get_view_permission(user_type)

    def walk(self):
        if not self.is_visible():
            return
        for e in self.wrapped.walk():
            yield e
        yield self

    def as_plain_html(self, ar, obj):
        for chunk in self.wrapped.as_plain_html(ar, obj):
            yield chunk

    def ext_options(self, **kw):
        kw = super(Wrapper, self).ext_options(**kw)
        if self.wrapped.field is not None:
            if is_hidden_babel_field(self.wrapped.field):
                kw.update(hidden=True)
                # print("20130827 hidden %s" % self.wrapped.field)
        return kw


class Container(LayoutElement):
    """
    Base class for Layout Elements that can contain other Layout Elements:
    :class:`Panel`,
    :class:`TabPanel`,
    :class:`FormPanel`,
    :class:`GridPanel`
    """
    vertical = False
    hpad = 1
    is_fieldset = False
    value_template = "new Ext.Container(%s)"
    hideCheckBoxLabels = True
    # label_align = layouts.LABEL_ALIGN_TOP

    declare_type = jsgen.DECLARE_VAR

    oui5_field_template = None  # "openui5/elems/field/DisplayElement.xml"

    def __init__(self, layout_handle, name, *elements, **kw):
        self.active_children = []
        self.elements = elements
        # self.label_align = kw.pop('label_align', layouts.LABEL_ALIGN_TOP)
        for e in elements:
            e.set_parent(self)
            if not isinstance(e, LayoutElement):
                raise Exception("%r is not a LayoutElement" % e)
            if e.active_child:
                self.active_children.append(e)
            elif isinstance(e, Panel):
                self.active_children += e.active_children

        LayoutElement.__init__(self, layout_handle, name, **kw)

    def as_plain_html(self, ar, obj):
        if self.vertical:
            children = []
            for e in self.elements:
                for chunk in e.as_plain_html(ar, obj):
                    children.append(chunk)
            yield E.fieldset(*children)
        else:
            # if len(children) > 1:
            # span = 'span' + str(12 / len(children))
            # children = [E.div(ch,class_=span) for ch in children]
            # yield E.div(*children,class_="row-fluid")
            # else:
            # yield children[0]

            # for ch in children:
            # yield E.fieldset(ch)
            # yield ch
            # tr = E.tr(*[E.td(ch) for ch in children])
            tr = []
            for e in self.elements:
                cell = E.td(*tuple(e.as_plain_html(ar, obj)), style="vertical-align: top;")
                tr.append(cell)
            yield E.table(E.tr(*tr))

    def subvars(self):
        return self.elements

    def walk(self):
        if not self.is_visible():
            return
        for e in self.elements:
            if e.is_visible():
                for el in e.walk():
                    yield el
        yield self

    def find_by_name(self, name):
        for e in self.walk():
            if e.name == name:
                return e

    def pprint(self, level=0):
        margin = "  " * level
        s = margin + str(self) + ":\n"
        # self.__class__.__name__
        for e in self.elements:
            for ln in e.pprint(level + 1).splitlines():
                s += ln + "\n"
        return s

    def ext_options(self, **kw):
        kw = LayoutElement.ext_options(self, **kw)
        if self.layout_handle.ui.renderer.extjs_version == 3:
            kw.update(labelAlign=self.layout_handle.layout.label_align)
        # not necessary to filter elements here, jsgen does that
        kw.update(items=self.elements)
        # if all my children are hidden, i am myself hidden
        for e in self.elements:
            if e.is_visible():
                return kw
        kw.update(hidden=True)
        return kw

    def get_view_permission(self, user_type):
        """A Panel which doesn't contain a single visible element becomes
        itself hidden.

        """
        # if the Panel itself is invisble, no need to loop through the
        # children
        if not super(Container, self).get_view_permission(user_type):
            return False
        for e in self.elements:
            if (not isinstance(e, Permittable)) or \
                    e.get_view_permission(user_type):
                # one visible child is enough, no need to continue loop
                return True
                # if not isinstance(e, Permittable):
                #     return True
                # if isinstance(e, Panel) and \
                #    e.get_view_permission(user_type):
                #     return True
        # logger.info("20120925 not a single visible element in %s of %s",self,self.layout_handle)
        return False


class Panel(Container):
    """A vertical Panel is vflex if and only if at least one of its
    children is vflex.  A horizontal Panel is vflex if and only if
    *all* its children are vflex (if vflex and non-vflex elements are
    together in a hbox, then the vflex elements will get the height of
    the highest non-vflex element).

    """
    ext_suffix = "_panel"
    active_child = False
    value_template = "new Ext.Panel(%s)"
    oui5_field_template = "openui5/elems/field/Panel.xml"

    def set_layout_manager(self, name, **cfg):
        d = self.value
        if cfg:
            if self.layout_handle.ui.renderer.extjs_version == 3:
                d['layout'] = name
                d['layoutConfig'] = cfg
            else:
                d.update(layout=dict(type=name, **cfg))
        else:
            d.update(layout=name)

    def get_layout_name(self):
        x = self.value.get('layout')
        if x is not None:
            if isinstance(x, dict):
                return x.get('type')
            return x

    def __init__(self, layout_handle, name, vertical, *elements, **kw):

        # for e in elements:
        #     if isinstance(e, FieldElement):
        #         self.is_fieldset = True

        Container.__init__(self, layout_handle, name, *elements, **kw)

        self.vertical = vertical
        self.vflex = not vertical
        for e in elements:
            if self.vertical:
                if e.vflex:
                    self.vflex = True
            else:
                if not e.vflex:
                    self.vflex = False

        if len(elements) > 1 and self.vflex:
            if self.vertical:
                """
                Example : The panel contains a mixture of fields and grids.
                Fields are not vflex, grids well.
                """
                # print 20100615, self.layout_handle, self
                # so we must split this panel into several containers.
                # vflex elements go into a vbox, the others into a form layout.

            else:  # not self.vertical
                self.set_layout_manager('hbox', align='stretch')

        for e in elements:
            if isinstance(e, FieldElement):
                self.is_fieldset = True

        # Container.__init__(self, layout_handle, name, *elements, **kw)

        w = h = 0
        has_height = False  # 20120210
        for e in self.elements:
            ew = e.width or e.preferred_width
            eh = e.height or e.preferred_height
            if self.vertical:
                # h += e.flex
                h += eh
                w = max(w, ew)
            else:
                if e.height:
                    has_height = True
                # w += e.flex
                w += ew
                h = max(h, eh)
        if has_height:
            self.height = h
            self.vflex = True
        else:
            self.preferred_height = h
        self.preferred_width = w
        assert self.preferred_height > 0, "%s : preferred_height is 0" % self
        assert self.preferred_width > 0, "%s : preferred_width is 0" % self

        d = self.value
        if 'layout' not in d:
            if len(self.elements) == 1:
                d.update(layout='fit')
            elif self.vertical:
                if layout_handle.ui.renderer.extjs_version == 3:
                    if self.vflex:
                        self.set_layout_manager('vbox', align='stretch')
                    else:
                        self.set_layout_manager('form')
                        d.update(autoHeight=True)
                else:
                    self.set_layout_manager('vbox', align='stretch')
            else:
                if layout_handle.ui.renderer.extjs_version == 3:
                    self.set_layout_manager('hbox')
                    d.update(autoHeight=True)
                else:
                    self.set_layout_manager('hbox', autoHeight=True)

        if self.get_layout_name() == 'form':
            assert self.vertical
            # self.update(labelAlign=self.label_align)
            self.wrap_formlayout_elements()
            if len(self.elements) == 1 and self.elements[0].vflex:
                self.elements[0].update(anchor=FULLWIDTH + ' ' + FULLHEIGHT)
            else:
                for e in self.elements:
                    e.update(anchor=FULLWIDTH)

        elif self.get_layout_name() == 'hbox':
            # elif d['layout'] == 'hbox':
            self.wrap_formlayout_elements()
            for e in self.elements:
                # a hbox having at least one child with explicit
                # height will become itself vflex
                if e.height:
                    self.vflex = True

                if e.hflex:
                    w = e.width or e.preferred_width
                    e.value.update(flex=int(w * 100 / self.preferred_width))

            if not self.vflex:  # 20101028
                d.update(autoHeight=True)
                self.set_layout_manager('hbox', align='stretchmax')

        elif self.get_layout_name() in ['vbox', 'anchor']:
            # a vbox with 2 or 3 elements, of which at least two are
            # vflex will be implemented as a VBorderPanel.
            assert len(self.elements) > 1
            self.wrap_formlayout_elements()
            vflex_count = 0
            h = self.height or self.preferred_height
            for e in self.elements:
                eh = e.height or e.preferred_height
                if e.vflex:
                    e.update(flex=int(eh * 100 / h))
                    vflex_count += 1
            if vflex_count >= 2 and len(self.elements) <= 3:
                self.remove('layout', 'layoutConfig')
                if layout_handle.ui.renderer.extjs_version == 3:
                    self.value_template = 'new Lino.VBorderPanel(%s)'
                else:
                    self.value_template = 'Lino.VBorderPanel(%s)'
                for e in self.elements:
                    if e.vflex:
                        e.update(flex=e.height or e.preferred_height)
                    e.update(split=True)
                # lino.utils.jsgen.VisibleComponent#ext_options catches edge case where due to user view permission
                # Ticket #2916
                self.elements[0].update(region='north')
                self.elements[1].update(region='center')
                if len(self.elements) == 3:
                    self.elements[2].update(region='south')
        elif self.get_layout_name() == 'fit':
            self.wrap_formlayout_elements()
        else:
            raise Exception("layout is %r" % d['layout'])

    def wrap_formlayout_elements(self):
        if self.layout_handle.ui.renderer.extjs_version != 3:
            return

        def wrap(e):
            if not isinstance(e, FieldElement):
                return e
            if e.get_label() is None:
                return e
            if e.hidden:
                return e
            if isinstance(e, HtmlBoxElement):
                return e
            if settings.SITE.use_tinymce:
                if isinstance(e, TextFieldElement) and e.format == 'html':
                    # no need to wrap them since they are Panels
                    return e
            return Wrapper(e)

        self.elements = [wrap(e) for e in self.elements]

    def ext_options(self, **d):

        label = self.get_label()
        if label:
            if not isinstance(self.parent, TabPanel):
                self.update(title=label)
                if self.layout_handle.ui.renderer.extjs_version == 3:
                    self.value_template = "new Ext.form.FieldSet(%s)"
                else:
                    self.value_template = "Ext.create('Ext.form.FieldSet',%s)"
                self.update(frame=False)
                self.update(bodyBorder=True)
                self.update(border=True)

        d = Container.ext_options(self, **d)

        # hide scrollbars
        d.update(autoScroll=False)

        if self.is_fieldset:
            # Note that the value of labelWidth depends on the
            # language.  For example the sign_in dialog window has a
            # field labelled "Username:" which is "Nom d'utilisateur:"
            # in French (#2240 spacing problem in french login form).

            label_width = 0
            for e in self.elements:
                if isinstance(e, FieldElement):
                    label = e.get_label()
                    if label:
                        w = len(label) + 1  # +1 for the ":"
                        if label_width < w:
                            label_width = w
            d.update(labelWidth=label_width * EXT_CHAR_WIDTH)

        if self.parent is None or (len(self.elements) > 1 and self.vertical):
            """
            The `self.parent is None` test is e.g. for Parameter
            Panels which are usually not vertical but still want a frame
            since they are the main panel.
            """
            d.update(frame=True)
            d.update(bodyBorder=False)
            d.update(border=False)
            if self.layout_handle.ui.renderer.extjs_version != 3:
                d.update(layout=dict(type='vbox', align='stretch'))
            # d.update(style=dict(padding='0px'),color='green')
        else:
            d.update(frame=False)
            # self.update(bodyBorder=False)
            d.update(border=False)

        return d


class GridElement(Container):
    """Represents a Lino.GridPanel, i.e. the widget used to represent a
    table or a slave table.

    """
    declare_type = jsgen.DECLARE_VAR
    # declare_type = jsgen.DECLARE_THIS
    # value_template = "new Ext.grid.EditorGridPanel(%s)"
    # value_template = "new Ext.grid.GridPanel(%s)"
    # value_template = "new Lino.GridPanel(%s)"
    ext_suffix = "_grid"
    vflex = True
    xtype = None
    preferred_height = 5
    refers_to_ww = True
    oui5_field_template = "openui5/elems/field/GridElement.xml"

    def __init__(self, layout_handle, name, rpt, *columns, **kw):
        """:param layout_handle: the handle of the FormLayout owning this grid.

        :param rpt: the table being displayed
        (:class:`lino.core.tables.AbstractTable`)

        """
        # assert isinstance(rpt,dd.AbstractTable), "%r is not a Table!" % rpt
        if layout_handle.ui.renderer.extjs_version == 3:
            self.value_template = "new Lino.%s.GridPanel(%%s)" % rpt
        else:
            self.value_template = "Ext.create('Lino.%s.GridPanel',%%s)" % rpt
        self.actor = rpt
        if len(columns) == 0:
            self.rh = rpt.get_handle()
            if not hasattr(self.rh, 'list_layout'):
                raise Exception(
                    "Handle for {0} (model {1}) has no list_layout".format(
                        rpt, rpt.model))
            columns = self.rh.list_layout.main.columns
            # columns = self.rh.list_layout._main.elements
        w = 0
        for e in columns:
            w += (e.width or e.preferred_width)
        self.preferred_width = constrain(w, 10, 120)
        # kw.update(boxMinWidth=500)
        self.columns = columns

        # vc = dict(emptyText=_("No data to display."))
        # if rpt.editable:
        # vc.update(getRowClass=js_code('Lino.getRowClass'))
        # if rpt.auto_fit_column_widths:
        # vc.update(forceFit=True)
        if False:  # removed 20131107
            if rpt.variable_row_height:
                vc = dict(cellTpl=js_code("Lino.auto_height_cell_template"))
                kw.update(viewConfig=vc)

        # kw.setdefault('label', rpt.label)
        if len(self.columns) == 1:
            kw.setdefault('hideHeaders', True)

        layout_handle.ui.renderer.add_help_text(kw, rpt.help_text, rpt.title or rpt.label,
                      rpt.app_label, rpt.actor_id)

        # kw.update(containing_window=js_code("this.containing_window"))
        if layout_handle.ui.renderer.extjs_version is not None:
            kw.update(containing_panel=js_code("this"))
        # if not rpt.show_params_at_render:
        if rpt.params_panel_hidden:
            kw.update(params_panel_hidden=True)
        Container.__init__(self, layout_handle, name, **kw)
        self.active_children = columns

    def get_label(self):
        return self.actor.label

    def get_view_permission(self, user_type):
        # skip Container parent:
        if not super(Container, self).get_view_permission(user_type):
            return False
        return self.actor.default_action.get_view_permission(user_type)

    def ext_options(self, **kw):
        # not direct parent (Container), only LayoutElement
        kw = LayoutElement.ext_options(self, **kw)
        return kw

    def headers2html(self, ar, columns, headers, header_links, **cellattrs):
        assert len(headers) == len(columns)
        for i, e in enumerate(columns):
            txt = headers[i]
            # print 20131015, txt
            txt = join_elems(txt.split('\n'), sep=E.br)
            if header_links and ar.renderer.is_interactive:
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
        sar = ar.spawn(self.actor.default_action, master_instance=obj)
        yield table2html(sar, as_main=(self.name == "main"))
        # yield sar.as_bootstrap_html(as_main=(self.name == "main"))


class DetailMainPanel(Panel):
    xtype = None
    value_template = "new Ext.Panel(%s)"
    oui5_field_template = "openui5/elems/field/DetailMainPanel.xml"

    def __init__(self, layout_handle, name, vertical, *elements, **kw):
        kw.update(autoScroll=True)
        Panel.__init__(self, layout_handle, name, vertical, *elements, **kw)

    def ext_options(self, **kw):
        kw = Panel.ext_options(self, **kw)
        label = self.layout_handle.main.get_label()
        if label:
            kw.update(title=label)
        return kw


class ParamsPanel(Panel):
    """
    The optional Panel for `parameters` of a Table.
    JS part stored in `Lino.GridPanel.params_panel`.
    """
    # value_template = "new Ext.form.FormPanel(%s)"
    # value_template = "new Ext.form.FormPanel({layout:'fit', autoHeight: true, frame: true, items:new Ext.Panel(%s)})"
    value_template = "%s"


class ActionParamsPanel(Panel):
    """
    The optional Panel for `parameters` of an Action.
    """
    xtype = None
    value_template = "new Lino.ActionParamsPanel(%s)"


class TabPanel(Panel):
    value_template = "new Ext.TabPanel(%s)"
    oui5_field_template = "openui5/elems/field/TabPanel.xml"

    def __init__(self, layout_handle, name, *elems, **kw):
        kw.update(autoScroll=True)
        kw.update(
            split=True,
            activeTab=0,
            # ~ layoutOnTabChange=True, # 20101028
            # ~ forceLayout=True, # 20101028
            # ~ deferredRender=False, # 20120212
            enableTabScroll=True,
            # ~ width=300, # ! http://code.google.com/p/lino/wiki/20100513
            # items=elems,
            # http://www.extjs.com/forum/showthread.php?26564-Solved-FormPanel-in-a-TabPanel
            # listeners=dict(activate=js_code("function(p) {p.doLayout();}"),single=True),
        )

        Container.__init__(self, layout_handle, name, *elems, **kw)

    def as_plain_html(self, ar, obj):
        nav = E.ul(**{'class': "nav nav-tabs"})
        for e in self.elements:
            tab = E.li()
            tab.append(E.a(str(e.get_label()), data_toggle="tab", href="#" + e.ext_name))
            nav.append(tab)
        nav[0].set("class", "active")

        yield nav
        main = E.div(**{'class':"tab-content"})
        for e in self.elements:
            main.append(E.div(*tuple(e.as_plain_html(ar, obj)), id=e.ext_name, **{'class': "tab-pane fade"}))
        main[0].set("class", main[0].get("class") + " in active")
        yield main


_FIELD2ELEM = (
    # (dd.Constant, ConstantElement),
    (fields.RecurrenceField, RecurrenceElement),
    (fields.HtmlBox, HtmlBoxElement),
    # (dd.QuickAction, QuickActionElement),
    # (dd.RequestField, RequestFieldElement),
    (fields.DisplayField, DisplayElement),
    (fields.QuantityField, QuantityFieldElement),
    (fields.IncompleteDateField, IncompleteDateFieldElement),
    # (dd.LinkedForeignKey, LinkedForeignKeyElement),
    (models.URLField, URLFieldElement),
    (models.FileField, FileFieldElement),
    (models.EmailField, CharFieldElement),
    # (dd.HtmlTextField, HtmlTextFieldElement),
    # (dd.RichTextField, RichTextFieldElement),
    (models.TextField, TextFieldElement),  # also dd.RichTextField
    (fields.PasswordField, PasswordFieldElement),
    (models.CharField, CharFieldElement),
    (fields.MonthField, MonthFieldElement),
    (models.DateTimeField, DateTimeFieldElement),
    (fields.DatePickerField, DatePickerFieldElement),
    (models.DateField, DateFieldElement),
    (models.TimeField, TimeFieldElement),
    (models.IntegerField, IntegerFieldElement),
    (models.DecimalField, DecimalFieldElement),
    (models.AutoField, AutoFieldElement),
    (models.BooleanField, BooleanFieldElement),
    # TODO: Lino currently renders NullBooleanField like BooleanField
    (models.NullBooleanField, BooleanFieldElement),
    # (models.ManyToManyField, M2mGridElement),
    (models.ForeignKey, ForeignKeyElement),
)

TRIGGER_BUTTON_WIDTH = 3


def field2elem(layout_handle, field, **kw):
    if isinstance(field, models.OneToOneField):
        # logger.info("20180712 field2elem OneToOneField %s", field)
        return GenericForeignKeyElement(layout_handle, field, **kw)
    # kw = layout_handle.layout._datasource.get_widget_options(
    #     field.name, **kw)
    # if field.name == 'item_ref':
    #     print("20180828", kw)

    rnd = layout_handle.ui.renderer
    holder = layout_handle.layout.get_chooser_holder()
    ch = holder.get_chooser_for_field(field.name)

    if ch:
        if ch.can_create_choice or not ch.force_selection:
            kw.update(forceSelection=False)
        elif rnd.extjs_version == 6:
            # Ticket #2006, even with ch.force_selection == True for timezone, the js defaults to False
            kw.update(forceSelection=True)
        if ch.simple_values:
            return SimpleRemoteComboFieldElement(layout_handle, field, **kw)
        else:
            if isinstance(field, models.ForeignKey):
                return ForeignKeyElement(layout_handle, field, **kw)
            else:
                return ComplexRemoteComboFieldElement(
                    layout_handle, field, **kw)
    if field.choices:
        if isinstance(field, choicelists.ChoiceListField):
            if field.choicelist.preferred_width is None:
                msg = "{0} has no preferred_width. Is the plugin installed?"
                msg = msg.format(field.choicelist)
                raise Exception(msg)
            kw.setdefault(
                'preferred_width',
                field.choicelist.preferred_width + TRIGGER_BUTTON_WIDTH)
            kw.update(forceSelection=field.force_selection)
            return ChoiceListFieldElement(layout_handle, field, **kw)
        else:
            kw.setdefault('preferred_width', 20)
            return ChoicesFieldElement(layout_handle, field, **kw)

    if isinstance(field, fields.RequestField):
        return RequestFieldElement(layout_handle, field, **kw)

    selector_field = field
    if isinstance(field, fields.RemoteField):
        selector_field = field.field
        kw.update(sortable=False)
    if isinstance(selector_field, fields.VirtualField):
        selector_field = selector_field.return_type
    # remember the case of RemoteField to VirtualField

    if isinstance(selector_field, fields.CustomField):
        e = selector_field.create_layout_elem(
            rnd, CharFieldElement, layout_handle, field, **kw)
        if e is not None:
            return e

    if isinstance(selector_field, models.BooleanField) and not field.editable:
        return BooleanDisplayElement(layout_handle, field, **kw)

    for df, cl in _FIELD2ELEM:
        if isinstance(selector_field, df):
            return cl(layout_handle, field, **kw)
    if isinstance(field, fields.VirtualField):
        raise NotImplementedError(
            "No LayoutElement for VirtualField %s on %s in %s" % (
                field.name, field.return_type.__class__,
                layout_handle.layout))
    if isinstance(field, fields.RemoteField):
        raise NotImplementedError(
            "No LayoutElement for RemoteField %s to %s" % (
                field.name, field.field.__class__))
    raise NotImplementedError(
        "No LayoutElement for %s (%s) in %s" % (
            field.name, field.__class__, layout_handle.layout))


def create_layout_panel(lh, name, vertical, elems, **kwargs):
    """
    This also must translate ui-agnostic parameters
    like `label_align` to their ExtJS equivalent `labelAlign`.
    """
    pkw = dict()
    # if rnd.extjs_version == 3:
    #     # pkw.update(labelAlign=kwargs.pop('label_align', 'top'))
    #     pkw.update(label_align=kwargs.pop(
    #         'label_align', lh.layout.label_align))
    pkw.update(hideCheckBoxLabels=kwargs.pop('hideCheckBoxLabels', True))
    pkw.update(label=kwargs.pop('label', None))
    pkw.update(width=kwargs.pop('width', None))
    pkw.update(height=kwargs.pop('height', None))
    # pkw.update(help_text=kwargs.pop('help_text', None))
    v = kwargs.pop('required_roles', NOT_PROVIDED)
    if v is not NOT_PROVIDED:
        pkw.update(required_roles=v)
    if kwargs:
        raise Exception("Unknown panel attributes %r for %s" % (kwargs, lh))
    if name == 'main':
        if isinstance(lh.layout, ColumnsLayout):
            e = GridElement(
                lh, name, lh.layout._datasource, *elems, **pkw)
        elif isinstance(lh.layout, ActionParamsLayout):
            e = ActionParamsPanel(lh, name, vertical, *elems, **pkw)
        elif isinstance(lh.layout, ParamsLayout):
            e = ParamsPanel(lh, name, vertical, *elems, **pkw)
        elif isinstance(lh.layout, FormLayout):
            if len(elems) == 1 or vertical:
                e = DetailMainPanel(
                    lh, name, vertical, *elems, **pkw)
            else:
                e = TabPanel(lh, name, *elems, **pkw)
        else:
            raise Exception("No element class for layout %r" % lh.layout)
        return e
    return Panel(lh, name, vertical, *elems, **pkw)


def create_layout_element(lh, name, **kw):
    """
    Create a layout element from the named data element.
    """

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
                return None
        # ctx = (lh.layout.__class__, name, ', '.join(dir(lh.layout)))
        # raise Exception(
        #     "Instance of %s has no data element '%s' (names are %s)" % ctx)
        raise Exception("{0} has no data element '{1}'".format(
            lh.layout, name))

    if isinstance(de, type) and issubclass(de, fields.Dummy):
        return None

    if isinstance(de, DummyPanel):
        return None

    if isinstance(de, GenericRelation):
        return None

    if isinstance(de, fields.DummyField):
        lh.add_store_field(de)
        return None

    if isinstance(de, fields.Constant):
        return ConstantElement(lh, de, **kw)

    if isinstance(de, fields.RemoteField):
        return create_field_element(lh, de, **kw)

    if isinstance(de, SingleRelatedObjectDescriptor):
        return SingleRelatedObjectElement(lh, de.related, **kw)

    if isinstance(de, (
            ManyRelatedObjectsDescriptor, ForeignRelatedObjectsDescriptor)):
        e = ManyRelatedObjectElement(lh, de.related, **kw)
        lh.add_store_field(e.field)
        return e

    if isinstance(de, models.ManyToManyField):
        # Replacing related by remote_field to supports Django 1.9.9 and 1.10
        e = ManyToManyElement(lh, de.remote_field, **kw)
        lh.add_store_field(e.field)
        return e

    if isinstance(de, (ManyToManyRel, ManyToOneRel)):
        e = ManyRelatedObjectElement(lh, de, **kw)
        lh.add_store_field(e.field)
        return e

    if isinstance(de, models.Field):
        if isinstance(de, (BabelCharField, BabelTextField)):
            if len(settings.SITE.BABEL_LANGS) > 0:
                elems = [create_field_element(lh, de, **kw)]
                for lang in settings.SITE.BABEL_LANGS:
                    bf = lh.get_data_elem(name + lang.suffix)
                    elems.append(create_field_element(lh, bf, **kw))
                return elems
        return create_field_element(lh, de, **kw)

    if isinstance(de, fields.DisplayField):
        return create_field_element(lh, de, **kw)

    if isinstance(de, GenericForeignKey):
        # create a horizontal panel with 2 comboboxes
        de.primary_key = False  # for ext_store.Store()
        lh.add_store_field(de)
        return GenericForeignKeyElement(lh, de, **kw)

    if isinstance(de, type) and issubclass(de, tables.AbstractTable):
        # The data element refers to a slave table. Slave tables make
        # no sense in an insert window because the master does not yet
        # exist.

        if lh.ui.renderer.extjs_version is not None:
            kw.update(master_panel=js_code("this"))

        if isinstance(lh.layout, FormLayout):
            # When a table is specified in the layout of a
            # DetailWindow, then it will be rendered as a panel that
            # displays a "summary" of that table. The panel will have
            # a tool button to "open that table in its own
            # window". The format of that summary is defined by the
            # `display_mode` of the table.

            if lh.ui.renderer.extjs_version is not None:
                js = "Lino.show_in_own_window_button(Lino.%s)" % de.default_action.full_name()
                kw.update(tools=[js_code(js)])
                if False:
                    js = 'alert("Oops")'
                    url = lh.ui.renderer.js2url(js)
                    btn = lh.ui.renderer.href_button(
                        url, "⏏",  # 23CF
                        title=_("Show this table in own window"),
                        style="text-decoration:none;")
                    kw.update(label='{} {}'.format(de.get_label(), tostring(btn)))
            if de.display_mode == 'grid':
                kw.update(hide_top_toolbar=True)
                if de.preview_limit is not None:
                    kw.update(preview_limit=de.preview_limit)
                return GridElement(lh, name, de, **kw)

            elif de.display_mode == 'html':
                # if de.editable:
                #     a = de.insert_action
                #     if a is not None:
                #         kw.update(ls_insert_handler=js_code("Lino.%s" %
                #                                             a.full_name()))
                #         kw.update(ls_bbar_actions=[
                #             lh.ui.renderer.a2btn(a)])
                field = fields.HtmlBox(verbose_name=de.get_label())
                field.name = de.__name__
                field.help_text = de.help_text
                field._return_type_for_method = de.slave_as_html
                lh.add_store_field(field)
                e = HtmlBoxElement(lh, field, **kw)
                e.add_requirements(*de.required_roles)
                return e

            elif de.display_mode == 'summary':
                e = SlaveSummaryPanel(lh, de, **kw)
                e.add_requirements(*de.required_roles)
                lh.add_store_field(e.field)
                return e
            else:
                raise Exception(
                    "Invalid display_mode %r" % de.display_mode)

        else:
            e = SlaveSummaryPanel(lh, de, **kw)
            lh.add_store_field(e.field)
            return e

    if isinstance(de, Action):
        return ButtonElement(lh, name, de)

    if isinstance(de, fields.VirtualField):
        return create_vurt_element(lh, name, de, **kw)

    if callable(de):
        rt = getattr(de, 'return_type', None)
        if rt is not None:
            return create_meth_element(lh, name, de, rt, **kw)

    # Now we tried everything. Build an error message.

    if hasattr(lh, 'rh'):
        msg = "Unknown element '%s' (%r) referred in layout <%s of %s>." % (
            name, de, lh.layout, lh.rh.actor)
        l = [wde.name for wde in lh.rh.actor.wildcard_data_elems()]
        # VirtualTables don't have a model
        model = getattr(lh.rh.actor, 'model', None)
        if getattr(model, '_lino_slaves', None):
            l += [str(rpt) for rpt in list(model._lino_slaves.values())]
        msg += " Possible names are %s." % ', '.join(l)
    else:
        msg = "Unknown element '%s' (%r) referred in layout <%s>." % (
            name, de, lh.layout)
        # if de is not None:
        #     msg += " Cannot handle %r" % de
    raise KeyError(msg)


def create_vurt_element(lh, name, vf, **kw):
    e = create_field_element(lh, vf, **kw)
    # e.sortable = False
    if not vf.is_enabled(lh):
        e.editable = False
    return e


def create_meth_element(lh, name, meth, rt, **kw):
    rt.name = name
    rt._return_type_for_method = meth
    if meth.__code__.co_argcount < 2:
        raise Exception("Method %s has %d arguments (must have at least 2)" %
                        (meth, meth.__code__.co_argcount))
    return create_field_element(lh, rt, **kw)


def create_field_element(lh, field, **kw):
    e = field2elem(lh, field, **kw)
    # if not lh.layout.editable and isinstance(e, ForeignKeyElement):
    #     raise Exception(20160907)
    #     return CharFieldElement(lh, field, **kw)   

    assert e.field is not None, "e.field is None for %s.%s" % (lh.layout, kw)
    lh.add_store_field(e.field)
    return e
