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

from django import forms
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.text import capfirst
from django.template.loader import render_to_string

            
class Element:
    label = None
    name = None
    def __init__(self,layout,name,width=None,height=None):
        assert isinstance(layout,Layout)
        self.layout = layout
        self.name = name
        self.width = width
        self.height = height
        
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

class StaticText(Element):
    def __init__(self,text):
          self.text = mark_safe(text)
    def render(self,row):
        return self.text
          
class FieldElement(Element):
    def __init__(self,layout,field,**kw):
        Element.__init__(self,layout,field.name,**kw)
        self.field = field
        
    def render(self,row):
        #~ if self.name == "items":
          #~ print self.__class__.__name__, self.name, "render()"
        return row.render_field(self)
        
class InlineElement(Element):

    def render(self,row):
        return row.render_inline(self)

class MethodElement(Element):

    def render(self,row):
        return row.render_field(self)


        
class Container(Element):
    vertical = False
    def __init__(self,layout,name,*elements,**kw):
        Element.__init__(self,layout,name)
        #print self.__class__.__name__, elements
        self.label = kw.get('label',self.label)
        self.elements = []
        for elem in elements:
            assert elem is not None
            if type(elem) == str:
                if "\n" in elem:
                    lines=[]
                    for line in elem.splitlines():
                        line = line.strip()
                        if len(line) > 0 and not line.startswith("#"):
                            #lines.append(HBOX(layout,line))
                            lines.append(layout,line)
                        self.elements.append(VBOX(layout,None,*lines))
                else:
                    for name in elem.split():
                        if not name.startswith("#"):
                            self.elements.append(layout[name])
            else:
                self.elements.append(elem)
        
    def __str__(self):
        s = Element.__str__(self)
        # self.__class__.__name__
        s += "(%s)" % (",".join([str(e) for e in self.elements]))
        return s
        
    def get_width(self):
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

    def set_width(self,w):
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
        context = dict(
          element = BoundElement(self,row)
        )
        try:
            return render_to_string(self.template,context)
        except Exception,e:
            traceback.print_exc(e)
            raise
            #print e
            #return mark_safe("<PRE>%s</PRE>" % e)

class HBOX(Container):
    template = "lino/includes/hbox.html"
        
class VBOX(Container):
    template = "lino/includes/vbox.html"
    vertical = True
    
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
        w = main.get_width()
        if w is not None:
            main.set_width(w)
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
                    lines.append(self.desc2elem(name+'_'+str(i),line))
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
        return self.__class__.__name__ + "(%s)" % self._main
        
    def bound_to(self,row):
        return BoundElement(self._main,row)

    def inlines(self):
        return {}
         
    def get_label(self):
        if self.label is None:
            return self.__class__.__name__
        return self.label

class PageLayout(Layout):
    show_labels = True
    join_str = "\n"

class RowLayout(Layout):
    show_labels = False
    join_str = " "
    hbox_class = GRID_ROW
    vbox_class = GRID_CELL
    


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
        #print "row_management", self.element
        try:
            assert isinstance(self.element,GRID_ROW)
            #row = self.renderer.get_row()
            s = "<td>%s</td>" % self.row.links()
            if self.row.renderer.editing:
                s += "<td>%d%s</td>" % (self.row.number,
                    self.row.pk_field())
                if self.row.renderer.can_delete:
                    s += "<td>%s</td>" % self.row.form["DELETE"]
            else:
                s += "<td>%d</td>" % (self.row.number)
            return mark_safe(s)
        except Exception,e:
            print "Exception in BoundElement.row_management():"
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

