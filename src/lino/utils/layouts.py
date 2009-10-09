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

#import traceback
#import types
import logging

#from django import forms
from django.db import models
from django.conf import settings
#from django.utils.safestring import mark_safe
#from django.utils.text import capfirst
#from django.template.loader import render_to_string

def get_unbound_meth(cl,name):
    meth = getattr(cl,name,None)
    if meth is not None:
        return meth
    for b in cl.__bases__:
        meth = getattr(b,name,None)
        if meth is not None:
            return meth



class Layout:
    """
    A Layout specifies how fields of a Report should be arranged when they are
    displayed in a form or a grid. When instanciated, a Layout analyzes its 
    "descriptor" and builds a tree of LayoutElements. 
    
    A layout descriptor is a plain text with some simple rules:
    - each word will lead to an element
    - ...todo...
    
    """
    join_str = None # set by subclasses
    main_class = None
    
    
    def __init__(self,report,index,desc=None,main=None):
        from lino.utils import extjs
        #from . import reports
        #assert isinstance(report,reports.Report)
        # Component.__init__(self,report.name + str(index))
        self.name = report.name + str(index)
        self.slave_grids = []
        self.report = report
        self.index = index
        self._store_fields = []
        logging.debug("Layout.__init__() : %s", self.name)
        if main is None:
            if hasattr(self,"main"):
                main = self.create_element(self.main_class,'main')
            else:
                if desc is None:
                    desc = self.join_str.join([ 
                        f.name for f in report.model._meta.fields 
                        + report.model._meta.many_to_many])
                main = self.desc2elem(self.main_class,"main",desc)
                #print main
        self._main = main
        self.store = extjs.Store(self)
        
    def desc2elem(self,panelclass,name,desc,**kw):
        from lino.utils import extjs
        #print "desc2elem()", repr(name),repr(desc)
        #assert desc != 'Countries_choices2'
        if "\n" in desc:
            elems = []
            i = 0
            for x in desc.splitlines():
                x = x.strip()
                if len(x) > 0 and not x.startswith("#"):
                    i += 1
                    elems.append(self.desc2elem(extjs.Panel,name+'_'+str(i),x,**kw))
            if len(elems) == 1 and panelclass != self.main_class:
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
            if len(elems) == 1 and panelclass != self.main_class:
                return elems[0]
            #return self.hbox_class(self,name,*elems,**kw)
            return panelclass(self,name,False,*elems,**kw)
            
    #~ def create_container(self,name,vertical,*elems,**kw):
        #~ return MainPanel(self,name,vertical,*elems,**kw)
            
    def create_element(self,panelclass,name):
        from lino.utils import extjs
        #print "create_element()", name
        name,kw = self.splitdesc(name)
        if not name in ('__str__','__unicode__','name','label'):
            value = getattr(self,name,None)
            if value is not None:
                if type(value) == str:
                    return self.desc2elem(panelclass,name,value,**kw)
                if isinstance(value,extjs.StaticText):
                    return value
        rpt = self.report.get_slave(name)
        if rpt is not None:
            #rpt.setup()
            #slaverpt = slaveclass()
            #self._slave_dict[name] = slaverpt
            #elems = rpt.row_layout._main.elements
            #elems = rpt.row_layout.columns
            e = extjs.GridElement(self,name,rpt,**kw)
            self.slave_grids.append(e)
            return e
        try:
            field = self.report.model._meta.get_field(name)
        except models.FieldDoesNotExist,e:
            meth = get_unbound_meth(self.report.model,name)
            if meth is not None:
                e = extjs.MethodElement(self,name,meth,**kw)
                assert e.field is not None,"e.field is None for %s.%s" % (self,name)
                self._store_fields.append(e.field)
                return e
        else:
            e = extjs.field2elem(self,field,**kw)
            assert e.field is not None,"e.field is None for %s.%s" % (self,name)
            self._store_fields.append(e.field)
            return e
            #return FieldElement(self,field,**kw)
        msg = "Unknown element %r referred in layout %s[%d]" % (name,self.report,self.index)
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
                
    def __str__(self):
        return self.report.model._meta.app_label+"."+self.name # __class__.__name__
        
    def __repr__(self):
        s = self.__class__.__name__ 
        if hasattr(self,'_main'):
            s += "(%s)" % self._main
        return s
        
    def add_hidden_field(self,field):
        return HiddenField(self,field)
        
    def renderer(self,rr):
        return LayoutRenderer(self,rr)
        
    def get_label(self):
        if self.label is None:
            return self.__class__.__name__
        return self.label
        
    def get_title(self):
        return self.report.get_title(None) + " - " + self.get_label()
        
    def walk(self):
        return self._main.walk()
        
        
    def ext_lines(self,request):
        return self._main.ext_lines(request)
    
        
class RowLayout(Layout):
    label = "List"
    show_labels = False
    join_str = " "
    
    def __init__(self,report,index,desc=None,main=None):
        from lino.utils import extjs
        self.main_class = extjs.MainGridElement
        Layout.__init__(self,report,index,desc,main)
        #print "RowLayout.__init__(%r,%r,%r,%r)" % (report.name,index,desc,main)
        assert len(self._main.elements) > 0, "%s : Grid %s has no columns" % (report.name,self.ext_name)
        self.columns = self._main.elements
        #self._main = extjs.Panel(self,"scrollgrid",True,self._main,region="center",autoScroll=True)
    

class PageLayout(Layout):
    label = "Detail"
    show_labels = True
    join_str = "\n"
    #main_class = extjs.MainPanel
    def __init__(self,*args,**kw):
        from lino.utils import extjs
        self.main_class = extjs.MainPanel
        Layout.__init__(self,*args,**kw)
    
        
                
