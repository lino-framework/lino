## Copyright 2009 Luc Saffre
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

import lino

class FormReport:
    "Wrapper around a Django form to make it usable as report of a PageLayout."
    def __init__(self,form):
        self.app_label = form.__module__.split()[-2]
        self.name = form.name

    def get_fields(self):
        return [ f.name for f in self.form.fields ]
          
    def get_slave(self,name):
        return None
        
    def try_get_meth(self,name):
        return None
        
    def try_get_field(self,name):
        try:
            return self.form[name]
        except KeyError,e:
            pass

    def get_title(self,renderer):
        return self.form.title or self.form.label

class Layout:
    """
    A Layout specifies how fields of a Report should be arranged when they are
    displayed in a form or a grid. When instanciated, a Layout analyzes its 
    "descriptor" and builds a tree of LayoutElements. 
    
    A layout descriptor is a plain text with some simple rules:
    - each word will lead to an element
    - ...todo...
    
    """
    target = None
    join_str = None # set by subclasses
    label = None
    
    
    def get_label(self):
        if self.label is None:
            return self.__class__.__name__
        return self.label
        
    
    
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
    
        
class StaticText:
    def __init__(self,text):
          self.text = text
    def render(self,row):
        return self.text


class LayoutHandle:
  
    def __init__(self,report,layout,index,desc=None,main=None):
        assert isinstance(layout,Layout)
        #assert isinstance(report,reports.ReportHandle)
        self.ui = report.ui
        self._ld = layout
        self.name = report._rd.app_label + "_" + report._rd.name + str(index)
        lino.log.debug('LayoutHandle.__init__(%s)',self.name)
        self.report = report
        self.index = index
        lino.log.debug("Layout.__init__() : %s", self.name)
        self._store_fields = []
        self.slave_grids = []
        self._store_fields = []
        self._main_class = self.ui.main_panel_class(layout)
        if hasattr(layout,"main"):
            self._main = self.create_element(self._main_class,'main')
        else:
            if desc is None:
                desc = self._ld.join_str.join(self.report.get_fields())
                self._main = self.desc2elem(self._main_class,"main",desc)
            else:
                if not isinstance(desc,basestring):
                    raise Exception("%r is not a string" % desc)
                self._main = self.desc2elem(self._main_class,"main",desc)
        if isinstance(self._ld,RowLayout):
            assert len(self._main.elements) > 0, "%s : Grid %s has no columns" % (report.name,self.ext_name)
            self.columns = self._main.elements
                
        
            
    def __str__(self):
        return self.name # self.report.model._meta.app_label+"."+self.name # __class__.__name__
        
    def unused__repr__(self):
        s = self.name # self.__class__.__name__ 
        if hasattr(self,'_main'):
            s += "(%s)" % self._main
        return s
        
    def add_hidden_field(self,field):
        return HiddenField(self,field)
        
    #~ def renderer(self,rr):
        #~ return LayoutRenderer(self,rr)
        
    def get_title(self):
        return self.report._rd.get_title(None) + " - " + self._ld.get_label()
        
    def walk(self):
        return self._main.walk()
        
        
    def ext_lines(self,request):
        return self._main.ext_lines(request)
  
  
        
    def desc2elem(self,panelclass,name,desc,**kw):
        #lino.log.debug("desc2elem(%r,%r)", name,desc)
        #assert desc != 'Countries_choices2'
        if "\n" in desc:
            elems = []
            i = 0
            for x in desc.splitlines():
                x = x.strip()
                if len(x) > 0 and not x.startswith("#"):
                    i += 1
                    elems.append(self.desc2elem(self.ui.Panel,name+'_'+str(i),x,**kw))
            if len(elems) == 1 and panelclass != self._main_class:
                return elems[0]
            #return self.vbox_class(self,name,*elems,**kw)
            return panelclass(self,name,True,*elems,**kw)
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
            return panelclass(self,name,False,*elems,**kw)
            
    def create_element(self,panelclass,name):
        #print "create_element()", name
        name,kw = self.splitdesc(name)
        if not name in ('__str__','__unicode__','name','label'):
            value = getattr(self._ld,name,None)
            if value is not None:
                if type(value) == str:
                    return self.desc2elem(panelclass,name,value,**kw)
                if isinstance(value,self.StaticText):
                    return self.ui.StaticText(value)
        rpt = self.report.get_slave(name)
        if rpt is not None:
            #rpt.setup()
            #slaverpt = slaveclass()
            #self._slave_dict[name] = slaverpt
            #elems = rpt.row_layout._main.elements
            #elems = rpt.row_layout.columns
            e = self.ui.GridElement(self,name,rpt.get_handle(self.ui),**kw)
            self.slave_grids.append(e)
            return e
        field = self.report._rd.try_get_field(name)
        if field is None:
            meth = self.report._rd.try_get_meth(name)
            if meth is not None:
                e = self.ui.MethodElement(self,name,meth,**kw)
                assert e.field is not None,"e.field is None for %s.%s" % (self._ld,name)
                self._store_fields.append(e.field)
                return e
        else:
            e = self.ui.field2elem(self,field,**kw)
            assert e.field is not None,"e.field is None for %s.%s" % (self._ld,name)
            self._store_fields.append(e.field)
            return e
            #return FieldElement(self,field,**kw)
        msg = "Unknown element %r referred in layout %s" % (name,self.name)
        #print "[Warning]", msg
        raise KeyError(msg)
        
         
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
                
