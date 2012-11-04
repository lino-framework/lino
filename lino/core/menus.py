# -*- coding: UTF-8 -*-
## Copyright 2009-2012 Luc Saffre
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

"""
Defines the classes :class:`MenuItem`
"""

import traceback
import copy

from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.shortcuts import render_to_response
#~ from django.utils.safestring import mark_safe
from django import template 
from django.utils.encoding import force_unicode
from django.db import models

from lino.core import actors
from lino.utils.jsgen import js_code
from lino.utils.xmlgen import html as xghtml

from lino.core import actions

class MenuItem:
    """
    Represents a menu item
    """
    HOTKEY_MARKER = '~'
    
    name = None
    
    def __init__(self,parent,action,
                 name=None,label=None,doc=None,enabled=True,
                 #~ can_view=None,
                 hotkey=None,params=None,
                 request=None,
                 instance=None,
                 href=None):
        self.parent = parent
        if action is not None:
            if not isinstance(action,actions.BoundAction):
                raise Exception("20121003 not a BoundAction: %r")
        self.bound_action = action
        self.params = params
        self.href = href
        self.request = request
        self.instance = instance
        
        if instance is not None:
            if label is None:
                label = unicode(instance)
                
        if action is not None:
            if label is None:
                label = action.get_button_label()
        
        if name is not None:
            self.name = name
        self.doc = doc
        self.enabled = enabled
        self.hotkey = hotkey
        
        if label:
            label = label.replace('~','')
        self.label = label
        
        
    def compress(self):
        pass

    def getLabel(self):
        return self.label
    
    def getDoc(self):
        return self.doc

    #~ def __repr__(self):
        #~ s = self.__class__.__name__+"("
        #~ s += ', '.join([
            #~ k+"="+repr(v) for k,v in self.interesting()])
        #~ return s+")"
    
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
  
    def get_url_path(self):
        if self.action:
            return str(self.action)
        if self.parent:
            s = self.parent.get_url_path()
            if len(s) and not s.endswith("/"):
                s += "/"
        else:
            s='/'
        if self.name:
            return s + self.name
        return s

    def as_html(self,ar,level=None):
        if self.bound_action:
            sr = ar.spawn(self.bound_action.actor,action=self.bound_action)
            url = sr.get_request_url()
        elif self.request:
            url = self.request.get_request_url()
        else:
            url = self.href
        assert self.label is not None
        if url is None:
            return xghtml.E.p() # spacer
            #~ raise Exception("20120901 %s" % self.__dict__)
        return xghtml.E.a(self.label,href=url)
        #~ return '<a href="%s">%s</a>' % (
              #~ self.get_url_path(),self.label)
              
    def menu_request(self,user):
        #~ if self.can_view.passes(user):
        return self
        
def has_items(menu):
    for i in menu.items:
        if not i.label.startswith('-'):
            return True
    return False


class Menu(MenuItem):
    """
    Represents a menu. A menu is conceptually a :class:`MenuItem` 
    which contains other menu items.
    """
    #~ template_to_response = 'lino/menu.html'
    def __init__(self,user,name,label=None,parent=None,**kw):
        MenuItem.__init__(self,parent,None,name,label,**kw)
        self.user = user
        self.clear()

    def clear(self):
        self.items = []
        self.items_dict = {}
        
    def compress(self):
        """
        Dynamically removes empty menu entries.
        Collapses menu with only one item into their parent.
        """
        for mi in self.items:
            mi.compress()
        newitems = []
        for mi in self.items:
            if isinstance(mi,Menu):
                #~ if len(mi.items) == 1:
                    #~ newitems.append(mi.items[0])
                #~ elif len(mi.items) > 1:
                    #~ newitems.append(mi)
                #~ if len(mi.items) > 0:
                if has_items(mi) > 0:
                    #~ if self.parent is None or len(mi.items) > 1:
                        #~ newitems.append(mi)
                    #~ elif len(mi.items) == 1:
                        #~ newitems.append(mi.items[0])
                    if len(mi.items) == 1:
                        if not mi.items[0].label.startswith('-'):
                            if self.parent is None:
                                newitems.append(mi)
                            else:
                                newitems.append(mi.items[0])
                    elif len(mi.items) > 1:
                        newitems.append(mi)
            else:
                newitems.append(mi)
        self.items = newitems
                
    def add_action(self,spec,action=None,**kw):
        if isinstance(spec,basestring):
            spec = settings.LINO.modules.resolve(spec)
            #~ a = actors.resolve_action(spec)
            #~ if a is None:
                #~ raise Exception("Could not resolve action specifier %r" % spec)
        if isinstance(spec,actions.BoundAction):
            a = spec
        elif isinstance(spec,type) and issubclass(spec,models.Model):
            if action:
                a = spec._lino_default_table.get_url_action(action)
            else:
                a = spec._lino_default_table.default_action
            #~ a = actions.BoundAction(spec._lino_default_table,a)
        elif isinstance(spec,type) and issubclass(spec,actors.Actor):
            if action:
                a = spec.get_url_action(action)
            else:
                a = spec.default_action
            #~ a = actions.BoundAction(spec,a)

        else:
            raise Exception("(%r,%r) is not a valid action specifier" % (spec,action))
        if a is None:
            raise Exception("add_action(%r,%r,%r) found None" % (spec,action,kw))
        #~ if kw.has_key('params'):
            #~ if a.actor.__name__ == 'Contacts':
              #~ raise Exception("20120103")
        return self._add_item(MenuItem(self,a,**kw))
        
    #~ def add_action_(self,action,**kw):
        #~ return self._add_item(MenuItem(self,action,**kw))

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
        return self._add_item(Menu(self.user,name,label,self,**kw))

    def get_item(self,name):
        return self.items_dict[name]

    #~ def add_url_button(self,url,label):
    def add_url_button(self,url,**kw):
        kw.update(href=url)
        return self._add_item(MenuItem(self,None,**kw))
        #~ self.items.append(dict(
          #~ xtype='button',text=label,
          #~ handler=js_code("function() {window.location='%s';}" % url)))

    def _add_item(self,mi):
        assert isinstance(mi,MenuItem)
        if mi.bound_action is not None:
            #~ if not mi.action.actor.get_view_permission(self.user):
            if not mi.bound_action.get_view_permission(self.user):
                return 
        if mi.name is not None:
            old = self.items_dict.get(mi.name)
            if old is not None:
                if mi.label != old.label:
                    raise Exception("Menu item %r labelled %s cannot override existing label %s" % (mi.name,mi.label,old.label))
                return old
            self.items_dict[mi.name] = mi
        self.items.append(mi)
        return mi
        
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
                

    def as_html(self,ar,level=1):
        items = [xghtml.E.li(mi.as_html(ar,level+1)) for mi in self.items]
        #~ print 20120901, items
        if level == 1:
            #~ return xghtml.E.ul(*items,class_='jd_menu')
            #~ return xghtml.E.ul(*items,id='navbar')
            #~ return xghtml.E.ul(*items,id='Navigation') # SelfHTML
            #~ return xghtml.E.ul(*items,class_='dd_menu')
            return xghtml.E.ul(*items,id='nav')
        assert self.label is not None
        return xghtml.E.p(self.label,xghtml.E.ul(*items))
      
    def old_as_html(self,request,level=1):
        try:
            if level == 1:
                s = '<ul class="jd_menu">' 
            else:
                #s = Component.as_html(self,request)
                s = self.label
                s += '\n<ul>' 
            for mi in self.items:
                s += '\n<li>%s</li>' % mi.as_html(request,level+1)
            s += '\n</ul>\n'
            return s
        except Exception, e:
            raise
            #~ traceback.print_exc(e)

    def menu_request(self,user):
        #~ if self.can_view.passes(user):
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
    """
    A Toolbar is a top-level :class:`Menu`.
    """
    pass

