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
#~ from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _

import lino
from lino.utils import perms, menus, actors
from lino import actions
from lino import datalinks

from lino.modlib.tools import resolve_model, model_label

LABEL_ALIGN_TOP = 'top'
LABEL_ALIGN_LEFT = 'left'
LABEL_ALIGN_RIGHT = 'right'



#~ def setup():
    #~ lino.log.info("Register Layouts...")
    #~ for layout in actors.actors_dict.values():
        #~ if isinstance(layout,PageLayout) and layout.__class__ is not PageLayout:
            #~ layout.setup()

    
class StaticText:
    def __init__(self,text):
        self.text = text


class LayoutHandle:
    """
    LayoutHandle analyzes a Layout and builds a tree of LayoutElements.
    
    """
    start_focus = None
    
    def __init__(self,dl,layout):
        # lino.log.debug('LayoutHandle.__init__(%s,%s,%d)',link,layout,index)
        assert isinstance(layout,Layout)
        #assert isinstance(link,reports.ReportHandle)
        self.ui = dl.ui
        self.layout = layout
        #~ if index == 1:
            #~ self.name = dl.name
        #~ else:
            #~ self.name = dl.name + str(index)
        #lino.log.debug('LayoutHandle.__init__(%s)',self.name)
        self.datalink = dl
        self.name = layout._actor_name
        self.label = layout.label or ''
        self._store_fields = []
        self._needed_stores = set()
        self.slave_grids = []
        self._store_fields = []
        self._buttons = []
        self.hide_elements = layout.get_hidden_elements(self)
        self.main_class = self.ui.main_panel_class(layout)
        if layout.main is not None:
        #~ if hasattr(layout,"main"):
            self._main = self.create_element(self.main_class,'main')
        else:
            main = self.layout.join_str.join(dl.data_elems())
            self._main = self.desc2elem(self.main_class,"main",main)
        if isinstance(self.layout,RowLayout):
            assert len(self._main.elements) > 0, "%s : Grid has no columns" % self.name
            self.columns = self._main.elements
            
        #~ self.width = self.layout.width or self._main.width
        #~ self.height = self.layout.height or self._main.height
        self.width = self._main.width
        self.height = self._main.height
        #~ self.write_debug_info()
        #~ self.default_button = None
        #~ if layout.default_button is not None:
            #~ for e in self._buttons:
                #~ if e.name == layout.default_button:
                    #~ self.default_button = e
                    #~ break
                
    def needs_store(self,rh):
        self._needed_stores.add(rh)
            
    def __str__(self):
        return str(self.layout) + " Handle"
        
    def unused__repr__(self):
        s = self.name # self.__class__.__name__ 
        if hasattr(self,'_main'):
            s += "(%s)" % self._main
        return s
        
    def setup_element(self,e):
        if e.name in self.hide_elements:
            self.hidden = True
            
    def setup(self):
        pass
        
        
    def get_absolute_url(self,**kw):
        return self.datalink.get_absolute_url(layout=self.index,**kw)
        
    def add_hidden_field(self,field):
        return HiddenField(self,field)
        
    def write_debug_info(self):
        if False:
            f = file(self.name+".debug.csv","w")
            f.write("\n".join(self._main.debug_lines()))
            f.close()
        
    def get_title(self,renderer):
        if self.layout.label is None:
            return self.datalink.get_title(renderer) 
        return self.datalink.get_title(renderer) + " - " + self.layout.label

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
                name for name in self.datalink.data_elems() \
                  if (name not in explicit_specs) \
                    and (name not in self.hide_elements)])
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
            if len(elems) == 1 and panelclass != self.main_class:
                return elems[0]
            #return self.vbox_class(self,name,*elems,**kw)
            return panelclass(self,desc_name,True,*elems,**kw)
        else:
            elems = []
            for x in desc.split():
                if not x.startswith("#"):
                    """
                    20100214 dsbe.PersonDetail hatte 2 MainPanels, 
                    weil PageLayout kein einzeiliges (horizontales) `main` vertrug
                    """
                    #~ e = self.create_element(panelclass,x) 
                    e = self.create_element(self.ui.Panel,x)
                    if e:
                        elems.append(e)
            if len(elems) == 1 and panelclass != self.main_class:
                return elems[0]
            #return self.hbox_class(self,name,*elems,**kw)
            return panelclass(self,desc_name,False,*elems,**kw)
            
    def create_element(self,panelclass,desc_name):
        #lino.log.debug("create_element(panelclass,%r)", desc_name)
        name,kw = self.splitdesc(desc_name)
        return self.ui.create_layout_element(self,panelclass,name,**kw)
        
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

class Layout(actors.HandledActor):
    """
    A Layout specifies how fields of a Report should be arranged when they are
    displayed in a form or a grid. 
    
    A layout descriptor is a plain text with some simple rules:
    - each word will lead to an element
    - ...todo...
   
    """
    # for internal use:
    _handle_class = LayoutHandle
    _handle_selector = datalinks.DataLink
    join_str = None # set by subclasses
    
    #~ label = None
    has_frame = False # True
    label_align = LABEL_ALIGN_TOP
    #label_align = LABEL_ALIGN_LEFT
    #label_align = 'left'
    default_button = None
    collapsible_elements  = {}
    main = None
    
    def get_hidden_elements(self,lh):
        return set()
        
    #~ def get_handle(self,dl):
        #~ return LayoutHandle(dl,self)
        

class FormLayout(Layout):
    #label = "Dialog"
    show_labels = True
    join_str = "\n"
    form = None
    title = None
    label_align = 'left'
    layout_command = None
    
    def setup(self):
        self.layout_command = actors.resolve_actor(self.layout_command,self.app_label)
        if self.layout_command is None:
            raise ValueError("%s : layout_command is None" % self)
        self.layout_command.forms[self._actor_name] = self
        #~ self.app_label = self.layout_command.app_label
    

class ModelLayout(Layout):
    layout_model = None
    def setup(self):
        lino.log.debug("ModelLayout.setup() %s",self)
        if self.layout_model is None:
            #~ raise ValueError("%s : layout_model is None" % self)
            pass 
            # e.g. contacts.contactdetail is an abstract ModelLayout
        else:
            self.layout_model = resolve_model(self.layout_model,self.app_label)
        #~ self.app_label = self.layout_model._meta.app_label
        
  
class RowLayout(ModelLayout):
    label = _("List")
    show_labels = False
    join_str = " "
    
    def get_hidden_elements(self,lh):
        if lh.datalink.report.hide_columns is None:
            return set()
        return set(lh.datalink.report.hide_columns.split())

class PageLayout(ModelLayout):
    label = _("Detail")
    show_labels = True
    join_str = "\n"
    def setup(self):
        ModelLayout.setup(self)
        if self.layout_model is not None:
            l = getattr(self.layout_model,'_lino_layouts',None)
            if l is None:
                l = []
                setattr(self.layout_model,'_lino_layouts',l)
            lino.log.debug('Register %s detail layout %d for %s',self,len(l),model_label(self.layout_model))
            l.append(self)
    

def row_layout_factory(rpt):
    cls = type(rpt._actor_name+"Grid",(RowLayout,),dict(app_label=rpt.app_label,main=rpt.column_names,layout_model=rpt.model))
    return actors.register_actor(cls())

