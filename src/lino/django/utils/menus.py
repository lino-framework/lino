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
        
class Component:
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
    
    def interesting(self,**kw):
        l=[]
        if self.label is not None:
            l.append(('label',self.label.strip()))
        if not self.enabled:
            l.append( ('enabled',self.enabled))
        return l

    def parents(self):
        l = []
        p=self.parent
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
        try:
            if not self.can_view.passes(request):
                #print self.__class__.__name__, "as_html() : can_view failed" 
                return u''
            return mark_safe('<a href="%s">%s</a>' % (
                  self.get_url_path(),self.label))
        except Exception,e:
            traceback.print_exc(e)
              
    #~ def can_view(self,request):
        #~ return True
        
class MenuItem(Component):
    pass


class Action(MenuItem):
    def __init__(self,parent,actor,
                 name=None,label=None,
                 hotkey=None,
                 *args,**kw):
        
        if not kw.has_key('can_view'):
            kw.update(can_view=actor.can_view)
        if name is None:
            name = actor.name
        if label is None:
            label = actor.label
        Component.__init__(self,parent,name,label,*args,**kw)
        self.actor = actor
        self.hotkey = hotkey
        
    def view(self,request):
        return self.actor.view(request)
        
    def get_urls(self,name):
        return self.actor.get_urls(name)


class Menu(MenuItem):
    template_to_response = 'lino/menu.html'
    def __init__(self,name,label=None,parent=None,**kw):
        MenuItem.__init__(self,parent,name,label,**kw)
        self.items = []
        self.items_dict = {}

    def add_action(self,*args,**kw):
        return self.add_item(Action(self,*args,**kw))
        
    
    def add_menu(self,name,label,**kw):
        return self.add_item(Menu(name,label,self,**kw))
        
    def add_item(self,m):
        old = self.items_dict.get(m.name,None)
        if old:
            i = self.items.index(old)
            # print [ mi.name for mi in self.items ]
            print "[debug] Replacing menu item %s at position %d" % (m.name,i)
            self.items[i] = m
        else:
            self.items.append(m)
        self.items_dict[m.name] = m
        #~ if m.name in [i.name for i in self.items]:
            #~ raise "Duplicate item name %s for menu %s" % (m.name,self.name)
        return m
        
    def findItem(self,name):
        return self.items_dict[name]
        #~ for mi in self.items:
            #~ if mi.name == name: return mi

    def get_items(self):
        for mi in self.items:
            yield mi
        
    def as_html(self,request,level=1):
        try:
            if not self.can_view.passes(request):
                #print self.__class__.__name__, "as_html() : can_view failed" 
                return u''
            if level == 1:
                s = ''
            else:
                s = Component.as_html(self,request)
            s += '\n<ul class="menu%d">' % level
            for mi in self.items:
                s += '\n<li>%s</li>' % mi.as_html(request,level+1)
            s += '\n</ul>\n'
            return mark_safe(s)
        except Exception, e:
            traceback.print_exc(e)
        
    def get_urls(self,name=''):
        #print "Menu.get_urls()",name
        l = [url(r'^%s$' % name, self.view)]
        if len(name) and not name.endswith("/"):
            name += "/"
        for mi in self.items:
            l += mi.get_urls(name+mi.name)
        #print urlpatterns
        return patterns('',*l)
        
    def urls(self):
        return self.get_urls() #self.name)
    urls = property(urls)
        
        
    def view(self,request):
        from lino.django.utils.sites import lino_site
        context = lino_site.context(request,
            title = self.label,
            menu = MenuRenderer(self,request),
        )
        #return render_to_response("lino/menu.html",context)
        return render_to_response(self.template_to_response,
          context,
          context_instance=template.RequestContext(request))
        
        

class MenuRenderer:
    def __init__(self,menu,request):
        self.menu = menu
        self.request = request
        
    def as_html(self):
        return self.menu.as_html(self.request)