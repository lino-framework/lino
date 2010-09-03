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

from lino import layouts, reports, actions
from lino.utils import constrain
from lino.utils import choosers
from lino.utils import jsgen
from lino.utils.jsgen import py2js, Variable, Component, id2js, js_code
from lino.utils import choosers
from . import ext_requests
#~ from lino.modlib.properties import models as properties # import Property, CharPropValue
#~ from lino.modlib.system import models as system

EXT_CHAR_WIDTH = 9
EXT_CHAR_HEIGHT = 22

DEFAULT_GC_NAME = 'std'


def varname_field(f):
    if hasattr(f,'model'):
        return f.model.__name__ + '_' + f.name + '_field'
    else: # e.g. Field instances used as return_type for methods
        return f.name + '_field'
        
def a2btn(a):
    return dict(
      opens_a_slave=a.opens_a_slave,
      handler=js_code("Lino.%s" % a),
      name=a.name,
      label=unicode(a.label),
      #~ url="/".join(("/ui",a.actor.app_label,a.actor._actor_name,a.name))
    )
      
def before_row_edit(panel):
    l = []
    #~ l.append("console.log('20100730',record);")
    #~ for e in panel.walk():
    #~ if isinstance(panel,TabPanel):
        #~ print panel, panel.active_children
    for e in panel.active_children:
        #~ if e is not panel and isinstance(e,GridElement):
        if isinstance(e,GridElement):
            l.append(
              "%s.load_master_record(record);" % e.as_ext())
        elif isinstance(e,PictureElement):
            l.append(
              "this.load_picture_to(%s,record);" % e.as_ext())
        elif isinstance(e,FieldElement):
            chooser = choosers.get_for_field(e.field)
            if chooser:
                #~ lino.log.debug("20100615 %s.%s has chooser", self.lh.layout, e.field.name)
                for f in chooser.context_fields:
                    if panel.has_field(f):
                        l.append("%s.setContextValue(%r,record.data[%r]);" % (
                            e.ext_name,f.name,ext_requests.form_field_name(f)))
                    elif True: # f.name = panel.fk_name:
                        l.append("%s.setContextValue(%r,this.ww.get_current_record().id)" % (e.ext_name,f.name))
    return js_code('function(record){%s}' % ('\n'.join(l)))




class unused_GridFilters(Component):
    ext_suffix = "_filters"
    declare_type = jsgen.DECLARE_VAR
    value_template = "new Ext.ux.grid.GridFilters(%s)"
    
    def __init__(self,name,**kw):
        #~ assert isinstance(grid,GridElement)
        #~ kw.update(encode='json')
        kw.update(encode=True)
        kw.update(local=False)
        #~ kw.update(filters=[])
        Component.__init__(self,name,**kw)



class GridColumn(Component):
    #~ declare_type = jsgen.DECLARE_VAR
    declare_type = jsgen.DECLARE_INLINE
    #~ ext_suffix = "_col"
    #~ value_template = "new Ext.grid.Column(%s)"
    
    def __init__(self,index,editor,**kw):
        """editor may be a Panel for columns on a GenericForeignKey
        """
        #~ print 20100515, editor.name, editor.__class__
        #~ assert isinstance(editor,FieldElement), \
            #~ "%s.%s is a %r (expected FieldElement instance)" % (cm.grid.report,editor.name,editor)
        self.editor = editor
        #~ self.value_template = editor.grid_column_template
        kw.update(self.editor.get_column_options())
        kw.update(editor=self.editor)
        kw.update(colIndex=index)
        kw.update(hidden=editor.hidden)
        kw.update(filter=dict(type=editor.filter_type))
        #~ if isinstance(editor,FieldElement) and editor.field.primary_key:
        if isinstance(editor,FieldElement) and isinstance(editor.field,models.AutoField):
            kw.update(renderer=js_code('Lino.id_renderer'))
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
    
    label = None
    label_width = 0 
    editable = False
    sortable = False
    xtype = None # set by subclasses
    #~ grid_column_template = "new Ext.grid.Column(%s)"
    collapsible = False
    hidden = False
    active_child = True
    
    def __init__(self,lh,name,**kw):
        #lino.log.debug("LayoutElement.__init__(%r,%r)", lh.layout,name)
        #self.parent = parent
        #~ name = lh.layout._actor_name + '_' + name
        VisibleComponent.__init__(self,name,**kw)
        self.lh = lh
        #~ if lh is not None:
        assert isinstance(lh,layouts.LayoutHandle)
        lh.setup_element(self)

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
    declare_type = jsgen.DECLARE_VAR
    #~ declare_type = jsgen.DECLARE_INLINE
    value_template = "new Ext.BoxComponent(%s)"
    vflex = True
    
    def __init__(self,lh,name,action,**kw):
        #~ print 20100730, name
        #~ kw.update(html='<img height="100%"/>')
        #~ kw.update(html='<img height="100%" onclick="Lino.img_onclick()"/>')
        kw.update(autoEl=dict(tag='img'))
        #~ kw.update(autoEl=dict(tag='img',onclick="Lino.img_onclick(%s)" % name))
        #~ kw.update(autoEl=dict(tag='img',onclick="Lino.img_onclick(this)" ))
        #~ kw.update(onclick=js_code('"Lino.img_onclick()"'))
        #~ kw.update(cls='ext-el-mask')
        kw.update(style=dict(height='100%',cursor='pointer'))
        kw.update(plugins=js_code('Lino.PictureBoxPlugin'))
        #~ kw.update(plugins=js_code('new Lino.PictureBoxPlugin(caller)'))
        #~ kw.update(listeners=dict(click=js_code('Lino.img_onclick')))
        LayoutElement.__init__(self,lh,name,**kw)
        

        

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
        LayoutElement.__init__(self,lh,varname_field(field),label=unicode(field.verbose_name),**kw)
        
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
            kw.update(readOnly=True)
        return kw
        
    def ext_options(self,**kw):
        kw = LayoutElement.ext_options(self,**kw)
        kw.update(self.get_field_options())
        return kw
    
        
        
class TextFieldElement(FieldElement):
    #~ xtype = 'textarea'
    filter_type = 'string'
    vflex = True
    value_template = "new Ext.form.TextArea(%s)"
    #~ value_template = "new Ext.form.HtmlEditor(%s)"
    xtype = None
    #~ xtype = 'htmleditor'
    #width = 60
    preferred_width = 60
    preferred_height = 3
    #collapsible = True

        
class CharFieldElement(FieldElement):
    filter_type = 'string'
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
        
class ComboFieldElement(FieldElement):
    #~ value_template = "new Ext.form.ComboBox(%s)"        
    sortable = True
    xtype = None
    filter_type = 'string'
    
class ChoicesFieldElement(ComboFieldElement):
    value_template = "new Lino.ChoicesFieldElement(%s)"
  
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        self.preferred_width = 20
        
    def get_field_options(self,**kw):
        kw = FieldElement.get_field_options(self,**kw)
        kw.update(store=self.field.choices)
        kw.update(hiddenName=self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX)
        return kw
        

class RemoteComboFieldElement(ComboFieldElement):
    value_template = "new Lino.RemoteComboFieldElement(%s)"
  
    def store_options(self,**kw):
        proxy = dict(url=self.lh.ui.get_choices_url(self),method='GET')
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
    value_template = "new Lino.SimpleRemoteComboFieldElement(%s)"
    
  
class ComplexRemoteComboFieldElement(RemoteComboFieldElement):
    #~ value_template = "new Lino.ComplexRemoteComboFieldElement(%s)"
        
    def get_field_options(self,**kw):
        kw = RemoteComboFieldElement.get_field_options(self,**kw)
        kw.update(hiddenName=self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX)
        return kw
        
        
class ForeignKeyElement(ComplexRemoteComboFieldElement):
    
    def __init__(self,*args,**kw):
        FieldElement.__init__(self,*args,**kw)
        #~ print 20100903,repr(self.field.rel.to)
        #~ assert issubclass(self.field.rel.to,models.Model), "%r is not a model" % self.field.rel.to
        self.report = reports.get_model_report(self.field.rel.to)
      
    def submit_fields(self):
        return [self.field.name,self.field.name+ext_requests.CHOICES_HIDDEN_SUFFIX]
        
        
    def get_field_options(self,**kw):
        kw = ComplexRemoteComboFieldElement.get_field_options(self,**kw)
        kw.update(pageSize=self.report.page_length)
        kw.update(emptyText=_('Select a %s...') % self.report.model.__name__)
        return kw



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
        kw.update(format=self.lh.layout.datalink_report.date_format)
        return kw
        
    def get_column_options(self,**kw):
        kw = FieldElement.get_column_options(self,**kw)
        kw.update(xtype='datecolumn')
        kw.update(format=self.lh.layout.datalink_report.date_format)
        return kw
    
class IntegerFieldElement(FieldElement):
    filter_type = 'numeric'
    xtype = 'numberfield'
    sortable = True
    preferred_width = 5
    data_type = 'int' 

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
  
    xtype = 'checkbox'
    data_type = 'boolean' 
    filter_type = 'boolean'
    #~ grid_column_template = "new Ext.grid.BooleanColumn(%s)"
    #~ def __init__(self,*args,**kw):
        #~ FieldElement.__init__(self,*args,**kw)
        
    def get_field_options(self,**kw):
        kw = FieldElement.get_field_options(self,**kw)
        del kw['fieldLabel']
        kw.update(boxLabel=self.label)
        return kw
        
    def get_column_options(self,**kw):
        kw = FieldElement.get_column_options(self,**kw)
        kw.update(xtype='booleancolumn')
        kw.update(trueText=self.lh.layout.datalink_report.boolean_texts[0])
        kw.update(falseText=self.lh.layout.datalink_report.boolean_texts[1])
        kw.update(undefinedText=self.lh.layout.datalink_report.boolean_texts[2])
        return kw
        
    def get_from_form(self,instance,values):
        """
        standard HTML submits checkboxes of a form only when they are checked.
        So if the field is not contained in values, we take False as value.
        """
        instance[self.field.name] = values.get(self.field.name,False)



#~ class DelegateFieldElement(FieldElement):

class MethodElement(FieldElement):
    stored = True
    editable = False
    filter_type = None

    def __init__(self,lh,name,meth,return_type,**kw):
        assert isinstance(lh,layouts.LayoutHandle)
        # uh, this is tricky...
        return_type.name = name
        return_type.verbose_name = name
        return_type._return_type_for_method = meth
        FieldElement.__init__(self,lh,return_type)
        delegate = lh.main_class.field2elem(lh,return_type,**kw)
        for a in ('ext_options','get_column_options',
                  'filter_type',
                  #~ 'get_filter_options', 
                  'get_field_options'):
                  #~ ): # ,'grid_column_template'):
            setattr(self,a,getattr(delegate,a))
        

class Container(LayoutElement):
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
        self.active_children = []
        for e in elements:
            if not isinstance(e,LayoutElement):
                raise Exception("%r is not a LayoutElement" % e)
            if e.active_child:
                self.active_children.append(e)
            elif isinstance(e,Panel):
                self.active_children += e.active_children
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
    active_child = False
    
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
        A horizontal Panel is vflex if and only if *all* its children are vflex 
        (if vflex and non-vflex elements are together in a hbox, then the 
        vflex elements will get the height of the highest non-vflex element).
        """        
        self.vflex = not vertical
        for e in elements:
            if self.vertical:
                if e.vflex:
                    self.vflex = True
            else:
                if not e.vflex:
                    self.vflex = False
                    #~ print 20100615, self.lh.layout, self, "hbox loses vflex because of", e
                    
        if self.vflex and len(elements) > 1:
            if self.vertical:
                #~ print 20100615, self.lh, self
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
            else: # not self.vertical
                self.update(layout='hbox',layoutConfig=dict(align='stretch'))
              
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
                #~ d.update(layout='column') # 20100615
                d.update(layout='hbox')
                
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
        #~ elif d['layout'] == 'column': # 20100615
        elif d['layout'] == 'hbox':
            for e in elements:
                w = e.width or e.preferred_width
                #~ e.value.update(columnWidth=float(w)/self.preferred_width) # 20100615
                e.value.update(flex=int(w*100/self.preferred_width))
            
        
        
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
  

class GridElement(Container): 
    declare_type = jsgen.DECLARE_VAR
    #value_template = "new Ext.grid.EditorGridPanel(%s)"
    #~ value_template = "new Ext.grid.GridPanel(%s)"
    value_template = "new Lino.GridPanel(%s)"
    ext_suffix = "_grid"
    vflex = True
    xtype = None
    
    def __init__(self,lh,name,rpt,*elements,**kw):
        """
        :param lh: the handle of the DetailLayout owning this grid
        :param rpt: the report being displayed
        """
        assert isinstance(rpt,reports.Report), "%r is not a Report!" % rpt
        self.report = rpt
        if len(elements) == 0:
            self.rh = rpt.get_handle(lh.ui)
            elements = self.rh.list_layout._main.elements
        w = 0
        for e in elements:
            w += (e.width or e.preferred_width)
        self.preferred_width = constrain(w,10,120)
        Container.__init__(self,lh,name,*elements,**kw)
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
        rh = self.report.get_handle(self.lh.ui)
        kw = LayoutElement.ext_options(self,**kw)
        #~ d.update(ls_data_url=rh.ui.get_actor_url(self.report))
        kw.update(ls_url=rh.ui.build_url(self.report.app_label,self.report._actor_name))
        kw.update(ls_store_fields=[js_code(f.as_js()) for f in rh.store.fields])
        kw.update(ls_columns=[GridColumn(i,e) for i,e in enumerate(self.elements)])
        #~ kw.update(ls_filters=[e.get_filter_options() for e in self.elements if e.filter_type])
        kw.update(ls_id_property=rh.store.pk.name)
        kw.update(ls_quick_edit=True)
        kw.update(ls_bbar_actions=[rh.ui.a2btn(a) for a in rh.get_actions(rh.report.default_action)])
        kw.update(ls_grid_configs=self.report.grid_configs)
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
                return ComplexRemoteComboFieldElement(lh,field,**kw)
        if field.choices:
            return ChoicesFieldElement(lh,field,**kw)
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
        MainPanel.__init__(self)
        GridElement.__init__(self,lh,name,lh.layout.datalink_report,*elements,**kw)
        #lino.log.debug("GridMainPanel.__init__() %s",self.name)
        



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
        
class TabPanel(jsgen.Component):
#~ class TabPanel(jsgen.Value):
    value_template = "new Ext.TabPanel(%s)"
        
    def __init__(self,tabs,**kw):
        self.active_children = []
        for t in tabs:
            self.active_children += t.active_children
      
        self.tabs = tabs
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
        
    def has_field(self,f):
        for t in self.tabs:
            if t.has_field(f): 
                return True



class FormPanel(jsgen.Component):
#~ class FormPanel(VisibleComponent):
    declare_type = jsgen.DECLARE_VAR
    value_template = "new Lino.FormPanel(%s)"
    #~ value_template = "new Ext.form.FormPanel(%s)"
    
    def __init__(self,rh,action,main,**kw):
        self.main = main
        kw.update(
          items=main,
          #~ autoScroll=True,
          layout='fit',
        )
        if not isinstance(action,actions.InsertRow):
            kw.update(has_navigator=True)
        
        on_render = []
        for e in main.active_children:
            if isinstance(e,FieldElement):
                chooser = choosers.get_for_field(e.field)
                if chooser:
                    #~ lino.log.debug("20100615 %s.%s has chooser", self.lh.layout, e.field.name)
                    for f in chooser.context_fields:
                        #~ if main.has_field(f):
                        varname = varname_field(f)
                        on_render.append("%s.on('change',Lino.chooser_handler(%s,%r));" % (varname,e.ext_name,f.name))
        
        if on_render:
            assert not kw.has_key('listeners')
            kw.update(listeners=dict(render=js_code('function(){%s}' % '\n'.join(on_render))))
        kw.update(before_row_edit=before_row_edit(main))
        
        kw.update(ls_bbar_actions=[rh.ui.a2btn(a) for a in rh.get_actions(action)])
        kw.update(ls_url=rh.ui.build_url(rh.report.app_label,rh.report._actor_name))
        jsgen.Component.__init__(self,'form_panel',**kw)
        
    def has_field(self,f):
        return self.main.has_field(f)



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
    

