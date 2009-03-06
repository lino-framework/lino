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
    def __init__(self,name,label=None,doc=None,enabled=True):
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
        if self._label is not None:
            l.append(('label',self.getLabel().strip()))
        if not self.enabled:
            l.append( ('enabled',self.enabled))
        return l



class Button(Component):
    def __init__(self,name=None,label=None,
                 action=None,hotkey=None,
                 *args,**kw):
        Component.__init__(self,name,label,*args,**kw)
        self.action=action
        self.hotkey=hotkey

    def setAction(self,action):
        self.action = action

    def click(self):
        if self.enabled:
            return self.action()
        
        
class MenuItem(Button):
    pass

class Menu(Component):
    def __init__(self,*args,**kw):
        Component.__init__(self,*args,**kw)
        self.items = []

    def addItem(self,name,*args,**kw):
        assert not name in [i.name for i in self.items]
        i = MenuItem(name,*args,**kw)
        self.items.append(i)
        return i
    
    def addMenu(self,name,*args,**kw):
        mnu = Menu(name,*args,**kw)
        i = MenuItem(name,action=mnu,label=mnu.label)
        self.items.append(i)
        return i
        
    def findItem(self,name):
        for mi in self.items:
            if mi.name == name: return mi

    def get_items(self):
        for mi in self.items:
            yield mi
        
    def get_urls(self,name):
        urlpatterns = []
        urlpatterns += patterns('',url(r'^%s$' % name, self.view))
        for mi in self.items:
            urlpatterns += mi.action.get_urls(name+"/"+mi.name)
        return urlpatterns
        
        
    def view(self,request):
        context = dict(
            menu=self,
        )
        return render_to_response("tom/menu.html",context)
        

class MenuContainer:
    def __init__(self):
        self.menus = [] # Menu("menu")
        
    def addMenu(self,name,*args,**kw):
        assert not name in [m.name for m in self.menus]
        m=Menu(name,*args,**kw)
        self.menus.append(m)
        return m
        
    def getMenu(self,name):
        for m in self.menus:
            if m.name == name: return m
        
    #~ def addItem(self,*args,**kw):
        #~ return self.menu.addItem(*args,**kw)
        
    #~ def get_items(self):
        #~ return self.menu.get_items()
        
    def get_urls(self,name):
        #return self.menu.get_urls(name)
        urlpatterns = []
        #urlpatterns += self.menu.get_urls(name)
        for menu in self.menus:
            urlpatterns += menu.get_urls(name+"/"+menu.name)
        return urlpatterns
        
    def urls(self):
        return self.get_urls('')
    urls = property(urls)
    
    def view(self,request):
        context = dict(
            menus=self.menus,
        )
        return render_to_response("tom/index.html",context)
    
    