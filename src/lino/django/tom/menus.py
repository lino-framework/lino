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
    def get_url_path(self):
        s=self.name
        p=self.parent
        while p is not None:
            s = p.name + "/" + s
            p = p.parent
        return "/"+s


class Action(MenuItem):
    def __init__(self,parent,name,label=None,
                 action=None,hotkey=None,
                 *args,**kw):
        Component.__init__(self,parent,name,label,*args,**kw)
        self.action=action
        self.hotkey=hotkey
        
    def view(self,request):
        return self.action.view(request)
        
    def get_urls(self,name):
        return self.action.get_urls(name)
        
class Menu(MenuItem):
    def __init__(self,*args,**kw):
        MenuItem.__init__(self,*args,**kw)
        self.items = []

    def addAction(self,name,*args,**kw):
        if name in [i.name for i in self.items]:
            raise "Duplicate item name %s for menu %s" % (name,self.name)
        i = Action(self,name,*args,**kw)
        self.items.append(i)
        return i
    
    def addMenu(self,name,*args,**kw):
        if name in [i.name for i in self.items]:
            raise "Duplicate item name %s for menu %s" % (name,self.name)
        mnu = Menu(self,name,*args,**kw)
        #i = MenuItem(self,name,action=mnu,label=mnu.label)
        self.items.append(mnu)
        return mnu
        
    def findItem(self,name):
        for mi in self.items:
            if mi.name == name: return mi

    def get_items(self):
        for mi in self.items:
            yield mi
        
    def get_urls(self,name):
        #print "Menu.get_urls()",name
        urlpatterns = patterns('',
          url(r'^%s$' % name, self.view))
        for mi in self.items:
            urlpatterns += mi.get_urls(name+"/"+mi.name)
        #print urlpatterns
        return urlpatterns
        
    def urls(self):
        return self.get_urls(self.name)
    urls = property(urls)
        
    def view(self,request):
        context = dict(
            menu=self,
        )
        return render_to_response("tom/menu.html",context)
        
        

#~ class MenuContainer:
    #~ def __init__(self):
        #~ self.menus = [] # Menu("menu")
        
    #~ def addMenu(self,name,*args,**kw):
        #~ assert not name in [m.name for m in self.menus]
        #~ m=Menu(None,name,*args,**kw)
        #~ self.menus.append(m)
        #~ return m
        
    #~ def getMenu(self,name):
        #~ for m in self.menus:
            #~ if m.name == name: return m
        
    #~ def get_urls(self,name):
        #~ #return self.menu.get_urls(name)
        #~ urlpatterns = []
        #~ #urlpatterns += self.menu.get_urls(name)
        #~ urlpatterns = patterns('',
          #~ url(r'^%s$' % name, self.view))
        #~ for menu in self.menus:
            #~ if len(name):
                #~ urlpatterns += menu.get_urls(name+"/"+menu.name)
            #~ else:
                #~ urlpatterns += menu.get_urls(menu.name)
        #~ return urlpatterns
        
    #~ def urls(self):
        #~ return self.get_urls('')
    #~ urls = property(urls)
    
    #~ def view(self,request):
        #~ context = dict(
            #~ menus=self.menus,
            #~ title="Main Menu"
        #~ )
        #~ return render_to_response("tom/index.html",context)
    
    