#coding: UTF-8
## Copyright 2009-2010 Luc Saffre
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

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _

import lino

from lino import layouts, reports
from lino.utils import constrain
from lino.utils import jsgen
from lino.utils.jsgen import py2js, Variable, Component, id2js, js_code
from lino.utils import chooser
from lino.ui.extjs import ext_requests
from lino.modlib.properties import models as properties # import Property, CharPropValue

EXT_CHAR_WIDTH = 9
EXT_CHAR_HEIGHT = 22



class ColumnModel(Component):
    #~ declare_type = jsgen.DECLARE_THIS
    #declare_type = jsgen.DECLARE_VAR
    declare_type = jsgen.DECLARE_INLINE
    ext_suffix = "_cols"
    value_template = "new Ext.grid.ColumnModel(%s)"
    #declaration_order = 2
    
    def __init__(self,grid):
        assert isinstance(grid,GridElement)
        self.grid = grid
        Component.__init__(self,grid.name)
        self.columns = [GridColumn(self,e) for e in self.grid.elements if not e.hidden]
        
    def subvars(self):
        for col in self.columns:
            yield col.editor
            yield col
        
        
    def ext_options(self,**d):
        #self.report.setup()
        d = Component.ext_options(self,**d)
        #d.update(columns=[e.get_column_options() for e in self.grid.elements])
        #d.update(defaultSortable=True)
        d.update(columns=self.columns)
        return d
        
class GridColumn(Component):
    #~ declare_type = jsgen.DECLARE_VAR
    declare_type = jsgen.DECLARE_INLINE
    ext_suffix = "_col"
    value_template = "new Ext.grid.Column(%s)"
    
    def __init__(self,cm,editor,**kw):
        #~ print 20100515, editor.name, editor.__class__
        #~ assert isinstance(editor,FieldElement), \
            #~ "%s.%s is a %r (expected FieldElement instance)" % (cm.grid.report,editor.name,editor)
        self.editor = editor
        self.value_template = editor.grid_column_template
        kw.update(self.editor.get_column_options())
        kw.update(editor=self.editor)
        if isinstance(editor,FieldElement) and editor.field.primary_key:
            kw.update(renderer=js_code('Lino.id_renderer'))
        Component.__init__(self,editor.name,**kw)
    
        #~ if self.editable:
            #~ editor = self.get_field_options()
        
        
class ComboBox(Component):
    value_template = 'new Ext.form.ComboBox(%s)'
                    
        
        
class VisibleComponent(Component):
    vflex = False
    width = None
    height = None
    preferred_width = 10
    preferred_height = 0
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
        if self.width is None:
            return self.name
        if self.height is None:
            return self.name + ":%d" % self.width
        return self.name + ":%dx%d" % (self.width,self.height)
        
    def pprint(self,level=0):
        return ("  " * level) + self.__str__()
        
    def walk(self):
        yield self
        
    def debug_lines(self):
        sep = ","
        cols = "name label __class__ labelAlign vertical width preferred_width height preferred_height flex".split()
        yield sep.join(cols) 
        for e in self.walk():
            yield sep.join([str(getattr(e,n,"N/A")) for n in cols])
            
        
class LayoutElement(VisibleComponent):
    stored = False
    ext_name = None
    ext_suffix = ""
    data_type = None 
    parent = None # will be set by Container
    
    label = None
    label_width = 0 
    editable = False
    sortable = False
    xtype = None # set by subclasses
    grid_column_template = "new Ext.grid.Column(%s)"
    collapsible = False
    hidden = False
    
    def __init__(self,lh,name,**kw):
        #lino.log.debug("LayoutElement.__init__(%r,%r)", lh.layout,name)
        #self.parent = parent
        VisibleComponent.__init__(self,name,**kw)
        self.lh = lh
        if lh is not None:
            assert isinstance(lh,layouts.LayoutHandle)
            lh.setup_element(self)

    def submit_fields(self):
        return []
        
        
    def get_property(self,name):
        v = getattr(self,name,None)
        if self.parent is None or v is not None:
            return v
        return self.parent.get_property(name)
        
    def get_column_options(self,**kw):
        kw.update(
          dataIndex=self.name, 
          editable=self.editable,
          header=unicode(self.label) if self.label else self.name,
          sortable=self.sortable
          )
        w = self.width or self.preferred_width
        kw.update(width=w*EXT_CHAR_WIDTH)
        return kw    
        
    def set_parent(self,parent):
        if self.parent is not None:
            raise Exception("%s : parent is already %s, cannot set it to %s" % (self,self.parent,parent))
        self.parent = parent
        if self.label:
            if parent.labelAlign == layouts.LABEL_ALIGN_LEFT:
                self.preferred_width += len(self.label)

    def ext_options(self,**kw):
        kw = VisibleComponent.ext_options(self,**kw)
        if self.xtype is not None:
            kw.update(xtype=self.xtype)
        if self.collapsible:
            kw.update(collapsible=self.collapsible)
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
    declare_type = jsgen.DECLARE_INLINE
    value_template = "new Ext.BoxComponent(%s)"
    vflex = True
    
    def __init__(self,lh,name,picture,**kw):
        kw.update(autoEl=dict(tag='img'))
        #~ kw.update(cls='ext-el-mask')
        kw.update(style=dict(height='100%'))
        kw.update(plugins=js_code('new Lino.PictureBoxPlugin(caller)'))
        LayoutElement.__init__(self,lh,name,**kw)

        

class StaticTextElement(LayoutElement):
    declare_type = jsgen.DECLARE_INLINE
    #declare_type = jsgen.DECLARE_THIS
    #~ declare_type = jsgen.DECLARE_VAR
    xtype = 'label'
    
    def __init__(self,lh,name,text,**kw):
        LayoutElement.__init__(self,lh,name,**kw)
        self.text = text

    def ext_options(self,**kw):
        #kw = super(StaticTextElement,self).ext_options(**kw)
        kw = LayoutElement.ext_options(self,**kw)
        #kw.update(xtype=self.xtype)
        kw.update(html=self.text.text)
        return kw
        
        
        

class Spacer(LayoutElement):
    declare_type = jsgen.DECLARE_INLINE
    #xtype = 'label'
    value_template = "new Ext.Spacer(%s)"
    
        
class unused_VirtualFieldElement(LayoutElement):
    def __init__(self,lh,name,gfk,**kw):
        assert isinstance(gfk,generic.GenericForeignKey)
        self.gfk = gfk
        LayoutElement.__init__(self,lh,name,label=name,**kw)
        #print "20091210", name,gfk
        
    def ext_options(self,**kw):
        kw = LayoutElement.ext_options(self,**kw)
        #kw.update(maxHeight=self.preferred_height*EXT_CHAR_HEIGHT)
    
        
        
class FieldElement(LayoutElement):
    declare_type = jsgen.DECLARE_INLINE
    #declare_type = jsgen.DECLARE_THIS
    #~ declare_type = jsgen.DECLARE_VAR
    stored = True
    #declaration_order = 3
    ext_suffix = "_field"
    
    def __init__(self,lh,field,**kw):
        assert field.name, Exception("field %r has no name!" % field)
        self.field = field
        self.editable = field.editable and not field.primary_key
        LayoutElement.__init__(self,lh,field.name,label=unicode(field.verbose_name),**kw)
        
    #~ def get_column_options(self,**kw):
        #~ kw = LayoutElement.get_column_options(self,**kw)
        #~ if self.editable:
            #~ fo = self.get_field_options()
            #~ kw.update(editor=fo)
        #~ return kw    
        
    def submit_fields(self):
        return [self.field.name]
        
    def get_field_options(self,**kw):
        if self.xtype:
            kw.update(xtype=self.xtype)
        kw.update(name=self.name)
        #~ kw.update(anchor="100%")
        #~ kw.update(anchor="100% 100%")
        #kw.update(style=dict(padding='0px'),color='green')
        if self.label:
            kw.update(fieldLabel=unicode(self.label))
        if not self.field.blank:
            kw.update(allowBlank=False)
        if not self.editable:
            kw.update(readOnly=True)
        #kw.update(maxHeight=self.preferred_height*EXT_CHAR_HEIGHT)
        return kw
        
    def ext_options(self,**kw):
        """
        ExtJS renders fieldLabels only if the field's Container has layout 'form', so we create a panel around each field
        """
        kw = LayoutElement.ext_options(self,**kw)
        kw.update(self.get_field_options())
        #~ h = self.preferred_height*EXT_CHAR_HEIGHT
        #~ kw.update(minHeight=h)
        #~ kw.update(height=h)
        #kw.update(flex=0)
        #kw.update(xtype='panel',layout='form') 
        #kw.update(style=dict(padding='0px'),color='green')
        #kw.update(hideBorders=True)
        #kw.update(margins='0')
        return kw
        #~ kw.update(xtype='container',layout='form')
        #~ kw.update(items=self.get_field_options())
        #~ return kw
    
        
        
class TextFieldElement(FieldElement):
    #~ xtype = 'textarea'
    vflex = True
    value_template = "new Ext.form.HtmlEditor(%s)"
    xtype = None
    #~ xtype = 'htmleditor'
    #width = 60
    preferred_width = 60
    preferred_height = 3
    #collapsible = True

    #~ def get_field_options(self,**kw):
        #~ kw = FieldElement.get_field_options(self,**kw)
        #~ kw.update(anchor="100% 100%")
        #~ return kw
        
class CharFieldElement(FieldElement):
    #~ xtype = "textfield"
    sortable = True
    value_template = "new Ext.form.TextField(%s)"
    xtype = None
  
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        self.preferred_width = min(20,self.field.max_length)
        #~ if self.width is None and self.field.max_length < 10:
            #~ # "small" texfields should not be expanded, so they get an explicit width
            #~ self.width = self.field.max_length
        #~ if self.field.choices...
            #~ self.value_template = "new Ext.form.ComboBox(%s)"
            
    def get_field_options(self,**kw):
        kw = FieldElement.get_field_options(self,**kw)
        kw.update(maxLength=self.field.max_length)
        return kw
        
#~ class PropertyElement(LayoutElement):        
    #~ def __init__(self,lh,prop,**kw):
        #~ assert field.name, Exception("field %r has no name!" % field)
        #~ LayoutElement.__init__(self,lh,prop.name,label=prop.label,**kw)
        #~ self.prop = prop
        #~ self.editable = True
        #~ self.delegate = field2e
        #~ value_type = prop.value_type._meta.get_field value
        #~ fk, remote, direct, m2m = self.model._meta.get_field_by_name(self.fk_name)
        #~ FieldElement.__init__(self,lh,value_type)
        #~ delegate = lh.main_class.field2elem(lh,return_type,**kw)
        #~ for a in ('ext_options','get_column_options','get_field_options','grid_column_template'):
            #~ setattr(self,a,getattr(delegate,a))

        
class ForeignKeyElement(FieldElement):
    #xtype = "combo"
    sortable = True
    #width = 20
    value_template = "new Ext.form.ComboBox(%s)"
    
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        self.report = reports.get_model_report(self.field.rel.to)
      
    def submit_fields(self):
        return [self.field.name,self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX]
        
    def store_options(self,**kw):
        proxy = dict(url=self.lh.ui.get_choices_url(self),method='GET')
        kw.update(proxy=js_code(
          "new Ext.data.HttpProxy(%s)" % py2js(proxy)
        ))
        # a JsonStore without explicit proxy sometimes used method POST
        # kw.update(autoLoad=True)
        kw.update(totalProperty='count')
        kw.update(root='rows')
        kw.update(id=ext_requests.CHOICES_VALUE_FIELD) # self.report.model._meta.pk.name)
        kw.update(fields=[ext_requests.CHOICES_VALUE_FIELD,ext_requests.CHOICES_TEXT_FIELD])
        #~ kw.update(listeners=dict(exception=js_code("Lino.on_store_exception")))
        kw.update(listeners=dict(exception=js_code("Lino.on_store_exception")))
        return kw
      
        
    def get_field_options(self,**kw):
        # see blog 20100222
        kw = FieldElement.get_field_options(self,**kw)
        kw.update(mode='remote')
        #setup_report(self.report)
        #kw.update(store=self.rh.store)
        sto = self.store_options()
        #print repr(sto)
        kw.update(store=js_code("new Ext.data.JsonStore(%s)" % py2js(sto)))
        #kw.update(store=js_code(self.store.as_ext_value(request)))
        kw.update(hiddenName=self.name+ext_requests.CHOICES_HIDDEN_SUFFIX)
        kw.update(valueField=ext_requests.CHOICES_VALUE_FIELD) #self.report.model._meta.pk.name)
        #kw.update(valueField='id')
        #kw.update(valueField=self.name)
        kw.update(triggerAction='all')
        #kw.update(listeners=dict(beforequery=js_code("function(qe) {console.log('beforequery',qe); return true;}")))
        
        kw.update(submitValue=True)
        kw.update(displayField=ext_requests.CHOICES_TEXT_FIELD) # self.report.display_field)
        kw.update(typeAhead=True)
        kw.update(minChars=2) # default 4 is to much
        kw.update(queryDelay=300) # default 500 is maybe slow
        kw.update(queryParam=ext_requests.URL_PARAM_FILTER)
        kw.update(typeAhead=True)
        #kw.update(typeAheadDelay=300) # default 500 is maybe slow
        kw.update(selectOnFocus=True) # select any existing text in the field immediately on focus.
        kw.update(resizable=True)
        kw.update(pageSize=self.report.page_length)
        kw.update(emptyText='Select a %s...' % self.report.model.__name__)
        # test whether field has a %s_choices() method
        #~ if self.lh.link.report.get_field_choices_meth(self.field): 
            #~ kw.update(contextParam=ext_requests.URL_PARAM_CHOICES_PK)
            #kw.update(lazyInit=True)
        rh = self.lh.layout.datalink_report.get_handle(self.lh.ui)
        chooser = rh.choosers[self.field.name]
        if chooser.context_params:
        #~ cp = chooser.get_context_params(self.lh.link.report.model,self.field.name)
        #~ if cp:    
            kw.update(contextParams=chooser.context_params)
            
        #~ ... hier weiss ich noch nicht...
        #~ if chooser.context_values:
            #~ kw.update(contextValueNames=chooser.chooser.context_values)
            #~ def js():
                #~ yield "  this.add_row_listener(function(sm,rowIndex,record) {" 
                #~ yield "    %s.setContextValues([" % self.as_ext()
                #~ yield "      " + ",".join(["record.data." + name for name in chooser.context_values])
                #~ yield "])})}"
            #~ kw.update(master_listener=js)
        return kw
        
    #~ def js_on_load_record(self):
        #~ for ln in super(ForeignKeyElement,self).js_on_load_record():
            #~ yield ln
        #~ chooser = self.lh.datalink.choosers[self.field.name]
        #~ if chooser.context_values:
            #~ yield "  %s.setContextValues([" % self.as_ext()
            #~ yield ",".join("record.data." + name for name in chooser.context_values]
            #~ yield "]);"

    def js_body(self):
        for ln in super(ForeignKeyElement,self).js_body():
            yield ln
        chooser = self.lh.datalink.choosers[self.field.name]
        if chooser.context_values:
            yield "this.window.on('render',function() {" 
            #~ yield "  console.log(20100311);" 
            yield "  this.add_row_listener(function(sm,rowIndex,record) {" 
            yield "    %s.setContextValues([" % self.as_ext()
            yield "      " + ",".join(["record.data." + name for name in chooser.context_values])
            yield "])})},this);"


        
            
class DateFieldElement(FieldElement):
    xtype = 'datefield'
    data_type = 'date' # for store column
    sortable = True
    preferred_width = 8 
    # todo: DateFieldElement.preferred_width should be computed from Report.date_format
    grid_column_template = "new Ext.grid.DateColumn(%s)"
    
    def get_column_options(self,**kw):
        kw = FieldElement.get_column_options(self,**kw)
        #kw.update(xtype='datecolumn')
        kw.update(format=self.lh.layout.datalink_report.date_format)
        return kw
    
class IntegerFieldElement(FieldElement):
    xtype = 'numberfield'
    sortable = True
    preferred_width = 5
    data_type = 'int' 

class DecimalFieldElement(FieldElement):
    xtype = 'numberfield'
    sortable = True
    data_type = 'float' 
    grid_column_template = "new Ext.grid.NumberColumn(%s)"
    
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        self.preferred_width = min(5,self.field.max_digits) \
                + self.field.decimal_places
                
    def get_column_options(self,**kw):
        kw = FieldElement.get_column_options(self,**kw)
        #kw.update(xtype='numbercolumn')
        kw.update(align='right')
        fmt = "0,000"
        if self.field.decimal_places > 0:
            fmt += "." + ("0" * self.field.decimal_places)
        kw.update(format=fmt)
        return kw
        
                

class BooleanFieldElement(FieldElement):
  
    xtype = 'checkbox'
    data_type = 'boolean' 
    grid_column_template = "new Ext.grid.BooleanColumn(%s)"
    #~ def __init__(self,*args,**kw):
        #~ FieldElement.__init__(self,*args,**kw)
        
    def get_field_options(self,**kw):
        kw = FieldElement.get_field_options(self,**kw)
        del kw['fieldLabel']
        kw.update(boxLabel=self.label)
        return kw
        
    def get_column_options(self,**kw):
        kw = FieldElement.get_column_options(self,**kw)
        #kw.update(xtype='booleancolumn')
        kw.update(trueText=self.lh.layout.datalink_report.boolean_texts[0])
        kw.update(falseText=self.lh.layout.datalink_report.boolean_texts[1])
        kw.update(undefinedText=self.lh.layout.datalink_report.boolean_texts[2])
        return kw
        
    def get_from_form(self,instance,values):
        """
        standard HTML submits checkboxes of a form only when they are checked.
        So if the field is not contained in values, we take False as value.
        """
        instance[self.name] = values.get(self.name,False)



#~ class DelegateFieldElement(FieldElement):

class MethodElement(FieldElement):
    stored = True
    editable = False

    def __init__(self,lh,name,meth,return_type,**kw):
        assert isinstance(lh,layouts.LayoutHandle)
        # uh, this is tricky...
        return_type.name = name
        return_type._return_type_for_method = meth
        FieldElement.__init__(self,lh,return_type)
        delegate = lh.main_class.field2elem(lh,return_type,**kw)
        for a in ('ext_options','get_column_options','get_field_options','grid_column_template'):
            setattr(self,a,getattr(delegate,a))
        

class Container(LayoutElement):
    #ext_template = 'lino/includes/element.js'
    #ext_container = 'Ext.Panel'
    vertical = False
    hpad = 1
    is_fieldset = False
    xtype = 'container'
    
    #declare_type = jsgen.DECLARE_INLINE
    #declare_type = jsgen.DECLARE_THIS
    #declare_type = jsgen.DECLARE_VAR
    #~ declare_type = jsgen.DECLARE_THIS
    
    
    def __init__(self,lh,name,*elements,**kw):
        self.has_frame = lh.layout.has_frame
        self.labelAlign = lh.layout.label_align
        self.elements = elements
        LayoutElement.__init__(self,lh,name,**kw)
        
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
    ext_suffix = "_panel"
    
    def __init__(self,lh,name,vertical,*elements,**kw):
        self.vertical = vertical
        Container.__init__(self,lh,name,*elements,**kw)
        label = lh.layout.collapsible_elements.get(name,None)
        if label:
            self.collapsible = True
            self.label = label
            
        #~ if self.vertical:
            #~ vflex_elems = [e for e in elements if e.vflex]
            #~ if len(flex_elems) > 0:
                #~ assert len(kw) == 0, "%r is not empty" % kw
                #~ vfix_elems = [e for e in elements if not e.vflex]
                #~ flex_panel = Panel(lh,name,vertical,*vflex_elems)
                #~ fix_panel = Panel(lh,name,vertical,*vfix_elems)
                
        """
        A vertical Panel is vflex if and only if at least one of its children is vflex.
        A horizontal Panel is vflex, if and only if *all* its children are vflex 
        (if vflex and non-vflex elements are together in a hbox, then the 
        vflex elements will get the height of the highest non-vflex element).
        """        
        self.vflex = not vertical
        for e in elements:
            if not isinstance(e,LayoutElement):
                raise Exception("%r is not a LayoutElement" % e)
            if self.vertical:
                if e.vflex:
                    self.vflex = True
            else:
                if not e.vflex:
                    self.vflex = False
                    
        if len(elements) > 1 and self.vertical and self.vflex:
            #~ print 20100301, self
            # so we must split this panel into several containers. 
            # vflex elements go into a vbox, the others into a form layout. 
            
            # Rearrange elements into "element groups"
            # Each element of egroups is a list of elements who have same vflex
            egroups = []
            for e in elements:
                if len(egroups) and egroups[-1][0].vflex == e.vflex:
                    egroups[-1].append(e)
                else:
                    egroups.append([e])
                    
            if len(egroups) == 1:
                # all elements are vflex
                assert tuple(egroups[0]) == elements, "%r != %r" % (tuple(egroups[0]), elements)
                
            elements = []
            for eg in egroups:
                if eg[0].vflex:
                    #~ for e in eg: e.update(flex=1,align='stretch')
                    for e in eg: e.update(flex=1)
                    if len(eg) == 1:
                        g = eg[0]
                    else:
                        g = Container(lh,name,*eg,**dict(layout='vbox',flex=1))
                else:
                    #~ for e in eg: e.update(align='stretch')
                    if len(eg) == 1:
                        g = eg[0]
                    else:
                        g = Container(lh,name,*eg,**dict(layout='form',autoHeight=True))
                #~ g.update(align='stretch')
                #~ g.update(layoutConfig=dict(align='stretch'))
                elements.append(g)
            self.update(layout='vbox',layoutConfig=dict(align='stretch'))
            #~ self.value['align'] = 'stretch'
              
        for e in elements:
            e.set_parent(self)
            if isinstance(e,FieldElement):
                self.is_fieldset = True
                #~ if self.label_width < e.label_width:
                    #~ self.label_width = e.label_width
                if e.label:
                    w = len(e.label) + 1 # +1 for the ":"
                    if self.label_width < w:
                        self.label_width = w

        w = h = 0
        for e in elements:
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
        
        d = self.value
        if not d.has_key('layout'):
            if len(elements) == 1:
                d.update(layout='fit')
            elif self.vertical:
                d.update(layout='form')
            else:
                d.update(layout='column')
                
        if d['layout'] == 'form':
            assert self.vertical
            if len(elements) == 1 and elements[0].vflex:
                elements[0].update(anchor="100% 100%")
            else:
                for e in elements:
                    #~ assert not e.vflex
                    #~ h = e.height or e.preferred_height
                    #~ if e.vflex:
                        #~ e.value.update(anchor="100% 100%")
                    #~ else:
                        #~ e.value.update(anchor="100%")
                    e.update(anchor="100%")
        elif d['layout'] == 'column':
            for e in elements:
                w = e.width or e.preferred_width
                e.value.update(columnWidth=float(w)/self.preferred_width)
            
        
        
    def ext_options(self,**d):
        d = Container.ext_options(self,**d)
        if self.collapsible:
            d.update(xtype='panel')
            #~ js = "function(cmp,aw,ah,rw,rh) { console.log('Panel.collapse',this,cmp,aw,ah,rw,rh); this.main_panel.doLayout(); }"
            #~ d.update(listeners=dict(scope=js_code('this'),collapse=js_code(js),expand=js_code(js)))
            #d.update(monitorResize=True)
        #~ else:
            #~ d.update(xtype='container')
        #d.update(margins='0')
        #d.update(style=dict(padding='0px'))
        
        d.update(items=self.elements)
        #l = [e.as_ext() for e in self.elements ]
        #d.update(items=js_code("[\n  %s\n]" % (", ".join(l))))
        #d.update(items=js_code("this.elements"))
        
        if self.is_fieldset:
            d.update(labelWidth=self.label_width * EXT_CHAR_WIDTH)
            
        if self.vertical:
            #d.update(frame=self.has_frame)
            d.update(frame=True)
            d.update(bodyBorder=False)
            d.update(border=False)
            d.update(labelAlign=self.labelAlign)
            #d.update(style=dict(padding='0px'),color='green')
        else:
            d.update(frame=False)
            #d.update(bodyBorder=False)
            d.update(border=False)
            
        return d
        


#~ class DataElementMixin:
    #~ "common for Grids, Details and Forms"
  

class GridElement(Container): #,DataElementMixin):
    #value_template = "new Ext.grid.EditorGridPanel(%s)"
    #~ value_template = "new Ext.grid.GridPanel(%s)"
    value_template = "new Lino.GridPanel(%s)"
    ext_suffix = "_grid"
    vflex = True
    
    def __init__(self,lh,name,rpt,*elements,**kw):
        """
        Note: lh is the owning layout handle, rpt is the report being displayed by this GridElement.
        """
        assert isinstance(rpt,reports.Report), "%r is not a Report!" % rpt
        self.report = rpt
        #~ assert isinstance(rh,reports.ReportHandle), "%r is not a ReportHandle!" % rh
        if len(elements) == 0:
            self.rh = rpt.get_handle(lh.ui)
            elements = self.rh.list_layout._main.elements
        w = 0
        for e in elements:
            w += (e.width or e.preferred_width)
        self.preferred_width = constrain(w,10,120)
        
        Container.__init__(self,lh,name,*elements,**kw)
        #DataElementMixin.__init__(self,rh)
        #self.dl = rh
        
        # override Container's height algorithm
        self.preferred_height = rpt.page_length 
        #~ ADD_GRID_HEIGHT = 4 # experimental value...
        #~ if self.height:
            #~ self.height += ADD_GRID_HEIGHT
        #~ else:
            #~ self.preferred_height += ADD_GRID_HEIGHT
        
        #~ self.rh = rh
        #~ lh.needs_store(rh)
        self.column_model = ColumnModel(self)
        #self.mt = ContentType.objects.get_for_model(self.report.model).pk
        if self.report.master is not None:
            self.mt = ContentType.objects.get_for_model(self.report.master).pk
        else:
            self.mt = 'undefined'

        
          
    def unused_subvars(self):
        """
        GridElement, unlike Container, doesn't generate the declaration of its elements 
        because self.column_model does this indirectly.
        """
        #self.setup()
        #yield self.rh.store
        yield self.column_model

    def ext_options(self,**d):
        #~ self.setup()
        rh = self.report.get_handle(self.lh.ui)
        d = LayoutElement.ext_options(self,**d)
        d.update(clicksToEdit=2)
        d.update(viewConfig=dict(
          #autoScroll=True,
          #autoFill=True,
          #forceFit=True,
          #enableRowBody=True,
          showPreview=True,
          scrollOffset=200,
          emptyText="Nix gefunden!"
        ))
        #d.update(autoScroll=True)
        #d.update(fitToFrame=True)
        d.update(emptyText="Nix gefunden...")
        #~ d.update(store=rh.store) # js_code(self.rh.store.ext_name))
        #~ d.update(ls_data_url=rh.store) # js_code(self.rh.store.ext_name))
        d.update(ls_data_url=rh.ui.get_actor_url(rh.report)) 
        d.update(ls_store_fields=[js_code(f.as_js()) for f in rh.store.fields]) 
        d.update(colModel=self.column_model)
        #d.update(colModel=js_code('this.cols'))
        #d.update(colModel=js_code(self.column_model.ext_name))
        #~ d.update(autoHeight=True)
        #d.update(layout='fit')
        d.update(enableColLock=False)
        d.update(ls_quick_edit=True)
        d.update(ls_content_type=rh.report.content_type)
        
        #~ def a2btn(a):
            #~ return dict(
              #~ handler=js_code("Lino.%s.createCallback(this)" % a),
              #~ text=unicode(a.label),
            #~ )
        
        #~ d.update(bbar=[a2btn(a) for a in rh.get_actions() if not a.hidden])
        d.update(ls_bbar_actions=[a2btn(a) for a in rh.get_actions() if not a.hidden])
        #~ d.update(ls_bbar_actions=[a for a in rh.get_actions() if not a.hidden])
        
        
        return d
        
def a2btn(a):
    return dict(
      opens_a_slave=a.opens_a_slave,
      handler=js_code("Lino.%s" % a),
      name=a.name,
      label=unicode(a.label),
      #~ url="/".join(("/ui",a.actor.app_label,a.actor._actor_name,a.name))
    )
      
class SlaveGridElement(GridElement):
    def ext_options(self,**kw):
        kw = GridElement.ext_options(self,**kw)
        kw.update(plugins=js_code('new Lino.SlaveGridPlugin(caller)'))
        
        kw.update(title=unicode(self.report.label))
        
        #~ js = "Lino.do_action(caller,%r)" % \
            #~ rh.list_layout.get_absolute_url(run=True)
        #~ js = "function(){ Lino.notify('Das ist noch nicht fertig... siehe ext_elems.py:990');}"
        #~ kw.update(listeners=dict(click=js_code(js)))
        return kw
      
        
class M2mGridElement(GridElement):
    def __init__(self,lh,field,*elements,**kw):
        self.field = field
        rpt = reports.get_model_report(field.rel.to)
        #~ rh = rpt.get_handle(lh.ui)
        GridElement.__init__(self,lh,id2js(rpt.actor_id),rpt,*elements,**kw)
  

            
class MainPanel(jsgen.Variable):
    declare_type = jsgen.DECLARE_INLINE
  
    def __init__(self):
        self.keys = None
        self.buttons = None
        #~ self.cmenu = None
        #~ self.props_button = None
        
    def unused_get_datalink(self):
        raise NotImplementedError
        
    def apply_window_config(self,wc):
        pass
  
    def setup(self):
        pass
        #~ if self.keys:
            #~ return
        #~ keys = []
        #~ buttons = []
        #~ dl = self.get_datalink() # the ReportHandle
            
        #~ self.keys = Variable(self.ext_name+'_keys',keys)
        #~ self.buttons = Variable(self.ext_name+'_buttons',buttons)
        #~ self.cmenu = Variable('cmenu',js_code("new Ext.menu.Menu(%s)" % py2js(self.buttons)))
        
    #~ def subvars(self):
        #~ self.setup()
        #~ for rh in self.lh._needed_stores:
            #~ yield rh.store
        
  
    #~ def js_body(self):
        #~ yield "this.content_type = %s;" % py2js(self.lh.datalink.content_type)
        #~ for ln in jsgen.Variable.js_body(self):
            #~ yield ln
        
                
    @classmethod
    def field2elem(cls,lh,field,**kw):
        for cl,x in _field2elem:
            if isinstance(field,cl):
                return x(lh,field,**kw)
        raise NotImplementedError("No LayoutElement for %s" % field.__class__)
        #~ raise NotImplementedError("field %r" % field)



class WrappingMainPanel(MainPanel):
    """Inherited by DetailMainPanel and FormMainPanel (not GridPanel)
    Wraps each FieldElement into a Panel with FormLayout.
    """
    
    @classmethod
    def field2elem(cls,lh,field,**kw):
        e = MainPanel.field2elem(lh,field,**kw)
        po = dict(layout='form')
        #~ if isinstance(e,TextFieldElement):
            #~ po.update(anchor='100% 100%')
        ct = Panel(lh,field.name+"_ct",True,e,**po)#,flex=0)
        ct.field = field
        return ct

class GridMainPanel(GridElement,MainPanel):
    #~ value_template = "new Lino.GridPanel(%s)"
    def __init__(self,lh,name,vertical,*elements,**kw):
        'ignore the "vertical" arg'
        #lh.report.setup()
        #~ self.pager = None
        MainPanel.__init__(self)
        GridElement.__init__(self,lh,name,lh.layout.datalink_report,*elements,**kw)
        #lino.log.debug("GridMainPanel.__init__() %s",self.name)
        
    #~ def setup(self):
        #~ if self.pager is not None:
            #~ return
        #~ MainPanel.setup(self)
        #~ self.pager = PagingToolbar(self,'pager')
        
    #~ def apply_window_config(self,wc):
        #~ i = 0
        #~ for w in wc.column_widths:
            #~ self.column_model.columns[i].update(width=w)
            #~ i += 1
        
    #~ def subvars(self):
        #~ for e in GridElement.subvars(self):
            #~ yield e
        #~ for e in MainPanel.subvars(self):
            #~ yield e
        #~ yield self.pager
        
    #~ def unused_get_datalink(self):
        #~ return self.rh
        
    #~ def ext_options(self,**kw):
        #~ self.setup()
        #~ kw = GridElement.ext_options(self,**kw)
        #~ del kw['autoHeight']
        #~ del kw['title']
        #~ kw.update(selModel=js_code("new Ext.grid.RowSelectionModel({singleSelect:false})"))
        #~ kw.update(tbar=self.pager)
        #~ return kw



class DetailMainPanel(Panel,WrappingMainPanel):
    #~ declare_type = jsgen.DECLARE_THIS
    #~ xtype = 'form'
    xtype = None
    #~ value_template = "new Ext.form.FormPanel(%s)"
    value_template = "new Ext.Panel(%s)"
    def __init__(self,lh,name,vertical,*elements,**kw):
        #~ self.rh = lh.datalink
        self.report = lh.layout.datalink_report
        MainPanel.__init__(self)
        #~ DataElementMixin.__init__(self,lh.link)
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
        kw.update(title=unicode(self.lh.layout.label))
        #d.update(region='east',split=True) #,width=300)
        kw.update(autoScroll=True)
        if False:
            kw.update(tbar=js_code("""new Ext.PagingToolbar({
              store: %s,
              displayInfo: true,
              pageSize: 1,
              prependButtons: true,
            }) """ % self.rh.store.ext_name))
        #d.update(items=js_code(self._main.as_ext(request)))
        #d.update(items=js_code("[%s]" % ",".join([e.as_ext() for e in self.elements])))
        kw.update(items=self.elements)
        #d.update(autoHeight=False)
        #~ kw.update(bbar=self.bbar_buttons)
        #~ kw.update(bbar=self.buttons)
        #d.update(standardSubmit=True)
        return kw
        
class TabPanel(jsgen.Value):
    value_template = "new Ext.TabPanel(%s)"
    #~ def __init__(self,lh,name,*elements,**options):
        #~ Container.__init__(self,lh,name,*elements,**options)
        #~ self.width = self.elements[0].ext_width() or 300
        
    def __init__(self,tabs,**kw):
        kw.update(
          split=True,
          activeTab=0,
          #~ autoScroll=True, 
          #~ width=300, # ! http://code.google.com/p/lino/wiki/20100513
          items=tabs,
          # http://www.extjs.com/forum/showthread.php?26564-Solved-FormPanel-in-a-TabPanel
          #~ listeners=dict(activate=js_code("function(p) {p.doLayout();}"),single=True),
        )
        jsgen.Value.__init__(self,kw)

        
class FormPanel(jsgen.Value):
    value_template = "new Ext.form.FormPanel(%s)"
    def __init__(self,main,**kw):
        kw.update(
          items=main,
          #~ autoScroll=True,
          layout='fit',
        )
        jsgen.Value.__init__(self,kw)

class unused_FormMainPanel(Panel,WrappingMainPanel):
    value_template = "new Ext.form.FormPanel(%s)"
    
    def __init__(self,lh,name,vertical,*elements,**kw):
        #DataElementMixin.__init__(self,lh.link)
        Panel.__init__(self,lh,name,vertical,*elements,**kw)
        MainPanel.__init__(self)

    def unused_get_datalink(self):
        return self.lh.datalink
        
    def ext_options(self,**d):
        d = Panel.ext_options(self,**d)
        #d.update(title=self.lh.label)
        #d.update(region='east',split=True) #,width=300)
        d.update(autoScroll=True)
        #d.update(items=js_code("[%s]" % ",".join([e.as_ext() for e in self.elements])))
        d.update(items=self.elements)
        d.update(autoHeight=False)
        return d
        
    def subvars(self):
        for e in WrappingMainPanel.subvars(self):
            yield e
        for e in Panel.subvars(self):
            yield e
            

    def unused_js_body(self):
        yield "  this.get_values = function() {"
        yield "    var v = {};"
        for e in self.lh.datalink.inputs:
            yield "    v[%r] = this.main_panel.getForm().findField(%r).getValue();" % (e.name,e.name)
        yield "    return v;"
        yield "  };"
        yield "this.get_window_config = function() {"
        yield "  return { 'window_type': 'form' }"
        yield "}"

_field2elem = (
    (models.TextField, TextFieldElement),
    (models.CharField, CharFieldElement),
    (models.DateField, DateFieldElement),
    (models.IntegerField, IntegerFieldElement),
    (models.DecimalField, DecimalFieldElement),
    (models.BooleanField, BooleanFieldElement),
    (models.ManyToManyField, M2mGridElement),
    (models.ForeignKey, ForeignKeyElement),
    (models.AutoField, IntegerFieldElement),
    (models.EmailField, CharFieldElement),
    #~ (properties.Property, PropertyElement),
)
    

