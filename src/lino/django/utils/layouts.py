## Copyright 2009 Luc Saffre

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import traceback
import types

from django import forms
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.template.loader import render_to_string

def get_unbound_meth(cl,name):
    meth = getattr(cl,name,None)
    if meth is not None:
        return meth
    for b in cl.__bases__:
        meth = getattr(b,name,None)
        if meth is not None:
            return meth


EXT_CHAR_WIDTH = 9
EXT_CHAR_HEIGHT = 12

def dict2js(d):
    return ", ".join(["%s: %s" % (k,py2js(v,k)) for k,v in d.items()])

def py2js(v,k):
    if type(v) is types.BooleanType:
        return str(v).lower()
    if type(v) is unicode:
        return repr(v.encode('utf8'))
    return repr(v)
            
class js_code:
    "A string that py2js will represent as is, not between quotes."
    def __init__(self,s):
        self.s = s
    def __repr__(self):
        return self.s
      
class Component:
    declared = False
    #name_suffix = None
    value_template = "{ %s }"
    
    def __init__(self,name,**options):
        self.name = name
        self.options = options
        self.ext_name = name
        
    def ext_variables(self):
        if self.declared:
            yield self
        
    def ext_lines(self,request):
        return []
        
    def ext_options(self,request):
        d = {}
        d.update(self.options)
        return d
        
    def as_ext_value(self,request):
        options = self.ext_options(request)
        s = self.value_template % dict2js(options)
        return mark_safe(s)
        
    def as_ext(self,request):
        if self.declared:
            return self.ext_name
        else:
            return self.as_ext_value(request)
            
    #~ def ext_name(self):
        #~ return self.name
        
        
class Element(Component):
    stored = False
    width = None
    height = None
    ext_name = None
    ext_suffix = ""
    #parent = None # will be set by Container
    def __init__(self,layout,name,**kw):
        #print "Element.__init__()", layout,name
        assert isinstance(layout,Layout)
        self.layout = layout
        #self.parent = parent
        Component.__init__(self,name,**kw)
        if self.declared:
            layout.add_variable(self)
            self.ext_name = self.layout.name +"_" + self.name + self.ext_suffix
            
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
        return [ self ]
        
    def as_store_field(self):
        return "{ %s }" % dict2js(dict(name=self.name))

    def load_to_form(self,obj,d):
        d[self.name] = getattr(obj,self.name)

        

class Store(Element):
    value_template = "new Ext.data.JsonStore({ %s })"
    declared = True
    ext_suffix = "_store"
    
    def __init__(self,layout,report,layout_index=0,**options):
        Element.__init__(self,layout,report.name)
        self.report = report
        self.options = options
        #report.setup()
        self.layout_index = layout_index
        #~ if report == layout.report:
            #~ # it's the master store
            #~ self.data_layout = layout
        #~ else:
            #~ report.setup()
            #~ self.data_layout = report.row_layout
        #print "Store.__init__()",self.name
        #print self,report.get_absolute_url()
        
    def ext_options(self,request):
        d = Element.ext_options(self,request)
        self.report.setup()
        data_layout = self.report.layouts[self.layout_index]
        url = self.report.get_absolute_url(json=True,
          layout=data_layout.index)
        #~ if request._lino_report.report == self.report:
            #~ #rr = request._lino_report
            #~ layout = self.layout
            #~ url = request._lino_report.get_absolute_url(json=True)
        #~ else:
            #~ # it's a slave
            #~ layout = request._lino_report.report.row_layout
            #~ #rr = self.report.renderer()
            #~ url = self.report.get_absolute_url(json=True)
        #self.report.setup()
        d.update(storeId=self.ext_name)
        d.update(remoteSort=True)
        d.update(proxy=js_code(
          "new Ext.data.HttpProxy({url:'%s',method:'GET'})" % url           
        ))
        # a JsonStore without explicit proxy sometimes used method POST
        # d.update(url=self.rr.get_absolute_url(json=True))
        # d.update(method='GET')
        d.update(totalProperty='count')
        d.update(root='rows')
        #print self.report.model._meta
        #d.update(id=self.report.model._meta.pk.attname)
        d.update(id=data_layout.pk.field.name)
        #~ d.update(fields=js_code(
          #~ "[ %s ]" % ",".join([repr(e.field.name) 
          #~ for e in self.data_layout.ext_store_fields])
        #~ ))
        d.update(fields=js_code(
            "[ %s ]" % ",".join([
                e.as_store_field() for e in data_layout.ext_store_fields
            ])
        ))
        return d
        
class ColumnModel(Element):
    declared = True
    ext_suffix = "cols"
    value_template = "new Ext.grid.ColumnModel({ %s })"
    
    def __init__(self,layout,report):
        Element.__init__(self,layout,report.name)
        #Element.__init__(self,layout,report.name+"_cols"+str(layout.index))
        #Element.__init__(self,layout,report.name+"_cols")
        self.report = report
        
    #~ def __init__(self,layout,report):
        #~ self.layout = layout # the owning layout
        #~ self.report = report
        #~ self.name = report.name
        
        
    def ext_options(self,request):
        self.report.setup()
        d = Element.ext_options(self,request)
        #editing = self.layout.report.can_change.passes(request)
        l = [e.as_ext_column(request) for e in self.report.columns]
        d.update(columns=js_code("[ %s ]" % ", ".join(l)))
        #d.update(defaultSortable=True)
        return d
        
            
        
class HiddenField(Element):
    def __init__(self,layout,field):
        Element.__init__(self,layout,field.attname)
        self.field = field
        
    #~ def value2js(self,obj):
        #~ return getattr(obj,self.name)
        
        
class VisibleElement(Element):
    label = None
    label_width = 0 
    parent = None
    editable = False
    sortable = False
    xpadding = 5
    editable = False
    preferred_width = 10
    #ext_template = 'lino/includes/element.js'
    def __init__(self,layout,name,width=None,height=None,label=None):
        Element.__init__(self,layout,name)
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if label is not None:
            self.label = label
        #    label = name.replace("_"," ")
        #~ if label is not None:
            #~ self.label_width = len(label) + 1
        
    def get_property(self,name):
        v = getattr(self,name)
        if self.parent is None or v is not None:
            return v
        return self.parent.get_property(name)
        
    def get_width(self):
        return self.width
        
    def set_width(self,w):
        self.width = w
        
    #~ def as_ext(self):
        #~ s = self.ext_editor(label=True)
        #~ if s is not None:
            #~ return mark_safe(s)
        #~ return self.name
        
    def get_column_options(self,request,**kw):
        kw.update(
          dataIndex=self.name, 
          editable=self.editable,
          header=unicode(self.label) if self.label else self.name,
          sortable=self.sortable)
        if self.width:
            kw.update(width=self.width * EXT_CHAR_WIDTH)
        else:
            kw.update(width=self.preferred_width * EXT_CHAR_WIDTH)
        return kw    
        
    def as_ext_column(self,request):
        kw = self.get_column_options(request)
        return "{ %s }" % dict2js(kw)
        
    #~ def as_ext_column(self,request):
        #~ d = dict(
          #~ dataIndex=self.name, 
          #~ header=unicode(self.label) if self.label else self.name,
          #~ sortable=self.sortable)
        #~ if self.width:
            #~ d.update(width=self.width * EXT_CHAR_WIDTH)
        #~ if request._lino_report.editing and self.editable:
            #~ fo = self.get_field_options(request)
            #~ # del fo['fieldLabel']
            #~ d.update(editor=js_code("{ %s }" % dict2js(fo)))
        #~ return "{ %s }" % dict2js(d)
    
    def ext_options(self,request):
        d = Element.ext_options(self,request)
        if self.width is None:
            """
            an element without explicit width will get flex=1 when in a hbox, otherwise anchor="100%".
            """
            if isinstance(self.parent,HBOX):
                d.update(flex=1)
            else:
                d.update(anchor="100%")
        else:
            d.update(width=self.ext_width())
        if self.height is not None:
            d.update(height=(self.height+2) * EXT_CHAR_HEIGHT)
        return d
        
    def ext_width(self):
        if self.width is None:
            return None
        #if self.parent.labelAlign == 'top':
        return max(self.width,self.label_width) * EXT_CHAR_WIDTH + self.xpadding
        #return (self.width + self.label_width) * EXT_CHAR_WIDTH + self.xpadding
        
        
    #~ def as_ext(self):
        #~ try:
            #~ context = dict(
              #~ element = self
            #~ )
            #~ return render_to_string(self.ext_template,context)
        #~ except Exception,e:
            #~ traceback.print_exc(e)
        
    #~ def ext_column(self,editing):
        #~ s = """
        #~ {
          #~ dataIndex: '%s', 
          #~ header: '%s', 
          #~ sortable: true,
        #~ """ % (self.name, self.label)
        #~ if self.width:
            #~ s += " width: %d, " % (self.width * 10)
        #~ if editing and self.editable:
            #~ s += " editor: %s, " % self.ext_editor(label=False)
        #~ s += " } "
        #~ return s
        
        
    #~ def ext_editor(self,label=False):
        #~ s = " new Ext.form.TextField ({ " 
        #~ s += " name: '%s', " % self.name
        #~ if label:
            #~ s += " fieldLabel: '%s', " % self.label
        #~ s += " disabled: true, " 
        #~ s += """
          #~ }) """
        #~ return s
        

class StaticText(VisibleElement):
    def __init__(self,text):
          self.text = mark_safe(text)
    def render(self,row):
        return self.text
          
#~ django2ext = (
    #~ (models.TextField, 'Ext.form.TextArea'),
    #~ (models.CharField, 'Ext.form.TextField'),
    #~ (models.DateField, 'Ext.form.DateField'),
    #~ (models.IntegerField, 'Ext.form.NumberField'),
    #~ (models.DecimalField, 'Ext.form.NumberField'),
    #~ (models.BooleanField, 'Ext.form.Checkbox'),
    #~ (models.ForeignKey, 'Ext.form.ComboBox'),
    #~ (models.AutoField, 'Ext.form.NumberField'),
#~ )


#~ def ext_class(field):
    #~ for cl,x in django2ext:
        #~ if isinstance(field,cl):
            #~ return x
            
#~ _ext_options = (
    #~ (models.TextField, dict(xtype='textarea')),
    #~ (models.CharField, dict(xtype='textfield')),
    #~ (models.DateField, dict(xtype='datefield')),
    #~ (models.IntegerField, dict(xtype='numberfield')),
    #~ (models.DecimalField, dict(xtype='numberfield')),
    #~ (models.BooleanField, dict(xtype='checkbox')),
    #~ (models.ForeignKey, dict(xtype='combo')),
    #~ (models.AutoField, dict(xtype='numberfield')),
#~ )
            
#~ def ext_options(field):
    #~ for cl,x in _ext_options:
        #~ if isinstance(field,cl):
            #~ return x

class FieldElement(VisibleElement):
    declared = True
    stored = True
    #name_suffix = "field"
    def __init__(self,layout,field,**kw):
        VisibleElement.__init__(self,layout,field.name,label=field.verbose_name,**kw)
        self.field = field
        self.editable = field.editable and not field.primary_key
        
    def get_column_options(self,request,**kw):
        kw = VisibleElement.get_column_options(self,request,**kw)
        if request._lino_report.editing and self.editable:
            fo = self.get_field_options(request)
            kw.update(editor=js_code("{ %s }" % dict2js(fo)))
        return kw    
        

    #~ def value2js(self,obj):
        #~ return getattr(obj,self.name)
        
    def update_from_form(self,instance,values):
        setattr(instance,self.name,values.get(self.name,None))
    def load_to_form(self,obj,d):
        d[self.name] = getattr(obj,self.name)
        
    #~ def render(self,row):
        #~ return row.render_field(self)
        
    #~ def ext_editor(self,label=False):
        #~ cl = ext_class(self.field)
        #~ if not cl:
            #~ print "no ext editor class for field ", \
              #~ self.field.__class__.__name__, self
            #~ return None
        #~ s = " new %s ({ " % cl
        #~ s += " name: '%s', " % self.name
        #~ if label:
            #~ s += " fieldLabel: '%s', " % self.label
        #~ if not self.field.blank:
            #~ s += " allowBlank: false, "
        #~ if isinstance(self.field,models.CharField):
            #~ s += " maxLength: %d, " % self.field.max_length
        #~ s += """
          #~ }) """
        #~ return s
        
    def get_field_options(self,request,**kw):
        kw.update(xtype=self.xtype,name=self.name)
        kw.update(anchor="100%")
        if self.label:
            kw.update(fieldLabel=unicode(self.label))
        if not self.field.blank:
            kw.update(allowBlank=False)
        if not self.editable:
            kw.update(readOnly=True)
            print "get_field_options() readOnly", self
        return kw
        
    def get_panel_options(self,request,**kw):
        d = VisibleElement.ext_options(self,request,**kw)
        d.update(xtype='panel',layout='form')
        return d

    def ext_options(self,request,**kw):
        """
        ExtJS renders fieldLabels only if the field's container has layout 'form', so we create a panel around each field
        """
        fo = self.get_field_options(request)
        po = self.get_panel_options(request)
        po.update(items=js_code("[ { %s } ]" % dict2js(fo)))
        return po
        
class TextFieldElement(FieldElement):
    xtype = 'textarea'
    #width = 60
    preferred_width = 60


class CharFieldElement(FieldElement):
    xtype = "textfield"
    sortable = True
  
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        self.preferred_width = min(20,self.field.max_length)
        if self.width is None and self.field.max_length < 10:
            # "small" texfields should not be expanded, so they get an explicit width
            self.width = self.field.max_length
            
    def get_field_options(self,request,**kw):
        kw = FieldElement.get_field_options(self,request,**kw)
        kw.update(maxLength=self.field.max_length)
        return kw
        
class ForeignKeyElement(FieldElement):
    xtype = "combo"
    sortable = True
    #width = 20
    
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        if self.editable:
            rpt = self.layout.report.get_choices(self.field)
            self.store = Store(self.layout,rpt,autoLoad=True)
      
    def get_field_options(self,request,**kw):
        kw = FieldElement.get_field_options(self,request,**kw)
        if self.editable:
            kw.update(store=js_code(self.store.ext_name))
            #kw.update(store=js_code(self.store.as_ext_value(request)))
            kw.update(hiddenName=self.name+"Hidden")
            kw.update(valueField=self.store.report.model._meta.pk.attname)
            #kw.update(valueField=self.name)
            """
            valueField: The underlying data value name to bind to this ComboBox (defaults to undefined if mode = 'remote' or 'field2' if transforming a select or if the field name is autogenerated based on the store configuration).

Note: use of a valueField requires the user to make a selection in order for a value to be mapped. See also hiddenName, hiddenValue, and displayField.
            """
            kw.update(displayField=self.store.report.display_field)
            kw.update(typeAhead=True)
            #kw.update(lazyInit=False)
            kw.update(mode='remote')
            kw.update(selectOnFocus=True)
            #kw.update(pageSize=self.store.report.page_length)
            
        kw.update(triggerAction='all')
        kw.update(emptyText='Select a %s...' % self.store.report.model.__name__)
        return kw
        
    #~ def value2js(self,obj):
        #~ v = getattr(obj,self.name)
        #~ if v is not None:
            #~ return v.pk
        
    def as_store_field(self):
        return "{ %s },{ %s }" % (
          dict2js(dict(name=self.name)),
          dict2js(dict(name=self.name+"Hidden"))
        )

    def update_from_form(self,instance,values):
        #v = values.get(self.name,None)
        v = values.get(self.name+"Hidden",None)
        if v is not None:
            v = self.store.report.model.objects.get(pk=v)
        setattr(instance,self.name,v)
        
    def load_to_form(self,obj,d):
        v = getattr(obj,self.name)
        if v is None:
            #d[self.name] = ''
            d[self.name+"Hidden"] = None
            d[self.name] = None
        else:
            d[self.name] = unicode(v)
            d[self.name+"Hidden"] = v.pk
            #d[self.name] = v.pk
        

        
            
class DateFieldElement(FieldElement):
    xtype = 'datefield'
    sortable = True
    #width = 10
    
class IntegerFieldElement(FieldElement):
    xtype = 'numberfield'
    sortable = True
    width = 8

class DecimalFieldElement(FieldElement):
    xtype = 'numberfield'
    sortable = True
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        if self.width is None:
            self.width = min(10,self.field.max_digits) + self.field.decimal_places

class BooleanFieldElement(FieldElement):
  
    xtype = 'checkbox'
    
    def get_column_options(self,request,**kw):
        kw = FieldElement.get_column_options(self,request,**kw)
        kw.update(xtype='booleancolumn')
        return kw
        
    def update_from_form(self,instance,values):
        """
        standard HTML submits checkboxes of a form only when they are checked.
        So if the field is not contained in values, we take False as value.
        """
        setattr(instance,self.name,values.get(self.name,False))

class GridElement(VisibleElement):
    value_template = "new Ext.grid.GridPanel({ %s })"
    declared = True
    ext_suffix = "_grid"

    def __init__(self,layout,report,store=None,**kw):
        VisibleElement.__init__(self,layout,report.name)
        #VisibleElement.__init__(self,layout,report.name+"_grid"+str(layout.index),**kw)
        #VisibleElement.__init__(self,layout,report.name+"_grid",**kw)
        self.report = report
        if store is None:
            store = Store(layout,report)
        self.store = store
        self.column_model = ColumnModel(layout,report)
      
    def ext_options(self,request):
        #print self.name, self.layout.detail_reports
        #rpt = self.slave
        #r = rpt.renderer(request)
        # print rpt
        d = VisibleElement.ext_options(self,request)
        #editing = self.report.can_change.passes(request)
        if request._lino_report.editing:
            d.update(clicksToEdit=2)
            #~ d.update(xtype='editorgrid')
        #~ else:
            #~ d.update(xtype='grid')
        #d.update(store=self.store)
        #d.update(colModel=self.column_model)
        d.update(autoScroll=True)
        d.update(fitToFrame=True)
        d.update(store=js_code(self.store.ext_name))
        d.update(colModel=js_code(self.column_model.ext_name))
        #d.update(store=js_code(rpt.as_ext_store()))
        #d.update(colModel=js_code(r.as_ext_colmodel()))
        
        #d.update(columnLines=True)
        #d.update(stripeRows=True)
        d.update(autoHeight=True)
        d.update(enableColLock=False)
        d.update(selModel=js_code("new Ext.grid.RowSelectionModel({singleSelect:false})"))
        return d
            
    def value2js(self,obj):
        return "1"
        
class M2mGridElement(GridElement):
    def __init__(self,layout,field,**kw):
        from . import reports
        rpt = reports.get_model_report(field.rel.to)
        GridElement.__init__(self,layout,rpt,**kw)
  
        

class MethodElement(VisibleElement):
    stored = True

    def __init__(self,layout,name,meth,**kw):
        VisibleElement.__init__(self,layout,name,**kw)
        self.meth = meth
        # print "MethodElement", name, meth
        
    def value2js(self,obj):
        fn = getattr(obj,self.name)
        return fn()
        
    def load_to_form(self,obj,d):
        fn = getattr(obj,self.name)
        try:
            d[self.name] = fn()
        except Exception,e:
            print "[Warning] %s : %s" % (self.ext_name,e)
        


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
)
            
def field2elem(layout,field,**kw):
    for cl,x in _field2elem:
        if isinstance(field,cl):
            return x(layout,field,**kw)
    print "TODO: no layout element for %s" % field.__class__
    return None
    #raise NotImplementedError("field %s (%s)" %(field.name,field.__class__))
            


class Container(VisibleElement):
    #ext_template = 'lino/includes/element.js'
    #ext_container = 'Ext.Panel'
    vertical = False
    hpad = 1
    is_fieldset = False
    preferred_width = None
    
    # ExtJS options
    frame = True
    labelAlign = 'top'
    
    def __init__(self,layout,name,*elements,**kw):
        VisibleElement.__init__(self,layout,name,**kw)
        #print self.__class__.__name__, elements
        #self.label = kw.get('label',self.label)
        self.elements = elements
        #~ self.elements = []
        #~ for elem in elements:
            #~ assert elem is not None
            #~ if type(elem) == str:
                #~ if "\n" in elem:
                    #~ lines = []
                    #~ for line in elem.splitlines():
                        #~ line = line.strip()
                        #~ if len(line) > 0 and not line.startswith("#"):
                            #~ lines.append(layout,line)
                        #~ self.elements.append(VBOX(layout,None,*lines))
                #~ else:
                    #~ for name in elem.split():
                        #~ if not name.startswith("#"):
                            #~ self.elements.append(layout[name])
            #~ else:
                #~ self.elements.append(elem)
        self.compute_width()
        
        # some more analysis:
        for e in self.elements:
            e.parent = self
            if isinstance(e,FieldElement):
                self.is_fieldset = True
                #~ if self.label_width < e.label_width:
                    #~ self.label_width = e.label_width
                if e.label:
                    w = len(e.label) + 1 # +1 for the ":"
                    if self.label_width < w:
                        self.label_width = w
            if e.width == self.width:
                """
                e was the width-giving element for this container.
                remove e's width to avoid padding differences.
                """
                e.width = None
                
    def compute_width(self,unused_insist=False):
        """
        If all children have a width (in case of a horizontal layout), 
        or (in a vertical layout) if at at least one element has a width, 
        then my width is also known.
        """
        if self.width is None:
            #print self, "compute_width..."
            w = 0
            xpadding = self.xpadding
            for e in self.elements:
                ew = e.width or e.preferred_width
                #~ ew = e.width
                #~ if ew is None and insist:
                    #~ ew = e.preferred_width
                if self.vertical:
                    if ew is not None:
                        if w < ew:
                            w = ew
                            xpadding = e.xpadding
                        # w = max(w,e.width) # + self.hpad*2)
                else:
                    if ew is None:
                        return # don't set this container's width since at least one element is flexible
                    w += ew # + self.hpad*2
                    xpadding += e.xpadding
            if w > 0:
                self.width = w
                self.xpadding = xpadding
                
        
    #~ def children(self):
        #~ return self.elements
        
    def walk(self):
        l = [ self ]
        for e in self.elements:
            l += e.walk()
        return l
        
    #~ def __str__(self):
        #~ s = Element.__str__(self)
        #~ # self.__class__.__name__
        #~ s += "(%s)" % (",".join([str(e) for e in self.elements]))
        #~ return s

    def pprint(self,level=0):
        margin = "  " * level
        s = margin + str(self) + ":\n"
        # self.__class__.__name__
        for e in self.elements:
            for ln in e.pprint(level+1).splitlines():
                s += ln + "\n"
        return s

    #~ def render(self,row):
        #~ try:
            #~ context = dict(
              #~ element = BoundElement(self,row),
              #~ renderer = row.renderer
            #~ )
            #~ return render_to_string(self.template,context)
        #~ except Exception,e:
            #~ traceback.print_exc(e)
            #~ raise
            #~ #print e
            #~ #return mark_safe("<PRE>%s</PRE>" % e)
            
    def ext_options(self,request):
        d = VisibleElement.ext_options(self,request)
        if self.is_fieldset:
            d.update(labelWidth=self.label_width * EXT_CHAR_WIDTH)
        #if not self.is_fieldset:
        #d.update(frame=self.get_property('frame'))
        d.update(frame=self.frame)
        d.update(border=False)
        d.update(labelAlign=self.get_property('labelAlign'))
        l = [e.as_ext(request) for e in self.elements ]
        d.update(items=js_code("[\n  %s\n]" % (", ".join(l))))
        return d
            
    #~ def as_ext(self,request,**kw):
        #~ options = self.ext_options(request)
        #~ options.update(kw)
        #~ s = "{ "
        #~ s += ", ".join(["%s: %s" % (k,py2js(v,k)) for k,v in options.items()])
        #~ s += ", items: [\n  %s\n]" % (", ".join([e.as_ext(request) for e in self.elements]))
        #~ #s += extra
        #~ s += " }\n"
        #~ return mark_safe(s)
        
        

class HBOX(Container):
        
    def ext_options(self,request):
        d = Container.ext_options(self,request)
        d.update(xtype='panel')
        d.update(layout='hbox')
        return d
        
class VBOX(Container):
    vertical = True
                
    def ext_options(self,request):
        d = Container.ext_options(self,request)
        #~ if self.is_fieldset:
            #~ d.update(xtype='fieldset')
            #~ d.update(layout='form')
        #~ else:
            #~ d.update(xtype='panel')
            #~ d.update(layout='vbox')
        d.update(xtype='panel')
        #d.update(layout='vbox')
        d.update(layout='anchor')
        return d
        
    
class GRID_ROW(Container):
    template = "lino/includes/grid_row.html"
    
class GRID_CELL(Container):
    template = "lino/includes/grid_cell.html"


class Layout(Component):
    declared = True
    #detail_reports = {}
    join_str = None # set by subclasses
    vbox_class = VBOX
    hbox_class = HBOX
    width = None
    
    def __init__(self,report,index,desc=None,main=None):
        #from . import reports
        #assert isinstance(report,reports.Report)
        Component.__init__(self,report.name + str(index))
        self.variables = []
        self.slave_grids = []
        self.report = report
        self.index = index
        #print "Layout.__init__()", self.name
        self.master_store = Store(self,report,self.index)
        #self._slave_dict = {}
        if main is None:
            if hasattr(self,"main"):
                main = self.create_element('main')
            else:
                if desc is None:
                    desc = self.join_str.join([ 
                        f.name for f in report.model._meta.fields 
                        + report.model._meta.many_to_many])
                main = self.desc2elem("main",desc)
                #~ for e in main.leaves():
                    #~ if e.name == report.model._meta.pk.name
        else:
            print "main is", main

        self._main = main
        
        self.fields = tuple([e for e in self.walk() if e.stored])
                  
        pk = None
        for e in self.fields:
            if isinstance(e,FieldElement) and e.field.name == report.model._meta.pk.name:
                pk = e
                break
                
        if pk is None:
            self.pk = self.add_hidden_field(report.model._meta.pk)
            self.ext_store_fields = self.fields + (self.pk,)
        else:
            self.pk = pk
            self.ext_store_fields = self.fields
        
        #print "Layout.__init__() done:", self.name
              
        

    #~ def add_variable(self,e):
        #~ name = e.as_ext_name()
        #~ assert not self.variables.has_key(name)
        #~ self.variables[name] = e
              
    #~ def slaves(self):
        #~ for e in self.leaves():
            #~ if isinstance(e,SlaveElement):
                #~ yield e.slave
        
            
    def desc2elem(self,name,desc,**kw):
        #print "desc2elem()", repr(name),repr(desc)
        #assert desc != 'Countries_choices2'
        if "\n" in desc:
            lines = []
            i = 0
            for line in desc.splitlines():
                line = line.strip()
                if len(line) > 0 and not line.startswith("#"):
                    i += 1
                    lines.append(self.desc2elem(name+'_'+str(i),line,**kw))
            if len(lines) == 1:
                return lines[0]
            return self.vbox_class(self,name,*lines,**kw)
        else:
            l = []
            for x in desc.split():
                if not x.startswith("#"):
                    e = self.create_element(x)
                    if e:
                        l.append(e)
            if len(l) == 1:
                return l[0]
            return self.hbox_class(self,name,*l,**kw)
            
    def create_element(self,name):
        #print "create_element()", name
        name,kw = self.splitdesc(name)
        if not name in ('__str__','__unicode__','name','label'):
            value = getattr(self,name,None)
            if value is not None:
                if type(value) == str:
                    return self.desc2elem(name,value,**kw)
                if isinstance(value,StaticText):
                    return value
        slaveclass = self.report.get_slave(name)
        if slaveclass is not None:
            slaverpt = slaveclass()
            #self._slave_dict[name] = slaverpt
            e = GridElement(self,slaverpt,**kw)
            self.slave_grids.append(e)
            return e
        try:
            field = self.report.model._meta.get_field(name)
        except models.FieldDoesNotExist,e:
            meth = get_unbound_meth(self.report.model,name)
            if meth is not None:
                return MethodElement(self,name,meth,**kw)
        else:
            return field2elem(self,field,**kw)
            #return FieldElement(self,field,**kw)
        msg = "%s has no attribute '%s' (used in layout %s)" % (
          self.report.model, name, self.__class__)
        #print "[Warning]", msg
        raise KeyError(msg)
        
         
    def splitdesc(self,picture):
        a = picture.split(":",1)
        if len(a) == 1:
            return picture,{}
        if len(a) == 2:
            name = a[0]
            a = a[1].split("x",1)
            if len(a) == 1:
                return name, dict(width=int(a[0]))
            elif len(a) == 2:
                return name, dict(width=int(a[0]),height=int(a[1]))
        raise Exception("Invalid picture descriptor %s" % picture)
                
    def __str__(self):
        return self.report.model._meta.app_label+"."+self.__class__.__name__
        
    def __repr__(self):
        s = self.__class__.__name__ 
        if hasattr(self,'_main'):
            s += "(%s)" % self._main
        return s
        
    def add_hidden_field(self,field):
        return HiddenField(self,field)
        
    def add_variable(self,elem):
        self.variables.append(elem)
        
    def renderer(self,rr):
        return LayoutRenderer(self,rr)
        
    def get_label(self):
        if self.label is None:
            return self.__class__.__name__
        return self.label
        
    def walk(self):
        return self._main.walk()
        
    def ext_variables(self):
        later = []
        for e in self.variables:
            if isinstance(e,VisibleElement):
                later.append(e)
            else:
                yield e
        for e in later: yield e
        yield self
        
    def ext_lines(self,request):
        raise NotImplementedError
    
        
class RowLayout(Layout):
    show_labels = False
    join_str = " "
    hbox_class = GRID_ROW
    vbox_class = GRID_CELL
    #ext_layout = 'Ext.layout.HBoxLayout'
    #value_template = "new Ext.grid.EditorGridPanel({ %s })"
    value_template = "new Ext.form.FormPanel({ %s })"
    
    def __init__(self,report,index,desc=None,**kw):
        Layout.__init__(self,report,index,desc,**kw)
        self.grid = GridElement(self,report,self.master_store)
        #self.column_model = ColumnModel(self,report)
    
    
    def ext_options(self,request):
        # d = Layout.ext_options(self,request)
        d = dict(title=request._lino_report.get_title()) 
        d.update(region='center',split=True)
        if True:
            d.update(tbar=js_code("""new Ext.PagingToolbar({
              store: %s,
              displayInfo: true,
              pageSize: %d,
              prependButtons: true,
            }) """ % (self.master_store.ext_name,self.report.page_length)))
        #d.update(items=js_code("[ %s ]" % self.grid.name))
        d.update(items=js_code(self.grid.ext_name))
        return d
        
    def ext_lines(self,request):
        s = """
function save(oGrid_event){
    Ext.Ajax.request({
        waitMsg: 'Please wait...',
        url: '%s',""" % request._lino_report.get_absolute_url(ajax='update')
        d = {}
        for e in self.ext_store_fields:
            d[e.name] = js_code('oGrid_event.record.data.%s' % e.name)
        
        s += """
        params: { %s }, """ % dict2js(d)
        s += """
        success: function(response){							
           var result=eval(response.responseText);
           switch(result){
           case 1:
              ds.commitChanges(); // get rid of the red triangles
              ds.reload();        // reload our datastore.
              break;					
           default:
              Ext.MessageBox.alert('Uh uh...','We could not save him...');
              break;
           }
        },
        failure: function(response){
           var result=response.responseText;
           Ext.MessageBox.alert('error','could not connect to the database. retry later');		
        }
     });
  }"""
        yield s
        yield "// frm.on('afteredit', save);"

        s = """
function onRowSelect(grid, rowIndex, e) {"""
        for layout in self.report.layouts[1:]:
            s += """
    var pgnum = rowIndex + 1;
    %s.getTopToolbar().changePage(pgnum);""" % layout.ext_name
    
        #~ l = self.report.get_absolute_url(mode='detail').split('?')
        #~ if len(l) == 1:
            #~ l.append('')
        #~ s += """
  #~ url = "%s?row=" + String(rowIndex) + "%s";
  #~ // Ext.MessageBox.alert(url,url);
  #~ document.location = url;
  #~ """ % tuple(l)
        s += "};"
        yield s
        yield "%s.getSelectionModel().on('rowselect', onRowSelect);" % self.grid.ext_name
        yield "%s.load();" % self.master_store.ext_name


class PageLayout(Layout):
    label = "Detail"
    show_labels = True
    join_str = "\n"
    #ext_layout = ""
    value_template = "new Ext.form.FormPanel({ %s })"
    
    def __init__(self,*args,**kw):
        Layout.__init__(self,*args,**kw)
        if self._main.width is None:
            print "[Warning] Could not compute width for PageLayout", self
            #self._main.compute_width(insist=True)
        #print self._main.pprint()
        
    def ext_options(self,request):
        d = self._main.ext_options(request)
        d.update(title=self.label) 
        d.update(region='east',split=True) #,width=300)
        d.update(autoScroll=True)
        d.update(tbar=js_code("""new Ext.PagingToolbar({
          store: %s,
          displayInfo: true,
          pageSize: 1,
          prependButtons: true,
        }) """ % self.master_store.ext_name))
        #d.update(items=js_code(self._main.as_ext(request)))
        d.update(items=js_code("[%s]" % ",".join([e.as_ext(request) for e in self._main.elements])))
        return d
        
        
    def ext_lines(self,request):
        s = "%s.addListener('load',function(store,rows,options) { " % self.master_store.ext_name
        s += "\n  %s.form.loadRecord(rows[0]);" % self.ext_name
        for slave in self.slave_grids:
            s += "\n  %s.load({params: { master: rows[0].data['%s'] } });" % (
                 slave.store.ext_name,self.master_store.layout.pk.name)
                 #slave.store.name,request._lino_report.layout.pk.name)
        s += "\n});"
        yield s
        url = self.report.get_absolute_url(save=True)
        s = """
%s.addButton({
    text: 'Submit',
    handler: function(btn,evt){""" % self.ext_name
        #s += "console.log(btn,evt);"
        #s += "console.log(%s.getAt(0));" % self.master_store.ext_name
        s += """
        var pk = %s.getAt(0).data.%s;""" % (self.master_store.ext_name,self.pk.name)
        d = dict(
            url=self.report.get_absolute_url(save=True),
            params=js_code("{pk:pk,layout:%d}" % self.master_store.layout_index),
            waitMsg='Saving Data...',
            success=js_code("""function (form, action) {
                Ext.MessageBox.alert('Saved OK',
                  action.result ? action.result.msg : '(undefined action result)');
            }"""),
            failure=js_code("""function(form, action) {
                // console.log("form:",form);
                Ext.MessageBox.alert('Submit failed!', 
                  action.result ? action.result.msg : '(undefined action result)');
            }""")
            )
        
        s += "\n  %s.form.submit({%s});" % (self.ext_name,dict2js(d))
        s += """
}});"""
        yield s
        yield "%s.load({params:{limit:1,start:0}});" % self.master_store.ext_name
    
        
class TabbedPanel(Component):
    value_template = "new Ext.TabPanel({ %s })"
    def __init__(self,name,layouts):
        Component.__init__(self,name)
        self.layouts = layouts
        self.width = self.layouts[0]._main.ext_width() or 300
    

    def ext_lines(self,request):
        for layout in self.layouts:
            for ln in layout.ext_lines(request):
                yield ln
                
    def ext_variables(self):
        for layout in self.layouts:
            for ln in layout.ext_variables():
                yield ln
                
    def ext_options(self,request):
        d = dict(
          xtype="tabpanel",
          region="east",
          split=True,
          activeTab=0,
          width=self.width,
          items=js_code("[%s]" % ",".join([l.ext_name for l in self.layouts])))
        return d
                