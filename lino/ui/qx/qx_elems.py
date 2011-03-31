#coding: UTF-8
## Copyright 2009-2011 Luc Saffre
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

from cgi import escape

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from django.conf import settings

import lino

from lino import reports, actions, fields
from lino.utils import constrain
from lino.utils import jsgen
from lino.utils.jsgen import py2js, Variable, Component, id2js, js_code
from lino.utils import choosers
#~ from . import ext_requests
from lino.ui import requests as ext_requests

EXT_CHAR_WIDTH = 9
EXT_CHAR_HEIGHT = 22

#~ DEFAULT_GC_NAME = 'std'
DEFAULT_GC_NAME = 0


def a2btn(a):
    return dict(
      opens_a_slave=a.opens_a_slave,
      handler=js_code("Lino.%s" % a),
      name=a.name,
      label=unicode(a.label),
      #~ url="/".join(("/ui",a.actor.app_label,a.actor._actor_name,a.name))
    )
      
def py2html(obj,name):
    for n in name.split('.'):
        obj = getattr(obj,n,"N/A")
    return escape(unicode(obj))
    
def before_row_edit(panel):
    l = []
    #~ l.append("console.log('before_row_edit',record);")
    for e in panel.active_children:
        if isinstance(e,GridElement):
            l.append("%s.on_master_changed();" % e.as_ext())
        elif isinstance(e,PictureElement):
            l.append("this.load_picture_to(%s,record);" % e.as_ext())
        elif isinstance(e,HtmlBoxElement):
            l.append("%s.refresh();" % e.as_ext())
        elif isinstance(e,FieldElement):
            chooser = choosers.get_for_field(e.field)
            if chooser:
                #~ logger.debug("20100615 %s.%s has chooser", self.lh.layout, e.field.name)
                for f in chooser.context_fields:
                    #~ l.append("console.log('20110128 before_row_edit',record.data);")
                    l.append("%s.setContextValue(%r,record ? record.data[%r] : undefined);" % (
                        e.ext_name,f.name,ext_requests.form_field_name(f)))
    #~ return js_code('function(record){\n  %s\n}' % ('\n  '.join(l)))
    return js_code('function(record){ %s }' % (' '.join(l)))

class GridColumn(Component):
    declare_type = jsgen.DECLARE_INLINE
    field = None
    
    def __init__(self,index,editor,**kw):
        """editor may be a Panel for columns on a GenericForeignKey
        """
        #~ print 20100515, editor.name, editor.__class__
        #~ assert isinstance(editor,FieldElement), \
            #~ "%s.%s is a %r (expected FieldElement instance)" % (cm.grid.report,editor.name,editor)
        self.editor = editor
        #~ self.value_template = editor.grid_column_template
        kw.update(sortable=True)
        self.index = index
        self.label = editor.label
        kw.update(self.editor.get_column_options())
        kw.update(hidden=editor.hidden)
        if settings.USE_GRIDFILTERS and editor.filter_type:
            kw.update(filter=dict(type=editor.filter_type))
        #~ if isinstance(editor,FieldElement) and editor.field.primary_key:
        if isinstance(editor,FieldElement):
            self.field = editor.field
            rend = None
            if isinstance(editor.field,models.AutoField):
                rend = 'Lino.id_renderer'
                #~ kw.update(renderer=js_code('Lino.id_renderer'))
            elif isinstance(editor.field,models.ForeignKey):
                # FK fields are clickable if their target has a detail view
                rpt = editor.field.rel.to._lino_model_report
                if rpt.detail_action is not None:
                #~ a = rpt.get_action('detail')
                #~ if a is not None:
                    rend = "Lino.fk_renderer('%s','Lino.%s')" % (
                      editor.field.name + 'Hidden',
                      rpt.detail_action)
                    #~ rend = "Lino.fk_renderer('%s','%s')" % (
                      #~ editor.field.name + 'Hidden',
                      #~ editor.lh.rh.ui.get_actor_url(rpt))
            #~ if not rend:
                #~ rend = 'Lino.default_renderer'
            if rend:
                kw.update(renderer=js_code(rend))
            kw.update(editable=editor.editable)
            if editor.editable:
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
    
                    
        
        
class VisibleComponent(Component):
    vflex = False
    hflex = True
    width = None
    height = None
    preferred_width = 10
    preferred_height = 1
    #flex = None
    
    def __init__(self,name,width=None,height=None,label=None,**kw):
        Component.__init__(self,name,**kw)
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if label is not None:
            self.label = label
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
        cols = "ext_name name parent label __class__.__name__ labelAlign vertical width preferred_width height preferred_height flex".split()
        yield '<tr><td>' + sep.join(cols) + '</td></tr>'
        for e in self.walk():
            yield '<tr><td>'+sep.join([py2html(e,n) for n in cols]) +'</td></tr>'
            
    def has_field(self,fld):
        for de in self.walk():
            if isinstance(de,FieldElement) and de.field is fld:
                return True
        return False
        
        
class LayoutElement(VisibleComponent):
    stored = False
    ext_name = None
    ext_suffix = ""
    data_type = None 
    filter_type = None
    parent = None # will be set by Container
    field = None
    
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
    
    def __init__(self,lh,name,**kw):
        #logger.debug("LayoutElement.__init__(%r,%r)", lh.layout,name)
        #self.parent = parent
        #~ name = lh.layout._actor_name + '_' + name
        VisibleComponent.__init__(self,name,**kw)
        self.lh = lh
        #~ if lh is not None:
        assert isinstance(lh,reports.LayoutHandle)
        #~ lh.setup_element(self)

    def submit_fields(self):
        return []
        
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
        if self.label and isinstance(parent,Panel):
            if parent.labelAlign == reports.LABEL_ALIGN_LEFT:
                self.preferred_width += len(self.label)

    def ext_options(self,**kw):
        kw = VisibleComponent.ext_options(self,**kw)
        if self.xtype is not None:
            kw.update(xtype=self.xtype)
        if self.collapsible:
            kw.update(collapsible=True)
        return kw


class DataViewElement(LayoutElement):
    declare_type = jsgen.DECLARE_INLINE
    value_template = "new Ext.DataView(%s)"
    vflex = True
    
    def __init__(self,lh,name,dv,**kw):
        #~ self.dv = dv
        kw.update(store=js_code('this.store'))
        kw.update(tpl=js_code('new Ext.XTemplate(%s)' % py2js(dv.xtemplate)))
        kw.update(emptyText='No images to display')
        kw.update(itemSelector='div.thumb-wrap')
        kw.update(loadingText='Loading...')
        LayoutElement.__init__(self,lh,name,**kw)

class TemplateElement(LayoutElement):
    declare_type = jsgen.DECLARE_INLINE
    value_template = "new Ext.BoxComponent(%s)"
    vflex = True
    
    def __init__(self,lh,name,dv,**kw):
        #~ self.dv = dv
        #~ kw.update(tpl=js_code('new Ext.XTemplate(%s)' % py2js(dv.xtemplate)))
        kw.update(plugins=js_code('new Lino.TemplateBoxPlugin(caller,%s)' % py2js(dv.xtemplate)))
        LayoutElement.__init__(self,lh,name,**kw)

class PictureElement(LayoutElement):
    declare_type = jsgen.DECLARE_VAR
    #~ declare_type = jsgen.DECLARE_INLINE
    value_template = "new Ext.BoxComponent(%s)"
    vflex = False
    hflex = False
    #~ vflex = True
    
    def __init__(self,lh,name,action,**kw):
        #~ print 20100730, name
        #~ kw.update(html='<img height="100%"/>')
        #~ kw.update(html='<img height="100%" onclick="Lino.img_onclick()"/>')
        #~ kw.update(autoHeight=True)
        #~ kw.update(anchor="100% 100%")
        kw.update(autoEl=dict(tag='img'))
        #~ kw.update(autoEl=dict(tag='img',onclick="Lino.img_onclick(%s)" % name))
        #~ kw.update(autoEl=dict(tag='img',onclick="Lino.img_onclick(this)" ))
        #~ kw.update(onclick=js_code('"Lino.img_onclick()"'))
        #~ kw.update(cls='ext-el-mask')
        #~ kw.update(style=dict(width='100px',cursor='pointer'))
        #~ kw.update(style=dict(width='100px',height='150px',cursor='pointer'))
        kw.update(plugins=js_code('Lino.PictureBoxPlugin'))
        #~ kw.update(plugins=js_code('new Lino.PictureBoxPlugin(caller)'))
        #~ kw.update(listeners=dict(click=js_code('Lino.img_onclick')))
        LayoutElement.__init__(self,lh,name,**kw)
        #~ print "PictureElement", self.width, self.preferred_width
        self.update(style=dict(
          width='%dpx' % ((self.width or self.preferred_width)*10), # assume 1 char ~ 10px
          cursor='pointer'))
        

class unused_ButtonElement(LayoutElement):
    value_template = "new Ext.Component(%s)"
    
    def __init__(self,lh,name,meth,label,**kw):
        self.label = label
        self.meth = meth
        #~ onclick='alert("oops")'
        #~ kw.update(html='<input type="button" onclick="%s" value=" %s ">' % (onclick,label))
        LayoutElement.__init__(self,lh,name,**kw)
    
    def get_column_options(self,**kw):
        #~ kw.update(dataIndex=self.field.name)
        #~ if self.label is None:
            #~ kw.update(header=self.field.name)
        #~ else:
        kw.update(header=unicode(self.label))
        kw.update(editable=False)
        kw.update(sortable=False)
        rend = 'Lino.cell_button_renderer'
        kw.update(renderer=js_code(rend))
        return kw    
                
        

class StaticTextElement(LayoutElement):
    declare_type = jsgen.DECLARE_INLINE
    #declare_type = jsgen.DECLARE_THIS
    #~ declare_type = jsgen.DECLARE_VAR
    xtype = 'label'
    
    def __init__(self,lh,name,text,**kw):
        kw.update(html=text.text)
        LayoutElement.__init__(self,lh,name,**kw)
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
    #declaration_order = 3
    #~ ext_suffix = "_field"
    
    def __init__(self,lh,field,**kw):
        assert field.name, Exception("field %r has no name!" % field)
        self.field = field
        self.editable = field.editable # and not field.primary_key
        #~ LayoutElement.__init__(self,lh,varname_field(field),label=unicode(field.verbose_name),**kw)
        LayoutElement.__init__(self,lh,field.name,label=unicode(field.verbose_name),**kw)
        
    #~ def get_filter_options(self,**kw):
        #~ if self.filter_type:
            #~ kw.update(dataIndex=self.field.name)
            # 20100805 see also GridFilters.js
            #~ kw.update(filterable=True)  
            #~ kw.update(filter=dict(type='auto'))
            #~ kw.update(type=self.filter_type)
        #~ return kw
            
    def get_column_options(self,**kw):
        #~ raise "get_column_options() %s" % self.__class__
        #~ kw.update(xtype='gridcolumn')
        kw.update(dataIndex=self.field.name)
        #~ if self.label is None:
            #~ kw.update(header=self.field.name)
        #~ else:
        kw.update(header=unicode(self.label))
        if not self.editable:
            kw.update(editable=False)
        if not self.sortable:
            kw.update(sortable=False)
        w = self.width or self.preferred_width
        kw.update(width=w*EXT_CHAR_WIDTH)
        return kw    
        
        
    def submit_fields(self):
        return [self.field.name]
        
    def get_field_options(self,**kw):
        if self.xtype:
            kw.update(xtype=self.xtype)
        kw.update(name=self.field.name)
        if self.label:
            kw.update(fieldLabel=unicode(self.label))
        if not self.field.blank:
            kw.update(allowBlank=False)
        if not self.editable:
            kw.update(disabled=True)
            kw.update(readOnly=True)
        #~ http://www.rowlands-bcs.com/extjs/tips/tooltips-form-fields
        #~ if self.field.__doc__:
            #~ kw.update(toolTipText=self.field.__doc__)
        return kw
        
    def ext_options(self,**kw):
        kw = LayoutElement.ext_options(self,**kw)
        kw.update(self.get_field_options())
        return kw
    
        
class TextFieldElement(FieldElement):
    #~ xtype = 'textarea'
    filter_type = 'string'
    vflex = True
    value_template = "new qx.ui.form.TextField().set(%s)"
    xtype = None
    #width = 60
    preferred_width = 60
    #~ preferred_height = 1
    #collapsible = True
    
    #~ def __init__(self,*args,**kw):
        #~ kw.update(defaultAutoCreate = dict(
            #~ tag="textarea",
            #~ autocomplete="off"
        #~ ))
        #~ FieldElement.__init__(self,*args,**kw)

class HtmlTextFieldElement(TextFieldElement):
    pass
    #~ value_template = "new Ext.form.HtmlEditor(%s)"
    #~ # xtype = 'htmleditor'
        
class CharFieldElement(FieldElement):
    filter_type = 'string'
    value_template = "new qx.ui.form.TextField().set(%s)"
    sortable = True
    xtype = None
  
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        self.preferred_width = min(20,max(3,self.field.max_length))
            
    def get_field_options(self,**kw):
        kw = FieldElement.get_field_options(self,**kw)
        kw.update(maxLength=self.field.max_length)
        return kw
        
class FileFieldElement(CharFieldElement):
    #~ value_template = "Lino.file_field_handler(ww,%s)"
    value_template = "new qx.ui.basic.Atom().set(%s)"
    
    #~ def __init__(self,lh,*args,**kw):
        #~ CharFieldElement.__init__(self,lh,*args,**kw)
        #~ lh.has_upload = True
        
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
    
class ChoicesFieldElement(ComboFieldElement):
    #~ value_template = "new Lino.ChoicesFieldElement(%s)"
    #~ value_template = "new qx.ui.form.ComboBox().set(%s)"
    value_template = "new qx.ui.basic.Atom().set(%s)"
  
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        self.preferred_width = 20
        
    def get_field_options(self,**kw):
        kw = FieldElement.get_field_options(self,**kw)
        kw.update(store=self.field.choices)
        kw.update(hiddenName=self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX)
        return kw
        

class RemoteComboFieldElement(ComboFieldElement):
    #~ value_template = "new Lino.RemoteComboFieldElement(%s)"
    value_template = "new qx.ui.basic.Atom().set(%s)"
  
    def store_options(self,**kw):
        proxy = dict(url=self.lh.rh.ui.get_choices_url(self),method='GET')
        kw.update(proxy=js_code("new Ext.data.HttpProxy(%s)" % py2js(proxy)))
        # a JsonStore without explicit proxy sometimes used method POST
        return kw
      
    def get_field_options(self,**kw):
        kw = FieldElement.get_field_options(self,**kw)
        sto = self.store_options()
        #print repr(sto)
        kw.update(store=js_code("new Lino.ComplexRemoteComboStore(%s)" % py2js(sto)))
        return kw
        
class SimpleRemoteComboFieldElement(RemoteComboFieldElement):
    #~ value_template = "new Lino.SimpleRemoteComboFieldElement(%s)"
    value_template = "new qx.ui.basic.Atom().set(%s)"
    
  
class ComplexRemoteComboFieldElement(RemoteComboFieldElement):
    #~ value_template = "new Lino.ComplexRemoteComboFieldElement(%s)"
        
    def get_field_options(self,**kw):
        kw = RemoteComboFieldElement.get_field_options(self,**kw)
        kw.update(hiddenName=self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX)
        return kw
        
        
class ForeignKeyElement(ComplexRemoteComboFieldElement):
    
    def __init__(self,lh,field,**kw):
    #~ def __init__(self,*args,**kw):
        #~ print 20100903,repr(self.field.rel.to)
        #~ assert issubclass(self.field.rel.to,models.Model), "%r is not a model" % self.field.rel.to
        self.report = reports.get_model_report(field.rel.to)
        a = self.report.detail_action
        if a is not None:
            #~ self.value_template = "new Lino.TwinCombo(%s)"
            self.value_template = "new qx.ui.basic.Atom().set(%s)"
            kw.update(onTrigger2Click=js_code(
              "function(e){ Lino.show_fk_detail(this,e,Lino.%s)}" % a))
        FieldElement.__init__(self,lh,field,**kw)
      
    def submit_fields(self):
        return [self.field.name,self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX]
        
        
    def get_field_options(self,**kw):
        kw = ComplexRemoteComboFieldElement.get_field_options(self,**kw)
        kw.update(pageSize=self.report.page_length)
        kw.update(emptyText=_('Select a %s...') % self.report.model._meta.verbose_name)
        return kw



class TimeFieldElement(FieldElement):
    xtype = 'timefield'
    data_type = 'time' # for store column
    sortable = True
    preferred_width = 8
    filter_type = 'time'
  
class DateFieldElement(FieldElement):
    xtype = 'datefield'
    data_type = 'date' # for store column
    sortable = True
    preferred_width = 8
    filter_type = 'date'
    # todo: DateFieldElement.preferred_width should be computed from Report.date_format
    #~ grid_column_template = "new Ext.grid.DateColumn(%s)"
    
    def get_field_options(self,**kw):
        kw = FieldElement.get_field_options(self,**kw)
        kw.update(format=self.lh.rh.report.date_format)
        return kw
        
    def get_column_options(self,**kw):
        kw = FieldElement.get_column_options(self,**kw)
        kw.update(xtype='datecolumn')
        kw.update(format=self.lh.rh.report.date_format)
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
    #~ value_template = "new Lino.URLField(%s)"
    value_template = "new qx.ui.basic.Atom().set(%s)"
    
    #~ def get_field_options(self,**kw):
        #~ kw = FieldElement.get_field_options(self,**kw)
        #~ kw.update(vtype='url') #,vtypeText=
        #~ return kw
        
    
class IntegerFieldElement(FieldElement):
    value_template = "new qx.ui.form.TextField().set(%s)"
    filter_type = 'numeric'
    #~ xtype = 'numberfield'
    sortable = True
    preferred_width = 5
    data_type = 'int' 
    def __init__(self,*args,**kw):
        kw.update(textAlign='right')
        FieldElement.__init__(self,*args,**kw)

class DecimalFieldElement(FieldElement):
    filter_type = 'numeric'
    xtype = 'numberfield'
    sortable = True
    data_type = 'float' 
    #~ grid_column_template = "new Ext.grid.NumberColumn(%s)"
    
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        self.preferred_width = min(5,self.field.max_digits) \
                + self.field.decimal_places
                
    def get_column_options(self,**kw):
        kw = FieldElement.get_column_options(self,**kw)
        kw.update(xtype='numbercolumn')
        kw.update(align='right')
        fmt = "0,000"
        if self.field.decimal_places > 0:
            fmt += "." + ("0" * self.field.decimal_places)
        kw.update(format=fmt)
        return kw
        
                

class BooleanFieldElement(FieldElement):
  
    value_template = "new qx.ui.form.CheckBox().set(%s)"
    #~ xtype = 'checkbox'
    data_type = 'boolean' 
    filter_type = 'boolean'
    #~ grid_column_template = "new Ext.grid.BooleanColumn(%s)"
    #~ def __init__(self,*args,**kw):
        #~ FieldElement.__init__(self,*args,**kw)
        
    def set_parent(self,parent):
        FieldElement.set_parent(self,parent)
        #~ if isinstance(parent,Panel) and parent.hideCheckBoxLabels:
        if parent.hideCheckBoxLabels:
            self.update(hideLabel=True)
            
    def get_field_options(self,**kw):
        kw = FieldElement.get_field_options(self,**kw)
        del kw['fieldLabel']
        #~ kw.update(hideLabel=True)
        kw.update(boxLabel=self.label)
        return kw
        
    def get_column_options(self,**kw):
        kw = FieldElement.get_column_options(self,**kw)
        kw.update(xtype='booleancolumn')
        kw.update(trueText=self.lh.rh.report.boolean_texts[0])
        kw.update(falseText=self.lh.rh.report.boolean_texts[1])
        kw.update(undefinedText=self.lh.rh.report.boolean_texts[2])
        return kw
        
    def get_from_form(self,instance,values):
        """
        standard HTML submits checkboxes of a form only when they are checked.
        So if the field is not contained in values, we take False as value.
        """
        instance[self.field.name] = values.get(self.field.name,False)


class DisplayElement(FieldElement):
#~ class ShowOrCreateElement(FieldElement):
    ext_suffix = "_disp"
    declare_type = jsgen.DECLARE_VAR
    #~ value_template = "new Ext.form.DisplayField(%s)"
    value_template = "new qx.ui.basic.Atom().set(%s)"
    #~ value_template = "new Lino.ButtonField(ww,%s)"
    #~ preferred_height = 5
    #~ vflex = True
    #~ filter_type = 'string'
    #~ refers_to_ww = True
    
#~ class QuickActionElement(DisplayElement):
    #~ pass
    #~ ext_suffix = "_quick"
    #~ value_template = "new Lino.QuickAction(ww,%s)"
    
  
  
class HtmlBoxElement(DisplayElement):
    ext_suffix = "_htmlbox"
    #~ declare_type = jsgen.DECLARE_VAR
    #~ value_template = "new Lino.HtmlBoxPanel(ww,%s)"
    value_template = "new qx.ui.basic.Atom().set(%s)"
    preferred_height = 5
    vflex = True
    filter_type = 'string'
    refers_to_ww = True
    
    #~ def __init__(self,lh,name,action,**kw):
        #~ kw.update(plugins=js_code('Lino.HtmlBoxPlugin'))
        #~ LayoutElement.__init__(self,lh,name,**kw)
        
    def get_field_options(self,**kw):
        kw.update(name=self.field.name)
        kw.update(layout='fit')
        if self.field.drop_zone: # testing with drop_zone 'FooBar'
            kw.update(listeners=dict(render=js_code('initialize%sDropZone' % self.field.drop_zone)))
        kw.update(items=js_code("new Ext.BoxComponent()"))
        if self.label:
            kw.update(title=unicode(self.label))
        #~ if self.field.bbar is not None:
            #~ kw.update(ls_bbar_actions=self.field.bbar)
        return kw
        


class Container(LayoutElement):
    vertical = False
    hpad = 1
    is_fieldset = False
    #~ xtype = 'container'
    value_template = "new qx.ui.container.Composite().set(%s)"
    #~ hideCheckBoxLabels = True
    
    #declare_type = jsgen.DECLARE_INLINE
    #declare_type = jsgen.DECLARE_THIS
    declare_type = jsgen.DECLARE_VAR
    #~ declare_type = jsgen.DECLARE_THIS
    
    
    def __init__(self,lh,name,*elements,**kw):
        self.has_frame = lh.layout.has_frame
        self.labelAlign = lh.layout.label_align
        self.hideCheckBoxLabels = lh.layout.hideCheckBoxLabels
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
            kw.update(items=elements)
                
        LayoutElement.__init__(self,lh,name,**kw)
        
        #~ if lh.layout.__class__.__name__ == 'CompanyDetail':
            #~ print 20100919, self.__class__.__name__, name, ':', str(elements)
        
        #~ onlyCheckBoxes = True
        #~ for e in self.walk():
            #~ if not isinstance(e,BooleanFieldElement):
                #~ onlyCheckBoxes = False
        #~ if onlyCheckBoxes:
            #~ for e in self.walk():
                #~ e.update(hideLabel=True)
                #~ print 'hideLabel:', e,
        
    def subvars(self):
        return self.elements
            
    def walk(self):
        for e in self.elements:
            for el in e.walk():
                yield el
        yield self
        

    def pprint(self,level=0):
        margin = "  " * level
        s = margin + str(self) + ":\n"
        # self.__class__.__name__
        for e in self.elements:
            for ln in e.pprint(level+1).splitlines():
                s += ln + "\n"
        return s




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
    
    def __init__(self,lh,name,vertical,*elements,**kw):
        self.vertical = vertical
            
        #~ if self.vertical:
            #~ vflex_elems = [e for e in elements if e.vflex]
            #~ if len(flex_elems) > 0:
                #~ assert len(kw) == 0, "%r is not empty" % kw
                #~ vfix_elems = [e for e in elements if not e.vflex]
                #~ flex_panel = Panel(lh,name,vertical,*vflex_elems)
                #~ fix_panel = Panel(lh,name,vertical,*vfix_elems)
                
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
                    #~ print 20100615, self.lh.layout, self, "hbox loses vflex because of", e
                    
        if len(elements) > 1 and self.vflex:
            if self.vertical:
                """
                Example : The panel contains a mixture of fields and grids. 
                Fields are not vflex, grids well.
                """
                #~ print 20100615, self.lh, self
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
                                #~ g = Container(lh,name,*eg,**dict(layout='vbox',flex=1)
                                g = Panel(lh,name,vertical,*eg,**dict(layout='vbox',
                                  flex=1,layoutConfig=dict(align='stretch')))
                                assert g.vflex is True
                        else:
                            #~ for e in eg: e.update(align='stretch')
                            if len(eg) == 1:
                                g = eg[0]
                            else:
                                g = Container(lh,name,*eg,**dict(layout='form',autoHeight=True))
                                #~ g = Container(lh,name,*eg,**dict(layout='form'))
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


        label = lh.layout.collapsible_elements.get(name,None)
        if label:
            self.collapsible = True
            self.label = label

        Container.__init__(self,lh,name,*elements,**kw)
        

        w = h = 0
        for e in self.elements:
            ew = e.width or e.preferred_width
            eh = e.height or e.preferred_height
            if self.vertical:
                #~ h += e.flex
                h += eh
                w = max(w,ew)
            else:
                #w += e.flex
                w += ew
                h = max(h,eh)
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
                #~ d.update(layout='hbox')
                #~ 20101116 d.update(layoutConfig=dict(align='stretchmax'))
                #~ if stretch : # 20100912
                    #~ d.update(layoutConfig=dict(align='stretch'))
                #~ else:
                    #~ d.update(layoutConfig=dict(align='stretchmax'))
                
        if d['layout'] == 'form':
            assert self.vertical
            #~ d.update(autoHeight=True)
            if len(self.elements) == 1 and self.elements[0].vflex:
                self.elements[0].update(anchor="100% 100%")
            else:
                for e in self.elements:
                    #~ assert not e.vflex
                    #~ h = e.height or e.preferred_height
                    #~ if e.vflex:
                        #~ e.value.update(anchor="100% 100%")
                    #~ else:
                        #~ e.value.update(anchor="100%")
                    e.update(anchor="100%")
                
        if d['layout'] == 'hbox':
            if not self.vflex: # 20101028
                d.update(autoHeight=True)
                d.update(layoutConfig=dict(align='stretchmax'))
            for e in self.elements:
                if e.hflex:
                    w = e.width or e.preferred_width
                    #~ e.value.update(columnWidth=float(w)/self.preferred_width) # 20100615
                    e.value.update(flex=int(w*100/self.preferred_width))
                
            #~ wrappers = []
            #~ for e in self.elements:
                #~ wrappers.append(dict(layout='form',autoHeight=True,items=e))
            #~ d.update(items=wrappers)
              
        elif d['layout'] == 'vbox':
            "a vbox with 2 or 3 elements, of which at least two are vflex will be implemented as a VBorderPanel"
            assert len(self.elements) > 1
            vflex_count = 0
            h = self.height or self.preferred_height
            for e in self.elements:
                eh = e.height or e.preferred_height
                if e.vflex:
                    e.value.update(flex=int(eh*100/h))
                    vflex_count += 1
            if vflex_count >= 2 and len(self.elements) <= 3:
            #~ if vflex_count >= 1 and len(self.elements) <= 3:
                self.remove('layout','layoutConfig')
                #~ self.value_template = 'new Lino.VBorderPanel(%s)'
                for e in self.elements:
                    #~ if e.vflex: # """as long as there are bugs, make also non-vflex resizable"""
                    e.update(split=True)
                self.elements[0].update(region='north')
                self.elements[1].update(region='center')
                if len(self.elements) == 3:
                    self.elements[1].update(region='south')
        
        

class GridElement(Container): 
    declare_type = jsgen.DECLARE_VAR
    #~ value_template = "new lino.TablePanel(ww,%s)"
    value_template = "new qx.ui.basic.Atom().set(%s)"
    ext_suffix = "_grid"
    vflex = True
    xtype = None
    preferred_height = 5
    refers_to_ww = True
    
    def __init__(self,lh,name,rpt,*elements,**kw):
        """
        :param lh: the handle of the DetailLayout owning this grid
        :param rpt: the report being displayed
        """
        assert isinstance(rpt,reports.Report), "%r is not a Report!" % rpt
        self.report = rpt
        if len(elements) == 0:
            self.rh = rpt.get_handle(lh.rh.ui)
            elements = self.rh.list_layout._main.elements
            #~ columns = self.rh.list_layout._main.elements
        w = 0
        for e in elements:
            w += (e.width or e.preferred_width)
        self.preferred_width = constrain(w,10,120)
        #~ kw.update(boxMinWidth=500)
        #~ self.columns = elements
        #~ self.store = qx_store.Store(lh)
        self.columns = [GridColumn(i,e) for i,e in enumerate(elements)]
        
        kw.update(page_length=self.report.page_length)

        a = rpt.get_action('detail')
        if a:
            kw.update(ls_detail_handler=js_code("Lino.%s" % a))
        a = rpt.get_action('insert')
        if a:
            kw.update(ls_insert_handler=js_code("Lino.%s" % a))
        
        Container.__init__(self,lh,name,*elements,**kw)
        #~ self.active_children = columns
        assert not kw.has_key('before_row_edit')
        self.update(before_row_edit=before_row_edit(self))
        
        self.preferred_height = rpt.page_length 
        if self.report.master is not None:
            self.mt = ContentType.objects.get_for_model(self.report.master).pk
        else:
            self.mt = 'undefined'
            
            
    def update_config(self,wc):
        pass
        #~ for i,w in enumerate(wc['column_widths']):
            #~ self.column_model.columns[i].update(width = w)

    def ext_options(self,**kw):
        rh = self.report.get_handle(self.lh.rh.ui)
        kw = LayoutElement.ext_options(self,**kw)
        #~ d.update(ls_data_url=rh.ui.get_actor_url(self.report))
        kw.update(ls_url=rh.ui.build_url(self.report.app_label,self.report._actor_name))
        kw.update(ls_store_fields=[js_code(f.as_js()) for f in rh.store.list_fields])
        #~ kw.update(ls_columns=[GridColumn(i,e) for i,e in enumerate(self.columns)])
        #~ kw.update(ls_filters=[e.get_filter_options() for e in self.elements if e.filter_type])
        kw.update(ls_id_property=rh.store.pk.name)
        kw.update(pk_index=rh.store.pk_index)
        kw.update(ls_quick_edit=rh.report.cell_edit)
        kw.update(ls_bbar_actions=[rh.ui.a2btn(a) for a in rh.get_actions(rh.report.default_action)])
        kw.update(ls_grid_configs=[gc.data for gc in self.report.grid_configs])
        kw.update(gc_name=DEFAULT_GC_NAME)
        #~ gc = self.report.grid_configs.get('',None)
        #~ if gc is not None:
            #~ kw.update(ls_grid_config=gc)
        return kw
        
class SlaveGridElement(GridElement):
    def ext_options(self,**kw):
        kw = GridElement.ext_options(self,**kw)
        #~ kw.update(plugins=js_code('new Lino.SlaveGridPlugin(caller)'))
        
        kw.update(title=unicode(self.report.label))
        
        #~ js = "Lino.do_action(caller,%r)" % \
            #~ rh.list_layout.get_absolute_url(run=True)
        #~ js = "function(){ Lino.notify('Das ist noch nicht fertig... siehe ext_elems.py:990');}"
        #~ kw.update(listeners=dict(click=js_code(js)))
        return kw
      
        
class M2mGridElement(GridElement):
    def __init__(self,lh,field,*columns,**kw):
        self.field = field
        rpt = reports.get_model_report(field.rel.to)
        #~ rh = rpt.get_handle(lh.ui)
        GridElement.__init__(self,lh,id2js(rpt.actor_id),rpt,*columns,**kw)
  

            
class MainPanel(jsgen.Variable):
    declare_type = jsgen.DECLARE_INLINE
    refers_to_ww = True
  
    def apply_window_config(self,wc):
        pass
  
    def setup(self):
        pass
                
    @classmethod
    def field2elem(cls,lh,field,**kw):
        #~ if hasattr(field,'_lino_chooser'):
        ch = choosers.get_for_field(field)
        if ch:
            if ch.simple_values:
                return SimpleRemoteComboFieldElement(lh,field,**kw)
            else:
                if isinstance(field,models.ForeignKey):
                    return ForeignKeyElement(lh,field,**kw)
                else:
                    return ComplexRemoteComboFieldElement(lh,field,**kw)
        if field.choices:
            return ChoicesFieldElement(lh,field,**kw)
            
        if isinstance(field,fields.VirtualField):
            field = field.return_type
        for cl,x in _field2elem:
            if isinstance(field,cl):
                return x(lh,field,**kw)
        raise NotImplementedError("No LayoutElement for %s" % field.__class__)
        #~ raise NotImplementedError("field %r" % field)



class GridMainPanel(GridElement,MainPanel):
    def __init__(self,lh,name,vertical,*columns,**kw):
        """ignore the "vertical" arg"""
        self.value_template = "new lino.%s(%%s)" % lh.rh.report
        GridElement.__init__(self,lh,name,lh.rh.report,*columns,**kw)
        



class DetailMainPanel(Panel,MainPanel):
#~ class DetailMainPanel(Panel,WrappingMainPanel):
    #~ declare_type = jsgen.DECLARE_THIS
    #~ xtype = 'form'
    xtype = None
    #~ value_template = "new Ext.form.FormPanel(%s)"
    value_template = "new Ext.Panel(%s)"
    def __init__(self,lh,name,vertical,*elements,**kw):
        #~ self.rh = lh.datalink
        self.report = lh.rh.report
        #~ MainPanel.__init__(self)
        #~ DataElementMixin.__init__(self,lh.link)
        kw.update(autoScroll=True)
        #~ kw.update(height=800, autoScroll=True)
        Panel.__init__(self,lh,name,vertical,*elements,**kw)
        #lh.needs_store(self.rh)
        
        
    def unused_get_datalink(self):
        return self.rh
        
    def subvars(self):
        #~ print 'DetailMainPanel.subvars()', self
        for e in MainPanel.subvars(self):
            yield e
        for e in Panel.subvars(self):
            yield e
            
    def ext_options(self,**kw):
        self.setup()
        kw = Panel.ext_options(self,**kw)
        if self.lh.layout.label:
            #~ kw.update(title=unicode(self.lh.layout.label))
            kw.update(title=_(self.lh.layout.label))
        #d.update(region='east',split=True) #,width=300)
        #~ kw.update(width=800)
        #~ kw.update(autoScroll=True)
        if False:
            kw.update(tbar=js_code("""new Ext.PagingToolbar({
              store: %s,
              displayInfo: true,
              pageSize: 1,
              prependButtons: true,
            }) """ % self.rh.store.ext_name))
        #d.update(items=js_code(self._main.as_ext(request)))
        #d.update(items=js_code("[%s]" % ",".join([e.as_ext() for e in self.elements])))
        #~ kw.update(items=self.elements)
        #d.update(autoHeight=False)
        #~ kw.update(bbar=self.bbar_buttons)
        #~ kw.update(bbar=self.buttons)
        #d.update(standardSubmit=True)
        return kw
        
    #~ @classmethod
    #~ def field2elem(cls,lh,field,**kw):
        #~ e = MainPanel.field2elem(lh,field,**kw)
        #~ if isinstance(e,HtmlBoxElement): return e
        #~ po = dict(layout='form',autoHeight=True) # 20101028
        #~ ct = Panel(lh,field.name+"_ct",True,e,**po)#,flex=0)
        #~ ct.field = field
        #~ return ct

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
        
    def has_field(self,f):
        for t in self.tabs:
            if t.has_field(f): 
                return True



class FormPanel(jsgen.Component):
    declare_type = jsgen.DECLARE_VAR
    #~ value_template = "new Lino.FormPanel(ww,%s)"
    listeners = None
    
    def __init__(self,rh,action,main,**kw):
        self.rh = rh
        self.value_template = "new Lino.%s.FormPanel(ww,%%s)" % self.rh.report
        self.main = main
        kw.update(
          #~ items=main,
          #~ autoScroll=True,
          #~ autoHeight=True,
          layout='fit',
        )
        if not isinstance(action,reports.InsertRow):
            kw.update(has_navigator=rh.report.has_navigator)
            
        on_render = []
        elems_by_field = {}
        field_elems = []
        for e in main.active_children:
            if isinstance(e,FieldElement):
                field_elems.append(e)
                l = elems_by_field.get(e.field.name,None)
                if l is None:
                    l = []
                    elems_by_field[e.field.name] = l
                l.append(e)
            
        for e in field_elems:
            #~ if isinstance(e,FileFieldElement):
                #~ kw.update(fileUpload=True)
            chooser = choosers.get_for_field(e.field)
            if chooser:
                #~ logger.debug("20100615 %s.%s has chooser", self.lh.layout, e.field.name)
                for f in chooser.context_fields:
                    for el in elems_by_field.get(f.name,[]):
                        #~ if main.has_field(f):
                        #~ varname = varname_field(f)
                        #~ on_render.append("%s.on('change',Lino.chooser_handler(%s,%r));" % (varname,e.ext_name,f.name))
                        on_render.append(
                            "%s.on('change',Lino.chooser_handler(%s,%r));" % (
                            el.ext_name,e.ext_name,f.name))
        
        if on_render:
            assert not kw.has_key('listeners')
            #~ kw.update(listeners=dict(render=js_code('function(){%s}' % '\n'.join(on_render))))
            self.listeners=dict(render=js_code('function(){%s}' % '\n'.join(on_render)))
        #~ kw.update(before_row_edit=before_row_edit(main))
        self.before_row_edit=before_row_edit(main)
        
        rpt = rh.report
        a = rpt.get_action('detail')
        if a:
            kw.update(ls_detail_handler=js_code("Lino.%s" % a))
        a = rpt.get_action('insert')
        if a:
            kw.update(ls_insert_handler=js_code("Lino.%s" % a))
        
        kw.update(ls_bbar_actions=[rh.ui.a2btn(a) for a in rpt.get_actions(action)])
        kw.update(ls_url=rh.ui.build_url(rpt.app_label,rpt._actor_name))
        jsgen.Component.__init__(self,'form_panel',**kw)
        
    def has_field(self,f):
        return self.main.has_field(f)



_field2elem = (
    (fields.HtmlBox, HtmlBoxElement),
    #~ (fields.QuickAction, QuickActionElement),
    (fields.DisplayField, DisplayElement),
    (models.URLField, URLFieldElement),
    (models.FileField, FileFieldElement),
    (models.EmailField, CharFieldElement),
    (fields.HtmlTextField, HtmlTextFieldElement),
    (models.TextField, TextFieldElement),
    (models.CharField, CharFieldElement),
    (fields.MonthField, MonthFieldElement),
    (models.DateField, DateFieldElement),
    #~ (models.TimeField, TimeFieldElement),
    (models.IntegerField, IntegerFieldElement),
    (models.DecimalField, DecimalFieldElement),
    (models.BooleanField, BooleanFieldElement),
    (models.ManyToManyField, M2mGridElement),
    (models.ForeignKey, ForeignKeyElement),
    (models.AutoField, IntegerFieldElement),
)
    

