# -*- coding: UTF-8 -*-
## Copyright 2009-2011 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.


import traceback
import copy

from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from django import template 
from django.utils.encoding import force_unicode

from lino.core import actors
from lino.utils import perms
from lino.utils.jsgen import js_code
from lino.core import actions

class MenuItem:
  
    HOTKEY_MARKER = '~'
    
    def __init__(self,parent,action,
                 name=None,label=None,doc=None,enabled=True,
                 can_view=None,hotkey=None,params=None,
                 request=None,
                 instance=None,
                 href=None):
        #~ p = parent
        #~ l = []
        #~ while p is not None:
            #~ if p in l:
                #~ raise Exception("circular parent")
            #~ l.append(p)
            #~ p = p.parent
        self.parent = parent
        
        self.action = action
        #~ if params is None and action is not None:
            #~ params = action.actor.default_params
        #~ if params is not None:
        self.params = params
            
        #~ if params:
            #~ assert request is None
            #~ assert action is not None
            #~ request = action.request(**params)
            
        #~ self.params = params
        self.href = href
        self.request = request
        self.instance = instance
        
        if instance is not None:
            if label is None:
                label = unicode(instance)
                
        if action is not None:
            if name is None:
                name = action.name
            if label is None:
                label = action.get_button_label()
            if can_view is None:
                can_view = action.can_view
        
        self.name = name
        self.doc = doc
        self.enabled = enabled
        self.hotkey = hotkey
        
        if label:
            #~ if "~" in label:
            label = label.replace('~','')
        self.label = label
        
        self.can_view = can_view or perms.always
        
        

    def getLabel(self):
        return self.label
    
    def getDoc(self):
        return self.doc

    def __repr__(self):
        s = self.__class__.__name__+"("
        s += ', '.join([
            k+"="+repr(v) for k,v in self.interesting()])
        return s+")"
    
    def walk_items(self):
        yield self
        
    #~ def interesting(self,**kw):
        #~ l = []
        #~ if self.label is not None:
            #~ l.append(('label',self.label.strip()))
        #~ if not self.enabled:
            #~ l.append( ('enabled',self.enabled))
        #~ return l

    #~ def parents(self):
        #~ l = []
        #~ p = self.parent
        #~ while p is not None:
            #~ l.append(p)
            #~ p = p.parent
        #~ return l
  
    #~ def get_url_path(self):
        #~ if self.parent:
            #~ s = self.parent.get_url_path()
            #~ if len(s) and not s.endswith("/"):
                #~ s += "/"
        #~ else:
            #~ s='/'
        #~ return s + self.name

    #~ def as_html(self,request,level=None):
        #~ return mark_safe('<a href="%s">%s</a>' % (
              #~ self.get_url_path(),self.label))
              
    def menu_request(self,user):
        if self.can_view.passes(user):
            return self
        


class Menu(MenuItem):
    #~ template_to_response = 'lino/menu.html'
    def __init__(self,name,label=None,parent=None,**kw):
        MenuItem.__init__(self,parent,None,name,label,**kw)
        self.items = []
        #~ self.items_dict = {}

    def add_action(self,spec,**kw):
        if isinstance(spec,basestring):
            action = actors.resolve_action(spec)
            if action is None:
                raise Exception("%r is not a valid action specifier" % spec)
        elif isinstance(spec,actions.Action):
            action = spec
        elif issubclass(spec,actors.Actor):
            action = spec().default_action
        else:
            raise Exception("%r is not a valid action specifier" % spec)
        #~ if isinstance(actor,basestring):
            #~ actor = actors.resolve_action(actor)
            #~ actor = actors.get_actor(actor)
        #~ if can_view is None:
            #~ can_view = actor.can_view
        #~ return self._add_item(Action(self,actor,can_view=can_view,**kw))
        return self._add_item(MenuItem(self,action,**kw))
        
    def add_action_(self,action,**kw):
        return self._add_item(MenuItem(self,action,**kw))

    #~ def add_item(self,**kw):
        #~ return self._add_item(Action(self,**kw))
        
    def add_request_action(self,rr,**kw):
        kw.update(request=rr)
        return self._add_item(MenuItem(self,rr.action,**kw))
        
    def add_instance_action(self,obj,**kw):
        kw.update(instance=obj)
        return self._add_item(MenuItem(self,None,**kw))
   
    def add_item(self,name,label,**kw):
        return self._add_item(MenuItem(self,None,name,label,**kw))
        
    def add_separator(self,label,**kw):
        return self._add_item(MenuItem(self,None,None,label,**kw))
        
    def add_menu(self,name,label,**kw):
        return self._add_item(Menu(name,label,self,**kw))

    #~ def add_url_button(self,url,label):
    def add_url_button(self,url,**kw):
        kw.update(href=url)
        return self._add_item(MenuItem(self,None,**kw))
        #~ self.items.append(dict(
          #~ xtype='button',text=label,
          #~ handler=js_code("function() {window.location='%s';}" % url)))

    def _add_item(self,m):
        assert isinstance(m,MenuItem)
        #~ old = self.items_dict.get(m.name,None)
        #~ if old:
            #~ i = self.items.index(old)
            # print [ mi.name for mi in self.items ]
            # print "[debug] Replacing menu item %s at position %d" % (m.name,i)
            #~ self.items[i] = m
            #~ self.items_dict[m.name] = m
            #~ # assert len(m) == 0
            #~ return old 
        #~ else:
            #print "[debug] Adding menu item %s" % m.name
        self.items.append(m)
        #~ self.items_dict[m.name] = m
        #~ if m.name in [i.name for i in self.items]:
            #~ raise "Duplicate item name %s for menu %s" % (m.name,self.name)
        return m
        
    #~ def get(self,name):
        #~ return self.items_dict.get(name)

    def walk_items(self):
        yield self
        for mi in self.items:
            for i in mi.walk_items():
                yield i
        
    #~ def unused_sort_items(self,front=None,back=None):
        #~ new_items = []
        #~ if front:
            #~ for name in front.split():
                #~ new_items.append(self.findItem(name))
        #~ back_items = []
        #~ if back:
            #~ for name in back.split():
                #~ back_items.append(self.findItem(name))
        #~ for i in self.get_items():
            #~ if not i in new_items + back_items:
                #~ new_items.append(i)
        #~ self.items = new_items + back_items
        #~ self.items_dict = {}
        #~ for i in self.items:
            #~ self.items_dict[i.name] = i
                

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

    def menu_request(self,user):
        if self.can_view.passes(user):
            m = copy.copy(self)
            items = []
            for i in m.items:
                meth = getattr(i,'menu_request',None)
                if meth is None:
                    items.append(i)
                else:
                    r = meth(user)
                    #~ r = i.menu_request(user)
                    if r is not None:
                        items.append(r)
            m.items = items
            return m

class Toolbar(Menu):
    pass


#~ def menu_request(menu,request):
    #~ if menu.can_view.passes(request):
        #~ m = copy.copy(menu)
        #~ items = [i for i in m.items if i.can_view.passes(request)]
        #~ m.items = items
        #~ return m

