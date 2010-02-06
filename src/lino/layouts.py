## Copyright 2009-2010 Luc Saffre
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

#import traceback
#import types

#from django import forms
from django.db import models
from django.conf import settings
#from django.utils.safestring import mark_safe
#from django.utils.text import capfirst
#from django.template.loader import render_to_string
from django.contrib.contenttypes import generic

import lino
from lino.utils import perms, menus, actors
from lino import actions


LABEL_ALIGN_TOP = 'top'
LABEL_ALIGN_LEFT = 'left'
LABEL_ALIGN_RIGHT = 'right'


class DataLink:
    "inherited by lino.forms.FormHandle and lino.reports.ReportHandle"
    def __init__(self,ui,name):
        self.ui = ui
        self.name = name

    def try_get_virt(self,name):
        return None

    def get_absolute_url(self,*args,**kw):
        raise NotImplementedError

#~ def register_dialog_class(cls):
    #~ if cls.__name__ == 'DialogLayout':
        #~ return
    #~ lino.log.debug("register_layout_class(%s)", cls)
    #~ cls.app_label = cls.__module__.split('.')[-2]
    #~ dialogs.append(cls)
    
#~ def get_dialog(app_label,name):
    #~ app = models.get_app(app_label)
    #~ cls = getattr(app,name,None)
    #~ if cls is None:
        #~ return None
    #~ return cls()


#~ def setup():
    #~ lino.log.debug("Instantiate forms.")
    

#~ class DialogLayoutMetaClass(type):
    #~ def __new__(meta, classname, bases, classDict):
        #~ cls = type.__new__(meta, classname, bases, classDict)
        #~ register_dialog_class(cls)
        #~ return cls

    #~ def __init__(cls, name, bases, dict):
        #~ type.__init__(cls,name, bases, dict)
        #~ cls.instance = None 

    #~ def __call__(cls,*args,**kw):
        #~ if cls.instance is None:
            #~ cls.instance = type.__call__(cls,*args, **kw)
        #~ return cls.instance




class Layout:
    """
    A Layout specifies how fields of a Report should be arranged when they are
    displayed in a form or a grid. 
    
    Each Layout will get one LayoutHandle per UI that analyzes it's Layout's
    "descriptor" and builds a tree of LayoutElements. 
    
    A layout descriptor is a plain text with some simple rules:
    - each word will lead to an element
    - ...todo...
    
    """
    # for internal use:
    join_str = None # set by subclasses
    
    # the following may be overriddedn in subclasses:
    #target = None
    layout_for = None # not yet used
    label = None
    has_frame = False # True
    label_align = LABEL_ALIGN_TOP
    #label_align = LABEL_ALIGN_LEFT
    #label_align = 'left'
    default_button = None
    collapsible_elements  = {}
    
    

class RowLayout(Layout):
    label = "List"
    show_labels = False
    join_str = " "
    
    #~ def __init__(self,report,index,desc=None,main=None):
        #~ #from lino.utils import extjs
        #~ #self.main_class = extjs.MainGridElement
        #~ Layout.__init__(self,report,index,desc,main)
        #~ #print "RowLayout.__init__(%r,%r,%r,%r)" % (report.name,index,desc,main)
        #~ assert len(self._main.elements) > 0, "%s : Grid %s has no columns" % (report.name,self.ext_name)
        #~ self.columns = self._main.elements
        #~ #self._main = extjs.Panel(self,"scrollgrid",True,self._main,region="center",autoScroll=True)
    

class PageLayout(Layout):
    label = "Detail"
    show_labels = True
    join_str = "\n"
    #main_class = extjs.MainPanel
    #~ def __init__(self,*args,**kw):
        #~ from lino.utils import extjs
        #~ self.main_class = extjs.MainPanel
        #~ Layout.__init__(self,*args,**kw)
    
class FormLayout(Layout):
    #label = "Dialog"
    show_labels = True
    join_str = "\n"
    form = None
    title = None
    label_align = 'left'
    

class StaticText:
    def __init__(self,text):
          self.text = text
    def render(self,row):
        return self.text

class LayoutHandle:
    """
    todo: 
    - remove '_ld' attribute and test whether all external code is converted to use 'layout' instead
    - rename this. It is not a handle in the same meaning as for Report and Form.
    """
    start_focus = None
    
    def __init__(self,link,layout,index,desc=None,main=None):
        # lino.log.debug('LayoutHandle.__init__(%s,%s,%d)',link,layout,index)
        assert isinstance(link.name,basestring), "link.name %r is not a string" % link.name
        assert isinstance(layout,Layout)
        #assert isinstance(link,reports.ReportHandle)
        self.ui = link.ui
        self._ld = layout 
        self.layout = layout
        if index == 1:
            self.name = link.name
        else:
            self.name = link.name + str(index)
        #lino.log.debug('LayoutHandle.__init__(%s)',self.name)
        self.link = link
        self.index = index
        self.label = layout.label or ''
        #self.inputs = []
        self._store_fields = []
        self._needed_stores = set()
        self.slave_grids = []
        self._store_fields = []
        self._buttons = []
        self._main_class = self.ui.main_panel_class(layout)
        if hasattr(layout,"main"):
            self._main = self.create_element(self._main_class,'main')
        else:
            if desc is None:
                desc = self.layout.join_str.join(self.link.data_elems())
                #lino.log.debug('desc for %s is %r',self.name,desc)
                self._main = self.desc2elem(self._main_class,"main",desc)
            else:
                if not isinstance(desc,basestring):
                    raise Exception("%r is not a string" % desc)
                self._main = self.desc2elem(self._main_class,"main",desc)
        if isinstance(self.layout,RowLayout):
            assert len(self._main.elements) > 0, "%s : Grid %s has no columns" % (link.name,self.ext_name)
            self.columns = self._main.elements
            
        #~ self.width = self.layout.width or self._main.width
        #~ self.height = self.layout.height or self._main.height
        self.width = self._main.width
        self.height = self._main.height
        self.write_debug_info()
        self.default_button = None
        if layout.default_button is not None:
            for e in self._buttons:
                if e.name == layout.default_button:
                    self.default_button = e
                    break
                
    def needs_store(self,rh):
        self._needed_stores.add(rh)
            
    def __str__(self):
        return self.name # self.report.model._meta.app_label+"."+self.name # __class__.__name__
        
    def unused__repr__(self):
        s = self.name # self.__class__.__name__ 
        if hasattr(self,'_main'):
            s += "(%s)" % self._main
        return s
        
    def get_absolute_url(self,**kw):
        return self.link.get_absolute_url(layout=self.index,**kw)
        
    def add_hidden_field(self,field):
        return HiddenField(self,field)
        
    def write_debug_info(self):
        if False:
            f = file(self.name+".debug.csv","w")
            f.write("\n".join(self._main.debug_lines()))
            f.close()
        
        
    #~ def renderer(self,rr):
        #~ return LayoutRenderer(self,rr)
        
    #~ def get_title(self,renderer):
        #~ return self.link.get_title(renderer) 
        
    def get_title(self,renderer):
        if self.layout.label is None:
            return self.link.get_title(renderer) 
        return self.link.get_title(renderer) + " - " + self.layout.label
            

        
    def walk(self):
        return self._main.walk()
        
        
    def ext_lines(self,request):
        return self._main.ext_lines(request)
  
  
        
    def desc2elem(self,panelclass,desc_name,desc,**kw):
        #lino.log.debug("desc2elem(panelclass,%r,%r)",desc_name,desc)
        #assert desc != 'Countries_choices2'
        if '*' in desc:
            explicit_specs = set()
            for spec in desc.split():
                if spec != '*':
                    name,kw = self.splitdesc(spec)
                    explicit_specs.add(name)
            wildcard_fields = self.layout.join_str.join([
                name for name in self.link.data_elems() if name not in explicit_specs])
            desc = desc.replace('*',wildcard_fields)
            #lino.log.debug('desc -> %r',desc)
        if "\n" in desc:
            elems = []
            i = 0
            for x in desc.splitlines():
                x = x.strip()
                if len(x) > 0 and not x.startswith("#"):
                    i += 1
                    elems.append(self.desc2elem(self.ui.Panel,desc_name+'_'+str(i),x,**kw))
            if len(elems) == 1 and panelclass != self._main_class:
                return elems[0]
            #return self.vbox_class(self,name,*elems,**kw)
            return panelclass(self,desc_name,True,*elems,**kw)
        else:
            elems = []
            for x in desc.split():
                if not x.startswith("#"):
                    e = self.create_element(panelclass,x)
                    if e:
                        elems.append(e)
            if len(elems) == 1 and panelclass != self._main_class:
                return elems[0]
            #return self.hbox_class(self,name,*elems,**kw)
            return panelclass(self,desc_name,False,*elems,**kw)
            
    def create_element(self,panelclass,desc_name):
        lino.log.debug("create_element(panelclass,%r)", desc_name)
        name,kw = self.splitdesc(desc_name)
        
        if name == "_":
            return self.ui.Spacer(self,name,**kw)
            
        de = self.link.get_data_elem(name)
        
        if isinstance(de,models.Field):
            return self.create_field_element(de,**kw)
        if isinstance(de,generic.GenericForeignKey):
            return self.ui.VirtualFieldElement(self,name,de,**kw)
            
        from lino import reports
        
        if isinstance(de,reports.Report):
            e = self.ui.GridElement(self,name,de.get_handle(self.ui),**kw)
            self.slave_grids.append(e)
            return e
        if isinstance(de,actions.Action):
            e = self.ui.ButtonElement(self,name,de,**kw)
            self._buttons.append(e)
            return e
            
        from lino import forms
        
        if isinstance(de,forms.Input):
            e = self.ui.InputElement(self,de,**kw)
            if not self.start_focus:
                self.start_focus = e
            return e
        if callable(de):
            return self.create_meth_element(name,de,**kw)
            
        if not name in ('__str__','__unicode__','name','label'):
            value = getattr(self.layout,name,None)
            if value is not None:
                if isinstance(value,basestring):
                    return self.desc2elem(panelclass,name,value,**kw)
                if isinstance(value,StaticText):
                    return self.ui.StaticTextElement(self,name,value)
                raise KeyError("Cannot handle value %r in %s.%s." % (value,self.layout.name,name))
        msg = "Unknown element %r referred in layout %s" % (name,self.layout)
        #print "[Warning]", msg
        raise KeyError(msg)
        
    #~ def create_button_element(self,name,action,**kw):
        #~ e = self.ui.ButtonElement(self,name,action,**kw)
        #~ self._buttons.append(e)
        #~ return e
          
    def create_meth_element(self,name,meth,**kw):
        rt = getattr(meth,'return_type',None)
        if rt is None:
            rt = models.TextField()
        e = self.ui.MethodElement(self,name,meth,rt,**kw)
        assert e.field is not None,"e.field is None for %s.%s" % (self.layout,name)
        self._store_fields.append(e.field)
        return e
          
    #~ def create_virt_element(self,name,field,**kw):
        #~ e = self.ui.VirtualFieldElement(self,name,field,**kw)
        #~ return e
        
    def field2elem(self,field,**kw):
        # used also by lion.ui.extjs.MethodElement
        return self._main_class.field2elem(self,field,**kw)
        # return self.ui.field2elem(self,field,**kw)
        
    def create_field_element(self,field,**kw):
        e = self.field2elem(field,**kw)
        assert e.field is not None,"e.field is None for %s.%s" % (self.layout,name)
        self._store_fields.append(e.field)
        return e
        #return FieldElement(self,field,**kw)
        
    def splitdesc(self,picture):
        a = picture.split(":",1)
        if len(a) == 1:
            return picture,{}
        if len(a) == 2:
            name = a[0]
            a = a[1].split("x",1)
            if len(a) == 1:
                return name, dict(width=int(a[0]))
            elif len(a) == 2:
                return name, dict(width=int(a[0]),height=int(a[1]))
        raise Exception("Invalid picture descriptor %s" % picture)
                
