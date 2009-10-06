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

from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from django import template 

from lino.django.utils import perms
        
class MenuItem:
  
    HOTKEY_MARKER = '~'
    def __init__(self,parent,name,label,doc=None,enabled=True,
                 can_view=perms.always):
        p = parent
        l = []
        while p is not None:
            if p in l:
                raise Exception("circular parent")
            l.append(p)
            p = p.parent
        self.parent = parent
        self.name = name
        self.doc = doc
        self.enabled = enabled
        if label is None:
            label = self.__class__.__name__
        n = label.find(self.HOTKEY_MARKER)
        if n != -1:
            label = label.replace(self.HOTKEY_MARKER,'')
            #label=label[:n] + '<u>' + label[n] + '</u>' + label[n+1:]
        self.label = label
        self.can_view = can_view
        

    def getLabel(self):
        return self.label
    
    def getDoc(self):
        return self.doc

    def __repr__(self):
        s = self.__class__.__name__+"("
        s += ', '.join([
            k+"="+repr(v) for k,v in self.interesting()])
        return s+")"
    
    def get_items(self):
        yield self
        
    def interesting(self,**kw):
        l = []
        if self.label is not None:
            l.append(('label',self.label.strip()))
        if not self.enabled:
            l.append( ('enabled',self.enabled))
        return l

    def parents(self):
        l = []
        p = self.parent
        while p is not None:
            l.append(p)
            p = p.parent
        return l
  
    def get_url_path(self):
        if self.parent:
            s = self.parent.get_url_path()
            if len(s) and not s.endswith("/"):
                s += "/"
        else:
            s='/'
        return s + self.name

    def as_html(self,request,level=None):
        #~ if not self.can_view.passes(request):
            #~ return u''
        return mark_safe('<a href="%s">%s</a>' % (
              self.get_url_path(),self.label))
              
    #~ def can_view(self,request):
        #~ return True
        
    #~ def as_ext(self,level=1):
        #~ #s = """ { text: "%s", href: "%s" } """ % (self.label,self.get_url_path())
        #~ s = """ { text: "%s", handler: %s } """ % (self.label,self.actor.as_ext())
        #~ #return mark_safe(s)
        #~ return s
        


        
class Action(MenuItem):
    def __init__(self,parent,actor=None,
                 name=None,label=None,
                 hotkey=None,url=None,
                 args=[],**kw):
        
        if not kw.has_key('can_view'):
            kw.update(can_view=actor.can_view)
        #name = name or actor.name
        label = label or actor.label
        self.args = args
        #self._url = url or actor.get_absolute_url(**params)
        assert actor is not None
        self.actor = actor
        self.hotkey = hotkey
        MenuItem.__init__(self,parent,name,label,**kw)
        
    def get_url_path(self):
        return self._url
        
    #~ def view(self,request):
        #~ return self.actor.view(request)
        
    #~ def get_urls(self,name):
        #~ return self.actor.get_urls(name)


class Menu(MenuItem):
    template_to_response = 'lino/menu.html'
    def __init__(self,name,label=None,parent=None,**kw):
        MenuItem.__init__(self,parent,name,label,**kw)
        self.items = []
        #self.items_dict = {}

    def add_action(self,actor,**kw):
        return self._add_item(Action(self,actor,**kw))

    def add_item(self,**kw):
        return self._add_item(Action(self,**kw))

    
    def add_menu(self,name,label,**kw):
        return self._add_item(Menu(name,label,self,**kw))
        
    def _add_item(self,m):
        assert isinstance(m,MenuItem)
        #~ old = self.items_dict.get(m.name,None)
        #~ if old:
            #~ i = self.items.index(old)
            #~ # print [ mi.name for mi in self.items ]
            #~ print "[debug] Replacing menu item %s at position %d" % (m.name,i)
            #~ # self.items[i] = m
            #~ # assert len(m) == 0
            #~ return old 
        #~ else:
            #print "[debug] Adding menu item %s" % m.name
        self.items.append(m)
        #self.items_dict[m.name] = m
        #~ if m.name in [i.name for i in self.items]:
            #~ raise "Duplicate item name %s for menu %s" % (m.name,self.name)
        return m
        
    def findItem(self,name):
        return self.items_dict[name]

    def get_items(self):
        for mi in self.items:
            for i in mi.get_items():
                yield i
        
    def sort_items(self,front=None,back=None):
        new_items = []
        if front:
            for name in front.split():
                new_items.append(self.findItem(name))
        back_items = []
        if back:
            for name in back.split():
                back_items.append(self.findItem(name))
        for i in self.get_items():
            if not i in new_items + back_items:
                new_items.append(i)
        self.items = new_items + back_items
        self.items_dict = {}
        for i in self.items:
            self.items_dict[i.name] = i
                

    def as_html(self,request,level=1):
        try:
            #~ if not self.can_view.passes(request):
                #~ return u''
            items = [i for i in self.items if i.can_view.passes(request)]
            if level == 1:
                s = '<ul class="jd_menu">' 
            else:
                #s = Component.as_html(self,request)
                s = self.label
                s += '\n<ul>' 
            for mi in items:
                s += '\n<li>%s</li>' % mi.as_html(request,level+1)
            s += '\n</ul>\n'
            return mark_safe(s)
        except Exception, e:
            traceback.print_exc(e)

    def unused_as_ext(self,level=1,**kw):
        #items = [i for i in self.items if i.can_view.passes(request)]
        items = self.items
        s = ""
        if len(items) == 0: return ''
        if level == 1:
            s += "{region:'north', height:27, items:[ "
        else:
            s += """
            {
            text: "%s",
            menu: { items: [
            """ % self.label
        s += ",\n".join([mi.as_ext(level+1) for mi in items])
        if level == 1:
            s += " ]} "
        else:
            s += """
            ]}}"""
        return s


#~ class MenuRenderer:
    #~ def __init__(self,menu,request):
        #~ self.menu = menu
        #~ self.request = request
        
    #~ def as_html(self):
        #~ return self.menu.as_html(self.request)
        
    #~ def as_ext(self):
        #~ return mark_safe(self.menu.as_ext(self.request))
      
        
