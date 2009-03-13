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


from django.conf.urls.defaults import patterns, url, include
from django.shortcuts import render_to_response

        
class Component:
    def __init__(self,parent,name,label,doc=None,enabled=True):
        self.parent=parent
        self.name=name
        self.label=label or self.__class__.__name__
        self.doc=doc
        self.enabled=enabled

    def getLabel(self):
        return self.label
    
    def getDoc(self):
        return self.doc

    def __repr__(self):
        s=self.__class__.__name__+"("
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


class MenuItem(Component):
  
    def parents(self):
        l = []
        p=self.parent
        while p is not None:
            l.append(p)
            p = p.parent
        return l
  
    def get_url_path(self):
        return "/".join([p.name for p in self.parents() if len(p.name) ] + [self.name])


class Action(MenuItem):
    def __init__(self,parent,actor,
                 name=None,label=None,
                 hotkey=None,
                 *args,**kw):
        if name is None:
            name=actor.__class__.__name__.lower()
        if label is None:
            label=actor.getLabel()
        Component.__init__(self,parent,name,label,*args,**kw)
        self.actor=actor
        self.hotkey=hotkey
        
    def view(self,request):
        return self.actor.view(request)
        
    def get_urls(self,name):
        return self.actor.get_urls(name)
        
class Menu(MenuItem):
    def __init__(self,name,label=None,parent=None,**kw):
        MenuItem.__init__(self,parent,name,label,**kw)
        self.items = []

    def addAction(self,*args,**kw):
        return self.add_item(Action(self,*args,**kw))
    
    def addMenu(self,name,label,**kw):
        return self.add_item(Menu(name,label,self,**kw))
        
    def add_item(self,m):
        if m.name in [i.name for i in self.items]:
            raise "Duplicate item name %s for menu %s" % (m.name,self.name)
        self.items.append(m)
        return m
        
    def findItem(self,name):
        for mi in self.items:
            if mi.name == name: return mi

    def get_items(self):
        for mi in self.items:
            yield mi
        
    def get_urls_old(self,name=''):
        #print "Menu.get_urls()",name
        urlpatterns = patterns('',
          url(r'^%s$' % name, self.view))
        if len(name):
            name += "/"
        for mi in self.items:
            urlpatterns += mi.get_urls(name+mi.name)
        #print urlpatterns
        return urlpatterns
        
    def get_urls(self,name=''):
        #print "Menu.get_urls()",name
        l=[url(r'^%s$' % name, self.view)]
        if len(name):
            name += "/"
        for mi in self.items:
            l += mi.get_urls(name+mi.name)
        #print urlpatterns
        return l
        
    def urls(self):
        l = self.get_urls(self.name)
        return patterns('',*l)
    urls = property(urls)
        
    def view(self,request):
        context = dict(
            menu=self,
        )
        return render_to_response("tom/menu.html",context)
        
        

