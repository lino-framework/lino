## Copyright 2003-2009 Luc Saffre

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

def again(request,**kw):
    req=request.GET.copy()
    for k,v in kw.items():
        req[k] = v
    return mark_safe(request.path + "?" + req.urlencode())


class Link:
    def __init__(self,label,href):
        self.label=label
        self.href=href
        
    def as_html(self):
        return mark_safe('<a href="">%s</a>' % (self.href,self.label))

class Navigator:

    def __init__(self,request,page=None):
        self.request=request
        self.first=None
        self.previous=None
        self.next=None
        self.last=None
        if page is not None:
            self.fill_from_page(page)
            
    def again(self,**kw):
        return again(self,request,**kw)
            
    def fill_from_page(self,page)
        if page.has_next()
            self.next=Link("~Next",self.again(row=page.number+1))
        if page.has_previous()
            self.previous=Link("~Previous",self.again(row=page.number-1))
            
    
    def as_html(self):
        l = [ self.first, self.previous, self.next, self.last ]
        return " ".join([ e.as_html() for e in l if e is not None])
          