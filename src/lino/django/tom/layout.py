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
    
class FieldElement(Element):
    def __init__(self,layout,name):
        a=name.split(":",1)
        if len(a) == 1:
            self.name = name
            self.picture = None
            self.widget_attrs = {}
        elif len(a) == 2:
            self.name = a[0]
            self.picture = a[1]
            a = a[1].split("x",1)
            if len(a) == 1:
                self.widget_attrs = dict(size=a[0])
            elif len(a) == 2:
                self.widget_attrs = dict(rows=a[0],cols=a[1])
            #~ else:
                #~ raise Exception("Invalid picture spec %s" % name)
            
        
    def __str__(self):
        if self.picture is None:
            return self.name
        return self.name + ":" + self.picture
            
    def setup_widget(self,widget):
        if isinstance(widget,forms.widgets.Input):
            widget.attrs.update(self.widget_attrs)
        elif isinstance(widget,forms.Textarea):
            widget.attrs.update(self.widget_attrs)
            
        #~ if self.picture is not None:
            #~ if isinstance(widget,forms.widgets.Input):
                #~ widget.attrs["size"] = self.picture
            #~ elif isinstance(widget,forms.Textarea):
                #~ rows,cols=self.picture.split("x")
                #~ widget.attrs["rows"] = rows
                #~ widget.attrs["cols"] = cols

    def render(self,renderer):
        r = renderer.details.get(self.name)
        if r is not None:
            return r(renderer.get_instance())
            #return r.render_to_string()
        if renderer.editing:
            return self.as_editable(renderer)
        return self.as_readonly(renderer)
        #return mark_safe(renderer.field_to_html(self))
        
        
    def as_readonly(self,renderer):
        instance = renderer.get_instance()
        value = getattr(instance,self.name)
        try:
            model_field = instance._meta.get_field(self.name)
        except models.FieldDoesNotExist,e:
            # so it is a method
            value=value()
            #~ from lino.django.tom import reports
            #~ if isinstance(value,reports.Report):
                #~ return value.as_html()
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
        if isinstance(widget, forms.CheckboxInput):
            if value:
                s = "[X]"
            else: 
                s = "[&nbsp;]"
            if renderer.show_labels:
                s += " " + label
        elif isinstance(widget, forms.Select):
            s = "[" + value + "]"
            if renderer.show_labels:
                s = label + "<br/>" + s
        else:
            self.setup_widget(widget)
            s = widget.render(self.name,value,
              attrs={"readonly":"readonly","class":"readonly"})
            if renderer.show_labels:
                s = label + "<br/>" + s
        return mark_safe(s)
        
    def as_editable(self,renderer):
        form = renderer.get_form()
        try:
            bf = form[self.name] # a BoundField instance
        except KeyError,e:
            #~ r = renderer.details.get(self.name)
            #~ if r is not None:
                #~ return r.render_to_string()
            return self.as_readonly(renderer)
        if bf.field.widget.is_hidden:
            return self.as_readonly(renderer)
        self.setup_widget(bf.field.widget)
        s = bf.as_widget()
        if renderer.show_labels and bf.label:
            if isinstance(bf.field.widget, forms.CheckboxInput):
                s = s + " " + bf.label_tag()
            else:
                s = bf.label_tag() + "<br/>" + s
        return mark_safe(s)
        
        
        
class Container(Element):
    def __init__(self,layout,*elements,**kw):
        assert isinstance(layout,Layout)
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
          element = BoundElement(self,renderer)
        )
        try:
            return render_to_string(self.template,context)
        except Exception,e:
            print e
            return mark_safe("<PRE>%s</PRE>" % e)

class HBOX(Container):
    template = "tom/includes/hbox.html"
        
class VBOX(Container):
    template = "tom/includes/vbox.html"
    
class GRID_ROW(Container):
    template = "tom/includes/grid_row.html"


class Layout:
    detail_reports = {}
    join_str = None
    vbox_class = VBOX
    hbox_class = HBOX
    def __init__(self,model,desc=None):
        #self._meta = meta
        if hasattr(self,"main"):
            main = self['main']
        else:
            if desc is None:
                desc = self.join_str.join([ 
                    f.name for f in model._meta.fields 
                    + model._meta.many_to_many])
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
            return FieldElement(self,name)
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
            return self.vbox_class(self,*lines)
        else:
            l=[]
            for name in desc.split():
                if not name.startswith("#"):
                    l.append(self[name])
            return self.hbox_class(self,*l)

class PageLayout(Layout):
    show_labels = True
    join_str = "\n"

class RowLayout(Layout):
    show_labels = False
    join_str = " "
    hbox_class = GRID_ROW
    vbox_class = None # not yet allowed

    

class BoundElement:
    def __init__(self,element,renderer):
        self.element = element
        self.renderer = renderer

    def as_html(self):
        return self.element.render(self.renderer)
  
    def children(self):
        assert isinstance(self.element,Container)
        for e in self.element.elements:
            yield BoundElement(e,self.renderer)
            
    def row_management(self):
        #print "row_management", self.element
        assert isinstance(self.element,GRID_ROW)
        row = self.renderer.get_row()
        s = "<td>%s</td>" % row.links()
        if self.renderer.editing:
            s += "<td>%d%s</td>" % (row.number,row.pk_field())
            if row.renderer.can_delete:
                s += "<td>%s</td>" % row.form["DELETE"]
        else:
            s += "<td>%d</td>" % (row.number)
        return mark_safe(s)
            



class LayoutRenderer:
    def __init__(self,layout,details={},editing=False):
        self.layout = layout
        #self.data = data # either a model instance or a form
        self.details = details
        self.show_labels = layout.show_labels
        self.editing = editing
        
    def __unicode__(self):
        return self.render_to_string()
        
    def render_to_string(self):
        main = self.layout._main
        context = dict(
          element = BoundElement(main,self),
        )
        s = render_to_string(main.template,context)
        #print main
        #print s
        return s
        
       
class FormLayoutRenderer(LayoutRenderer):
    def __init__(self,form,*args,**kw):
        LayoutRenderer.__init__(self,*args,**kw)
        self.form = form
        
    def get_form(self):
        return self.form
        
    def get_instance(self):
        return self.form.instance

class InstanceLayoutRenderer(LayoutRenderer):
    def __init__(self,instance,*args,**kw):
        LayoutRenderer.__init__(self,*args,**kw)
        self.instance = instance
        
    def get_instance(self):
        return self.instance

class RowLayoutRenderer(LayoutRenderer):
    def __init__(self,row,*args,**kw):
        LayoutRenderer.__init__(self,*args,**kw)
        self.row = row
        
    def get_row(self):
        return self.row
    def get_instance(self):
        return self.row.instance
    def get_form(self):
        return self.row.form


#~ class ShowLayoutRenderer(LayoutRenderer):
    #~ editing = False
    #template = "tom/includes/layout_show.html"
    #~ def field_to_html(self,field):
        #~ return field.as_readonly(self.data)
      
#~ class EditLayoutRenderer(LayoutRenderer):
    #~ editing = True
    #template = "tom/includes/layout_edit.html"
      
    #~ def field_to_html(self,field):
        #~ try:
            #~ bf = self.data[field.name] # a BoundField instance
        #~ except KeyError,e:
            #~ r = self.details.get(field.name)
            #~ if r is not None:
                #~ return r.render_to_string()
            #~ return field.as_readonly(self.data.instance)
        #~ if bf.field.widget.is_hidden:
            #~ return field.as_readonly(self.data.instance)
        #~ field.setup_widget(bf.field.widget)
        #~ s = bf.as_widget()
        #~ if bf.label:
            #~ if isinstance(bf.field.widget, forms.CheckboxInput):
                #~ s = s + " " + bf.label_tag()
            #~ else:
                #~ s = bf.label_tag() + "<br/>" + s
        #~ return s

            
#~ def page_layout(obj):
    #~ model = obj.__class__
    #~ if model.page_layout_instance is None:
        #~ if model.page_layout is None:
            #~ model.page_layout_instance = PageLayout(model._meta)
        #~ else:
            #~ model.page_layout_instance = obj.page_layout(model._meta)
    #~ return model.page_layout_instance
            
    #~ return PageLayout("\n".join([ 
      #~ f.name for f in opts.fields + opts.many_to_many]))
      
