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

import os

from django.utils.translation import ugettext as _
from django.db import models

import lino
from lino import actions, layouts #, commands
from lino import reports
#~ from lino import forms
from lino.ui import base
from lino.core import actors
from lino.utils import menus
from lino.utils import choosers
from lino.utils import jsgen
#~ from lino.utils import build_url
from lino.utils.jsgen import py2js, js_code, id2js
from . import ext_elems, ext_requests
#~ from lino.ui.extjs import ext_viewport

#~ from lino.modlib.properties import models as properties

WC_TYPE_GRID = 'grid'
USE_FF_CONSOLE = False

class ActionRenderer(object):
    def __init__(self,ui,action):
        assert isinstance(action,actions.Action), "%r is not an Action" % action
        self.action = action
        self.ui = ui
        
    def update_config(self,wc):
        pass
        
    def js_render(self):
        yield "function(caller) { return new Lino.%s(caller,%s);}" % (self.__class__.__name__,py2js(self.config))
    
class DownloadRenderer(ActionRenderer):
  
    def js_render(self):
        url = '/'.join(('/api',self.action.actor.app_label,self.action.actor._actor_name))+'/'
        yield "function(caller) { "
        #~ yield "  console.log(caller.get_selected());"
        yield "  var l = caller.get_selected();"
        yield "  if (l.length == 0) Lino.notify('No selection.');"
        yield "  for (var i = 0; i < l.length; i++) "
        yield "    window.open(%r+l[i]+'?fmt=%s');" % (url,self.action.name)
        #~ yield "  caller.get_selected().forEach(function(pk) {"
        #~ yield "    console.log(pk);"
        #~ yield "    window.open(%r+pk+'.pdf');" % url
        #~ yield "  })"
        yield "}" 

class DeleteRenderer(ActionRenderer):
  
    def js_render(self):
        yield "function(caller) { Lino.delete_selected(caller); }"
        #~ yield "function() { Lino.delete_selected(this); }"

class WindowWrapper(ActionRenderer):
  
    window_config_type = None
    
    def __init__(self,action,ui,lh,main,**kw):
        ActionRenderer.__init__(self,ui,action)
        assert self.window_config_type is not None, "%s.window_config_type is None" % self.__class__
        self.main = main
        #~ self.permalink_name = str(action).replace('.','/')
        #~ self.permalink_name = str(action)
        self.lh = lh # may be None
        self.bbar_buttons = []
        self.config = self.get_config()
        #~ if ui.USE_WINDOWS:
            #~ self.main.update(autoHeight=True,height=None,width=None)
        
        
    def __str__(self):
        return self.ext_name + "(" + self.__class__.__name__ + ")"
        
    def get_config(self,**d):
        d.update(permalink_name=str(self.action))
        #~ wc = lh2win(self.lh)
        #~ wc = self.ui.load_window_config(self.action,**wc)
        #~ d.update(permalink_name=self.permalink_name)
        #~ d.update(wc=wc)
        #~ url = '/ui/' + '/'.join((self.action.actor.app_label,self.action.actor._actor_name,self.action.name))
        #~ d.update(url_action=url) # ,ext_requests.FMT_JSON))
        #~ d.update(handler=js_code("Lino.%s" % self.action)) 
        #~ d.update(ls_data_url=self.ui.get_actor_url(self.action.actor))
        return d
        
def lh2win(lh,**kw):
    #~ kw.update(height=300)
    #~ kw.update(width=400)
    if lh is not None:
        #~ kw.update(title=lh.get_title(None))
        #~ if lh.height is not None:
            #~ kw.update(height=lh.height*EXT_CHAR_HEIGHT + 7*EXT_CHAR_HEIGHT)
        #~ if lh.width is not None:
            #~ kw.update(width=lh.width*EXT_CHAR_WIDTH + 10*EXT_CHAR_WIDTH)
        if lh.start_focus is not None:
            kw.update(defaultButton=lh.start_focus.name)
    return kw
  

class MasterWrapper(WindowWrapper):
  
    def __init__(self,rh,action,lh,**kw):
        WindowWrapper.__init__(self,action,lh.ui,lh,lh._main,**kw)
        
    def js_render(self):
        yield "function(caller,params) { "
        #~ yield "  Ext.getCmp('main_area').el.setStyle({cursor:'wait'});"
        if USE_FF_CONSOLE:
            yield "  console.time('%s');" % self.action
        for ln in jsgen.declare_vars(self.config):
            yield '  '+ln
            
        yield "  var ww = new Lino.%s(caller,%s,params)" % (
            self.__class__.__name__,py2js(self.config))
            
        for e in self.main.walk():
            if e is not self.main and isinstance(e,ext_elems.GridElement):
                yield "  %s.ww = ww;" % e.ext_name
            
        yield "  ww.show();"
        if USE_FF_CONSOLE:
            yield "  console.timeEnd('%s');" % self.action
        yield "}"
        
            
    
class GridWrapperMixin(WindowWrapper):
  
    window_config_type = WC_TYPE_GRID
    
    def __init__(self,rh):
        self.rh = rh
    
    def get_config(self):
        d = super(GridWrapperMixin,self).get_config()
        d.update(content_type=self.rh.content_type)
        d.update(title=unicode(self.rh.get_title(None)))
        d.update(main_panel=self.lh._main)
        return d
        
    def update_config(self,wc):
        self.lh._main.update_config(wc)

class GridMasterWrapper(GridWrapperMixin,MasterWrapper):
  
    def __init__(self,rh,action,**kw):
        self.action = action
        GridWrapperMixin.__init__(self,rh)
        MasterWrapper.__init__(self,rh,action,rh.list_layout,**kw)
      

class BaseDetailWrapper(MasterWrapper):
  
    window_config_type = 'detail'
    
    def __init__(self,rh,action,**kw):
        self.rh = rh
        #~ assert isinstance(action,actions.BaseDetailAction)
        if len(rh.report.detail_layouts) == 1:
            lh = rh.report.detail_layouts[0].get_handle(rh.ui)
            main = ext_elems.FormPanel(rh,action,lh._main)
            WindowWrapper.__init__(self,action,rh.ui,lh,main,**kw)        
        else:
            lh = rh.report.detail_layouts[0].get_handle(rh.ui)
            tabs = [l.get_handle(rh.ui)._main for l in rh.report.detail_layouts]
            main = ext_elems.FormPanel(rh,action,ext_elems.TabPanel(tabs))
            WindowWrapper.__init__(self,action,rh.ui,None,main,**kw) 
        #~ self.config.update(ls_bbar_actions=[rh.ui.a2btn(a) for a in rh.get_actions(action)]) # if a.show_in_detail])
            
        
    def get_config(self):
        d = MasterWrapper.get_config(self)
        url = self.ui.build_url('api',self.action.actor.app_label,self.action.actor._actor_name)
        d.update(url_data=url) 
        d.update(main_panel=self.main)
        d.update(name=self.action.name)
        d.update(fk_name=self.action.actor.fk_name);
        #~ d.update(formdata=)
        return d
        
        
class DetailWrapper(BaseDetailWrapper):
    pass
    #~ def get_config(self):
        #~ d = BaseDetailWrapper.get_config(self)
        #~ d.update(ls_bbar_actions=[self.ui.a2btn(a) for a in self.rh.get_actions(self.action)])
        #~ return d
  
class InsertWrapper(BaseDetailWrapper):
    pass
    #~ def get_config(self):
        #~ d = BaseDetailWrapper.get_config(self)
        #~ d.update(title=_('%s into %s') %(self.action.label,self.action.actor.get_title(None)))
        #~ d.update(record_id=-99999)
        #~ return d


def key_handler(key,h):
    return dict(handler=h,key=key.keycode,ctrl=key.ctrl,alt=key.alt,shift=key.shift)


