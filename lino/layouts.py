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

from django.db import models
from django.conf import settings
#from django.utils.safestring import mark_safe
#from django.utils.text import capfirst
#from django.template.loader import render_to_string
#~ from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _

import lino
from lino.utils import perms, menus
from lino.core import actors
#~ from lino import forms
from lino import actions
from lino.core import datalinks
#~ from lino import commands
from lino.ui import base

from lino.modlib.tools import resolve_model, model_label
from lino.core import coretools

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
        
#~ class Picture:
    #~ pass
    
class DataView:
    def __init__(self,tpl):
        self.xtemplate = tpl
        
#~ class TabPanelHandle(base.Handle):
  
    #~ def __init__(self,ui,layouts):
        #~ assert isinstance(layout,DetailLayout)
        #~ self.layouts = layouts
        #~ base.Handle.__init__(self,ui)
        #~ self.label = layout.label or ''
  
class LayoutHandle(base.Handle):
    """
    LayoutHandle analyzes a Layout and builds a tree of LayoutElements.
    
    """
    start_focus = None
    
    def __init__(self,ui,layout):
        # lino.log.debug('LayoutHandle.__init__(%s,%s,%d)',link,layout,index)
        assert isinstance(layout,Layout)
        #assert isinstance(link,reports.ReportHandle)
        base.Handle.__init__(self,ui)
        #~ actors.ActorHandle.__init__(self,layout)
        self.layout = layout
        #~ self.datalink = layout.get_datalink(ui)
        #~ self.name = layout._actor_name
        self.label = layout.label or ''
        self._store_fields = []
        #~ self._submit_fields = []
        self.slave_grids = []
        self._buttons = []
        self.hide_elements = layout.get_hidden_elements(self)
        self.main_class = self.ui.main_panel_class(layout)
        
        if layout.main is not None:
        #~ if hasattr(layout,"main"):
            self._main = self.create_element(self.main_class,'main')
        elif self.layout.datalink is not None:
            elems = [de.name for de in coretools.data_elems(self.layout.datalink) 
                if de.name != self.layout.datalink_report.fk_name]
            main = self.layout.join_str.join(elems)
            self._main = self.desc2elem(self.main_class,"main",main)
        else:
            raise Exception("%s has no datalink" % self.layout)
            
        if isinstance(self.layout,ListLayout):
            assert len(self._main.elements) > 0, "%s : Grid has no columns" % self
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
                
    #~ def needs_store(self,rh):
        #~ self._needed_stores.add(rh)
        
    def __str__(self):
        return str(self.layout) + "Handle"
        
    def has_field(self,f):
        return self._main.has_field(f)
    def unused__repr__(self):
        s = self.name # self.__class__.__name__ 
        if hasattr(self,'_main'):
            s += "(%s)" % self._main
        return s
        
    def setup_element(self,e):
        if e.name in self.hide_elements:
            self.hidden = True
            
    #~ def get_absolute_url(self,**kw):
        #~ return self.datalink.get_absolute_url(layout=self.index,**kw)
        
        
    def add_hidden_field(self,field):
        return HiddenField(self,field)
        
    def write_debug_info(self):
        if False:
            f = file(self.name+".debug.csv","w")
            f.write("\n".join(self._main.debug_lines()))
            f.close()
        
    def get_title(self,ar):
        return self.layout.get_title(ar)
        
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
                de.name for de in coretools.data_elems(self.layout.datalink) \
                  if (de.name not in explicit_specs) \
                    and (de.name not in self.hide_elements) \
                    and (de.name != self.layout.datalink_report.fk_name) \
                ])
            desc = desc.replace('*',wildcard_fields)
            #lino.log.debug('desc -> %r',desc)
        if "\n" in desc:
            elems = []
            i = 0
            for x in desc.splitlines():
                x = x.strip()
                if len(x) > 0 and not x.startswith("# "):
                    i += 1
                    e = self.desc2elem(self.ui.Panel,desc_name+'_'+str(i),x,**kw)
                    if e is not None:
                        elems.append(e)
            if len(elems) == 0:
                return None
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
            if len(elems) == 0:
                return None
            if len(elems) == 1 and panelclass != self.main_class:
                return elems[0]
            #return self.hbox_class(self,name,*elems,**kw)
            return panelclass(self,desc_name,False,*elems,**kw)
            
    def create_element(self,panelclass,desc_name):
        #lino.log.debug("create_element(panelclass,%r)", desc_name)
        name,kw = self.splitdesc(desc_name)
        e = self.ui.create_layout_element(self,panelclass,name,**kw)
        #~ for child in e.walk():
            #~ self._submit_fields += child.submit_fields()
        return e
        
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
        
        
#~ class ShowDetailAction(actions.OpenWindowAction):
    #~ needs_selection = True
    #~ name = 'detail'
    #~ label = _("Detail")
        

class Layout(actors.Actor):
    """
    A Layout specifies how fields of a Report should be arranged when they are
    displayed in a form or a grid. 
    
    A layout descriptor is a plain text with some simple rules:
    - each word will lead to an element
    - ...todo...
   
    """
    # for internal use:
    _handle_class = LayoutHandle
    #~ _handle_selector = datalinks.DataLink
    #~ _handle_selector = base.UI
    datalink = None
    datalink_report = None
    join_str = None # set by subclasses

    
    #~ label = None
    has_frame = False # True
    label_align = LABEL_ALIGN_TOP
    #label_align = LABEL_ALIGN_LEFT
    #label_align = 'left'
    default_button = None
    collapsible_elements  = {}
    main = None
    #~ layout_name = None
    
    #~ def __init__(self):
        #~ if self.layout_name is None:
            #~ self.layout_name = self.__class__.__name__
        #~ actors.Actor.__init__(self)
    
    def get_title(self,ar):
        if self.label is None:
            return self.datalink_report.get_title(ar) 
        return self.datalink_report.get_title(ar) + " - " + self.label

    def get_hidden_elements(self,lh):
        return set()
        
    #~ def get_handle(self,dl):
        #~ return LayoutHandle(dl,self)
        
    #~ def do_setup(self):
        #~ self.default_action = ShowDetailAction(self)
        
        
class unused_FormLayout(Layout):
    #label = "Dialog"
    show_labels = True
    join_str = "\n"
    #~ form = None
    title = None
    label_align = 'left'
    #~ layout_command = None
    #~ actions = [actions.Cancel,actions.OK]
    
    #~ def do_setup(self):
        #~ self.datalink = forms.Form(self)
    #~ def do_setup(self):
        #~ self.datalink = actors.resolve_actor(self.datalink,self.app_label)
        #~ assert isinstance(self.datalink,commands.Command), \
          #~ "datalink for %s is %r, must be a Command." % (self,self.datalink)
        #~ self.datalink._forms[self._actor_name] = self
    
    def get_datalink(self,ui):
        return self.datalink.get_handle(ui)
        

class ModelLayout(Layout):
    #~ layout_model = None
    def do_setup(self):
        #~ lino.log.debug("ModelLayout.setup() %s",self)
        if self.datalink is None:
            if self.datalink_report is not None:
                self.datalink = self.datalink_report.model
            else:
                pass # e.g. contacts.contactdetail is an abstract ModelLayout
        else:
            self.datalink = resolve_model(self.datalink,self.app_label)
            assert issubclass(self.datalink,models.Model), \
              "datalink for %s is %r, must be a Model." % (self,self.datalink)
            if self.datalink_report is None:
                self.datalink_report = coretools.get_model_report(self.datalink)
        
          
        #~ self.app_label = self.layout_model._meta.app_label
        
  
class ListLayout(ModelLayout):
    label = _("List")
    show_labels = False
    join_str = " "
    
    def unused_get_hidden_elements(self,lh):
        if lh.datalink.report.hide_columns is None:
            return set()
        return set(lh.datalink.report.hide_columns.split())

class DetailLayout(ModelLayout):
    label = _("Detail")
    show_labels = True
    join_str = "\n"
    
    def do_setup(self):
        ModelLayout.do_setup(self)
        if self.datalink is not None:
            l = getattr(self.datalink,'_lino_layouts',None)
            if l is None:
                l = []
                setattr(self.datalink,'_lino_layouts',l)
            #~ lino.log.debug('Register DetailLayout %s as %r for model %s',
                #~ self,self._actor_name,model_label(self.datalink))
            new_details = []
            found = False
            #~ if len(l) > 0:
                #~ print self,l
            for dtl in l:
                if self._actor_name == dtl._actor_name:
                    #~ lino.log.debug('Detail %r : replaced %r by %r',dtl._actor_name,dtl.__class__,self)
                    new_details.append(self)
                    found = True
                else:
                    new_details.append(dtl)
            if not found:
                new_details.append(self)
            setattr(self.datalink,'_lino_layouts',new_details)
            #~ if len(new_details) > 1:
                #~ print self,new_details

#~ class TabPanelLayout(ModelLayout):
    #~ _handle_class = TabPanelLayoutHandle
    #~ def __init__(self,tabs):
        #~ if self.layout_name is None:
            #~ self.layout_name = self.__class__.__name__
        #~ self.tabs = tabs
        #~ actors.Actor.__init__(self)
    
    
            
def get_detail_layout(model):
    if len(model._lino_layouts) > 0:
        return model._lino_layouts[0]
            

def list_layout_factory(rpt):
    cls = type(rpt._actor_name+"List",(ListLayout,),dict(
      app_label=rpt.app_label,
      main=rpt.column_names,
      datalink_report=rpt
    ))
    #~ return type(rpt._actor_name+"List",(ListLayout,),dict(app_label=rpt.app_label,main=rpt.column_names,datalink=rpt.model))
    #~ cls = type(rpt._actor_name+"List",(ListLayout,),dict(app_label=rpt.app_label,main=rpt.column_names,datalink=rpt.model))
    layout = cls()
    #~ layout.setup()
    return actors.register_actor(layout)

