# -*- coding: UTF-8 -*-
# Copyright 2009-2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""Defines "layout elements" (widgets).

The biggest part of this module should actually be moved to
:mod:`lino.core.elems`.

"""

from __future__ import print_function
from builtins import str
from past.builtins import basestring
from builtins import object

import logging
logger = logging.getLogger(__name__)

from cgi import escape
import decimal

from lino import AFTER17, AFTER18

from django.db import models
from django.utils.translation import ugettext as _
from django.utils.translation import string_concat
from django.conf import settings
if AFTER18:
    from django.db.models.fields.related import \
        ReverseOneToOneDescriptor as SingleRelatedObjectDescriptor
    from django.db.models.fields.related import \
        ReverseManyToOneDescriptor as ForeignRelatedObjectsDescriptor
    from django.db.models.fields.related import \
        ManyToManyDescriptor as ManyRelatedObjectsDescriptor
else:
    from django.db.models.fields.related import SingleRelatedObjectDescriptor
    from django.db.models.fields.related import ForeignRelatedObjectsDescriptor
    from django.db.models.fields.related import ManyRelatedObjectsDescriptor



if AFTER17:
    from django.db.models.fields.related import ManyToManyRel, ManyToOneRel
from django.db.models.fields import NOT_PROVIDED

from lino.core import layouts
from lino.core import fields
from lino.core.actions import Permittable
from lino.core import constants
from lino.core.gfks import GenericRelation

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

from lino.utils.xmlgen import etree
from lino.utils.xmlgen.html import E

EXT_CHAR_WIDTH = 9
EXT_CHAR_HEIGHT = 22

# FULLWIDTH = '100%'
# FULLHEIGHT = '100%'

FULLWIDTH = '-20'
FULLHEIGHT = '-10'

USED_NUMBER_FORMATS = dict()

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
        kw.update(sortable=True)
        kw.update(colIndex=index)
        if editor.hidden:
            kw.update(hidden=True)
        if settings.SITE.use_filterRow:
            if editor.filter_type:
                if index == 0:
                    # first column used to show clear filter icon in this
                    # column
                    kw.update(clearFilter=True)
                # else:
                    # print index, "is not 1"
                kw.update(filterInput=js_code('new Ext.form.TextField()'))
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
                kw.update(filter=editor.gridfilters_settings)
        if isinstance(editor, FieldElement):
            if settings.SITE.use_quicktips:
                # if jsgen._for_user_profile.expert:
                if settings.SITE.show_internal_field_names:
                    ttt = "(%s.%s) " % (layout_handle.layout._datasource,
                                        self.editor.field.name)
                else:
                    ttt = ''
                if self.editor.field.help_text \
                   and "<" not in self.editor.field.help_text:
                    # and '"' not in self.editor.field.help_text
                    # GridColumn tooltips don't support html
                    ttt = string_concat(ttt, self.editor.field.help_text)
                if ttt:
                    kw.update(tooltip=ttt)

            def fk_renderer(fld, name):
                # FK fields are clickable only if their target has a
                # detail view
                rpt = fld.rel.model.get_default_table()
                if rpt.detail_action is not None:
                    if rpt.detail_action.get_view_permission(
                            jsgen._for_user_profile):
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
                kw.update(sortable=False)
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

    label = None
    label_width = 0
    editable = False
    sortable = False
    xtype = None  # set by subclasses
    collapsible = False
    active_child = True
    refers_to_ww = False

    def __init__(self, layout_handle, name, **kw):
        #logger.debug("LayoutElement.__init__(%r,%r)", layout_handle.layout,name)
        #self.parent = parent
        # name = layout_handle.layout._actor_name + '_' + name
        assert isinstance(layout_handle, layouts.LayoutHandle)
        opts = layout_handle.layout._element_options.get(name, {})
        for k, v in list(opts.items()):
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
        # if str(self.layout_handle.layout._datasource) == 'lino.Home':
            # logger.info("20120927 LayoutElement.__init__ %r required is %s, kw was %s, opts was %s",
              # self,self.required,kw,opts)

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

    def set_parent(self, parent):
        # if self.parent is not None:
            # raise Exception("%s : parent is already %s, cannot set it to %s" % (self,self.parent,parent))
        self.parent = parent
        # if isinstance(parent,FieldSetPanel):
            # self.label = None
            # self.update(label = None)
        if self.label:
            if isinstance(parent, Panel):
                if parent.label_align == layouts.LABEL_ALIGN_LEFT:
                    self.preferred_width += len(self.label)

    def ext_options(self, **kw):
        if self.hidden:
            kw.update(hidden=True)
        if isinstance(self.parent, TabPanel):
            if not self.label:
                raise Exception(
                    "Item %s of tabbed %s has no label!" % (
                        self, self.layout_handle))
            ukw = dict(title=self.label)
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
    #declare_type = jsgen.DECLARE_THIS
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


class Spacer(LayoutElement):
    declare_type = jsgen.DECLARE_INLINE
    #xtype = 'label'
    value_template = "new Ext.Spacer(%s)"


def add_help_text(kw, help_text, title, datasource, fieldname):
    if settings.SITE.use_quicktips:
        if settings.SITE.show_internal_field_names:
            ttt = "(%s.%s) " % (datasource, fieldname)
        else:
            ttt = ''
        if help_text:
            ttt = string_concat(ttt, help_text)
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
    if jsgen._for_user_profile is None:
        return False
    if jsgen._for_user_profile.hidden_languages is None:
        return False
    if lng in jsgen._for_user_profile.hidden_languages:
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
    #declaration_order = 3
    # ext_suffix = "_field"
    zero = 0

    def __init__(self, layout_handle, field, **kw):
        if not getattr(field, 'name', None):
            raise Exception("Field '%s' in %s has no name!" %
                            (field, layout_handle))
        self.field = field
        self.editable = field.editable  # and not field.primary_key

        if 'listeners' not in kw:
            if not isinstance(layout_handle.layout, layouts.ColumnsLayout):
                add_help_text(
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
        kw.setdefault('label', field.verbose_name)

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
        if self.label is None:
            kw.update(header=self.name)
        elif self.label:
            kw.update(header=self.label)
        else:
            kw.update(header=self.label)
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

        # When used as editor of an EditorGridPanel, don't set the
        # name attribute because it is not needed for grids and might
        # conflict with fields of a surronding detail form. See ticket
        # #38 (`/blog/2011/0408`).  Also don't set a label then.
        if not isinstance(self.layout_handle.layout, layouts.ColumnsLayout):
            kw.update(name=self.field.name)
            if self.label:
                label = self.label
                if self.field.help_text:
                    if settings.SITE.use_css_tooltips:
                        label = string_concat(
                            '<a class="tooltip" href="#">',
                            label,
                            '<span class="classic">',
                            self.field.help_text,
                            '</span></a>')
                    elif settings.SITE.use_quicktips:
                        label = string_concat(
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
        if i == ar.actor.sum_text_column:
            return E.b(ar.get_sum_text(sums))
        if sums[self.name]:
            return E.b(self.format_value(ar, sums[self.name]))
        return ''

    def value2num(self, v):
        # print "20120426 %s value2num(%s)" % (self,v)
        return 0


class TextFieldElement(FieldElement):
    # xtype = 'textarea'
    filter_type = 'string'
    gridfilters_settings = dict(type='string')
    vflex = True
    value_template = "new Ext.form.TextArea(%s)"
    xtype = None
    #width = 60
    preferred_width = 60
    preferred_height = 5
    #collapsible = True
    separate_window = False
    active_child = False
    format = 'plain'

    def __init__(self, layout_handle, field, **kw):
        self.format = getattr(field, 'textfield_format', None) \
            or settings.SITE.textfield_format
        if self.format == 'html':
            if settings.SITE.is_installed('tinymce'):
                self.value_template = "new Lino.RichTextPanel(%s)"
                self.active_child = True
                # if self.label:
                    # kw.update(title=unicode(self.label))
                self.separate_window = True
                # we don't call FieldElement.__init__ but do almost the same:
                self.field = field
                self.editable = field.editable  # and not field.primary_key
                # 20111126 kw.update(ls_url=rpt2url(layout_handle.rh.report))
                # kw.update(master_panel=js_code("this"))
                kw.update(containing_panel=js_code("this"))
                # kw.update(title=unicode(field.verbose_name)) 20111111
                kw.update(label=field.verbose_name)
                kw.update(title=field.verbose_name)
                return LayoutElement.__init__(
                    self, layout_handle, field.name, **kw)
            else:
                self.value_template = "new Ext.form.HtmlEditor(%s)"
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
        yield E.label(str(self.field.verbose_name))
        yield E.textarea(text, rows=str(self.preferred_height))

    def value2html(self, ar, v, **cellattrs):
        if self.format == 'html' and v:
            v = html2xhtml(v)
            top = E.fromstring(v)
        else:
            top = self.format_value(ar, v)
        return E.td(top, **cellattrs)


class CharFieldElement(FieldElement):
    filter_type = 'string'
    gridfilters_settings = dict(type='string')
    value_template = "new Ext.form.TextField(%s)"
    sortable = True
    xtype = None

    def __init__(self, *args, **kw):
        FieldElement.__init__(self, *args, **kw)
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
    sortable = True
    xtype = None
    filter_type = 'string'
    gridfilters_settings = dict(type='string')

    def get_field_options(self, **kw):
        kw = FieldElement.get_field_options(self, **kw)
        # When used as editor of an EditorGridPanel, don't set the name attribute
        # because it is not needed for grids and might conflict with fields of a
        # surronding detail form. See ticket #38 (`/blog/2011/0408`).
        # Also, Comboboxes with simple values may never have a hiddenName
        # option.
        if not isinstance(self.layout_handle.layout, layouts.ColumnsLayout) \
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

    def __init__(self, layout_handle, field, **kw):
        pw = field.choicelist.preferred_foreignkey_width
        if pw is not None:
            kw.setdefault('preferred_width', pw)
        FieldElement.__init__(self, layout_handle, field, **kw)

    def get_field_options(self, **kw):
        kw = ComboFieldElement.get_field_options(self, **kw)
        # kw.update(store=js_code('Lino.%s.choices' % self.field.choicelist.actor_id))
        js = 'Lino.%s' % self.field.choicelist.actor_id
        if self.field.blank:
            js = "[['','<br>']].concat(%s)" % js
        kw.update(store=js_code(js))
        return kw


class RemoteComboFieldElement(ComboFieldElement):
    value_template = "new Lino.RemoteComboFieldElement(%s)"

    def store_options(self, **kw):
        # ~ kw.update(baseParams=js_code('this.get_base_params()')) # 20120202
        if self.editable:
            url = self.layout_handle.get_choices_url(self.field, **kw)
            proxy = dict(url=url, method='GET')
            kw.update(proxy=js_code("new Ext.data.HttpProxy(%s)" %
                      py2js(proxy)))
        # a JsonStore without explicit proxy sometimes used method POST
        return kw

    def get_field_options(self, **kw):
        kw = ComboFieldElement.get_field_options(self, **kw)
        sto = self.store_options()
        # print repr(sto)
        kw.update(store=js_code("new Lino.ComplexRemoteComboStore(%s)" %
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

    preferred_width = 20

    def get_field_options(self, **kw):
        kw = super(ForeignKeyElement, self).get_field_options(**kw)
        if isinstance(self.field.rel.model, basestring):
            raise Exception("20130827 %s.rel.model is %r" %
                            (self.field, self.field.rel.model))
        pw = self.field.rel.model.preferred_foreignkey_width
        if pw is not None:
            kw.setdefault('preferred_width', pw)
        actor = self.field.rel.model.get_default_table()
        if not isinstance(self.layout_handle.layout, layouts.ColumnsLayout):
            a1 = actor.detail_action
            a2 = actor.insert_action
            if a1 is not None or a2 is not None:
                self.value_template = "new Lino.TwinCombo(%s)"
                js = "function(e){ Lino.show_fk_detail(this,%s,%s)}" % (
                    action_name(a1), action_name(a2))
                kw.update(onTrigger2Click=js_code(js))

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
        return E.td(ar.obj2html(v), **cellattrs)


class TimeFieldElement(FieldElement):
    value_template = "new Lino.TimeField(%s)"
    # xtype = 'timefield'
    # ~ data_type = 'time' # for store column
    sortable = True
    preferred_width = 8
    # filter_type = 'time'


class DateTimeFieldElement(FieldElement):
    # value_template = "new Lino.DateTimeField(%s)"
    value_template = "new Ext.form.DisplayField(%s)"
    # ~ data_type = 'date' # for store column
    sortable = True
    preferred_width = 16
    # filter_type = 'date'

    def __init__(self, layout_handle, field, **kw):
        if self.editable:
            self.value_template = "new Lino.DateTimeField(%s)"
        else:
            kw.update(value="<br>")
        FieldElement.__init__(self, layout_handle, field, **kw)


class DatePickerFieldElement(FieldElement):
    value_template = "new Lino.DatePickerField(%s)"

    def get_column_options(self, **kw):
        raise Exception("not allowed in grid")


class DateFieldElement(FieldElement):
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

    # def __init__(self,layout_handle,field,**kw):
        # ~ if False: # getattr(field,'picker',False):
            # self.value_template = "new Lino.DatePickerField(%s)"
        # FieldElement.__init__(self,layout_handle,field,**kw)

    # def get_field_options(self,**kw):
        # kw = FieldElement.get_field_options(self,**kw)
        # kw.update(format=self.layout_handle.rh.actor.date_format)
        # return kw

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
        # e.set('align','right')
        e.attrib.update(align='right')
        # logger.info("20130119 apply_cell_format %s",etree.tostring(e))

    def format_sum(self, ar, sums, i):
        return E.b(self.format_value(ar, sums[self.name]))

    def value2num(self, v):
        return v

    # def apply_cell_format(self,e):
        # e.set('align','right')

    def sum2html(self, ar, sums, i, **cellattrs):
        cellattrs.update(align="right")
        return super(NumberFieldElement, self).sum2html(
            ar, sums, i, **cellattrs)

    # 20130119b
    # def value2html(self,ar,v,**cellattrs):
        # cellattrs.update(align="right")
        # return E.td(self.format_value(ar,v),**cellattrs)

    def get_column_options(self, **kw):
        kw = FieldElement.get_column_options(self, **kw)
        # kw.update(xtype='numbercolumn')
        kw.update(align='right')

        # if settings.SITE.decimal_group_separator:
            # fmt = '0' + settings.SITE.decimal_group_separator + '000'
        # else:
        # Ext.utils.format.number() is not able to specify ' ' as group separator,
        # so we don't use grouping at all.
        if self.number_format != settings.SITE.default_number_format_extjs:
            kw.update(format=self.number_format)
        n = USED_NUMBER_FORMATS.get(self.number_format, 0)
        USED_NUMBER_FORMATS[self.number_format] = n + 1
        # ~ kw.update(format='') # 20130125
        # ~ kw.update(renderer=js_code('Lino.nullnumbercolumn_renderer')) # 20130125
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
        return E.td(E.a(str(n), href='javascript:'+url), **cellattrs)

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
        # return self.format_value(ar,sums[i])
        return E.b(str(sums[self.name]))


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
        fmt = '0'
        if self.field.decimal_places > 0:
            fmt += settings.SITE.decimal_separator + \
                ("0" * self.field.decimal_places)
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

    def __init__(self, *args, **kw):
        kw.setdefault('value', '<br/>')  # see blog/2012/0527
        kw.update(always_enabled=True)
        FieldElement.__init__(self, *args, **kw)
        self.preferred_height = self.field.preferred_height
        self.preferred_width = self.field.preferred_width
        if self.field.max_length:
            self.preferred_width = self.field.max_length

    def value_from_object(self, obj, ar):
        return self.field.value_from_object(obj, ar)

    def value2html(self, ar, v, **cellattrs):
        try:
            if E.iselement(v) and v.tag == 'div':
                return E.td(*[child for child in v], **cellattrs)
            return E.td(v, **cellattrs)
        except Exception as e:
            logger.error(e)
            return E.td(str(e), **cellattrs)

    def format_value(self, ar, v):
        from lino.utils.xmlgen.html import html2rst
        if etree.iselement(v):
            return html2rst(v)
        return self.field._lino_atomizer.format_value(ar, v)


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
        if not isinstance(self.layout_handle.layout, layouts.ColumnsLayout):
            if 'fieldLabel' in kw:
                del kw['fieldLabel']
            # kw.update(hideLabel=True)

            label = self.label

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
        kw.update(
            label=str(getattr(relobj.model._meta, 'verbose_name', None))
            or relobj.var_name)
        # DisplayElement.__init__(self,lh,relobj.field,**kw)

        # ~ kw.setdefault('value','<br/>') # see blog/2012/0527
        # kw.update(always_enabled=True)
        FieldElement.__init__(self, lh, relobj.field, **kw)
        # self.preferred_height = self.field.preferred_height
        # self.preferred_width = self.field.preferred_width
        # if self.field.max_length:
            # self.preferred_width = self.field.max_length

    def add_default_value(self, kw):
        pass


class GenericForeignKeyElement(DisplayElement):

    """
    A :class:`DisplayElement` specially adapted to a :term:`GFK` field.
    """

    def __init__(self, layout_handle, field, **kw):
        self.field = field
        self.editable = False
        kw.update(label=getattr(field, 'verbose_name', None) or field.name)
        # kw.update(label=field.verbose_name)
        LayoutElement.__init__(self, layout_handle, field.name, **kw)

    def add_default_value(self, kw):
        pass


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
        kw.update(items=js_code("new Ext.BoxComponent({autoScroll:true})"))
        if self.label:
            kw.update(title=self.label)
        return kw


class SlaveSummaryPanel(HtmlBoxElement):
    """The panel used to display a slave table whose `slave_grid_format`
is 'summary'.

    """
    def __init__(self, lh, actor, **kw):
        box = fields.HtmlBox(actor.label, help_text=actor.help_text)
        fld = fields.VirtualField(box, actor.get_slave_summary)
        fld.name = actor.__name__
        fld.lino_resolve_type()
        super(SlaveSummaryPanel, self).__init__(lh, fld, **kw)


class ManyRelatedObjectElement(HtmlBoxElement):

    def __init__(self, lh, relobj, **kw):
        name = relobj.field.rel.related_name

        def f(obj, ar):
            return qs2summary(ar, getattr(obj, name).all())

        box = fields.HtmlBox(name)
        fld = fields.VirtualField(box, f)
        fld.name = name
        fld.lino_resolve_type()
        super(ManyRelatedObjectElement, self).__init__(lh, fld, **kw)


class ManyToManyElement(HtmlBoxElement):

    def __init__(self, lh, relobj, **kw):
        name = relobj.field.name

        def f(obj, ar):
            return qs2summary(ar, getattr(obj, name).all())

        box = fields.HtmlBox(relobj.field.verbose_name)
        fld = fields.VirtualField(box, f)
        fld.name = name
        fld.lino_resolve_type()
        super(ManyToManyElement, self).__init__(lh, fld, **kw)


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
    label_align = layouts.LABEL_ALIGN_TOP

    declare_type = jsgen.DECLARE_VAR

    def __init__(self, layout_handle, name, *elements, **kw):
        self.active_children = []
        self.elements = elements
        if elements:
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
        children = []
        for e in self.elements:
            for chunk in e.as_plain_html(ar, obj):
                children.append(chunk)
        if self.vertical:
            # for ch in children:
                # yield ch
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
                cell = E.td(*tuple(e.as_plain_html(ar, obj)))
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
        # not necessary to filter elements here, jsgen does that
        kw.update(items=self.elements)
        # if all my children are hidden, i am myself hidden
        for e in self.elements:
            if e.is_visible():
                return kw
        kw.update(hidden=True)
        return kw

    def get_view_permission(self, profile):
        """A Panel which doesn't contain a single visible element becomes
        itself hidden.

        """
        # if the Panel itself is invisble, no need to loop through the
        # children
        if not super(Container, self).get_view_permission(profile):
            return False
        for e in self.elements:
            if (not isinstance(e, Permittable)) or \
               e.get_view_permission(profile):
                # one visible child is enough, no need to continue loop
                return True
            # if not isinstance(e, Permittable):
            #     return True
            # if isinstance(e, Panel) and \
            #    e.get_view_permission(profile):
            #     return True
        # logger.info("20120925 not a single visible element in %s of %s",self,self.layout_handle)
        return False


class Wrapper(VisibleComponent):

    """
    """
    # label = None

    def __init__(self, e, **kw):
        kw.update(layout='form')
        if not isinstance(e, TextFieldElement):
            kw.update(autoHeight=True)
        kw.update(labelAlign=e.parent.label_align)
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

    def get_view_permission(self, profile):
        return self.wrapped.get_view_permission(profile)

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

    def __init__(self, layout_handle, name, vertical, *elements, **kw):
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
                kw.update(layout='hbox', layoutConfig=dict(align='stretch'))

        for e in elements:
            if isinstance(e, FieldElement):
                self.is_fieldset = True
                if e.label:
                    w = len(e.label) + 1  # +1 for the ":"
                    if self.label_width < w:
                        self.label_width = w

        Container.__init__(self, layout_handle, name, *elements, **kw)

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
                # d.update(layout='form')
                if self.vflex:
                    d.update(layout='vbox', layoutConfig=dict(align='stretch'))
                else:
                    # 20100921b
                    # d.update(layout='form')
                    d.update(layout='form', autoHeight=True)
                    # d.update(layout='vbox',autoHeight=True)
            else:
                d.update(layout='hbox', autoHeight=True)  # 20101028

        if d['layout'] == 'form':
            assert self.vertical
            self.update(labelAlign=self.label_align)
            self.wrap_formlayout_elements()
            if len(self.elements) == 1 and self.elements[0].vflex:
                self.elements[0].update(anchor=FULLWIDTH + ' ' + FULLHEIGHT)
            else:
                for e in self.elements:
                    e.update(anchor=FULLWIDTH)

        elif d['layout'] == 'hbox':
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
                d.update(layoutConfig=dict(align='stretchmax'))

        elif d['layout'] == 'vbox':
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
                self.value_template = 'new Lino.VBorderPanel(%s)'
                for e in self.elements:
                    if e.vflex:
                        e.update(flex=e.height or e.preferred_height)
                    e.update(split=True)
                self.elements[0].update(region='north')
                self.elements[1].update(region='center')
                if len(self.elements) == 3:
                    self.elements[2].update(region='south')
        elif d['layout'] == 'fit':
            self.wrap_formlayout_elements()
        else:
            raise Exception("layout is %r" % d['layout'])

    def wrap_formlayout_elements(self):
        def wrap(e):
            if not isinstance(e, FieldElement):
                return e
            if e.label is None:
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

        if self.label:
            if not isinstance(self.parent, TabPanel):
                self.update(title=self.label)
                self.value_template = "new Ext.form.FieldSet(%s)"
                self.update(frame=False)
                self.update(bodyBorder=True)
                self.update(border=True)

        d = Container.ext_options(self, **d)

        # hide scrollbars
        d.update(autoScroll=False)

        if self.is_fieldset:
            d.update(labelWidth=self.label_width * EXT_CHAR_WIDTH)
        if self.parent is None or (len(self.elements) > 1 and self.vertical):
            """
            The `self.parent is None` test is e.g. for Parameter
            Panels which are usually not vertical but still want a frame
            since they are the main panel.
            """
            d.update(frame=True)
            d.update(bodyBorder=False)
            d.update(border=False)
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
    value_template = "new Lino.GridPanel(%s)"
    ext_suffix = "_grid"
    vflex = True
    xtype = None
    preferred_height = 5
    refers_to_ww = True

    def __init__(self, layout_handle, name, rpt, *columns, **kw):
        """:param layout_handle: the handle of the FormLayout owning this grid.

        :param rpt: the table being displayed
        (:class:`lino.core.tables.AbstractTable`)

        """
        # assert isinstance(rpt,dd.AbstractTable), "%r is not a Table!" % rpt
        self.value_template = "new Lino.%s.GridPanel(%%s)" % rpt
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

        kw.setdefault('label', rpt.label)
        if len(self.columns) == 1:
            kw.setdefault('hideHeaders', True)

        add_help_text(kw, rpt.help_text, rpt.title or rpt.label,
                      rpt.app_label, rpt.actor_id)

        # kw.update(containing_window=js_code("this.containing_window"))
        kw.update(containing_panel=js_code("this"))
        # if not rpt.show_params_at_render:
        if rpt.params_panel_hidden:
            kw.update(params_panel_hidden=True)
        Container.__init__(self, layout_handle, name, **kw)
        self.active_children = columns

    def get_view_permission(self, profile):
        # skip Container parent:
        if not super(Container, self).get_view_permission(profile):
            return False
        return self.actor.default_action.get_view_permission(profile)

    def ext_options(self, **kw):
        # not direct parent (Container), only LayoutElement
        kw = LayoutElement.ext_options(self, **kw)
        return kw

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


class DetailMainPanel(Panel):
    xtype = None
    value_template = "new Ext.Panel(%s)"

    def __init__(self, layout_handle, name, vertical, *elements, **kw):
        kw.update(autoScroll=True)
        Panel.__init__(self, layout_handle, name, vertical, *elements, **kw)

    def ext_options(self, **kw):
        kw = Panel.ext_options(self, **kw)
        if self.layout_handle.main.label:
            kw.update(title=_(self.layout_handle.main.label))
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
    holder = layout_handle.layout.get_chooser_holder()
    ch = holder.get_chooser_for_field(field.name)
    if ch:
        if ch.can_create_choice or not ch.force_selection:
            kw.update(forceSelection=False)
        if ch.simple_values:
            return SimpleRemoteComboFieldElement(layout_handle, field, **kw)
        else:
            if isinstance(field, models.OneToOneField):
                return GenericForeignKeyElement(layout_handle, field, **kw)
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
    if isinstance(selector_field, fields.VirtualField):
        selector_field = selector_field.return_type
    # remember the case of RemoteField to VirtualField

    if isinstance(selector_field, fields.CustomField):
        e = selector_field.create_layout_elem(layout_handle, field, **kw)
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
    pkw.update(labelAlign=kwargs.pop('label_align', 'top'))
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
        e = ManyToManyElement(lh, de.related, **kw)
        lh.add_store_field(e.field)
        return e

    if AFTER17:
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

    if isinstance(de, GenericForeignKey):
        # create a horizontal panel with 2 comboboxes
        de.primary_key = False  # for ext_store.Store()
        lh.add_store_field(de)
        return GenericForeignKeyElement(lh, de, **kw)

    if isinstance(de, type) and issubclass(de, tables.AbstractTable):
        # The data element refers to a slave table. Slave tables make
        # no sense in an insert window because the master does not yet
        # exist.
        kw.update(master_panel=js_code("this"))
        
        if isinstance(lh.layout, FormLayout):
            # When a table is specified in the layout of a
            # DetailWindow, then it will be rendered as a panel that
            # displays a "summary" of that table. The panel will have
            # a tool button to "open that table in its own
            # window". The format of that summary is defined by the
            # `slave_grid_format` of the table. `slave_grid_format` is
            # a string with one of the following values:

            kw.update(tools=[
                js_code("Lino.show_in_own_window_button(Lino.%s)" %
                      de.default_action.full_name())])
            if de.slave_grid_format == 'grid':
                kw.update(hide_top_toolbar=True)
                if de.preview_limit is not None:
                    kw.update(preview_limit=de.preview_limit)
                return GridElement(lh, name, de, **kw)

            elif de.slave_grid_format == 'html':
                if de.editable:
                    a = de.insert_action
                    if a is not None:
                        kw.update(ls_insert_handler=js_code("Lino.%s" %
                                  a.full_name()))
                        kw.update(ls_bbar_actions=[
                            settings.SITE.plugins.extjs.renderer.a2btn(a)])
                field = fields.HtmlBox(verbose_name=de.label)
                field.name = de.__name__
                field.help_text = de.help_text
                field._return_type_for_method = de.slave_as_html_meth()
                lh.add_store_field(field)
                e = HtmlBoxElement(lh, field, **kw)
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
    assert e.field is not None, "e.field is None for %s.%s" % (lh.layout, kw)
    lh.add_store_field(e.field)
    return e
