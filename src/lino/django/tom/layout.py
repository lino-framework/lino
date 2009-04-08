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


from django import forms
from django.db import models
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


            
class Element:
    pass
    
class FIELD(Element):
    def __init__(self,name):
        a=name.split(":")
        if len(a) == 1:
            self.name = name
            self.picture = None
        elif len(a) == 2:
            self.name = a[0]
            self.picture = a[1]
            
    def __str__(self):
        if self.picture is None:
            return self.name
        return self.name + ":" + self.picture
            
    def setup_widget(self,widget):
        if self.picture is not None:
            if isinstance(widget,forms.TextInput):
                widget.attrs["size"] = self.picture
            elif isinstance(widget,forms.Textarea):
                rows,cols=self.picture.split("x")
                widget.attrs["rows"] = rows
                widget.attrs["cols"] = cols

    def render(self,renderer):
        return mark_safe(renderer.field_to_html(self))
        
        
    def as_readonly(self,instance):
        value = getattr(instance,self.name)
        try:
            model_field = instance._meta.get_field(self.name)
        except models.FieldDoesNotExist,e:
            # so it is a method
            value=value()
            from lino.django.tom import reports
            if isinstance(value,reports.Report):
                return value.as_html()
            label=self.name
            #widget=widget_for_value(value)
            widget = forms.TextInput()
        else:
            label = model_field.verbose_name
            form_field = model_field.formfield() 
            if form_field is None:
                form_field = forms.CharField()
                #return ''
            #print self.instance, field.name
            widget = form_field.widget
        if value is None:
            value = ''
        else:
            value = unicode(value)
        self.setup_widget(widget)
        if isinstance(widget, forms.CheckboxInput):
            if value:
                s = "[X]"
            else: 
                s = "[&nbsp;]"
            s += " " + label
        elif isinstance(widget, forms.Select):
            s = label + "<br/>[" + value + "]"
        else:
            s = widget.render(self.name,value,
              attrs={"readonly":"readonly","class":"readonly"})
            s = label + "<br/>" + s
        return s
        
        
        
        
class Container(Element):
    def __init__(self,layout,*elements,**kw):
        assert isinstance(layout,PageLayout)
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
        
    def render(self,renderer):
        context = dict(
          element = ElementRenderer(self,renderer)
        )
        return render_to_string(self.template,context)
        
        
          
        
class HBOX(Container):
    template = "tom/includes/hbox.html"
        
class VBOX(Container):
    template = "tom/includes/vbox.html"
    
        
class PageLayout:
    detail_reports = None
    def __init__(self,desc=None):
        if desc is None:
            main = self['main']
        else:
            main = self.desc2elem(desc)
        self._main = main
        #~ for name in dir(self.__class__):
            #~ spec = getattr(self.__class__,name)
            #~ box = VBOX(spec)
            #~ if name == 'layout':
                #~ self._layout = box
                
    def __getitem__(self,name):
        try:
            s = getattr(self.__class__,name)
        except AttributeError,e:
            #~ print "%s has no attribute %s" % (
              #~ self.__class__.__name__,name)
            return FIELD(name)
        return self.desc2elem(s)

    def desc2elem(self,desc):
        if "\n" in desc:
            lines=[]
            for line in desc.splitlines():
                line = line.strip()
                if len(line) > 0 and not line.startswith("#"):
                    lines.append(self.desc2elem(line))
                    #lines.append(HBOX(layout,line))
                    #lines.append(layout,line)
            return VBOX(self,*lines)
        else:
            l=[]
            for name in desc.split():
                if not name.startswith("#"):
                    l.append(self[name])
            return HBOX(self,*l)
        

    #~ def as_html(self,*args,**kw):
        #~ return self._main.as_html(*args,**kw)





class ElementRenderer:
    def __init__(self,element,renderer):
        self.element = element
        self.renderer = renderer
        #self.template = element.template
        
    def as_html(self):
        s = self.element.render(self.renderer)
        #print "as_html(%s) -> %d" % (self.element, len(s))
        return s
  
    def children(self):
        for e in self.element.elements:
            yield ElementRenderer(e,self)
  
    def field_to_html(self,field):
        return self.renderer.field_to_html(field)
        
        
    
class LayoutRenderer:
    def __init__(self,layout,data,details={}):
        self.layout = layout
        self.data = data # either a model instance or a form
        self.details = details
        
    #~ def as_html(self):
        #~ return self.layout.as_html(self)
        
    #~ def __getitem__(self,name):
        #~ try:
            #~ return self.data.__getitem__(name)
        #~ except KeyError:
            #~ return self.details[name]
        
    def as_html(self):
        main = self.layout._main
        context = dict(
          element = ElementRenderer(main,self),
        )
        return render_to_string(main.template,context)
        
    def field_to_html(self,field):
        raise NotImplementedError
        
class ShowLayoutRenderer(LayoutRenderer):
    template = "tom/includes/layout_show.html"
    def field_to_html(self,field):
        return field.as_readonly(self.data)
      
class EditLayoutRenderer(LayoutRenderer):
    template = "tom/includes/layout_edit.html"
      
    def field_to_html(self,field):
        try:
            bf = self.data[field.name] # BoundField instance
        except KeyError,e:
            if self.details.has_key(field.name):
                #print "coucou", field.name
                r = self.details[field.name]
                #print "coco", r
                return r.render_to_string()
                #~ try:
                    #~ s = r.render_to_string()
                #~ except Exception,e:
                    #~ return str(e)
                #~ #print "caca", s
                #~ return s
            return field.as_readonly(self.data.instance)
        if bf.field.widget.is_hidden:
            return field.as_readonly(self.data.instance)
        field.setup_widget(bf.field.widget)
        s = bf.as_widget()
        if bf.label:
            if isinstance(bf.field.widget, forms.CheckboxInput):
                s = s + " " + bf.label_tag()
            else:
                s = bf.label_tag() + "<br/>" + s
        return s



            
def page_layout(obj):
    if obj.page_layout is not None:
        return obj.page_layout()  
    opts = obj._meta
    return PageLayout("\n".join([ 
      f.name for f in opts.fields + opts.many_to_many]))
      
