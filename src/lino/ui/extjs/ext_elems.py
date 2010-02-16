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

from lino import layouts, reports, actions

from lino.utils import constrain
from lino.utils import jsgen
from lino.utils.jsgen import py2js, Variable, Component, id2js, js_code

from lino.ui.extjs import ext_requests

from lino.modlib.properties import models as properties # import Property, CharPropValue

EXT_CHAR_WIDTH = 9
EXT_CHAR_HEIGHT = 22



class ColumnModel(Component):
    declare_type = jsgen.DECLARE_THIS
    #declare_type = jsgen.DECLARE_VAR
    #declare_type = jsgen.DECLARE_INLINE
    ext_suffix = "_cols"
    value_template = "new Ext.grid.ColumnModel(%s)"
    #declaration_order = 2
    
    def __init__(self,grid):
        self.grid = grid
        Component.__init__(self,grid.name)
        self.columns = [GridColumn(e) for e in self.grid.elements]
        
    def subvars(self):
        for col in self.columns:
            yield col.editor
            yield col
        
        
    def ext_options(self):
        #self.report.setup()
        d = Component.ext_options(self)
        #d.update(columns=[e.get_column_options() for e in self.grid.elements])
        d.update(columns=self.columns)
        #d.update(defaultSortable=True)
        return d
        
class GridColumn(Component):
    declare_type = jsgen.DECLARE_VAR
    ext_suffix = "_col"
    value_template = "new Ext.grid.Column(%s)"
    
    def __init__(self,editor,**kw):
        Component.__init__(self,editor.name,**kw)
        self.editor = editor
        self.value_template = editor.grid_column_template
    
        #~ if self.editable:
            #~ editor = self.get_field_options()
        
    def ext_options(self,**kw):
        kw = Component.ext_options(self,**kw)
        kw.update(self.editor.get_column_options())
        kw.update(editor=self.editor)
        return kw
        
class ComboBox(Component):
    value_template = 'new Ext.form.ComboBox(%s)'
                    
        
        
class VisibleComponent(Component):
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
    
    def __init__(self,lh,name,**kw):
        #lino.log.debug("LayoutElement.__init__(%r,%r)", lh.layout,name)
        #self.parent = parent
        VisibleComponent.__init__(self,name,**kw)
        self.lh = lh
        if lh is not None:
            assert isinstance(lh,layouts.LayoutHandle)
            #assert isinstance(layout,Layout), "%r is not a Layout" % layout
            #self.ext_name = layout.name + "_" + name + self.ext_suffix
            #self.ext_name = name
            #~ if self.declared:
                #~ self.layout.report.add_variable(self)
                

        
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
        
    #~ def as_ext_column(self):
        #~ return py2js(self.get_column_options())
        
    def set_parent(self,parent):
        if self.parent is not None:
            raise Exception("%s : parent is already %s, cannot set it to %s" % (self,self.parent,parent))
        self.parent = parent
        if self.label:
            if parent.labelAlign == layouts.LABEL_ALIGN_LEFT:
                self.preferred_width += len(self.label)
            #~ elif parent.labelAlign == layouts.LABEL_ALIGN_TOP:
                #~ self.preferred_height += 1
        #~ if self.flex is None:
            #~ if parent.vertical:
                #~ self.flex = self.height or self.preferred_height
            #~ else:
                #~ self.flex = self.width or self.preferred_width

    def ext_options(self,**kw):
        kw = VisibleComponent.ext_options(self,**kw)
        #~ if self.flex is not None:
            #~ kw.update(flex=self.flex)
        #~ if self.width is None:
            #~ """
            #~ an element without explicit width will get flex=1 when in a hbox, otherwise anchor="100%".
            #~ """
            #~ if self.parent is not None:
                #~ if self.parent.vertical:
                    #~ kw.update(anchor="100%")
                #~ else:
                    #~ kw.update(flex=1)
            #~ else:
                #~ lino.log.warning("%s %s : parent is None",self.__class__.__name__,self.ext_name)
        #~ else:
            #~ kw.update(width=self.ext_width())
        #~ if self.height is not None:
            #~ kw.update(height=self.height * EXT_CHAR_HEIGHT)
        if self.xtype is not None:
            kw.update(xtype=self.xtype)
        if self.collapsible:
            kw.update(collapsible=self.collapsible)
        return kw
        
    def js_column_lines(self,grid):
        return []
        
    #~ def ext_width(self):
        #~ if self.width is None:
            #~ return None
        #~ #if self.parent.labelAlign == 'top':
        #~ return max(self.width,self.label_width) * EXT_CHAR_WIDTH + self.xpadding
        
class InputElement(LayoutElement):
    #declare_type = jsgen.DECLARE_INLINE
    declare_type = jsgen.DECLARE_THIS
    #declare_type = jsgen.DECLARE_VAR
    ext_suffix = "_input"
    xtype = 'textfield'
    preferred_height = 0
    field = None 
    
    def __init__(self,lh,input,**kw):
        #lino.log.debug("InputElement.__init__(%r,%r)",lh,input)
        LayoutElement.__init__(self,lh,input.name,**kw)
        assert isinstance(lh.layout,layouts.FormLayout), "%s is not a FormLayout" % lh.name
        self.input = input
        
    def ext_options(self,**kw):
        kw = LayoutElement.ext_options(self,**kw)
        kw.update(self.input.options)
        kw.update(name=self.name)
        kw.update(id=self.name)
        #kw.update(xtype='textfield')
        panel_options = dict(xtype='container',layout='form',items=kw)
        #panel_options.update(maxHeight=self.preferred_height*EXT_CHAR_HEIGHT)
        return panel_options
        
class ButtonElement(LayoutElement):
    #declare_type = jsgen.DECLARE_INLINE
    #declare_type = jsgen.DECLARE_THIS
    declare_type = jsgen.DECLARE_VAR
    ext_suffix = "_btn"
    xtype = 'button'
    preferred_height = 0

    def __init__(self,lh,name,action,**kw):
        #lino.log.debug("ButtonElement.__init__(%r,%r,%r)",lh,name,action)
        LayoutElement.__init__(self,lh,name,**kw)
        assert isinstance(lh.layout,layouts.Layout), "%s is not a Layout" % lh.name
        self.action = action
        
    def ext_options(self,**kw):
        #kw = super(StaticTextElement,self).ext_options(**kw)
        kw = LayoutElement.ext_options(self,**kw)
        #kw.update(xtype=self.xtype)
        label = self.action.label or self.name
        kw.update(text=label)
        #kw.update(maxHeight=self.preferred_height*EXT_CHAR_HEIGHT)
        kw.update(maxWidth=len(label)*EXT_CHAR_WIDTH)
        kw.update(id=self.name)
        if self.lh.default_button == self:
            kw.update(plugins='defaultButton')
        kw.update(handler=js_code('Lino.form_action(this,%r,%s,%r)' % (
          self.name,py2js(self.action.needs_validation),self.lh.ui.get_button_url(self))))
        return kw


class StaticTextElement(LayoutElement):
    #declare_type = jsgen.DECLARE_INLINE
    #declare_type = jsgen.DECLARE_THIS
    declare_type = jsgen.DECLARE_VAR
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

class PropertiesWindow(Component):
    declare_type = jsgen.DECLARE_THIS
    #ext_suffix = "_props"
    value_template = "new Ext.Window(%s)"
    
    def __init__(self,ui,model,props):
        self.ui = ui
        self.model = model
        Component.__init__(self,'props')
        self.source = {}
        self.customEditors = {}
        self.propertyNames = {}
        for p in props:
            # PropValue model
            pvm = p.value_type.model_class()
            assert pvm is not None, ('%s.value_type.model_class() returned None'%p)
            # PropValue field
            pvf = pvm._meta.get_field('value') 
            default = pvf.default
            if default is models.NOT_PROVIDED:
                default = ''
            elif callable(default):
                default = default()
            self.source[p.name] = default 
            if p.label:
                self.propertyNames[p.name] = p.label
                
            if pvm is properties.CHAR:
                choices = [unicode(pv.value) for pv in pvm.objects.filter(prop=p,owner_id__isnull=True)]
                if choices:
                    editor = ComboBox(store=choices,mode='local',selectOnFocus=True)
                    editor = 'new Ext.grid.GridEditor(%s)' % py2js(editor)
                    self.customEditors[p.name] = js_code(editor)
    

    def ext_options(self,**kw):
        kw = Component.ext_options(self,**kw)
        grid = dict(xtype='propertygrid')
        grid.update(source=self.source,
          autoHeight=True)
        grid.update(customEditors=self.customEditors)
        url = self.ui.get_props_url(self.model)
        listeners = dict(
          afteredit=js_code('Lino.grid_afteredit(this,"%s")' % url))
        grid.update(listeners=listeners)
        if len(self.propertyNames) > 0:
            grid.update(propertyNames=self.propertyNames)
        kw.update(layout='fit',items=grid)
        return kw
    

#~ class PropertyGridElement(LayoutElement):
    #~ #declare_type = jsgen.DECLARE_INLINE
    #~ declare_type = jsgen.DECLARE_THIS
    #~ #declare_type = jsgen.DECLARE_VAR
    #~ xtype = 'propertygrid'
    #~ #value_template = 'new Ext.grid.PropertyGrid(%s)'
    #~ ext_suffix = '_pgrid'

    
    #~ def __init__(self,lh,name,pgrid,**kw):
        #~ LayoutElement.__init__(self,lh,name,**kw)
        #~ self.pgrid = pgrid
        #~ # fill the grid rows
        #~ self.source = {}
        #~ self.customEditors = {}
        #~ self.propertyNames = {}
        #~ for p in Property.properties_for_model(self.lh.link.report.model):
            #~ # PropValue model
            #~ pvm = p.value_type.model_class() 
            #~ # PropValue field
            #~ pvf = pvm._meta.get_field('value') 
            #~ default = pvf.default
            #~ if default is models.NOT_PROVIDED:
                #~ default = ''
            #~ elif callable(default):
                #~ default = default()
            #~ self.source[p.name] = default 
            #~ if p.label:
                #~ self.propertyNames[p.name] = p.label
                
            #~ if pvm is CharPropValue:
                #~ choices = [unicode(pv.value) for pv in pvm.objects.filter(prop=p,owner_id__isnull=True)]
                #~ if choices:
                    #~ editor = ComboBox(store=choices,mode='local',selectOnFocus=True)
                    #~ editor = 'new Ext.grid.GridEditor(%s)' % py2js(editor)
                    #~ self.customEditors[p.name] = js_code(editor)
    

    #~ def ext_options(self,**kw):
        #~ kw = LayoutElement.ext_options(self,**kw)
        #~ #kw.update(title='Properties')
        #~ kw.update(source=self.source,
          #~ autoHeight=True)
        #~ kw.update(customEditors=self.customEditors)
        #~ if len(self.propertyNames) > 0:
            #~ kw.update(propertyNames=self.propertyNames)
        #~ return kw


class Spacer(LayoutElement):
    declare_type = jsgen.DECLARE_INLINE
    #xtype = 'label'
    value_template = "new Ext.Spacer(%s)"
    
        
class VirtualFieldElement(LayoutElement):
    def __init__(self,lh,name,gfk,**kw):
        assert isinstance(gfk,generic.GenericForeignKey)
        self.gfk = gfk
        LayoutElement.__init__(self,lh,name,label=name,**kw)
        #print "20091210", name,gfk
        
    def ext_options(self,**kw):
        kw = LayoutElement.ext_options(self,**kw)
        #kw.update(maxHeight=self.preferred_height*EXT_CHAR_HEIGHT)
    
        
        
class FieldElement(LayoutElement):
    #declare_type = jsgen.DECLARE_INLINE
    #declare_type = jsgen.DECLARE_THIS
    declare_type = jsgen.DECLARE_VAR
    stored = True
    #declaration_order = 3
    ext_suffix = "_field"
    
    def __init__(self,lh,field,**kw):
        assert field.name, Exception("field %r has no name!" % field)
        LayoutElement.__init__(self,lh,field.name,label=field.verbose_name,**kw)
        self.field = field
        self.editable = field.editable and not field.primary_key
        
    #~ def get_column_options(self,**kw):
        #~ kw = LayoutElement.get_column_options(self,**kw)
        #~ if self.editable:
            #~ fo = self.get_field_options()
            #~ kw.update(editor=fo)
        #~ return kw    
        
    def get_field_options(self,**kw):
        if self.xtype:
            kw.update(xtype=self.xtype)
        kw.update(name=self.name)
        kw.update(anchor="100%")
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
    xtype = 'textarea'
    #width = 60
    preferred_width = 60
    preferred_height = 3
    #collapsible = True

class CharFieldElement(FieldElement):
    xtype = "textfield"
    sortable = True
  
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        self.preferred_width = min(20,self.field.max_length)
        #~ if self.width is None and self.field.max_length < 10:
            #~ # "small" texfields should not be expanded, so they get an explicit width
            #~ self.width = self.field.max_length
            
    def get_field_options(self,**kw):
        kw = FieldElement.get_field_options(self,**kw)
        kw.update(maxLength=self.field.max_length)
        return kw

        
class ForeignKeyElement(FieldElement):
    #xtype = "combo"
    sortable = True
    #width = 20
    value_template = "new Ext.form.ComboBox(%s)"
    
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        #self.report = self.lh.link.report.get_field_choices(self.field)
        self.report = reports.get_model_report(self.field.rel.to)
        #self.report = rd.get_handle(self.lh.ui)
        #self.rh = self.report.get_handle(self.lh.ui)
        #self.lh.needs_store(self.rh)
        #~ if self.editable:
            #~ setup_report(self.choice_report)
            #self.store = rpt.choice_store
            #self.layout.choice_stores.append(self.store)
            #self.report.setup()
            #self.store = Store(rpt,autoLoad=True)
            #self.layout.report.add_variable(self.store)
      
    #~ def ext_variables(self):
        #~ #yield self.store
        #~ setup_report(self.report)
        #~ yield self.report.choice_layout.store
        #~ yield self
        
    def unused_get_column_options(self,**kw):
        kw = FieldElement.get_column_options(self,**kw)
        #kw.update(dataIndex=self.name+CHOICES_HIDDEN_SUFFIX)
        #js = "function(v, meta, rec, row, col, store) {return rec.data.%s}" % (self.name+CHOICES_HIDDEN_SUFFIX)
        # js = "function(v, meta, rec, row, col, store) {return v.text}" 
        #js = "function(v, meta, rec, row, col, store) {return v[1]}" 
        #kw.update(renderer=js_code('Lino.ForeignKeyRenderer(%r)' % (self.name+"Hidden") ))
        #kw.update(renderer=js_code(js))
        return kw    
        
    def store_options(self,**kw):
        proxy = dict(url=self.lh.ui.get_choices_url(self),method='GET')
        kw.update(proxy=js_code(
          "new Ext.data.HttpProxy(%s)" % py2js(proxy)
        ))
        # a JsonStore without explicit proxy sometimes used method POST
        # d.update(url=self.rr.get_absolute_url(json=True))
        # d.update(method='GET')
        # kw.update(autoLoad=True)
        kw.update(totalProperty='count')
        kw.update(root='rows')
        kw.update(id=ext_requests.CHOICES_VALUE_FIELD) # self.report.model._meta.pk.name)
        kw.update(fields=[ext_requests.CHOICES_VALUE_FIELD,ext_requests.CHOICES_TEXT_FIELD])
        #~ kw.update(listeners=dict(exception=js_code("Lino.on_store_exception")))
        listeners = dict(exception=js_code("Lino.on_store_exception"))
        kw.update(listeners=listeners)
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
        if self.lh.link.report.get_field_choices_meth(self.field): 
            kw.update(contextParam=ext_requests.URL_PARAM_CHOICES_PK)
            #kw.update(lazyInit=True)
        return kw
        
    def js_column_lines(self,grid):
        if self.lh.link.report.get_field_choices_meth(self.field) is not None:
            yield "%s.add_row_listener(function(sm,rowIndex,record) {" % grid
            #yield "  console.log('20100124b',this,client_job);"
            yield "  %s.setQueryContext(record.data.id)});" % self.as_ext()
            #yield "client_job.add_row_listener(function(sm,rowIndex,record) {console.log('20100124b',this)},this);"
        

        
            
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
        kw.update(format=self.lh.link.report.date_format)
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
        
    def get_column_options(self,**kw):
        kw = FieldElement.get_column_options(self,**kw)
        #kw.update(xtype='booleancolumn')
        kw.update(trueText=self.lh.link.report.boolean_texts[0])
        kw.update(falseText=self.lh.link.report.boolean_texts[1])
        kw.update(undefinedText=self.lh.link.report.boolean_texts[2])
        return kw
        
    def get_from_form(self,instance,values):
        """
        standard HTML submits checkboxes of a form only when they are checked.
        So if the field is not contained in values, we take False as value.
        """
        instance[self.name] = values.get(self.name,False)



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
    declare_type = jsgen.DECLARE_THIS
    
    
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
        for e in elements:
            if not isinstance(e,LayoutElement):
                raise Exception("%r is not a LayoutElement" % e)
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
            if len(self.elements) == 1:
                d.update(layout='fit')
            elif self.vertical:
                d.update(layout='form')
                for e in self.elements:
                    h = e.height or e.preferred_height
                    e.value.update(anchor="100%")
                    #~ if h == 0:
                        #~ e.value.update(anchor="95%")
                    #~ else:
                        #~ e.value.update(anchor="95%% %d%%" % (100.0*self.preferred_height/h))
                    #e.value.update(flex=h)
                #~ #align = 'left'
                #~ align = 'stretch'
                #~ #align = 'stretchmax'
                #~ d.update(layout='vbox',layoutConfig=dict(align=align))
                #~ d.update(pack='end')
            else:
                d.update(layout='column')
                for e in self.elements:
                    w = e.width or e.preferred_width
                    e.value.update(columnWidth=float(w)/self.preferred_width)
                
                #~ #align = 'top'
                #~ align = 'stretch'
                #~ #align = 'stretchmax'
                #~ d.update(layout='hbox',layoutConfig=dict(align=align))
            
        
        
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
        

class TabPanel(Container):
    value_template = "new Ext.TabPanel(%s)"
    #~ def __init__(self,lh,name,*elements,**options):
        #~ Container.__init__(self,lh,name,*elements,**options)
        #~ self.width = self.elements[0].ext_width() or 300
    

    def ext_options(self):
        d = dict(
          xtype="tabpanel",
          #region="east",
          split=True,
          activeTab=0,
          width=300,
          #items=js_code("[%s]" % ",".join([l.ext_name for l in self.layouts]))
          items=self.elements
        )
        return d
        

#~ class DataElementMixin:
    #~ "common for Grids, Details and Forms"
  

class GridElement(Container): #,DataElementMixin):
    #value_template = "new Ext.grid.EditorGridPanel(%s)"
    value_template = "new Ext.grid.GridPanel(%s)"
    ext_suffix = "_grid"
    
    def __init__(self,lh,name,rh,*elements,**kw):
        """
        Note: lh is the owning layout handle, rh is the report being managed by this Grid.
        """
        assert isinstance(rh,reports.ReportHandle), "%r is not a ReportHandle!" % rh
        if len(elements) == 0:
            elements = rh.row_layout._main.elements
        w = 0
        for e in elements:
            w += (e.width or e.preferred_width)
        self.preferred_width = constrain(w,10,120)
        
        Container.__init__(self,lh,name,*elements,**kw)
        #DataElementMixin.__init__(self,rh)
        #self.dl = rh
        
        # override Container's height algorithm
        self.preferred_height = rh.report.page_length 
        #~ ADD_GRID_HEIGHT = 4 # experimental value...
        #~ if self.height:
            #~ self.height += ADD_GRID_HEIGHT
        #~ else:
            #~ self.preferred_height += ADD_GRID_HEIGHT
        
        self.rh = rh
        self.report = rh.report
        lh.needs_store(rh)
        self.column_model = ColumnModel(self)
        #self.mt = ContentType.objects.get_for_model(self.report.model).pk
        if self.report.master is not None:
            self.mt = ContentType.objects.get_for_model(self.report.master).pk
        else:
            self.mt = 'undefined'

        
          
    def subvars(self):
        """
        GridElement, unlike Container, doesn't generate the declaration of its elements 
        because self.column_model does this indirectly.
        """
        #self.setup()
        #yield self.rh.store
        yield self.column_model

    def ext_options(self):
        #~ self.setup()
        d = LayoutElement.ext_options(self)
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
        d.update(store=self.rh.store) # js_code(self.rh.store.ext_name))
        d.update(colModel=self.column_model)
        d.update(title=self.rh.report.label)
        #d.update(colModel=js_code('this.cols'))
        #d.update(colModel=js_code(self.column_model.ext_name))
        d.update(autoHeight=True)
        #d.update(layout='fit')
        d.update(enableColLock=False)
        if self.__class__ is not GridMainPanel: 
            mt = ContentType.objects.get_for_model(self.report.model).pk
            js="Lino.show_slave(this,%r,%s,%s)" % (
                self.rh.row_layout.get_absolute_url(run=True),
                py2js(self.rh.report.label),mt)
            d.update(listeners=dict(click=js_code(js)))
        return d
        
    #~ def js_declare(self):
        #~ for ln in Container.js_declare(self):
            #~ yield ln
        #~ if self.rh.report.master is not None:
            #~ yield "this.main_grid.add_row_listener(function(sm,rowIndex,record) {"
            #~ yield "  var p = { %s: record.id }" % URL_PARAM_MASTER_PK
            #~ yield "  p[%r] = %r;" % (URL_PARAM_MASTER_TYPE,self.mt)
            #~ yield "  console.log('20100212 GridElement.js_declare()',p);"
            #~ yield "  %s.load({params:p});" % self.rh.store.as_ext()
            #~ yield "});"
            
      
            
      
        
class M2mGridElement(GridElement):
    def __init__(self,lh,field,*elements,**kw):
        self.field = field
        rpt = reports.get_model_report(field.rel.to)
        rh = rpt.get_handle(lh.ui)
        GridElement.__init__(self,lh,id2js(rpt.actor_id),rh,*elements,**kw)
  
class Reaction:
  
    def setup(self):
        pass
        
    def subvars(self):
        return []
        
    def js_declare(self):
        return []
        
    def js_body(self):
        return []
        
    def js_after_body(self):
        return []
        
    def js_before_body(self):
        return []
        
    def js_job_constructor(self,**kw):
        yield "function(caller) {"
        yield "  var client_job = this;" 
        #~ yield "  // MainPanel.js_job_constructor() calls self.js_declare()"
        for ln in self.js_declare():
            yield "  " + ln
        #~ yield "  // MainPanel.js_job_constructor() called self.js_declare()"
        yield "  this.window = new Ext.Window(%s);" % py2js(kw)
        #~ yield "  console.log(4);"
        yield "  this.stop = function() {"
        yield "     this.window.close();"
        yield "  }"
        yield "  if (caller) {"
        yield "    caller.window.on('close',function() {"
        #yield "      console.log('close',caller,this);"
        yield "      this.stop();"
        yield "    },this);"
        yield "  }"
        for ln in self.js_before_body():
            yield "  " + ln
        for ln in self.js_body():
            yield "  " + ln
        for ln in self.js_after_body():
            yield "  " + ln
        yield "  this.window.show();"
        yield "  this.window.syncSize();"
        yield "  this.window.focus();"
        yield "}"
        
        
            
class MainPanel(Reaction):
  
    def __init__(self):
    #~ def __init__(self,dl):
        #~ self.dl = dl # DataLink (i.e. a ReportHandle or a FormHandle)
        self.keys = None
        self.buttons = None
        self.cmenu = None
        
    def subvars(self):
        self.setup()
        for rh in self.lh._needed_stores:
            yield rh.store
        yield self.buttons
        yield self.keys
        yield self.cmenu
  
    def js_after_body(self):
        for e in self.lh.walk():
            for ln in e.js_column_lines('this.main_grid'):
                yield ln
                
  
    def get_datalink(self):
        raise NotImplementedError
        
    def js_before_body(self):
        # for permalink:
        yield "  this.window._permalink = %s;" % py2js(id2js(self.lh.name))
        yield "  this.content_type = %s;" % py2js(self.lh.link.content_type)
        
    def setup(self):
        if self.keys:
            return
        #setup_report(self.report)
        keys = []
        buttons = []
        dl = self.get_datalink()
        for a in dl.get_actions():
            h = js_code("Lino.grid_action(this,'%s','%s')" % (
                  a.name, 
                  dl.get_absolute_url(grid_action=a.name)))
            buttons.append(dict(text=a.label,handler=h))
            if a.key:
                keys.append(dict(
                  handler=h,
                  key=a.key.keycode,ctrl=a.key.ctrl,alt=a.key.alt,shift=a.key.shift))
        if dl.props is not None:
            #~ h = js_code("function(btn,state) {Lino.toggle_props(this)}")
            h = js_code("Lino.toggle_props(this)")
            buttons.append(dict(text=_('Properties'),toggleHandler=h,enableToggle=True))
        if self.__class__ is GridMainPanel:
            details = dl.get_details()
            if len(details):
                # the first detail window can be opend with Ctrl+ENTER 
                key = actions.RETURN(ctrl=True)
                lh = details[0]
                keys.append(dict(
                  handler=js_code("Lino.show_slave(this,%r,%s,%s)" % (lh.get_absolute_url(run=True),py2js(lh.label),self.mt)),
                  key=key.keycode,ctrl=key.ctrl,alt=key.alt,shift=key.shift))

                for lh in details[1:]: # self.rh.layouts[2:]:
                    buttons.append(dict(
                  handler=js_code("Lino.show_slave(this,%r,%s,%s)" % (lh.get_absolute_url(run=True),py2js(lh.label),self.mt)),
                      text=lh.layout.label))
                  
            slaves = dl.get_slaves()
            for rh in slaves:
                #rh = sl.get_handle(self.lh.ui)
                buttons.append(dict(
                  handler=js_code("Lino.show_slave(this,%r,%s,%s)" % (
                    rh.row_layout.get_absolute_url(run=True),
                    py2js(rh.report.label),self.mt)),
                  #handler=js_code("Lino.show_slave(this,%r)" % id2js(rh.row_layout.name)),
                  text = rh.report.label,
                ))
            
        self.keys = Variable(self.ext_name+'_keys',keys)
        self.buttons = Variable(self.ext_name+'_buttons',buttons)
        self.cmenu = Variable('cmenu',js_code("new Ext.menu.Menu(%s)" % py2js(self.buttons)))
        
    @classmethod
    def field2elem(cls,lh,field,**kw):
        for cl,x in _field2elem:
            if isinstance(field,cl):
                return x(lh,field,**kw)
        raise NotImplementedError("No LayoutElement for %s" % field.__class__)
        #~ raise NotImplementedError("field %r" % field)

#~ class FieldPanel(Container):
    #~ xtype = "container"
  
class WrappingMainPanel(MainPanel):
    """Inherited by DetailMainPanel and FormMainPanel (not GridPanel)
    Wraps each FieldElement into a Panel with FormLayout.
    """
    
    @classmethod
    def field2elem(cls,lh,field,**kw):
        e = MainPanel.field2elem(lh,field,**kw)
        ct = Panel(lh,field.name+"_ct",True,e,layout='form')#,flex=0)
        ct.field = field
        return ct

class GridMainPanel(GridElement,MainPanel):
    value_template = "new Lino.GridPanel(%s)"
    #declare_type = jsgen.DECLARE_VAR
    #collapsible = False
    def __init__(self,lh,name,vertical,*elements,**kw):
        'ignore the "vertical" arg'
        #lh.report.setup()
        self.pager = None
        MainPanel.__init__(self)
        GridElement.__init__(self,lh,name,lh.link,*elements,**kw)
        #~ if self.height is None:
            #~ self.height = self.preferred_height
        #~ if self.width is None:
            #~ self.width = self.preferred_width
        #lino.log.debug("GridMainPanel.__init__() %s",self.name)
        
    def subvars(self):
        for e in GridElement.subvars(self):
            yield e
        for e in MainPanel.subvars(self):
            yield e
        yield self.pager
        if self.lh.link.props is not None:
            yield self.lh.link.props
        
    def get_datalink(self):
        return self.rh
        
    def ext_options(self,**kw):
        self.setup()
        kw = GridElement.ext_options(self,**kw)
        # d = Layout.ext_options(self,request)
        # d = dict(title=request._lino_report.get_title()) 
        #kw.update(title=request._lino_request.get_title()) 
        #kw.update(title=self.layout.label)
        #kw.update(title=self.report.get_title(None)) 
        #kw.update(region='center',split=True)
        del kw['autoHeight']
        del kw['title']
        kw.update(selModel=js_code("new Ext.grid.RowSelectionModel({singleSelect:false})"))
        kw.update(tbar=self.pager)
        kw.update(bbar=self.buttons)
        return kw
        
    #~ def js_declare(self):
        #~ for ln in GridElement.js_declare(self):
            #~ yield ln
            
    def js_declare(self):
        self.setup()
        for ln in Container.js_declare(self):
            yield ln
        yield "%s.on('afteredit', Lino.grid_afteredit(this,'%s'));" % (
          self.as_ext(),self.rh.get_absolute_url(grid_afteredit=True))
        yield "%s.on('cellcontextmenu', Lino.cell_context_menu(this));" % self.as_ext()
        # recalculate page size when size changes
        yield "%s.on('resize', function(cmp,aw,ah,rw,rh) {" % self.as_ext()
        yield "    this.pager.pageSize = cmp.calculatePageSize(this,aw,ah,rw,rh) || 10;" # % self.as_ext()
        yield "    this.refresh();"
        yield "  }, this, {delay:500});"
        # yield "  }, this);"
        # first load with "offset" and "limit" params
        #~ yield "%s.on('render', function() {" % self.as_ext()
        #~ yield "  this.pager.pageSize = %s.calculatePageSize('render') || 10;" % self.as_ext()
        #~ yield "  // this.refresh();"
        #~ #yield "  %s.load({params:{limit:this.pager.pageSize,start:this.pager.cursor}});" % self.rh.store.as_ext()
        #~ yield "}, this, {delay:100});"
        
    def setup(self):
        if self.pager:
            return
        MainPanel.setup(self)
        # searchString thanks to http://www.extjs.com/forum/showthread.php?t=82838
        def js_keypress():
            yield "function(field, e) {"
            # searching starts when user presses ENTER.
            yield "  if(e.getKey() == e.RETURN) {"
            # yield "    console.log('keypress',field.getValue(),store)"
            #    // var searchString = Ext.getCmp('seachString').getValue();
            yield "    store.setBaseParam('%s',field.getValue());" % ext_requests.URL_PARAM_FILTER
            yield "    store.load({params: { start: 0, limit: this.pager.pageSize }});" 
            yield "  }"
            yield "}"
        search_field = dict(
            id = 'seachString',
            fieldLabel = 'Search',
            xtype = 'textfield',
            enableKeyEvents = True, # required if you need to detect key-presses
            #listeners = dict(keypress=dict(handler=keypress,scope=js_code('this')))
            listeners = dict(keypress=js_keypress(),scope=js_code('this'))
        )
        dl = self.get_datalink()
        buttons = [search_field]
        #export_csv = dict(xtype='exportbutton',store=self.dl.store) #,scope=js_code('this'))
        #export_csv = dict(text="CSV",handler=js_code("function(){console.log('not implemented')}"),scope=js_code('this'))
        export_csv = dict(text=_("Download"),handler=js_code(
          "function() {window.open(%r);}" % dl.get_absolute_url(csv=True)))
        buttons.append(export_csv)
        tbar = dict(
          store=self.rh.store,
          displayInfo=True,
          pageSize=self.report.page_length,
          prependButtons=True,
          items=buttons, 
        )
        self.pager = Variable('pager',js_code("new Ext.PagingToolbar(%s)" % py2js(tbar)))
        
    def js_body(self):
        #yield "this.refresh = function() { this.%s.getStore().load()}" % self.ext_name
        yield "this.refresh = function() { "
        #yield "  this.pager.pageSize = %s.calculatePageSize() || 10;" % self.as_ext()
        yield "  %s.getStore().load({params:{limit:this.pager.pageSize,start:this.pager.cursor}});" % self.as_ext()
        yield "}"
        yield "this.get_current_record = function() { return this.main_grid.getSelectionModel().getSelected()};"
        yield "this.get_selected = function() {"
        yield "  var sel_pks = '';"
        yield "  var sels = this.main_grid.getSelectionModel().getSelections();"
        yield "  for(var i=0;i<sels.length;i++) { sel_pks += sels[i].id + ','; };"
        yield "  return sel_pks;"
        yield "}"
        
        #~ yield "var grid = this.main_grid;"
        #~ yield "var store = grid.getStore();"
        #~ if self.lh.link.report.master is None:
            #~ yield "store.load();" 
        #~ else:
            #~ master_type = ContentType.objects.get_for_model(self.lh.link.report.master).pk
            #~ #master_type = ContentType.objects.get_for_model(self.lh.link.report.model).pk
            #~ yield "this.load_master = function(record) {"
            #~ yield "  console.log('load_master() mt=%s,mk=',record.id);" % master_type
            #~ yield "  store.setBaseParam(%r,%s);" % (URL_PARAM_MASTER_TYPE,master_type)
            #~ yield "  store.setBaseParam(%r,record.id);" % URL_PARAM_MASTER_PK
            #~ yield "  store.load();" 
            #~ yield "}"
            #~ yield "caller.main_grid.add_row_listener("
            #~ yield "  function(sm,rowIndex,record) { client_job.load_master(record)})"
            #~ yield "this.load_master(caller.get_current_record());"
            
        
        # the following doesn't work and i don't understand why
        #~ yield "  this.window.on('show',function() {"
        #~ yield "    grid.focus();"
        #~ yield "  });"
        #~ yield "  grid.on('viewready',function() {"
        #~ #yield "    console.log('on render');"
        #~ #yield "    grid.getView().focusRow(1);"
        #~ yield "    grid.getSelectionModel().selectFirstRow();"
        #~ #yield "    grid.getView().focusEl.focus();"
        #~ yield "  });"



class DetailMainPanel(Panel,WrappingMainPanel):
    declare_type = jsgen.DECLARE_THIS
    value_template = "new Ext.form.FormPanel(%s)"
    def __init__(self,lh,name,vertical,*elements,**kw):
        self.rh = lh.link
        self.report = self.rh.report
        MainPanel.__init__(self)
        #~ DataElementMixin.__init__(self,lh.link)
        Panel.__init__(self,lh,name,vertical,*elements,**kw)
        #lh.needs_store(self.rh)
        
    def get_datalink(self):
        return self.rh
        
    #~ def subvars(self):
        #~ for e in DataElementMixin.subvars(self):
            #~ yield e
            
    def subvars(self):
        #~ print 'DetailMainPanel.subvars()', self
        for e in MainPanel.subvars(self):
            yield e
        for e in Panel.subvars(self):
            yield e
            
    def ext_options(self):
        self.setup()
        d = Panel.ext_options(self)
        #d.update(title=self.layout.label)
        #d.update(region='east',split=True) #,width=300)
        d.update(autoScroll=True)
        if False:
            d.update(tbar=js_code("""new Ext.PagingToolbar({
              store: %s,
              displayInfo: true,
              pageSize: 1,
              prependButtons: true,
            }) """ % self.rh.store.ext_name))
        #d.update(items=js_code(self._main.as_ext(request)))
        #d.update(items=js_code("[%s]" % ",".join([e.as_ext() for e in self.elements])))
        d.update(items=self.elements)
        #d.update(autoHeight=False)
        d.update(bbar=self.buttons)
        #d.update(standardSubmit=True)
        return d
        
    def js_declare(self):
        #yield "console.log(10);"
        #~ yield "// begin DetailMainPanel.js_declare()"
        yield "this.refresh = function() { if(caller) caller.refresh(); };"
        yield "this.get_current_record = function() { return this.current_record;};"
        yield "this.get_selected = function() {"
        yield "  return this.current_record.id;"
        yield "}"
        yield "if(caller) {"
        #yield "  this.add_row_listener = function(fn,scope){caller.add_row_listener(fn,scope)};"
        yield "  this.main_grid = caller.main_grid;"
        yield "  this.props = caller.props;"
        yield "}else{"
        #yield "  this.add_row_listener = function(fn,scope) {};"
        yield "  this.main_grid = undefined;"
        yield "}"
        #~ yield "// DetailMainPanel.js_declare() calls Panel.js_declare(self) :"
        for ln in Panel.js_declare(self):
            yield ln
        yield "// DetailMainPanel.js_declare() called Panel.js_declare(self) :"
        #yield "console.log(11);"
        #yield "mastergrid = Ext.getCmp()"
        #yield "var slaves = [ %s ];" % ','.join([slave.rh.store.as_ext() for slave in self.lh.slave_grids])
        yield "var load_record = this.load_record = function(record) {"
        #yield "function load_record (record) {"
        #yield "  console.log('DetailMainPanel-%s.load_record()',record);" % self.report
        #name = id2js(self.lh.name) + '.' + self.lh._main.ext_name
        #name = 'this.' + self.lh._main.ext_name
        #name = self.as_ext()
        #yield "  this.current_pk = record.data.id;" 
        yield "  this.current_record = record;" 
        yield "  %s.form.loadRecord(record);" % self.as_ext()
        
        #~ yield "  var p = { %s: record.id }" % URL_PARAM_MASTER_PK
        #~ #yield "  var p = { %s: record.data.%s }" % (URL_PARAM_MASTER_PK,self.rh.store.pk.name)
        #~ mt = ContentType.objects.get_for_model(self.report.model).pk
        #~ yield "  p[%r] = %r;" % (URL_PARAM_MASTER_TYPE,mt)
        #~ for slave in self.lh.slave_grids:
            #~ yield "  %s.load({params:p});" % slave.rh.store.as_ext()
        #~ #yield "  for(i=0;i++;i<slaves.length) { console.log('load slave',slaves[i],p); slaves[i].load({params:p}) };"
        
        yield "};"
        yield "if(this.main_grid) {"
        yield "  this.main_grid.add_row_listener("
        yield "    function(sm,rowIndex,record) { this.load_record(record); },this);"
        
        
        #~ yield "%s.addListener('load',function(store,rows,options) { " % self.report.store.ext_name
        #~ yield "  %s.form.loadRecord(rows[0]);" % self.ext_name
        #~ for slave in self.lh.slave_grids:
            #~ yield "  %s.load({params: { master: rows[0].data['%s'] } });" % (
                 #~ slave.report.store.ext_name,
                 #~ self.report.store.pk.name)
                 #~ #slave.store.name,request._lino_report.lh.pk.name)
        #~ yield "});"
      
        keys = []
        buttons = []

        #main_name = id2js(self.lh.link.row_layout.name) + '.' + 'main_grid'
        key = actions.PAGE_UP
        js = js_code("function() {this.main_grid.getSelectionModel().selectPrevious()}")
        keys.append(dict(
          handler=js,
          scope=js_code('this'),
          key=key.keycode,ctrl=key.ctrl,alt=key.alt,shift=key.shift))
        buttons.append(dict(handler=js,scope=js_code('this'),text="Previous"))

        key = actions.PAGE_DOWN
        js = js_code("function() {this.main_grid.getSelectionModel().selectNext()}")
        keys.append(dict(
          handler=js,
          scope=js_code('this'),
          key=key.keycode,ctrl=key.ctrl,alt=key.alt,shift=key.shift))
        buttons.append(dict(handler=js,scope=js_code('this'),text="Next"))
        if len(keys):
            #yield "console.log(%s);" % self.as_ext()
            #yield "console.log(%s.comp);" % self.as_ext()
            yield "  %s.keys = %s;" % (self.as_ext(),py2js(keys))
        
        for btn in buttons:
            yield "  %s.addButton(%s);" % (self.as_ext(),py2js(btn))
    
        yield "}"
        
        # the following also if caller was false

        buttons = []

        url = self.rh.get_absolute_url(submit=True)
        js = js_code("Lino.form_submit(this,'%s',this.main_grid.getStore(),'%s')" % (
                url,self.rh.store.pk.name))
        buttons.append(dict(handler=js,text='Submit'))
        
        for btn in buttons:
            yield "%s.addButton(%s);" % (self.as_ext(),py2js(btn))
    
        yield "// end DetailMainPanel.js_declare()"
        
    def js_body(self):
        yield "if(this.main_grid) {"
        yield "  var sels = this.main_grid.getSelectionModel().getSelections()"
        yield "  if(sels.length > 0) this.load_record(sels[0]);"
        yield "}"
        

class FormMainPanel(Panel,WrappingMainPanel):
    value_template = "new Ext.form.FormPanel(%s)"
    
    def __init__(self,lh,name,vertical,*elements,**kw):
        #DataElementMixin.__init__(self,lh.link)
        Panel.__init__(self,lh,name,vertical,*elements,**kw)
        MainPanel.__init__(self)

    def get_datalink(self):
        return self.lh.link
        
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
            

    def js_body(self):
        yield "  this.get_values = function() {"
        yield "    var v = {};"
        for e in self.lh.link.inputs:
            yield "    v[%r] = this.main_panel.getForm().findField(%r).getValue();" % (e.name,e.name)
        yield "    return v;"
        yield "  };"

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
)
    

