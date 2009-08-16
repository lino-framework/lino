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

EXT_CHAR_WIDTH = 9

def py2js(v):
    if type(v) is types.BooleanType:
        return str(v).lower()
    return repr(v)
            
class Element:
    label_width = 0 
    parent = None
    editable = False
    ext_template = 'lino/includes/element.js'
    def __init__(self,layout,name,width=None,height=None,label=None):
        assert isinstance(layout,Layout)
        self.layout = layout
        self.name = name
        self.width = width
        self.height = height
        #if label is None:
        #    label = name.replace("_"," ")
        self.label = label
        
    def __str__(self):
        if self.width is None:
            return self.name
        if self.height is None:
            return self.name + ":%d" % self.width
        return self.name + ":%dx%d" % (self.width,self.height)

    def get_width(self):
        return self.width
        
    def set_width(self,w):
        self.width = w
        
    def columns(self):
        return [ self ]

    #~ def as_ext(self):
        #~ s = self.ext_editor(label=True)
        #~ if s is not None:
            #~ return mark_safe(s)
        #~ return self.name
        
    
            
    def as_ext(self,**kw):
        options = self.ext_options()
        options.update(kw)
        s = "{ "
        s += ",\n".join(["%s: %s" % (k,py2js(v)) for k,v in options.items()])
        s += " }"
        return mark_safe(s)
        
    def ext_options(self):
        d = dict(name=self.name)
        if self.width is None:
            if isinstance(self.parent,HBOX):
                d.update(flex=1)
            else:
                d.update(anchor="100%")
        else:
            d.update(width=(self.width+self.label_width)*EXT_CHAR_WIDTH)
        if self.label:
            d.update(fieldLabel=self.label)
        return d
        
    #~ def as_ext(self):
        #~ try:
            #~ context = dict(
              #~ element = self
            #~ )
            #~ return render_to_string(self.ext_template,context)
        #~ except Exception,e:
            #~ traceback.print_exc(e)
        
    def ext_column(self,renderer):
        s = """
        {
          dataIndex: '%s', 
          header: '%s', 
          sortable: true,
        """ % (self.name, self.label)
        if self.width:
            s += " width: %d, " % (self.width * 10)
        if renderer.editing and self.editable:
            s += " editor: %s, " % self.ext_editor(label=False)
        s += " } "
        return s
        
        
    def ext_editor(self,label=False):
        s = " new Ext.form.TextField ({ " 
        s += " name: '%s', " % self.name
        if label:
            s += " fieldLabel: '%s', " % self.label
        s += " disabled: true, " 
        s += """
          }) """
        return s
        
    def children(self):
        return [ self ]

class StaticText(Element):
    def __init__(self,text):
          self.text = mark_safe(text)
    def render(self,row):
        return self.text
          
django2ext = (
    (models.TextField, 'Ext.form.TextArea'),
    (models.CharField, 'Ext.form.TextField'),
    (models.DateField, 'Ext.form.DateField'),
    (models.IntegerField, 'Ext.form.NumberField'),
    (models.DecimalField, 'Ext.form.NumberField'),
    (models.BooleanField, 'Ext.form.Checkbox'),
    (models.ForeignKey, 'Ext.form.ComboBox'),
    (models.AutoField, 'Ext.form.NumberField'),
)


def ext_class(field):
    for cl,x in django2ext:
        if isinstance(field,cl):
            return x
            
_ext_options = (
    (models.TextField, dict(xtype='textarea')),
    (models.CharField, dict(xtype='textfield')),
    (models.DateField, dict(xtype='datefield')),
    (models.IntegerField, dict(xtype='numberfield')),
    (models.DecimalField, dict(xtype='numberfield')),
    (models.BooleanField, dict(xtype='checkbox')),
    (models.ForeignKey, dict(xtype='combo')),
    (models.AutoField, dict(xtype='numberfield')),
)
            
def ext_options(field):
    for cl,x in _ext_options:
        if isinstance(field,cl):
            return x

class FieldElement(Element):
    def __init__(self,layout,field,**kw):
        Element.__init__(self,layout,field.name,
            label=field.verbose_name,**kw)
        self.field = field
        self.editable = field.editable
        
    def render(self,row):
        return row.render_field(self)
        
    def ext_editor(self,label=False):
        cl = ext_class(self.field)
        if not cl:
            print "no ext editor class for field ", \
              self.field.__class__.__name__, self
            return None
        s = " new %s ({ " % cl
        s += " name: '%s', " % self.name
        if label:
            s += " fieldLabel: '%s', " % self.label
        if not self.field.blank:
            s += " allowBlank: false, "
        if isinstance(self.field,models.CharField):
            s += " maxLength: %d, " % self.field.max_length
        s += """
          }) """
        return s
        
    def ext_options(self):
        d = Element.ext_options(self)
        d.update(ext_options(self.field))
        if not self.field.blank:
            d.update(allowBlank=False)
        if isinstance(self.field,models.CharField):
            d.update(maxLength=self.field.max_length)
        return d
        
        
class InlineElement(Element):

    def render(self,row):
        return row.render_inline(self)

class MethodElement(Element):

    def render(self,row):
        return row.render_field(self)

class Container(Element):
    ext_template = 'lino/includes/element.js'
    ext_container = 'Ext.Panel'
    vertical = False
    hpad = 1
    is_fieldset = False
    
    def __init__(self,layout,name,*elements,**kw):
        Element.__init__(self,layout,name,**kw)
        #print self.__class__.__name__, elements
        #self.label = kw.get('label',self.label)
        self.elements = []
        for elem in elements:
            assert elem is not None
            if type(elem) == str:
                if "\n" in elem:
                    lines = []
                    for line in elem.splitlines():
                        line = line.strip()
                        if len(line) > 0 and not line.startswith("#"):
                            lines.append(layout,line)
                        self.elements.append(VBOX(layout,None,*lines))
                else:
                    for name in elem.split():
                        if not name.startswith("#"):
                            self.elements.append(layout[name])
            else:
                self.elements.append(elem)
        self.compute_width()
        # some more analysis:
        for e in self.elements:
            e.parent = self
            if isinstance(e,FieldElement):
                self.is_fieldset = True
                if e.label:
                    w = len(e.label) + 1 
                    if self.label_width < w:
                        self.label_width = w
            if e.width == self.width:
                """
                this was the width-giving element. 
                remove this width to correct padding differences.
                """
                e.width = None
                
    def compute_width(self):
        """
        If all children have a width (in case of a horizontal layout), 
        or (in a vertical layout) if at at least one element has a width, 
        then my width is also known.
        """
        if self.width is None:
            #print self, "compute_width..."
            w = 0
            if self.vertical:
                #~ if self.name == 'main' and self.layout._model.__name__ == 'Product':
                    #~ print "foo", [e.width for e in self.elements]
                for e in self.elements:
                    if e.width is not None:
                        w = max(e.width,w)
            else:
                for e in self.elements:
                    if e.width is None:
                        return
                    w += e.width
            if w > 0:
                self.width = w
                
        
    def children(self):
        return self.elements
        
    def columns(self):
        l = []
        for e in self.elements:
            l += e.columns()
        #print l
        return l
        
    def __str__(self):
        s = Element.__str__(self)
        # self.__class__.__name__
        s += "(%s)" % (",".join([str(e) for e in self.elements]))
        return s
        
    def old_get_width(self):
        total_width = 0
        for elem in self.elements:
            w = elem.get_width()
            if w is not None:
                if self.vertical:
                    total_width = max(w,total_width)
                else:
                    total_width += w
            else:
                if not self.vertical:
                    return None
              
        if total_width == 0:
            return None
        #print self, "width is", w
        return w

    def old_set_width(self,w):
        self.width = w
        if self.vertical:
            for elem in self.elements:
                elem.set_width(w)
            return
        total_width = w
        missing = []
        for elem in self.elements:
            w = elem.get_width()
            if w is None:
                missing.append(elem)
            else:
                elem.set_width(w)
                total_width -= w
        while len(missing) > 0:
            if total_width <= 0:
                print "Warning: total_width <= 0 in ",
                print "  %s.set_width(%d) : " \
                  % (self.name,self.width)
                print "  missing:", [elem.name for elem in missing]
                return
            w = int(total_width / len(missing))
            missing[0].set_width(w)
            total_width -= w
            missing = missing[1:]
            

    def render(self,row):
        try:
            context = dict(
              element = BoundElement(self,row),
              renderer = row.renderer
            )
            return render_to_string(self.template,context)
        except Exception,e:
            traceback.print_exc(e)
            raise
            #print e
            #return mark_safe("<PRE>%s</PRE>" % e)

    def ext_options(self):
        d = Element.ext_options(self)
        if self.is_fieldset:
            d.update(labelWidth=self.label_width*EXT_CHAR_WIDTH)
        return d
            
    def as_ext(self,**kw):
        options = self.ext_options()
        options.update(kw)
        s = "{ "
        s += ", ".join(["%s: %r" % i for i in options.items()])
        s += ", items: [ %s ]" % ", ".join([e.as_ext() for e in self.elements])
        s += " }"
        return mark_safe(s)
        
        

class HBOX(Container):
    template = "lino/includes/hbox.html"
    ext_layout = 'Ext.layout.HBoxLayout'
        
    def ext_options(self):
        d = Container.ext_options(self)
        d.update(xtype='panel')
        d.update(layout='hbox')
        return d
        
class VBOX(Container):
    template = "lino/includes/vbox.html"
    vertical = True
    ext_layout = 'Ext.layout.VBoxLayout'
    
                
    def ext_options(self):
        d = Container.ext_options(self)
        if self.is_fieldset:
            d.update(xtype='fieldset')
            d.update(layout='form')
        else:
            d.update(xtype='panel')
            d.update(layout='vbox')
        return d
        
    
class GRID_ROW(Container):
    template = "lino/includes/grid_row.html"
    
class GRID_CELL(Container):
    template = "lino/includes/grid_cell.html"


class Layout:
    label = "General"
    detail_reports = {}
    join_str = None
    vbox_class = VBOX
    hbox_class = HBOX
    width = None
    
    def __init__(self,model,desc=None):
        #self._meta = meta
        self._model = model
        self._inlines = self.inlines()
        if hasattr(self,"main"):
            main = self.create_element('main')
        else:
            if desc is None:
                desc = self.join_str.join([ 
                    f.name for f in model._meta.fields 
                    + model._meta.many_to_many])
            main = self.desc2elem("main",desc)

        self._main = main
        #~ width = 0
        # w = main.get_width()
        # if w is not None:
        #     main.set_width(w)
        #~ from lino.django.igen.models import DocItem
        #~ if model == DocItem:
            #~ print self
            
    def create_element(self,name):
        #print self.__class__.__name__, "__getitem__()", name
        name,kw = self.splitdesc(name)
        if self._inlines.has_key(name):
            return InlineElement(self,name,**kw)
        try:
            value = getattr(self,name)
        except AttributeError,e:
            try:
                field = self._model._meta.get_field(name)
            except models.FieldDoesNotExist,e:
                return MethodElement(self,name,**kw)
            else:
                return FieldElement(self,field,**kw)

        if type(value) == str:
            return self.desc2elem(name,value,**kw)
        if isinstance(value,StaticText):
            return value
        raise KeyError("No handler for attribute %s = %r" % (name,value))
        
         
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
                
    def desc2elem(self,name,desc,**kw):
        if "\n" in desc:
            lines = []
            i = 0
            for line in desc.splitlines():
                line = line.strip()
                i += 1
                if len(line) > 0 and not line.startswith("#"):
                    lines.append(self.desc2elem(name+'_'+str(i),line,**kw))
            if len(lines) == 1:
                return lines[0]
            return self.vbox_class(self,name,*lines,**kw)
        else:
            l = []
            for x in desc.split():
                if not x.startswith("#"):
                    l.append(self.create_element(x))
            if len(l) == 1:
                return l[0]
            return self.hbox_class(self,name,*l,**kw)
            
    def __str__(self):
        s = self.__class__.__name__ 
        if hasattr(self,'_main'):
            s += "(%s)" % self._main
        return s
        
    def bound_to(self,row):
        return BoundElement(self._main,row)

    def inlines(self):
        return {}
         
    def get_label(self):
        if self.label is None:
            return self.__class__.__name__
        return self.label
        
    #~ def as_ext(self):
        #~ try:
          #~ return self._main.as_ext()
        #~ except Exception,e:
          #~ traceback.print_exc(e)

class PageLayout(Layout):
    show_labels = True
    join_str = "\n"
    ext_layout = ""
    
    def as_ext(self):
      try:
        s = "new Ext.form.FormPanel({ frame:true, " 
        if self._main.width is not None:
            s += " width:%d, " % ( (self._main.width+self._main.label_width) * EXT_CHAR_WIDTH)
        s += "items: [ %s ], " % ",\n".join([e.as_ext() for e in self._main.children()])
        # TODO : resolve code-template dependence 
        s += """
  bbar: new Ext.PagingToolbar({
    store: ds,       
    displayInfo: true,
    pageSize: 1,
    prependButtons: true,
  })
    """
        s += "})" 
        return mark_safe(s)
      except Exception,e:
        traceback.print_exc(e)

class RowLayout(Layout):
    show_labels = False
    join_str = " "
    hbox_class = GRID_ROW
    vbox_class = GRID_CELL
    ext_layout = 'Ext.layout.HBoxLayout'
    


class BoundElement:
    def __init__(self,element,row):
        assert isinstance(element,Element)
        self.element = element
        self.row = row
        #from lino.django.utils.render import Row
        #assert isinstance(row,Row)

    def as_html(self):
        try:
            return self.element.render(self.row)
        except Exception,e:
            print "Exception in BoundElement.as_html():"
            traceback.print_exc()
            raise e
  
    #~ def as_json(self):
        #~ return self.element.render_as_json(self.row)
        
    def __unicode__(self):
        return self.as_html()
        
    def children(self):
        try:
            assert isinstance(self.element,Container), "%s is not a Container" % self.element
            for e in self.element.elements:
                yield BoundElement(e,self.row)
        except Exception,e:
            print "Exception in BoundElement.children():"
            traceback.print_exc()
            raise e
            
    def row_management(self):
        return self.row.management()
        
    def unused_row_management(self):
        #print "row_management", self.element
        try:
            assert isinstance(self.element,GRID_ROW)
            #row = self.renderer.get_row()
            #s = "<td>%s</td>" % self.row.links()
            l = []
            if self.row.renderer.has_actions():
                l.append(unicode(
              self.renderer.selector[IS_SELECTED % self.row.number]))

            s = ''
            if self.row.renderer.editing:
                s += "<td>%d%s</td>" % (self.row.number,
                    self.row.pk_field())
                if self.row.renderer.can_delete:
                    s += "<td>%s</td>" % self.row.form["DELETE"]
            else:
                s += "<td>%d</td>" % (self.row.number)
            return mark_safe(s)
        except Exception,e:
            print "Exception in BoundElement.row_management() %s:" % \
                 self.row.renderer.request.path
            traceback.print_exc()
            raise e


from lino.django.utils import perms

class Dialog:
    form_class = None
    layout = None
    template_before = "lino/dialog_before.html"
    template_after = "lino/dialog_after.html"
    can_view = perms.always
    
    def __init__(self):
        self._layout = PageLayout(self.layout).bound_to(self)
    
    def execute(self):
        raise NotImplementedError
        
    def view(self,request):
        from lino.django.utils.render import DialogRenderer
        r = DialogRenderer(self,request)
        return r.render_to_response()

