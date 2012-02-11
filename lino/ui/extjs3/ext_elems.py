# -*- coding: UTF-8 -*-
## Copyright 2009-2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

import logging
logger = logging.getLogger(__name__)

from cgi import escape

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from django.conf import settings

import lino

from lino import dd
from lino.core import table
from lino.core import fields
from lino.utils import constrain
from lino.utils import jsgen
from lino.utils import mti
from lino.utils.jsgen import py2js, Variable, Component, id2js, js_code
from lino.utils import choosers
#~ from . import ext_requests
from lino.ui import requests as ext_requests

EXT_CHAR_WIDTH = 9
EXT_CHAR_HEIGHT = 22

#~ DEFAULT_GC_NAME = 'std'
DEFAULT_GC_NAME = 0


def form_field_name(f):
    if isinstance(f,models.ForeignKey) \
        or (isinstance(f,models.Field) and f.choices) \
        or isinstance(f,dd.LinkedForeignKey):
        return f.name + ext_requests.CHOICES_HIDDEN_SUFFIX
    else:
        return f.name
        

def rpt2url(rpt):
    return '/' + rpt.app_label + '/' + rpt.__name__

def a2btn(a):
    return dict(
      opens_a_slave=a.opens_a_slave,
      handler=js_code("Lino.%s" % a),
      name=a.name,
      label=a.label, # 20111111
      #~ label=unicode(a.label),
      #~ url="/".join(("/ui",a.actor.app_label,a.actor._actor_name,a.name))
    )
      
def py2html(obj,name):
    for n in name.split('.'):
        obj = getattr(obj,n,"N/A")
    if callable(obj):
        obj = obj()
    if getattr(obj, '__iter__', False):
        obj = list(obj)
    return escape(unicode(obj))
    
def before_row_edit(panel):
    l = []
    #~ l.append("console.log('before_row_edit',record);")
    for e in panel.active_children:
        if isinstance(e,GridElement):
            l.append("%s.on_master_changed();" % e.as_ext())
        #~ elif isinstance(e,PictureElement):
            #~ l.append("this.load_picture_to(%s,record);" % e.as_ext())
        #~ elif isinstance(e,TextFieldElement):
            #~ if e.separate_window:
                #~ l.append("%s.refresh();" % e.as_ext())
        elif isinstance(e,HtmlBoxElement):
            l.append("%s.refresh();" % e.as_ext())
        elif isinstance(e,TextFieldElement):
            if e.format == 'html' and settings.LINO.use_tinymce:
                l.append("%s.refresh();" % e.as_ext())
        elif isinstance(e,FieldElement):
            chooser = choosers.get_for_field(e.field)
            if chooser:
                #~ logger.debug("20100615 %s.%s has chooser", self.layout_handle.layout, e.field.name)
                for f in chooser.context_fields:
                    #~ l.append("console.log('20110128 before_row_edit',record.data);")
                    l.append(
                        "%s.setContextValue(%r,record ? record.data[%r] : undefined);" % (
                        e.as_ext(),f.name,form_field_name(f)))
    #~ return js_code('function(record){\n  %s\n}' % ('\n  '.join(l)))
    #~ return js_code('function(record){ %s }' % (' '.join(l)))
    return l

class GridColumn(Component):
    declare_type = jsgen.DECLARE_INLINE
    
    def __init__(self,index,editor,**kw):
        """editor may be a Panel for columns on a GenericForeignKey
        """
        #~ print 20100515, editor.name, editor.__class__
        #~ assert isinstance(editor,FieldElement), \
            #~ "%s.%s is a %r (expected FieldElement instance)" % (cm.grid.report,editor.name,editor)
        #~ if isinstance(editor,BooleanFieldElement):
            #~ self.editor = None
        #~ else:
        self.editor = editor
        #~ self.value_template = editor.grid_column_template
        kw.update(sortable=True)
        #~ kw.update(submitValue=False) # 20110406
        kw.update(colIndex=index)
        kw.update(editor.get_column_options())
        kw.update(hidden=editor.hidden)
        if settings.LINO.use_filterRow:
            if editor.filter_type:
                if index == 0:
                    kw.update(clearFilter=True) # first column used to show clear filter icon in this column
                #~ else:
                    #~ print index, "is not 1"
                kw.update(filterInput=js_code('new Ext.form.TextField()'))
                kw.update(filterOptions=[
                  #~ dict(value='startwith', text='Start With'),
                  #~ dict(value='endwith', text='End With'),
                  dict(value='empty', text='Is empty'),
                  dict(value='notempty', text='Is not empty'),
                  dict(value='contains', text='Contains'),
                  dict(value='doesnotcontain', text='Does not contain')
                ])
              
        if settings.LINO.use_gridfilters and editor.gridfilters_settings:
                kw.update(filter=editor.gridfilters_settings)
        #~ if isinstance(editor,FieldElement) and editor.field.primary_key:
        if isinstance(editor,FieldElement):
            def fk_renderer(fld,name):
                rpt = fld.rel.to._lino_model_report
                if rpt.detail_action is not None:
                    return "Lino.fk_renderer('%s','Lino.%s')" % (
                      name + ext_requests.CHOICES_HIDDEN_SUFFIX,
                      rpt.detail_action)
              
            rend = None
            if isinstance(editor.field,models.AutoField):
                rend = 'Lino.id_renderer'
                #~ kw.update(renderer=js_code('Lino.id_renderer'))
            elif isinstance(editor.field,dd.DisplayField):
                rend = 'Lino.raw_renderer'
            elif isinstance(editor.field,models.TextField):
                rend = 'Lino.text_renderer'
            elif isinstance(editor.field,dd.LinkedForeignKey):
                rend = "Lino.lfk_renderer(this,'%s')" % \
                  (editor.field.name + ext_requests.CHOICES_HIDDEN_SUFFIX)
            elif isinstance(editor.field,models.ForeignKey):
                # FK fields are clickable if their target has a detail view
                rend = fk_renderer(editor.field,editor.field.name)
            elif isinstance(editor.field,fields.VirtualField) \
              and isinstance(editor.field.return_type,models.ForeignKey):
                # FK fields are clickable if their target has a detail view
                rend = fk_renderer(editor.field.return_type,editor.field.name)
            #~ elif isinstance(editor.field,dd.GenericForeignKeyIdField):
                #~ rend = "Lino.gfk_renderer()"
            if rend:
                kw.update(renderer=js_code(rend))
            kw.update(editable=editor.editable)
            #~ if editor.editable:
            if editor.editable and not isinstance(editor,BooleanFieldElement):
                kw.update(editor=editor)
        else:
            kw.update(editable=False)
        Component.__init__(self,editor.name,**kw)
    
        #~ if self.editable:
            #~ editor = self.get_field_options()
        
        
class Toolbar(Component):
    value_template = "new Ext.Toolbar(%s)"
class ComboBox(Component):
    value_template = 'new Ext.form.ComboBox(%s)'
class ExtPanel(Component): # todo: rename this to Panel, and Panel to PanelElement or sth else
    value_template = "new Ext.Panel(%s)"

class Calendar(Component): 
    value_template = "new Lino.CalendarPanel(%s)"
    
                    
        
        
class VisibleComponent(Component):
    vflex = False
    hflex = True
    width = None
    height = None
    preferred_width = 10
    preferred_height = 1
    #flex = None
    
    def __init__(self,name,
        width=None,height=None,label=None,preferred_width=None,
        **kw):
        Component.__init__(self,name,**kw)
        if preferred_width is not None:
            self.preferred_width = preferred_width
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if label is not None:
            self.label = label
        #~ if name == 'versions':
            #~ assert self.height is not None
            #~ logger.info("20120210 c __init__() %s" % self)
        #~ if flex is not None:
            #~ self.flex = flex
    

    def __str__(self):
        "This shows how elements are specified"
        name = Component.__str__(self)
        if self.width is None:
            return name
        if self.height is None:
            return name + ":%d" % self.width
        return name + ":%dx%d" % (self.width,self.height)
        
    def __repr__(self):
        return str(self)
        
    def pprint(self,level=0):
        return ("  " * level) + str(self)
        
    def walk(self):
        yield self
        
        
    def debug_lines(self):
        sep = u"</td><td>"
        cols = """ext_name name parent label __class__.__name__ 
        elements js_value
        labelAlign vertical width preferred_width height 
        preferred_height vflex""".split()
        yield '<tr><td>' + sep.join(cols) + '</td></tr>'
        for e in self.walk():
            yield '<tr><td>'+sep.join([py2html(e,n) for n in cols]) +'</td></tr>'
            
    def unused_has_field(self,fld):
        for de in self.walk():
            if isinstance(de,FieldElement) and de.field is fld:
                return True
        return False
        
        
class LayoutElement(VisibleComponent):
    stored = False
    ext_name = None
    ext_suffix = ""
    #~ data_type = None 
    filter_type = None
    gridfilters_settings = None
    parent = None # will be set by Container
    
    label = None
    label_width = 0 
    editable = False
    sortable = False
    xtype = None # set by subclasses
    #~ grid_column_template = "new Ext.grid.Column(%s)"
    collapsible = False
    hidden = False
    active_child = True
    refers_to_ww = False
    
    def __init__(self,layout_handle,name,**kw):
        #logger.debug("LayoutElement.__init__(%r,%r)", layout_handle.layout,name)
        #self.parent = parent
        #~ name = layout_handle.layout._actor_name + '_' + name
        VisibleComponent.__init__(self,name,**kw)
        self.layout_handle = layout_handle
        #~ if layout_handle is not None:
        assert isinstance(layout_handle,table.LayoutHandle)
        #~ layout_handle.setup_element(self)

    #~ def submit_fields(self):
        #~ return []
        
    def update_config(self,wc):
        pass
        
    def get_property(self,name):
        v = getattr(self,name,None)
        if self.parent is None or v is not None:
            return v
        return self.parent.get_property(name)
        
    def get_column_options(self,**kw):
        return kw
        
    def set_parent(self,parent):
        #~ if self.parent is not None:
            #~ raise Exception("%s : parent is already %s, cannot set it to %s" % (self,self.parent,parent))
        self.parent = parent
        #~ if isinstance(parent,FieldSetPanel):
            #~ self.label = None
            #~ self.update(label = None)
        if self.label and isinstance(parent,Panel):
            if parent.labelAlign == table.LABEL_ALIGN_LEFT:
                self.preferred_width += len(self.label)

    def ext_options(self,**kw):
        kw = VisibleComponent.ext_options(self,**kw)
        if self.xtype is not None:
            kw.update(xtype=self.xtype)
        if self.collapsible:
            kw.update(collapsible=True)
        return kw



class ConstantElement(LayoutElement):
    declare_type = jsgen.DECLARE_INLINE
    #declare_type = jsgen.DECLARE_THIS
    #~ declare_type = jsgen.DECLARE_VAR
    xtype = 'label'
    vflex = True
    
    def __init__(self,lh,fld,**kw):
        kw.update(html=fld.text)
        #~ kw.update(autoHeight=True)
        LayoutElement.__init__(self,lh,fld.name,**kw)
        #~ self.text = text

    #~ def ext_options(self,**kw):
        #~ kw = LayoutElement.ext_options(self,**kw)
        #~ kw.update(html=self.text.text)
        #~ return kw
        
        
        

class Spacer(LayoutElement):
    declare_type = jsgen.DECLARE_INLINE
    #xtype = 'label'
    value_template = "new Ext.Spacer(%s)"
    
        
        
        
class FieldElement(LayoutElement):
    #~ declare_type = jsgen.DECLARE_INLINE
    #~ declare_type = jsgen.DECLARE_THIS
    declare_type = jsgen.DECLARE_VAR
    stored = True
    filter_type = None # 'auto'
    active_change_event = 'change'
    #declaration_order = 3
    #~ ext_suffix = "_field"
    
    def __init__(self,layout_handle,field,**kw):
        if not hasattr(field,'name'):
            raise Exception("Field %s.%s has no name!" % (layout_handle,field))
        assert field.name, Exception("field %r has no name!" % field)
        self.field = field
        self.editable = field.editable # and not field.primary_key
        
        #~ help_text = getattr(self.field,'help_text',None):
        if self.field.help_text:
            #~ kw.update(qtip=self.field.help_text)
            #~ kw.update(toolTipText=self.field.help_text)
            #~ kw.update(tooltip=self.field.help_text)
            kw.update(listeners=dict(render=js_code("Lino.quicktip_renderer(%s)" % py2js(self.field.help_text)))
            )
            

        #~ http://www.rowlands-bcs.com/extjs/tips/tooltips-form-fields
        #~ if self.field.__doc__:
            #~ kw.update(toolTipText=self.field.__doc__)
        kw.setdefault('label',field.verbose_name)
        self.add_default_value(kw)
        #~ kw.update(label=field.verbose_name) 
        LayoutElement.__init__(self,layout_handle,field.name,**kw)

    def cell_html(self,ui,row):
        return getattr(row,self.field.name)
            
    def get_column_options(self,**kw):
        #~ raise "get_column_options() %s" % self.__class__
        #~ kw.update(xtype='gridcolumn')
        kw.update(dataIndex=self.field.name)
        #~ if self.label is None:
            #~ kw.update(header=self.field.name)
        #~ else:
        #~ kw.update(header=unicode(self.label or self.name))
        kw.update(header=self.label or self.name)
        if not self.editable:
            kw.update(editable=False)
        if not self.sortable:
            kw.update(sortable=False)
        w = self.width or self.preferred_width
        kw.update(width=w*EXT_CHAR_WIDTH)
        return kw    
        
        
    #~ def submit_fields(self):
        #~ return [self.field.name]
    def add_default_value(self,kw):
        if self.field.has_default():
            dv = self.field.default
            if callable(dv):
                dv = dv()
            kw.update(value=dv)
            
        
    def get_field_options(self,**kw):
        if self.xtype:
            kw.update(xtype=self.xtype)
        
        # When used as editor of an EditorGridPanel, don't set the name attribute
        # because it is not needed for grids and might conflict with fields of a 
        # surronding detail form. See ticket #38 (:doc:`/blog/2011/0408`).
        if not isinstance(self.layout_handle.layout,table.ListLayout):
            kw.update(name=self.field.name)
            if self.label:
                #~ kw.update(fieldLabel=unicode(self.label)) 20111111
                kw.update(fieldLabel=self.label)
        if self.editable:
            if not self.field.blank:
                kw.update(allowBlank=False)
        else:
            kw.update(disabled=True)
            kw.update(readOnly=True)
        return kw
        
    def ext_options(self,**kw):
        kw = LayoutElement.ext_options(self,**kw)
        kw.update(self.get_field_options())
        return kw
    
        
class TextFieldElement(FieldElement):
    #~ xtype = 'textarea'
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
    def __init__(self,layout_handle,field,**kw):
        self.format = getattr(field,'textfield_format',None) \
            or settings.LINO.textfield_format
        if self.format == 'html':
            if settings.LINO.use_tinymce:
                self.value_template = "new Lino.RichTextPanel(%s)"
                self.active_child = True
                #~ if self.label:
                    #~ kw.update(title=unicode(self.label))
                self.separate_window = True
                # we don't call FieldElement.__init__ but do almost the same:
                self.field = field
                self.editable = field.editable # and not field.primary_key
                #~ 20111126 kw.update(ls_url=rpt2url(layout_handle.rh.report))
                #~ kw.update(master_panel=js_code("this"))
                kw.update(containing_panel=js_code("this"))
                #~ kw.update(title=unicode(field.verbose_name)) 20111111
                kw.update(title=field.verbose_name)
                #~ kw.update(tinymce_options=dict(
                    #~ template_external_list_url=layout_handle.ui.build_url('templates',layout_handle.rh.report.app_label,layout_handle.rh.report.name)
                  #~ template_templates=[
                    #~ dict(title="Editor Details",
                        #~ src="editor_details.htm",
                        #~ description="Adds Editor Name and Staff ID")]
                #~ ))
                #~ LayoutElement.__init__(self,layout_handle,varname_field(field),label=unicode(field.verbose_name),**kw)
                #~ LayoutElement.__init__(self,layout_handle,field.name,label=unicode(field.verbose_name),**kw)
                return LayoutElement.__init__(self,layout_handle,field.name,**kw)
            else:
                self.value_template = "new Ext.form.HtmlEditor(%s)"
                if settings.LINO.use_vinylfox:
                    kw.update(plugins=js_code('Lino.VinylFoxPlugins()'))
        elif self.format == 'plain':
            kw.update(
              growMax=2000,
              #~ defaultAutoCreate = dict(
                #~ tag="textarea",
                #~ autocomplete="off"
              #~ )
            )
        else:
            raise Exception(
                "Invalid textfield format %r for field %s.%s" % (
                self.format,field.model.__name__,field.name))
        FieldElement.__init__(self,layout_handle,field,**kw)
        
class CharFieldElement(FieldElement):
    filter_type = 'string'
    gridfilters_settings = dict(type='string')
    value_template = "new Ext.form.TextField(%s)"
    sortable = True
    xtype = None
  
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        self.preferred_width = min(20,max(3,self.field.max_length))
            
    def get_field_options(self,**kw):
        kw = FieldElement.get_field_options(self,**kw)
        kw.update(maxLength=self.field.max_length)
        return kw
        
        
class PasswordFieldElement(CharFieldElement):
    def get_field_options(self,**kw):
        kw = super(PasswordFieldElement,self).get_field_options(**kw)
        kw.update(inputType='password')
        return kw
    
class FileFieldElement(CharFieldElement):
    #~ xtype = 'fileuploadfield'
    #~ value_template = "new Lino.FileField(%s)"
    value_template = "Lino.file_field_handler(this,%s)"
    #~ value_template = "%s"
    
    #~ def __init__(self,layout_handle,*args,**kw):
        #~ CharFieldElement.__init__(self,layout_handle,*args,**kw)
        #~ layout_handle.has_upload = True
        
    #~ def get_field_options(self,**kw):
        #~ kw = CharFieldElement.get_field_options(self,**kw)
        #~ kw.update(emptyText=_('Select a document to upload...'))
        #~ # kw.update(buttonCfg=dict(iconCls='upload-icon'))
        #~ return kw
    
class ComboFieldElement(FieldElement):
    #~ value_template = "new Ext.form.ComboBox(%s)"        
    sortable = True
    xtype = None
    filter_type = 'string'
    gridfilters_settings = dict(type='string')
    
    def get_field_options(self,**kw):
        kw = FieldElement.get_field_options(self,**kw)
        # When used as editor of an EditorGridPanel, don't set the name attribute
        # because it is not needed for grids and might conflict with fields of a 
        # surronding detail form. See ticket #38 (:doc:`/blog/2011/0408`).
        # Also, Comboboxes with simple values may never have a hiddenName option.
        if not isinstance(self.layout_handle.layout,table.ListLayout) \
            and not isinstance(self,SimpleRemoteComboFieldElement):
            kw.update(hiddenName=self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX)
        return kw
      
class ChoicesFieldElement(ComboFieldElement):
    value_template = "new Lino.ChoicesFieldElement(%s)"
  
    #~ def __init__(self,*args,**kw):
        #~ self.preferred_width = 20
        #~ FieldElement.__init__(self,*args,**kw)
        
    def get_field_options(self,**kw):
        kw = ComboFieldElement.get_field_options(self,**kw)
        kw.update(store=self.field.choices)
        #~ kw.update(hiddenName=self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX)
        return kw
        

class RemoteComboFieldElement(ComboFieldElement):
    value_template = "new Lino.RemoteComboFieldElement(%s)"
  
    def store_options(self,**kw):
        #~ kw.update(baseParams=js_code('this.get_base_params()')) # 20120202
        if self.editable:
            url = self.layout_handle.ui.build_url("choices",
                #~ self.layout_handle.layout.table.model._meta.app_label,
                #~ self.layout_handle.layout.table.model.__name__,
                self.layout_handle.layout.table.app_label,
                self.layout_handle.layout.table.__name__,
                self.field.name,**kw)
            proxy = dict(url=url,method='GET')
            kw.update(proxy=js_code("new Ext.data.HttpProxy(%s)" % py2js(proxy)))
        # a JsonStore without explicit proxy sometimes used method POST
        return kw
      
    def get_field_options(self,**kw):
        kw = ComboFieldElement.get_field_options(self,**kw)
        sto = self.store_options()
        #print repr(sto)
        kw.update(store=js_code("new Lino.ComplexRemoteComboStore(%s)" % py2js(sto)))
        return kw
        
class SimpleRemoteComboFieldElement(RemoteComboFieldElement):
    value_template = "new Lino.SimpleRemoteComboFieldElement(%s)"
    #~ def get_field_options(self,**kw):
        #~ todo : store
        #~ # Do never add a hiddenName
        #~ return FieldElement.get_field_options(self,**kw)
    
  
class ComplexRemoteComboFieldElement(RemoteComboFieldElement):
    #~ value_template = "new Lino.ComplexRemoteComboFieldElement(%s)"
        
    def unused_get_field_options(self,**kw):
        kw = RemoteComboFieldElement.get_field_options(self,**kw)
        kw.update(hiddenName=self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX)
        return kw
        
        
class LinkedForeignKeyElement(ComplexRemoteComboFieldElement):
    pass
  
class ForeignKeyElement(ComplexRemoteComboFieldElement):
    
    def __init__(self,layout_handle,field,**kw):
    #~ def __init__(self,*args,**kw):
        #~ print 20100903,repr(self.field.rel.to)
        #~ assert issubclass(self.field.rel.to,models.Model), "%r is not a model" % self.field.rel.to
        pw = getattr(field.rel.to,'_lino_preferred_width',None)
        if pw is not None:
            kw.setdefault('preferred_width',pw)
            #~ kw.update(preferred_width=pw)
        self.report = table.get_model_report(field.rel.to)
        a = self.report.detail_action
        if a is not None:
            if not isinstance(layout_handle.layout,table.ListLayout):
                self.value_template = "new Lino.TwinCombo(%s)"
                kw.update(onTrigger2Click=js_code(
                    "function(){ Lino.show_fk_detail(this,Lino.%s)}" % a))
        FieldElement.__init__(self,layout_handle,field,**kw)
      
    #~ def submit_fields(self):
        #~ return [self.field.name,self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX]
        
        
    def get_field_options(self,**kw):
        kw = super(ForeignKeyElement,self).get_field_options(**kw)
        kw.update(pageSize=self.report.page_length)
        kw.update(emptyText=_('Select a %s...') % self.report.model._meta.verbose_name)
        return kw

    def cell_html(self,ui,row):
        obj = getattr(row,self.field.name)
        if obj is None:
            return ''
        return ui.href_to(obj)


class TimeFieldElement(FieldElement):
    value_template = "new Lino.TimeField(%s)"
    #~ xtype = 'timefield'
    #~ data_type = 'time' # for store column
    sortable = True
    preferred_width = 8
    #~ filter_type = 'time'
    
  
class DateTimeFieldElement(FieldElement):
    #~ value_template = "new Lino.DateTimeField(%s)"
    value_template = "new Ext.form.DisplayField(%s)"
    #~ data_type = 'date' # for store column
    sortable = True
    preferred_width = 16
    #~ filter_type = 'date'
    
    def __init__(self,layout_handle,field,**kw):
        if self.editable:
            self.value_template = "new Lino.DateTimeField(%s)"
        else:
            kw.update(value="<br>")
        FieldElement.__init__(self,layout_handle,field,**kw)
    
class DateFieldElement(FieldElement):
    value_template = "new Lino.DateField(%s)"
    #~ xtype = 'datefield'
    #~ data_type = 'date' # for store column
    sortable = True
    preferred_width = 8
    filter_type = 'date'
    gridfilters_settings = dict(type='date',dateFormat=settings.LINO.date_format_extjs)
    # todo: DateFieldElement.preferred_width should be computed from Report.date_format
    #~ grid_column_template = "new Ext.grid.DateColumn(%s)"
    
    #~ def get_field_options(self,**kw):
        #~ kw = FieldElement.get_field_options(self,**kw)
        #~ kw.update(format=self.layout_handle.rh.report.date_format)
        #~ return kw
        
    def get_column_options(self,**kw):
        kw = FieldElement.get_column_options(self,**kw)
        kw.update(xtype='datecolumn')
        #~ kw.update(format=self.layout_handle.rh.report.date_format)
        kw.update(format=settings.LINO.date_format_extjs)
        return kw
    
class MonthFieldElement(DateFieldElement):
    def get_field_options(self,**kw):
        kw = DateFieldElement.get_field_options(self,**kw)
        kw.update(format='m/Y')
        kw.update(plugins='monthPickerPlugin')
        return kw
        
    
class URLFieldElement(CharFieldElement):
    sortable = True
    preferred_width = 40
    value_template = "new Lino.URLField(%s)"
    
    #~ def get_field_options(self,**kw):
        #~ kw = FieldElement.get_field_options(self,**kw)
        #~ kw.update(vtype='url') #,vtypeText=
        #~ return kw
        
    
class IntegerFieldElement(FieldElement):
    filter_type = 'numeric'
    gridfilters_settings = dict(type='numeric')
    xtype = 'numberfield'
    sortable = True
    preferred_width = 5
    #~ data_type = 'int' 

class IncompleteDateFieldElement(CharFieldElement):
    preferred_width = 10
    value_template = "new Lino.IncompleteDateField(%s)"
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        
    def get_field_options(self,**kw):
        kw = FieldElement.get_field_options(self,**kw)
        kw.update(maxLength=10)
        return kw
        


class DecimalFieldElement(FieldElement):
    filter_type = 'numeric'
    gridfilters_settings = dict(type='numeric')
    xtype = 'numberfield'
    sortable = True
    #~ data_type = 'float' 
    #~ grid_column_template = "new Ext.grid.NumberColumn(%s)"
    
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        self.preferred_width = min(5,self.field.max_digits) \
                + self.field.decimal_places
                
    def get_field_options(self,**kw):
        kw = FieldElement.get_field_options(self,**kw)
        if self.field.decimal_places:
            kw.update(decimalPrecision=self.field.decimal_places)
            kw.update(decimalSeparator=settings.LINO.decimal_separator)
        else:
            kw.update(allowDecimals=False)
        return kw
        
    def get_column_options(self,**kw):
        kw = FieldElement.get_column_options(self,**kw)
        kw.update(xtype='numbercolumn')
        kw.update(align='right')
        if settings.LINO.decimal_separator == ',':
            fmt = "0.000"
            if self.field.decimal_places > 0:
                fmt += ',' + ("0" * self.field.decimal_places)
                fmt += "/i"
        elif settings.LINO.decimal_separator == '.':
            fmt = "0,000"
            if self.field.decimal_places > 0:
                fmt += '.' + ("0" * self.field.decimal_places)
        kw.update(format=fmt)
        return kw
        
class DisplayElement(FieldElement):
    preferred_width = 30
    preferred_height = 3
    ext_suffix = "_disp"
    #~ declare_type = jsgen.DECLARE_THIS
    declare_type = jsgen.DECLARE_VAR
    value_template = "new Ext.form.DisplayField(%s)"
    
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        if self.field.max_length:
            self.preferred_width = self.field.max_length
    
class BooleanDisplayElement(DisplayElement):
    preferred_width = 20
    preferred_height = 1
    
                
class BooleanFieldElement(FieldElement):
  
    value_template = "new Ext.form.Checkbox(%s)"
    #~ xtype = 'checkbox'
    #~ data_type = 'boolean' 
    filter_type = 'boolean'
    gridfilters_settings = dict(type='boolean')
    #~ grid_column_template = "new Ext.grid.BooleanColumn(%s)"
    #~ def __init__(self,*args,**kw):
        #~ FieldElement.__init__(self,*args,**kw)
    #~ active_change_event = 'check'
        
    def set_parent(self,parent):
        FieldElement.set_parent(self,parent)
        #~ if isinstance(parent,Panel) and parent.hideCheckBoxLabels:
        if parent.hideCheckBoxLabels:
            self.update(hideLabel=True)
            
    def add_default_value(self,kw):
        if self.field.has_default():
            dv = self.field.default
            if callable(dv):
                dv = dv()
            kw.update(checked=dv)
            #~ self.remove('value')

    def get_field_options(self,**kw):
        kw = FieldElement.get_field_options(self,**kw)
        if not isinstance(self.layout_handle.layout,table.ListLayout):
            if kw.has_key('fieldLabel'):
                del kw['fieldLabel']
            #~ kw.update(hideLabel=True)
            
            label = self.label
            #~ if isinstance(self.field,mti.EnableChild):
                #~ m = self.field.child_model
                #~ url = self.layout_handle.rh.ui.build_url('api',m._meta.app_label,m.__name__)
                #~ js = "Lino.show_mti_child('%s','%s')" % (self.field.name,url)
                #~ label += """ (<a href="javascript:%s">%s</a>)""" % (js,_("show"))
            if isinstance(self.field,mti.EnableChild):
                rpt = self.field.child_model._lino_model_report
                if rpt.detail_action is not None:
                    js = "Lino.show_mti_child('%s',Lino.%s)" % (
                      self.field.name,
                      rpt.detail_action)
                    label += """ (<a href="javascript:%s">%s</a>)""" % (
                      js,_("show"))
                
        #~ self.verbose_name = \
            #~ 'is a <a href="javascript:Lino.enable_child_label()">%s</a>' % self.field.child_model.__name__
            #~ 'is a <a href="foo">[%s]</a>' % self.child_model._meta.verbose_name
                
            kw.update(boxLabel=label)
        
        return kw
        
    def get_column_options(self,**kw):
        kw = FieldElement.get_column_options(self,**kw)
        kw.update(xtype='checkcolumn')
        return kw
        
    def get_from_form(self,instance,values):
        """
        standard HTML submits checkboxes of a form only when they are checked.
        So if the field is not contained in values, we take False as value.
        """
        instance[self.field.name] = values.get(self.field.name,False)



class GenericForeignKeyElement(DisplayElement):
    """
    A :class:`DisplayElement` specially adapted to a :term:`GFK` field.
    """
    def __init__(self,layout_handle,field,**kw):
        #~ if not hasattr(field,'name'):
            #~ raise Exception("Field %s.%s has no name!" % (layout_handle.rh.report,field))
        #~ assert field.name, Exception("field %r has no name!" % field)
        self.field = field
        self.editable = False
        kw.update(label=getattr(field,'verbose_name',None) or field.name)
        #~ kw.update(label=field.verbose_name) 
        LayoutElement.__init__(self,layout_handle,field.name,**kw)
  
    def add_default_value(self,kw):
        pass
    
    
class HtmlBoxElement(DisplayElement):
    ext_suffix = "_htmlbox"
    #~ declare_type = jsgen.DECLARE_VAR
    value_template = "new Lino.HtmlBoxPanel(%s)"
    preferred_height = 5
    vflex = True
    filter_type = 'string'
    gridfilters_settings = dict(type='string')
    refers_to_ww = True
    
    #~ def __init__(self,layout_handle,name,action,**kw):
        #~ kw.update(plugins=js_code('Lino.HtmlBoxPlugin'))
        #~ LayoutElement.__init__(self,layout_handle,name,**kw)
        
    def get_field_options(self,**kw):
        kw.update(master_panel=js_code("this"))
        kw.update(name=self.field.name)
        kw.update(containing_panel=js_code("this"))
        kw.update(layout='fit')
        kw.update(autoScroll=True)
        
        # hide horizontal scrollbar      
        # for this trick thanks to Vladimir 
        # <http://forums.ext.net/showthread.php?1513-CLOSED-Autoscroll-on-ext-panel>
        kw.update(bodyStyle="overflow-x:hidden !important;")
        
        #~ if self.field.drop_zone: # testing with drop_zone 'FooBar'
            #~ kw.update(listeners=dict(render=js_code('initialize%sDropZone' % self.field.drop_zone)))
        kw.update(items=js_code("new Ext.BoxComponent()"))
        if self.label:
            #~ kw.update(title=unicode(self.label)) 20111111
            kw.update(title=self.label)
        #~ if self.field.bbar is not None:
            #~ kw.update(ls_bbar_actions=self.field.bbar)
        return kw
        


class Container(LayoutElement):
    vertical = False
    hpad = 1
    is_fieldset = False
    #~ xtype = 'container'
    value_template = "new Ext.Container(%s)"
    #~ hideCheckBoxLabels = True
    
    #declare_type = jsgen.DECLARE_INLINE
    declare_type = jsgen.DECLARE_VAR
    #~ declare_type = jsgen.DECLARE_THIS
    #~ declare_type = jsgen.DECLARE_THIS
    
    
    def __init__(self,layout_handle,name,*elements,**kw):
        self.has_frame = layout_handle.layout.has_frame
        self.labelAlign = layout_handle.layout.label_align
        self.hideCheckBoxLabels = layout_handle.layout.hideCheckBoxLabels
        self.active_children = []
        self.elements = elements
        if elements:
            #~ self.has_fields = False
            for e in elements:
                e.set_parent(self)
                #~ if isinstance(e,FieldElement):
                    #~ self.has_fields = True
                if not isinstance(e,LayoutElement):
                    raise Exception("%r is not a LayoutElement" % e)
                if e.active_child:
                    self.active_children.append(e)
                elif isinstance(e,Panel):
                    self.active_children += e.active_children
                    #~ self.has_fields = True
            #~ kw.update(items=elements)
                
        LayoutElement.__init__(self,layout_handle,name,**kw)
        
        
    def subvars(self):
        return self.elements
            
    def walk(self):
        for e in self.elements:
            for el in e.walk():
                yield el
        yield self
        
    def find_by_name(self,name):
        for e in self.walk():
            if e.name == name:
                return e
        

    def pprint(self,level=0):
        margin = "  " * level
        s = margin + str(self) + ":\n"
        # self.__class__.__name__
        for e in self.elements:
            for ln in e.pprint(level+1).splitlines():
                s += ln + "\n"
        return s

    def ext_options(self,**kw):
        kw = LayoutElement.ext_options(self,**kw)
        kw.update(items=self.elements)
        return kw

class Wrapper(VisibleComponent):
    def __init__(self,e,**kw):
        kw.update(layout='form')
        if not isinstance(e,TextFieldElement):
            kw.update(autoHeight=True)
        kw.update(labelAlign=e.parent.labelAlign)
        kw.update(items=e,xtype='panel')
        VisibleComponent.__init__(self,e.name+"_ct",**kw)
        self.wrapped = e
        for n in ('width', 'height', 'preferred_width','preferred_height','vflex'):
            setattr(self,n,getattr(e,n))
        #~ e.update(anchor="100%")
        if e.vflex: 
            e.update(anchor="100% 100%")
        else:
            e.update(anchor="100%")
            
    def walk(self):
        for e in self.wrapped.walk():
            yield e
        yield self

class Panel(Container):
    """
    A vertical Panel is vflex if and only if at least one of its children is vflex.
    A horizontal Panel is vflex if and only if *all* its children are vflex 
    (if vflex and non-vflex elements are together in a hbox, then the 
    vflex elements will get the height of the highest non-vflex element).
    """
    ext_suffix = "_panel"
    active_child = False
    #~ declare_type = jsgen.DECLARE_VAR
    #~ value_template = "new Ext.Panel(%s)"
    
    def __init__(self,layout_handle,name,vertical,*elements,**kw):
        self.vertical = vertical
            
        #~ if self.vertical:
            #~ vflex_elems = [e for e in elements if e.vflex]
            #~ if len(flex_elems) > 0:
                #~ assert len(kw) == 0, "%r is not empty" % kw
                #~ vfix_elems = [e for e in elements if not e.vflex]
                #~ flex_panel = Panel(layout_handle,name,vertical,*vflex_elems)
                #~ fix_panel = Panel(layout_handle,name,vertical,*vfix_elems)
                
        self.vflex = not vertical
        stretch = False
        #~ monitorResize = False
        for e in elements:
            #~ if e.collapsible:
                #~ monitorResize = True
            if e.vflex:
                stretch = True
            if self.vertical:
                if e.vflex:
                    self.vflex = True
            else:
                if not e.vflex:
                    self.vflex = False
                    #~ print 20100615, self.layout_handle.layout, self, "hbox loses vflex because of", e
        if len(elements) > 1 and self.vflex:
            if self.vertical:
                """
                Example : The panel contains a mixture of fields and grids. 
                Fields are not vflex, grids well.
                """
                #~ print 20100615, self.layout_handle, self
                # so we must split this panel into several containers.
                # vflex elements go into a vbox, the others into a form layout. 
                
                if False:
                    # Rearrange elements into "element groups"
                    # Each element of egroups is a list of elements who have same vflex
                    egroups = []
                    for e in elements:
                        if len(egroups) and egroups[-1][0].vflex == e.vflex:
                            egroups[-1].append(e)
                        else:
                            egroups.append([e])
                            
                    if len(egroups) == 1:
                        # all elements have same vflex
                        assert tuple(egroups[0]) == elements, "%r != %r" % (tuple(egroups[0]), elements)
                        
                    elements = []
                    for eg in egroups:
                        if eg[0].vflex:
                            #~ for e in eg: e.update(flex=1,align='stretch')
                            for e in eg: 
                                e.update(flex=1)
                                e.collapsible = True
                                #~ e.update(collapsible=True)
                            if len(eg) == 1:
                                g = eg[0]
                            else:
                                #~ g = Container(layout_handle,name,*eg,**dict(layout='vbox',flex=1)
                                g = Panel(layout_handle,name,vertical,*eg,**dict(layout='vbox',
                                  flex=1,layoutConfig=dict(align='stretch')))
                                assert g.vflex is True
                        else:
                            #~ for e in eg: e.update(align='stretch')
                            if len(eg) == 1:
                                g = eg[0]
                            else:
                                g = Container(layout_handle,name,*eg,**dict(layout='form',autoHeight=True))
                                #~ g = Container(layout_handle,name,*eg,**dict(layout='form'))
                                assert g.vflex is False
                        #~ if monitorResize:
                            #~ g.update(monitorResize=True)
                        #~ g.update(align='stretch')
                        #~ g.update(layoutConfig=dict(align='stretch'))
                        elements.append(g)
                    kw.update(layout='vbox',layoutConfig=dict(align='stretch'))
                    #~ self.elements = elements
            else: # not self.vertical
                kw.update(layout='hbox',layoutConfig=dict(align='stretch'))
              
        for e in elements:
            #~ e.set_parent(self)
            if isinstance(e,FieldElement):
                self.is_fieldset = True
                #~ if self.label_width < e.label_width:
                    #~ self.label_width = e.label_width
                if e.label:
                    w = len(e.label) + 1 # +1 for the ":"
                    if self.label_width < w:
                        self.label_width = w


        label = layout_handle.layout.collapsible_elements.get(name,None)
        if label:
            self.collapsible = True
            self.label = label

        Container.__init__(self,layout_handle,name,*elements,**kw)

        w = h = 0
        has_height = False # 20120210
        for e in self.elements:
            ew = e.width or e.preferred_width
            eh = e.height or e.preferred_height
            if self.vertical:
                #~ h += e.flex
                h += eh
                w = max(w,ew)
            else:
                if e.height:
                    has_height = True
                #w += e.flex
                w += ew
                h = max(h,eh)
        if has_height:
            self.height = h
            self.vflex = True
        else:
            self.preferred_height = h
        self.preferred_width = w
        assert self.preferred_height > 0, "%s : preferred_height is 0" % self
        assert self.preferred_width > 0, "%s : preferred_width is 0" % self
        
        d = self.value
        if not d.has_key('layout'):
            if len(self.elements) == 1:
                d.update(layout='fit')
            elif self.vertical:
                #~ d.update(layout='form')
                if self.vflex:
                    d.update(layout='vbox',layoutConfig=dict(align='stretch'))
                else:
                    # 20100921b
                    #~ d.update(layout='form')
                    d.update(layout='form',autoHeight=True)
                    #~ d.update(layout='vbox',autoHeight=True)
            else:
                d.update(layout='hbox',autoHeight=True) # 20101028
                
        if d['layout'] == 'form':
            assert self.vertical
            self.update(labelAlign=self.labelAlign)
            self.wrap_formlayout_elements()
            #~ d.update(autoHeight=True)
            if len(self.elements) == 1 and self.elements[0].vflex:
                self.elements[0].update(anchor="100% 100%")
            else:
                for e in self.elements:
                    e.update(anchor="100%")
                
        elif d['layout'] == 'hbox':
                
            #~ if self.as_ext() == 'main_1_panel187':
                #~ logger.info("20120210 b main_1_panel187 : %r",[repr(e) for e in self.elements])
            
            self.wrap_formlayout_elements()
            for e in self.elements:
                """
                20120210
                a hbox having at least one child with explicit height 
                will become itself vflex
                """        
                if e.height:
                    #~ logger.info("20120210 %s becomes vflex because %s has height",self,e)
                    self.vflex = True
                  
                if e.hflex:
                    w = e.width or e.preferred_width
                    #~ e.value.update(columnWidth=float(w)/self.preferred_width) # 20100615
                    e.value.update(flex=int(w*100/self.preferred_width))
                    
            if not self.vflex: # 20101028
                d.update(autoHeight=True)
                d.update(layoutConfig=dict(align='stretchmax'))
                
              
        elif d['layout'] == 'vbox':
            "a vbox with 2 or 3 elements, of which at least two are vflex will be implemented as a VBorderPanel"
            assert len(self.elements) > 1
            self.wrap_formlayout_elements()
            vflex_count = 0
            h = self.height or self.preferred_height
            for e in self.elements:
                eh = e.height or e.preferred_height
                if e.vflex:
                    e.update(flex=int(eh*100/h))
                    vflex_count += 1
            if vflex_count >= 2 and len(self.elements) <= 3:
            #~ if vflex_count >= 1 and len(self.elements) <= 3:
                self.remove('layout','layoutConfig')
                self.value_template = 'new Lino.VBorderPanel(%s)'
                for e in self.elements:
                    #~ if self.ext_name == 'main_panel627':
                        #~ print 20110715, e.height, e.preferred_height
                    #~ if e.vflex: # """as long as there are bugs, make also non-vflex resizable"""
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
            raise Exception("layout is %r" % d['layout'] )
        
    def wrap_formlayout_elements(self):
        #~ if layout_handle.main_class is DetailMainPanel:
        def wrap(e):
            #~ if isinstance(e,Panel): return e
            if not isinstance(e,FieldElement): return e
            if e.label is None: return e
            if isinstance(e,HtmlBoxElement): return e
            if settings.LINO.use_tinymce:
                if isinstance(e,TextFieldElement) and e.format == 'html': 
                    # no need to wrap them since they are Panels
                    return e
            return Wrapper(e)
        self.elements = [wrap(e) for e in self.elements]
          
        
    def ext_options(self,**d):
        d = Container.ext_options(self,**d)
        #~ if self.collapsible:
            #~ d.update(xtype='panel')
            #~ js = "function(cmp,aw,ah,rw,rh) { console.log('Panel.collapse',this,cmp,aw,ah,rw,rh); this.main_panel.doLayout(); }"
            #~ d.update(listeners=dict(scope=js_code('this'),collapse=js_code(js),expand=js_code(js)))
            #d.update(monitorResize=True)
        #~ else:
            #~ d.update(xtype='container')
        #d.update(margins='0')
        #d.update(style=dict(padding='0px'))
        
        #~ d.update(items=self.elements)
        #l = [e.as_ext() for e in self.elements ]
        #d.update(items=js_code("[\n  %s\n]" % (", ".join(l))))
        #d.update(items=js_code("this.elements"))
        
        if self.is_fieldset:
            d.update(labelWidth=self.label_width * EXT_CHAR_WIDTH)
        if len(self.elements) > 1 and self.vertical:
            #d.update(frame=self.has_frame)
            d.update(frame=True)
            d.update(bodyBorder=False)
            d.update(border=False)
            #~ 20120115 d.update(labelAlign=self.labelAlign)
            #d.update(style=dict(padding='0px'),color='green')
        else:
            d.update(frame=False)
            #d.update(bodyBorder=False)
            d.update(border=False)
            
        if self.label:
            #~ d.update(title=unicode(self.label)) 20111111
            d.update(title=self.label)
            
        return d
        
class FieldSetPanel(Panel):
    value_template = "new Ext.form.FieldSet(%s)"
    def __init__(self,layout_handle,name,vertical,*elements,**kw):
        self.fieldset = getattr(layout_handle.layout.table.model,name)
        for child in elements:
            child.label = self.fieldset.get_child_label(child.name)
        Panel.__init__(self,layout_handle,name,vertical,*elements,**kw)
        
        self.label = self.fieldset.verbose_name
        
    def ext_options(self,**d):
        d = Panel.ext_options(self,**d)
        d.update(frame=False)
        d.update(bodyBorder=True)
        d.update(border=True)
        d.update(labelAlign=self.labelAlign)
        return d
        
    #~ def wrap_formlayout_elements(self):
        #~ pass
  

class GridElement(Container): 
    declare_type = jsgen.DECLARE_VAR
    #~ declare_type = jsgen.DECLARE_THIS
    #value_template = "new Ext.grid.EditorGridPanel(%s)"
    #~ value_template = "new Ext.grid.GridPanel(%s)"
    value_template = "new Lino.GridPanel(%s)"
    ext_suffix = "_grid"
    vflex = True
    xtype = None
    preferred_height = 5
    refers_to_ww = True
    
    def __init__(self,layout_handle,name,rpt,*columns,**kw):
        """
        :param layout_handle: the handle of the DetailLayout owning this grid
        :param rpt: the report being displayed
        """
        #~ assert isinstance(rpt,dd.AbstractTable), "%r is not a Table!" % rpt
        self.value_template = "new Lino.%s.GridPanel(%%s)" % rpt
        self.report = rpt
        if len(columns) == 0:
            self.rh = rpt.get_handle(layout_handle.ui)
            if not hasattr(self.rh,'list_layout'):
                raise Exception("%s has no list_layout" % self.rh)
            columns = self.rh.list_layout._main.columns
            #~ columns = self.rh.list_layout._main.elements
        w = 0
        for e in columns:
            w += (e.width or e.preferred_width)
        self.preferred_width = constrain(w,10,120)
        #~ kw.update(boxMinWidth=500)
        self.columns = columns
        
        vc = dict(emptyText=_("No data to display."))
        if rpt.editable:
            vc.update(getRowClass=js_code('Lino.getRowClass'))
        
        #~ //autoScroll:true,
        #~ //autoFill:true,
        #~ //forceFit=True,
        #~ //enableRowBody=True,
        #~ //~ showPreview:true,
        #~ //~ scrollOffset:200,
        #~ //~ enableRowBody: true,
        
        kw.update(viewConfig=vc)
        
        
        #~ kw.update(containing_window=js_code("this.containing_window"))
        kw.update(containing_panel=js_code("this"))
        #~ if not rpt.show_params_at_render:
        if rpt.params_panel_hidden:
            kw.update(params_panel_hidden=True)
        Container.__init__(self,layout_handle,name,**kw)
        self.active_children = columns
        #~ 20111125
        #~ assert not kw.has_key('before_row_edit')
        #~ self.update(before_row_edit=before_row_edit(self))
        
        #~ if self.report.master is not None and self.report.master is not models.Model:
            #~ self.mt = ContentType.objects.get_for_model(self.report.master).pk
        #~ else:
            #~ self.mt = 'undefined'
            
            
    def update_config(self,wc):
        pass
        #~ for i,w in enumerate(wc['column_widths']):
            #~ self.column_model.columns[i].update(width = w)

    def ext_options(self,**kw):
        "not direct parent (Container), only LayoutElement"
        kw = LayoutElement.ext_options(self,**kw)
        return kw
        
    def unused_ext_options(self,**kw):
        rh = self.report.get_handle(self.layout_handle.ui)
        kw = LayoutElement.ext_options(self,**kw)
        kw.update(ls_url=rpt2url(self.report))
        kw.update(ls_store_fields=[js_code(f.as_js()) for f in rh.store.list_fields])
        kw.update(ls_columns=[GridColumn(i,e) for i,e in enumerate(self.columns)])
        kw.update(ls_id_property=rh.store.pk.name)
        kw.update(pk_index=rh.store.pk_index)
        kw.update(ls_quick_edit=rh.report.cell_edit)
        kw.update(ls_bbar_actions=[rh.ui.a2btn(a) for a in rh.get_actions(rh.report.default_action)])
        kw.update(ls_grid_configs=[gc.data for gc in self.report.grid_configs])
        kw.update(gc_name=DEFAULT_GC_NAME)
        return kw
        
        

            
class MainPanel(jsgen.Variable):
    declare_type = jsgen.DECLARE_INLINE
    refers_to_ww = True
  
    def apply_window_config(self,wc):
        pass
  
    #~ def setup(self):
        #~ pass
                



class GridMainPanel(GridElement,MainPanel):
    def __init__(self,layout_handle,name,vertical,*columns,**kw):
        """ignore the "vertical" arg"""
        GridElement.__init__(self,layout_handle,name,layout_handle.rh.report,*columns,**kw)
        



class DetailMainPanel(Panel,MainPanel):
    #~ declare_type = jsgen.DECLARE_THIS
    #~ xtype = 'form'
    xtype = None
    #~ value_template = "new Ext.form.FormPanel(%s)"
    value_template = "new Ext.Panel(%s)"
    def __init__(self,layout_handle,name,vertical,*elements,**kw):
        #~ self.rh = layout_handle.datalink
        #~ 20111126 self.report = layout_handle.rh.report
        #~ MainPanel.__init__(self)
        #~ DataElementMixin.__init__(self,layout_handle.link)
        kw.update(autoScroll=True)
        #~ kw.update(height=800, autoScroll=True)
        Panel.__init__(self,layout_handle,name,vertical,*elements,**kw)
        #layout_handle.needs_store(self.rh)
        
    def subvars(self):
        #~ print 'DetailMainPanel.subvars()', self
        for e in MainPanel.subvars(self):
            yield e
        for e in Panel.subvars(self):
            yield e
            
    def ext_options(self,**kw):
        #~ self.setup()
        kw = Panel.ext_options(self,**kw)
        if self.layout_handle.layout.label:
            kw.update(title=_(self.layout_handle.layout.label))
        return kw
        

class ParameterPanel(DetailMainPanel):
    value_template = "new Ext.form.FormPanel(%s)"
    #~ pass
    
class unused_ParameterPanel(DetailMainPanel):
    #~ value_template = "new Ext.Container(%s)"
    #~ value_template = "new Ext.Panel(%s)"
    def __init__(self,layout_handle,name,vertical,*elements,**kw):
        DetailMainPanel.__init__(self,layout_handle,name,vertical,*elements,**kw)
        self.fields = []
        for e in self.walk():
            if isinstance(e,FieldElement):
                #~ logger.info("20120114 ")
                self.fields.append(e)
        #~ self.fields = [e for e in self.walk() if isinstance(e,FieldElement)]
        #~ print '20120115 ParameterPanel.elements =', self.elements
    def ext_options(self,**kw):
        kw = super(ParameterPanel,self).ext_options(**kw)
        kw.update(fields=self.fields)
        return kw
    

class TabPanel(jsgen.Component):
#~ class TabPanel(jsgen.Value):
    value_template = "new Ext.TabPanel(%s)"

    def __init__(self,tabs,**kw):
        self.active_children = []
        for t in tabs:
            self.active_children += t.active_children
            t.update(listeners=dict(activate=js_code("Lino.on_tab_activate")))
            #~ if t.has_upload:
                #~ self.has_upload = True
      
        self.tabs = tabs
        kw.update(
          split=True,
          activeTab=0,
          #~ layoutOnTabChange=True, # 20101028
          #~ forceLayout=True, # 20101028
          #~ deferredRender=False, # 20101028
          #~ autoScroll=True, 
          #~ width=300, # ! http://code.google.com/p/lino/wiki/20100513
          items=tabs,
          # http://www.extjs.com/forum/showthread.php?26564-Solved-FormPanel-in-a-TabPanel
          #~ listeners=dict(activate=js_code("function(p) {p.doLayout();}"),single=True),
        )
        jsgen.Value.__init__(self,kw)
        
    def unused_has_field(self,f):
        for t in self.tabs:
            if t.has_field(f): 
                return True


from lino.tools import full_model_name

class FormPanel(jsgen.Component):
    declare_type = jsgen.DECLARE_VAR
    #~ listeners = None
    
    def __init__(self,rh,action,**kw):
        self.rh = rh
        #~ self.value_template = "new Lino.%s.FormPanel(%%s)" % full_model_name(self.rh.report.model)
        self.value_template = "new Lino.%sPanel(%%s)" % action
        #~ hmm....
        #~ kw.update(
          #~ layout='fit',
          #~ empty_title=action.get_button_label()
        #~ )
        #~ kw.update(containing_window=js_code("ww"))
        #~ if not isinstance(action,table.InsertRow):
            #~ kw.update(has_navigator=rh.report.has_navigator)
            
        #~ rpt = rh.report
        #~ a = rpt.get_action('detail')
        #~ if a:
            #~ kw.update(ls_detail_handler=js_code("Lino.%s" % a))
        #~ a = rpt.get_action('insert')
        #~ if a:
            #~ kw.update(ls_insert_handler=js_code("Lino.%s" % a))
        
        #~ kw.update(ls_bbar_actions=[rh.ui.a2btn(a) for a in rpt.get_actions(action)])
        #~ kw.update(ls_url=rpt2url(rpt))
        #~ ... hmm
        jsgen.Component.__init__(self,'form_panel',**kw)
        
    def unused_has_field(self,f):
        return self.main.has_field(f)



_FIELD2ELEM = (
    #~ (dd.Constant, ConstantElement),
    (dd.HtmlBox, HtmlBoxElement),
    #~ (dd.QuickAction, QuickActionElement),
    (dd.DisplayField, DisplayElement),
    (dd.IncompleteDateField, IncompleteDateFieldElement),
    (dd.LinkedForeignKey, LinkedForeignKeyElement),
    (models.URLField, URLFieldElement),
    (models.FileField, FileFieldElement),
    (models.EmailField, CharFieldElement),
    #~ (dd.HtmlTextField, HtmlTextFieldElement),
    #~ (dd.RichTextField, RichTextFieldElement),
    (models.TextField, TextFieldElement), # also dd.RichTextField
    (dd.PasswordField, PasswordFieldElement),
    (models.CharField, CharFieldElement),
    (dd.MonthField, MonthFieldElement),
    (models.DateTimeField, DateTimeFieldElement),
    (models.DateField, DateFieldElement),
    (models.TimeField, TimeFieldElement),
    (models.IntegerField, IntegerFieldElement),
    (models.DecimalField, DecimalFieldElement),
    (models.BooleanField, BooleanFieldElement),
    #~ (models.ManyToManyField, M2mGridElement),
    (models.ForeignKey, ForeignKeyElement),
    (models.AutoField, IntegerFieldElement),
)
    

def field2elem(layout_handle,field,**kw):
    #~ if hasattr(field,'_lino_chooser'):
    ch = choosers.get_for_field(field)
    if ch:
        #~ if ch.on_quick_insert is not None:
        #~ if ch.meth.quick_insert_field is not None:
        if ch.can_create_choice or not ch.force_selection:
            kw.update(forceSelection=False)
            #~ print 20110425, field.name, layout_handle
        if ch.simple_values:
            #~ kw.update(forceSelection=False)
            return SimpleRemoteComboFieldElement(layout_handle,field,**kw)
        else:
            if isinstance(field,models.ForeignKey):
                return ForeignKeyElement(layout_handle,field,**kw)
            #~ elif isinstance(field,fields.GenericForeignKeyIdField):
                #~ return ComplexRemoteComboFieldElement(layout_handle,field,**kw)
            else:
                return ComplexRemoteComboFieldElement(layout_handle,field,**kw)
    if field.choices:
        if isinstance(field,fields.ChoiceListField):
            kw.setdefault('preferred_width',field.choicelist.preferred_width)
        else:
            kw.setdefault('preferred_width',20)
        return ChoicesFieldElement(layout_handle,field,**kw)
    
    selector_field = field
    if isinstance(field,dd.VirtualField):
        selector_field = field.return_type
    
    if isinstance(selector_field,models.BooleanField) and not field.editable:
        return BooleanDisplayElement(layout_handle,field,**kw)
        
    for cl,x in _FIELD2ELEM:
        if isinstance(selector_field,cl):
            return x(layout_handle,field,**kw)
    if isinstance(field,dd.VirtualField):
        raise NotImplementedError("No LayoutElement for VirtualField %s on %s" % (
          field.name,field.return_type.__class__))
    raise NotImplementedError("No LayoutElement for %s" % field.__class__)
