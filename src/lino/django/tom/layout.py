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
            
        
    def as_html(self,renderer):
        return mark_safe(renderer.field_to_html(self))
        
        
class Container(Element):
    html_before = ''
    html_between = '\n'
    html_after = ''
    def __init__(self,label,*elements):
        self.label = label
        self.elements = []
        for elem in elements:
            if type(elem) == str:
                for fieldname in elem.split():
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
        model_field = self.instance._meta.get_field(field.name)
        return model_field.verbose_name
        
      
class EditLayoutRenderer:
    def __init__(self,layout,form):
        self.form = form
        self.layout = layout
      
    def as_html(self):
        return self.layout.as_html(self)
            
    def field_to_html(self,field):
        bf = self.form[field.name] # BoundField instance
        if field.size is not None:
            if isinstance(bf.field.widget,forms.TextInput):
                bf.field.widget.attrs["size"] = field.size
            elif isinstance(bf.field.widget,forms.Textarea):
                rows,cols=field.size.split("x")
                bf.field.widget.attrs["rows"] = rows
                bf.field.widget.attrs["cols"] = cols
        s = bf.as_widget()
        if bf.label:
            if isinstance(bf.field.widget, forms.CheckboxInput):
                s = s + " " + bf.label_tag()
            else:
                s = bf.label_tag() + "<br/>" + s
        return s
        
            