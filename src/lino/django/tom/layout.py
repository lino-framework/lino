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

from django.utils.safestring import mark_safe
from django.db import models
from django import forms


class Element:
    def as_html(self):
        raise NotImplementedError
        
class FIELD(Element):
    def __init__(self,name):
        a=name.split(":")
        if len(a) == 1:
            self.name = name
            self.size=None
        elif len(a) == 2:
            self.name = a[0]
            self.size=a[1]
            
    def __str__(self):
        if self.size is None:
            return self.name
        return self.name + ":" + self.size
            
    def setup_widget(self,widget):
        if self.size is not None:
            if isinstance(widget,forms.TextInput):
                widget.attrs["size"] = self.size
            elif isinstance(widget,forms.Textarea):
                rows,cols=self.size.split("x")
                widget.attrs["rows"] = rows
                widget.attrs["cols"] = cols
        
    def as_html(self,renderer):
        return mark_safe(renderer.field_to_html(self))
        
    def as_readonly(self,instance):
        value = getattr(instance,self.name)
        try:
            model_field = instance._meta.get_field(self.name)
        except models.FieldDoesNotExist,e:
            # so it is a method
            value=value()
            label=self.name
            widget=forms.TextInput()
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
            s = label + "<br/>[" + value+"]"
        else:
            s = widget.render(self.name,value,
              attrs={"readonly":"readonly","class":"readonly"})
            s = label + "<br/>" + s
        return s
        
    def render_boolean(self,value):
        """
        <input type="checkbox" readonly="readonly"> renders a normal checkbox
        """
        if value:
            return "[X]"
        return "[&nbsp;]"
        
        
class Container(Element):
    html_before = ''
    html_between = '\n'
    html_after = ''
    def __init__(self,*elements,**kw):
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
                            lines.append(HBOX(line))
                    self.elements.append(VBOX(*lines))
                else:
                    for fieldname in elem.split():
                        if not fieldname.startswith("#"):
                            self.elements.append(FIELD(fieldname))
            else:
                self.elements.append(elem)
        
    def as_html(self,renderer):
        return '\n'.join([ e.as_html(renderer) for e in self.elements])
          
    def as_html(self,renderer):
        s = self.html_before
        s += self.html_between.join(
          [e.as_html(renderer) for e in self.elements])
        s += self.html_after
        return mark_safe(s)
          
        
class HBOX(Container):
    html_before = '<table width="100%" class="hbox"><tr><td>'
    html_between = '</td>\n<td>'
    html_after = '</td></tr></table>'
        
class VBOX(Container):
    html_before = '<table class="vbox"><tr><td>'
    html_between = '</td><tr/>\n<tr><td>'
    html_after = '</td><tr/></table>'
    
        
    
        
class ShowLayoutRenderer:
    def __init__(self,layout,instance):
        self.layout = layout
        self.instance=instance
      
    def as_html(self):
        return self.layout.as_html(self)
        
        
    def field_to_html(self,field):
        return field.as_readonly(self.instance)
        
        
      
class EditLayoutRenderer:
    def __init__(self,layout,form):
        self.form = form
        self.layout = layout
      
    def as_html(self):
        return self.layout.as_html(self)
        
    def field_to_html(self,field):
        try:
            bf = self.form[field.name] # BoundField instance
        except KeyError,e:
            return field.as_readonly(self.form.instance)
        if bf.field.widget.is_hidden:
            return field.as_readonly(self.form.instance)
        field.setup_widget(bf.field.widget)
        s = bf.as_widget()
        if bf.label:
            if isinstance(bf.field.widget, forms.CheckboxInput):
                s = s + " " + bf.label_tag()
            else:
                s = bf.label_tag() + "<br/>" + s
        return s
        
            