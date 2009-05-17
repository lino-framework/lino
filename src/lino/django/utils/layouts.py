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
    def __init__(self,layout):
        assert isinstance(layout,Layout)
        self.layout = layout
        self.width = None
        self.height = None

    
class FieldElement(Element):
    def __init__(self,layout,name,params=None):
        Element.__init__(self,layout)
        a = name.split(":",1)
        if len(a) == 1:
            self.name = name
            #self.picture = None
            #self.widget_attrs = {}
        elif len(a) == 2:
            self.name = a[0]
            #self.picture = a[1]
            a = a[1].split("x",1)
            if len(a) == 1:
                self.width = int(a[0])
            elif len(a) == 2:
                self.width = int(a[0])
                self.height = int(a[1])
            #~ else:
                #~ raise Exception("Invalid picture spec %s" % name)
        
    def __str__(self):
        if self.width is None:
            return self.name
        if self.height is None:
            return self.name + ":%d" % self.width
        return self.name + ":%dx%d" % (self.width,self.height)

    def render(self,row):
        #~ if self.name == "items":
          #~ print self.__class__.__name__, self.name, "render()"
        return row.render_field(self)
        
#~ class InlineElement(FieldElement):        

    #~ def render(self,row):
        #~ return row.render_inline(self)


        
class Container(Element):
    def __init__(self,layout,*elements,**kw):
        Element.__init__(self,layout)
        #print self.__class__.__name__, elements
        self.label = kw.get('label',None)
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
                        self.elements.append(VBOX(layout,*lines))
                else:
                    for name in elem.split():
                        if not name.startswith("#"):
                            self.elements.append(layout[name])
            else:
                self.elements.append(elem)
        
    def __str__(self):
        return "%s(%s)" % (self.__class__.__name__,
          ",".join([str(e) for e in self.elements]))
        
    def render(self,row):
        context = dict(
          element = BoundElement(self,row)
        )
        try:
            return render_to_string(self.template,context)
        except Exception,e:
            print e
            return mark_safe("<PRE>%s</PRE>" % e)

class HBOX(Container):
    template = "lino/includes/hbox.html"
        
class VBOX(Container):
    template = "lino/includes/vbox.html"
    
class GRID_ROW(Container):
    template = "lino/includes/grid_row.html"
    
    
    
    


class Layout:
    label = "General"
    detail_reports = {}
    join_str = None
    vbox_class = VBOX
    hbox_class = HBOX
    
    def __init__(self,model,desc=None):
        #self._meta = meta
        self._inlines = self.inlines()
        if hasattr(self,"main"):
            main = self['main']
        else:
            if desc is None:
                desc = self.join_str.join([ 
                    f.name for f in model._meta.fields 
                    + model._meta.many_to_many])
            main = self.desc2elem(desc)

        self._main = main
                
    def __getitem__(self,name):
        #print self.__class__.__name__, "__getitem__()", name
        try:
            s = getattr(self,name)
        except AttributeError,e:
            return FieldElement(self,name)

        if type(s) == str:
            return self.desc2elem(s)
        #return InlineElement(self,name)
        raise KeyError("non handled attribute %r" % s)
        
         
    def inlines(self):
        return {}
         
    def desc2elem(self,desc):
        if "\n" in desc:
            lines=[]
            for line in desc.splitlines():
                line = line.strip()
                if len(line) > 0 and not line.startswith("#"):
                    lines.append(self.desc2elem(line))
                    #lines.append(HBOX(layout,line))
                    #lines.append(layout,line)
            return self.vbox_class(self,*lines)
        else:
            l=[]
            for name in desc.split():
                if not name.startswith("#"):
                    l.append(self[name])
            return self.hbox_class(self,*l)
            
    def __str__(self):
        return self.__class__.__name__ + "(%s)" % self._main
        
    def get_label(self):
        if self.label is None:
            return self.__class__.__name__
        return self.label

    def bound_to(self,row):
        return BoundElement(self._main,row)

class PageLayout(Layout):
    show_labels = True
    join_str = "\n"

class RowLayout(Layout):
    show_labels = False
    join_str = " "
    hbox_class = GRID_ROW
    vbox_class = None # not yet allowed



class BoundElement:
    def __init__(self,element,row):
        assert isinstance(element,Element)
        self.element = element
        #self.layout = layout
        self.row = row
        #self.renderer = renderer
        from lino.django.utils.render import Row
        assert isinstance(row,Row)

    def as_html(self):
        return self.element.render(self.row)
        #return self.renderer.render_element(self.element)
  
    def __unicode__(self):
        return self.element.render(self.row)
        
    def children(self):
        assert isinstance(self.element,Container), "%s is not a Container" % self.element
        for e in self.element.elements:
            yield BoundElement(e,self.row)
            
    def row_management(self):
        #print "row_management", self.element
        assert isinstance(self.element,GRID_ROW)
        #row = self.renderer.get_row()
        s = "<td>%s</td>" % self.row.links()
        if self.row.renderer.editing:
            s += "<td>%d%s</td>" % (self.row.number,self.row.pk_field())
            if self.row.renderer.can_delete:
                s += "<td>%s</td>" % self.row.form["DELETE"]
        else:
            s += "<td>%d</td>" % (self.row.number)
        return mark_safe(s)


