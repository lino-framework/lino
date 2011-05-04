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

import os

from django.utils.translation import ugettext as _
from django.db import models
from django.conf import settings

import lino
from lino import actions
from lino import reports
#~ from lino import forms
from lino.ui import base
from lino.core import actors
from lino.utils import menus
#~ from lino.utils import choosers
from lino.utils import jsgen
#~ from lino.utils import build_url
from lino.utils.jsgen import py2js, js_code, id2js
from . import ext_elems
from lino.ui import requests as ext_requests

#~ from lino.ui.extjs import ext_viewport

#~ from lino.modlib.properties import models as properties

#~ WC_TYPE_GRID = 'grid'
#~ USE_FF_CONSOLE = True

class ActionRenderer(object):
    def __init__(self,ui,action):
        assert isinstance(action,actions.Action), "%r is not an Action" % action
        self.action = action
        self.ui = ui
        
    def update_config(self,wc):
        pass
        
    def js_render(self):
        yield "Lino.%s = function(caller) { " % self.action
        yield "    return new Lino.%s(caller,%s);}" % (
            self.__class__.__name__,py2js(self.config))

class WindowWrapper(ActionRenderer):
   
    def __init__(self,action,ui,lh,main,**kw):
        ActionRenderer.__init__(self,ui,action)
        self.main = main
        self.lh = lh # may be None
        self.bbar_buttons = []
        self.config = self.get_config()
        
    def __str__(self):
        return self.ext_name + "(" + self.__class__.__name__ + ")"
        
    def get_config(self,**d):
        #~ d.update(permalink_name=str(self.action))
        return d
        

class MasterWrapper(WindowWrapper):
  
    def __init__(self,rh,action,lh,**kw):
        WindowWrapper.__init__(self,action,lh.rh.ui,lh,lh._main,**kw)
        
    def js_render(self):
        yield "Lino.%s = function(caller,params) { " % self.action
        #~ yield "function(caller,params) { "
        #~ yield "  Ext.getCmp('main_area').el.setStyle({cursor:'wait'});"
        #~ yield "Lino.notify();"
        if False and settings.USE_FIREBUG:
            yield "  console.time('%s');" % self.action
            #~ yield "  console.log('ext_windows',20100930,params);"
        yield "  var ww = new Lino.%s(caller,%s,params);" % (
            self.__class__.__name__,py2js(self.config))
        
        #~ yield "  ww.main_item = %s;" % self.main.as_ext()
        
        for ln in jsgen.declare_vars(self.main):
            yield '  '+ln
        yield "  ww.main_item = %s;" % self.main.as_ext()
            
        yield "  ww.show();"
        if False and settings.USE_FIREBUG:
            yield "  console.timeEnd('%s');" % self.action
        yield "}"
        
            
    
class GridWrapperMixin(WindowWrapper):
  
    #~ window_config_type = WC_TYPE_GRID
    
    def __init__(self,rh):
        self.rh = rh
    
    def get_config(self):
        d = super(GridWrapperMixin,self).get_config()
        d.update(content_type=self.rh.content_type)
        #~ d.update(title=unicode(self.rh.get_title(None)))
        #~ 20101022 d.update(main_panel=self.lh._main)
        return d
        
    def update_config(self,wc):
        self.lh._main.update_config(wc)

class GridMasterWrapper(GridWrapperMixin,MasterWrapper):
  
    def __init__(self,rh,action,**kw):
        self.action = action
        GridWrapperMixin.__init__(self,rh)
        MasterWrapper.__init__(self,rh,action,rh.list_layout,**kw)
      

class BaseDetailWrapper(MasterWrapper):
  
    def __init__(self,rh,action,**kw):
        self.rh = rh
        details = rh.get_detail_layouts()
        if len(details) == 1:
            self.tabbed = False
            lh = details[0]
            #~ lh.label = None
            main = ext_elems.FormPanel(rh,action,lh._main,method=self.method)
            WindowWrapper.__init__(self,action,rh.ui,lh,main,**kw)        
        else:
            self.tabbed = True
            tabs = [lh._main for lh in details]
            main = ext_elems.FormPanel(rh,action,ext_elems.TabPanel(tabs),method=self.method)
            WindowWrapper.__init__(self,action,rh.ui,None,main,**kw) 
            
        
    def get_config(self):
        d = MasterWrapper.get_config(self)
        url = self.ui.build_url('api',self.action.actor.app_label,self.action.actor._actor_name)
        d.update(content_type=self.rh.content_type)
        d.update(url_data=url) 
        #~ 20101022 d.update(main_panel=self.main)
        d.update(name=self.action.name)
        d.update(fk_name=self.action.actor.fk_name);
        return d
        
        
class DetailWrapper(BaseDetailWrapper):
    method = 'PUT'
  
    def js_render_formpanel(self):
        yield "Lino.%s.FormPanel = Ext.extend(Lino.FormPanel,{" % self.main.rh.report
        yield "  constructor : function(ww,config) {"
        for ln in jsgen.declare_vars(self.main.main):
            yield '  '+ln
        yield "  config.items = %s;" % self.main.main.as_ext()
        if self.main.listeners:
            yield "  config.listeners = %s;" % py2js(self.main.listeners)
        yield "  config.before_row_edit = %s;" % py2js(self.main.before_row_edit)
        yield "  Lino.%s.FormPanel.superclass.constructor.call(this, ww,config);" % self.main.rh.report
        yield "  }"
        yield "});"
        yield ""
        

    def js_render(self):
        assert isinstance(self.main,ext_elems.FormPanel)
        for ln in self.js_render_formpanel():
            yield ln
        for ln in MasterWrapper.js_render(self):
            yield ln

  
class InsertWrapper(BaseDetailWrapper):
    method = 'POST'
    def get_config(self):
        d = BaseDetailWrapper.get_config(self)
        d.update(record_id=-99999);
        return d
        


def key_handler(key,h):
    return dict(handler=h,key=key.keycode,ctrl=key.ctrl,alt=key.alt,shift=key.shift)


