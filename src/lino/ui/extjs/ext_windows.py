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

import lino
from lino import actions, layouts, commands
from lino import reports
from lino import forms
from lino.ui import base
from lino.core import actors
from lino.utils import menus
from lino.utils import chooser
from lino.utils import jsgen
from lino.utils.jsgen import py2js, js_code, id2js
from lino.ui.extjs import ext_elems, ext_requests
from lino.ui.extjs import ext_viewport

from lino.modlib.properties import models as properties

WC_TYPE_GRID = 'grid'


#~ class Param:
    #~ def parse(self,s):
        #~ return s
    
#~ class CharParam(Param):
    #~ pass
  
#~ class IntegerParam(Param):
    #~ pass
        
#~ class ListOfIntParam(Param):
    #~ def parse(self,s):
        #~ return s
      

class SaveWindowConfig(commands.Command):
  
    name = forms.Input()
    window_config_type = forms.Input()
    height = forms.Input()
    width = forms.Input()
    x = forms.Input()
    y = forms.Input()
    maximized = forms.Input()
    column_widths = forms.List()
    
    #~ params_def = dict(
      #~ name=actions.CharParam(),
      #~ type=actions.CharParam(),
      #~ height=actions.IntegerParam(),
      #~ width=actions.IntegerParam(),
      #~ x=actions.IntegerParam(),
      #~ y=actions.IntegerParam(),
      #~ maximized=actions.BooleanParam(),
      #~ column_widths=actions.ListOfIntParam(),
    #~ )
  
    def run_in_dlg(self,dlg):
        wc = WindowConfig(dlg.params)
        yield dlg.confirm(u"Save %s\nAre you sure?" % wc)
        dlg.ui.save_window_config(wc.name,wc) 
        yield dlg.notify(u"%s has been saved" % wc).over()
        
def parse_bool(s):
    return s == 'true'
    
def parse_int(s,default=None):
    if s is None: return None
    return int(s)

class WindowConfig:
    "pickleable object"
    def __init__(self,params):
        self.name = params.get('name')
        self.type = params.get('window_config_type')
        self.height = parse_int(params.get('height'))
        self.width = parse_int(params.get('width'))
        self.maximized = parse_bool(params.get('max'))
        self.x = parse_int(params.get('x'))
        self.y = parse_int(params.get('y'))
        cw = params.get('column_widths',None)
        if cw is not None: 
            assert type(cw) is list
            cw = [parse_int(w,100) for w in cw]
            #~ ocw = cw
            #~ for w in ocw:
                #~ if w: 
                    #~ cw.append(parse_int(w))
                #~ else:
                    #~ cw.append(100)
            #~ cw = map(int,cw)
        self.column_widths = cw
        
    def __unicode__(self):
        return u"WindowConfig %r (%r,%r,%r,%r,%r,%r,%r)" % (
          self.name,
          self.type,self.x,self.y,self.height,self.width,
          self.maximized,self.column_widths)



class WrappedWindow(jsgen.Component):
    declare_type = jsgen.DECLARE_THIS
    value_template = "new Ext.Window(%s)"
    
    def __init__(self,ww,ui,name,main,permalink_name,**kw):
        self.wrapper = ww
        self.ui = ui
        #~ self.lh = lh # may be None
        #~ if lh is not None:
            #~ kw.update(title=lh.get_title(None))
        self.main = main
        self.permalink_name = permalink_name
        
        #~ kw.update(title=self.rr.get_title())
        #~ kw.update(title=self.label)
        # kw.update(closeAction='hide')
        kw.update(maximizable=True)
        #kw.update(id=name)
        kw.update(layout='fit')
        kw.update(items=self.main)
        js = 'Lino.save_window_config(this)'
        kw.update(tools=[
          dict(id='save',handler=js_code(js),
              qtip=_("Save window config %s") % permalink_name )])
        
        jsgen.Component.__init__(self,name,**kw)
        
    def subvars(self):
        yield self.main


class WindowWrapper(jsgen.Object):
  
    window_config_type = None
    
    def __init__(self,name,window):
        #~ permalink_name = id2js(rr.layout.name)
        assert window.ext_name == 'window', ("expected 'window' but got %r" % window.ext_name)
        assert self.window_config_type is not None, "%s.window_config_type is None" % self.__class__
        self.window = window
        self.slave_windows = []
        self.bbar_buttons = []
        jsgen.Object.__init__(self,name)
        self.config = self.get_config()
        
        
    def subvars(self):
        for w in self.slave_windows:
            yield w
        for b in self.bbar_buttons:
            yield b
        yield self.window
        
        
    def __str__(self):
        return self.ext_name + "(" + self.__class__.__name__ + ")"
        
    def js_main(self):
        yield "// main %s" % self
        
    def js_get_values(self):
        return []
        
    def js_show(self):
        return []
        
    def js_add_row_listener(self):
        yield "console.log('js_add_rowlistener() not implemented')"
        
    def js_window_config(self):
        return []
        
    def js_on_window_render(self):
        return []
        
    def js_preamble(self):
        return []
        
    def try_apply_window_config(self,wc):
        try:
            self.apply_window_config(wc)
        except Exception,e:
            lino.log.warning("Error while applying window_config %s:",wc.name)
            lino.log.exception(e)
      
    def apply_window_config(self,wc):
        
        #~ if wc is None:
            #~ if win.lh is not None:
                #~ if win.lh.height is None:
                    #~ win.update(height=300)
                #~ else:
                    #~ win.update(height=win.lh.height*EXT_CHAR_HEIGHT + 7*EXT_CHAR_HEIGHT)
                #~ if win.lh.width is None:
                    #~ win.update(width=400)
                #~ else:
                    #~ win.update(width=win.lh.width*EXT_CHAR_WIDTH + 10*EXT_CHAR_WIDTH)
        if isinstance(wc,WindowConfig):
            self.window.update(x=wc.x)
            self.window.update(y=wc.y)
            self.window.update(width=wc.width)
            self.window.update(height=wc.height)
            self.window.update(maximized=wc.maximized)
        
        #~ if win.lh is not None: # report.use_layouts:
            #~ if win.lh.start_focus is not None:
                #~ win.update(defaultButton=win.lh.start_focus.name)
        #win.update(defaultButton=self.lh.link.inputs[0].name)
      
    def get_config(self,**d):
        wc = self.window.ui.load_window_config(self.window.permalink_name)
        self.try_apply_window_config(wc)
        for k in 'width','height','x','y','maximized':
            v = self.window.value.get(k,None)
            if v is not None:
                d[k] = v
        d.update(permalink_name=self.window.permalink_name)
        #~ d.update(url=self.ui.get_action_url(self.action)) # ,ext_requests.FMT_JSON))
        d.update(url=self.ui.get_actor_url(self.action.actor)) # ,ext_requests.FMT_JSON))
        return d
        
    def js_render(self):
        yield "function(caller) { return new Lino.%s(caller,%s);}" % (self.__class__.__name__,py2js(self.config))
        
    def unused_js_render(self):
        wc = self.window.ui.load_window_config(self.window.permalink_name)
        self.try_apply_window_config(wc)
        yield "function(caller,on_click) {"
        yield "  // begin js_render() %s" % self
        yield "  this.caller = caller;"
        yield "  this.on_click = on_click;"
        for ln in self.js_preamble():
            yield "  " + ln
        yield "  this.close = function() { this.window.close() }"
        yield "  this.hide = function() { this.window.hide() }"
        yield "  this.add_row_listener = function(fn) {"
        for ln in self.js_add_row_listener():
            yield "    " + ln
        yield "  }"
        yield "  this.show = function() {"
        for ln in self.js_show():
            yield "    " + ln
        yield "    this.window.show();"
        yield "    this.window.syncSize();"
        yield "    this.window.focus();"
        yield "  }"
        yield "  this.get_values = function() {"
        yield "    var v = {};"
        for ln in self.js_get_values():
            yield "    " + ln
        yield "    return v;"
        yield "  };"
        yield "  // declare variables of %s" % self
        for v in self.subvars():
            #~ yield "  // variable %s:" % v.ext_name
            for ln in v.js_declare():
                yield "  " + ln
        yield "  // js_main() %s :" % self
        for ln in self.js_main():
            yield "  " + ln
        yield "  // contributions of variables in %s" % self
        for v in self.subvars():
            yield "  // variable %s contributes:" % v.ext_name
            for ln in v.js_body():
                yield "  " + ln
        yield "  this.window._permalink_name = %s;" % py2js(self.window.permalink_name)
        for ln in self.js_on_window_render():
            yield "  " + ln
        yield "  this.get_window_config = function() {"
        yield "    var wc = { window_config_type: %r }" % self.window_config_type
        for ln in self.js_window_config():
            yield "    " + ln
        yield "    return wc;"
        yield "  }"
        
        yield "  // end js_render() %s" % self
        yield "}"
        
def lh2win(lh,kw):
    kw.update(height=300)
    kw.update(width=400)
    if lh is not None:
        kw.update(title=lh.get_title(None))
        if lh.height is not None:
            kw.update(height=lh.height*EXT_CHAR_HEIGHT + 7*EXT_CHAR_HEIGHT)
        if lh.width is not None:
            kw.update(width=lh.width*EXT_CHAR_WIDTH + 10*EXT_CHAR_WIDTH)
        if lh.start_focus is not None:
            kw.update(defaultButton=lh.start_focus.name)
  
class MasterWrapper(WindowWrapper):
  
    def __init__(self,lh,dl,**kw):
        self.ui = lh.ui
        #~ assert isinstance(lh.datalink,layouts.DataLink)
        self.lh = lh
        self.datalink = dl # lh.datalink
        #~ permalink_name = id2js(lh.layout.actor_id)
        permalink_name = lh.layout.actor_id
        name = id2js(lh.layout.actor_id)
        lh2win(lh,kw)
        window = WrappedWindow(self,dl.ui, "window", lh._main, permalink_name, **kw)
        #~ WindowWrapper.__init__(self,dl.name,window)
        WindowWrapper.__init__(self,name,window)
        
        
    def apply_window_config(self,wc):
        WindowWrapper.apply_window_config(self,wc)
        if isinstance(wc,WindowConfig):
            self.lh._main.apply_window_config(wc)
            
            
    def js_preamble(self):
        if self.datalink.content_type is not None:
            yield "this.content_type = %s;" % py2js(self.datalink.content_type)
            
class DetailMasterWrapper(MasterWrapper):
  
    window_config_type = 'form'
    
    def __init__(self,lh,dl,**kw):
        MasterWrapper.__init__(self,lh,dl,**kw)
        for a in dl.get_actions():
            self.bbar_buttons.append(ext_elems.FormActionElement(lh,a.name,a)) 
            #dict(text=a.label,handler=h))
            #~ if a.key:
                #~ keys.append(key_handler(a.key,h))
        lh._main.update(bbar=self.bbar_buttons)
        
    def js_main(self):
        for ln in MasterWrapper.js_main(self):
            yield ln
        yield "this.refresh = function() { console.log('DetailMasterWrapper.refresh() is not implemented') };"
        yield "this.get_current_record = function() { return this.current_record;};"
        yield "this.get_selected = function() {"
        yield "  return this.current_record.id;"
        yield "}"
        yield "this.load_record = function(record) {"
        yield "  this.current_record = record;" 
        yield "  if (record) this.main_panel.form.loadRecord(record)"
        yield "  else this.main_panel.form.reset();"
        yield "};"
        #~ yield "this.load_record(%s);" % py2js(ext_store.Record(self.datalink.store,object))
        yield "var fn = Ext.data.Record.create(%s)" % \
            py2js([js_code(f.as_js()) for f in self.datalink.store.fields])
        d = self.datalink.store.row2dict(self.datalink.row)
        yield "this.load_record(fn(%s));" % py2js(d)
        
        
    
class GridWrapperMixin(WindowWrapper):
    """
    Used by both GridMasterWrapper and GridSlaveWrapper
    """
  
    window_config_type = WC_TYPE_GRID
    
    def js_window_config(self):
        yield "wc['column_widths'] = Ext.pluck(this.main_grid.colModel.columns,'width');"

    def get_config(self):
        d = super(GridWrapperMixin,self).get_config()
        d.update(actions=[dict(type=a.action_type,name=a.name,label=a.label) for a in self.datalink.get_actions()])
        #~ d.update(actions=[dict(label=a.label,name=a.name) for a in self.bbar_buttons])
        d.update(fields=[js_code(f.as_js()) for f in self.datalink.store.fields])
        d.update(colModel=self.lh._main.column_model)
        d.update(content_type=self.datalink.content_type)
        d.update(title=self.datalink.get_title(None))
        #~ d.update(url='/'+self.datalink.report.app_label+'/'+self.datalink.report._actor_name )
        return d
        
class GridMasterWrapper(GridWrapperMixin,MasterWrapper):
  
    def __init__(self,ui,action,**kw):
        self.action = action
        ah = action.actor.get_handle(ui)
        MasterWrapper.__init__(self,ah.list_layout,ah,**kw)
        #~ self.config = self.get_config()
  
        #~ wc = self.window.ui.load_window_config(self.window.permalink_name)
        #~ self.try_apply_window_config(wc)
        #~ d = dict()
        #~ d.update(actions=self.actions)
        #~ d.update(fields=[js_code(f.as_js()) for f in self.datalink.store.fields])
        #~ d.update(colModel=self.lh._main.column_model)
        #~ d.update(content_type=self.datalink.content_type)
        #~ d.update(title=self.datalink.get_title(None))
        #~ d.update(url='/'+self.datalink.report.app_label+'/'+self.datalink.report._actor_name)
        #~ for k in 'width','height','x','y','maximized':
            #~ d[k] = self.window.value[k]
        #~ yield "function(caller) { return new Lino.GridMasterWrapper(caller,%s);}" % py2js(d)
      
  

class SlaveWrapper(WindowWrapper):
  
    pass

class GridSlaveWrapper(GridWrapperMixin,SlaveWrapper):
  
    def __init__(self,ui,name,action,**kw):
        self.ui = ui
        self.action = action
        self.name = name
        ah = action.actor.get_handle(ui)
        self.datalink = ah # slave_rh
        self.lh = ah.list_layout
        #~ button_text = slave_rh.report.button_label
        #~ permalink_name = id2js(slave_lh.name)
        permalink_name = self.lh.name
        name = None
        #~ name = id2js(self.lh.name)
        #~ kw.update(title=slave_lh.get_title(None))
        lh2win(self.lh,kw)
        window = WrappedWindow(self,ui,'window',self.lh._main,permalink_name,**kw)
        #~ SlaveWrapper.__init__(self, name, window, button_text)
        SlaveWrapper.__init__(self, name, window)
        #~ self.bbar_buttons = slave_rh.window_wrapper.bbar_buttons
        #~ self.slave_windows = slave_rh.window_wrapper.slave_windows
        #~ slave_lh._main.update(bbar=self.bbar_buttons)
        self.actions = [dict(type=a.action_type,name=a.name,label=a.label) for a in ah.get_actions()]
        
    def js_render(self):
        yield "function(caller) { return new Lino.GridSlaveWrapper(caller,%s);}" % py2js(self.config)
        
            
    def get_config(self):
        d = super(GridSlaveWrapper,self).get_config()
        d.update(name=self.name)
        return d
        
        
class DetailSlaveWrapper(SlaveWrapper):
  
    window_config_type = 'detail'
    
    def __init__(self,ui,action,**kw):
        self.ui = ui
        self.action = action
        #~ self.datalink = rh
        self.lh = action.layout.get_handle(ui)
        #~ button_text = slave_rh.report.button_label
        #~ permalink_name = id2js(slave_lh.name)
        permalink_name = self.lh.name
        name = id2js(self.lh.name)
        #~ kw.update(title=slave_lh.get_title(None))
        lh2win(self.lh,kw)
        window = WrappedWindow(self,ui,'window',self.lh._main,permalink_name,**kw)
        #~ SlaveWrapper.__init__(self, name, window, button_text)
        SlaveWrapper.__init__(self, name, window)
        #~ self.bbar_buttons = slave_rh.window_wrapper.bbar_buttons
        #~ self.slave_windows = slave_rh.window_wrapper.slave_windows
        #~ slave_lh._main.update(bbar=self.bbar_buttons)
        self.actions = [] # [dict(type=a.action_type,name=a.name,label=a.label) for a in rh.get_actions()]
        
    def js_render(self):
        yield "function(caller) { return new Lino.DetailSlaveWrapper(caller,%s);}" % py2js(self.config)
        
    def get_config(self):
        d = super(DetailSlaveWrapper,self).get_config()
        d.update(main_panel=self.lh._main)
        d.update(name=self.action.name)
        return d
        
        
        

        

class PropertiesWrapper(SlaveWrapper):
    window_config_type = 'props'
    #~ declare_type = jsgen.DECLARE_THIS
    #~ value_template = "new Ext.Window(%s)"
    
    def __init__(self,ui,action,**kw):
      
        assert isinstance(action,properties.PropertiesAction)
        self.action = action
        self.ui = ui
        self.model = action.actor.model # rr.master
        #~ self.rh = action.rh
        
        kw.update(closeAction='hide')
        self.source = {}
        self.customEditors = {}
        self.propertyNames = {}
        
        #~ for pv in self.rh.request(master=model,master_instance=None):
        #~ for pv in action.prop_values(ui):
        for pv in action.get_queryset(None):
            p = pv.prop
            self.source[p.name] = pv.value
            if p.label:
                self.propertyNames[p.name] = p.label
            #~ pvm = p.value_type.model_class()
            pvm = pv.__class__ 
            if pvm is properties.CHAR:
                #~ choices = [unicode(pv.value) for pv in pvm.objects.filter(prop=p,owner_id__isnull=True)]
                #~ choices = [unicode(choice) for choice in pv.value_choices(p)]
                choices = pvm.choices_list(p) # [unicode(choice) for choice in pv.value_choices(p)]
                if choices:
                    editor = ext_elems.ComboBox(store=choices,mode='local',selectOnFocus=True)
                    editor = 'new Ext.grid.GridEditor(%s)' % py2js(editor)
                    self.customEditors[p.name] = js_code(editor)
                    
        #~ print 20100226, self.model,len(self.source), self.source
        grid = dict(xtype='propertygrid')
        #~ grid.update(clicksToEdit=2)
        grid.update(source=self.source)
        grid.update(autoHeight=True)
        grid.update(customEditors=self.customEditors)
        #~ url = self.rh.get_absolute_url(grid_afteredit=True)
        #~ url = self.ui.get_props_url(self.model)
        listeners = dict(
          #~ afteredit=js_code('Lino.grid_afteredit(this,"%s")' % url))
          #~ afteredit=js_code('Lino.props_afteredit(this)'))
          afteredit=js_code('function(e){Lino.submit_property(this,e)}'),scope=js_code('this'))
        grid.update(listeners=listeners)
        #~ grid.update(pageSize=10)
        if len(self.propertyNames) > 0:
            grid.update(propertyNames=self.propertyNames)
        self.grid = grid
        panel = dict(xtype='panel',autoScroll=True,items=grid)
        main = jsgen.Value(panel)
        permalink_name = self.model._meta.app_label+'_'+self.model.__name__+'_properties'
        
        lh2win(None,kw)
        #~ window = Window(ui,rr.rh.name+'_properties',main,None,**kw)
        window = WrappedWindow(self,self.ui, 'window', main, permalink_name, **kw)
        
        #~ button_text = rr.rh.report.label
        
        SlaveWrapper.__init__(self,action.name,window)
                    
                    
    def has_properties(self):
        return len(self.source) > 0
        
        
    def js_render(self):
        yield "function(caller) { return new Lino.PropertiesWrapper(caller,%s);}" % py2js(self.config)
        
    def get_config(self):
        d = SlaveWrapper.get_config(self)
        d.update(main_panel=self.window.main)
        #~ d.update(url=self.ui.get_action_url(self.action,ext_requests.FMT_JSON))
        d.update(name=self.action.name)
        return d

    def apply_window_config(self,wc):
        WindowWrapper.apply_window_config(self,wc)
        if isinstance(wc,WindowConfig):
            self.grid['columns'] = [ dict(width=w) for w in wc.column_widths]
                
            
def key_handler(key,h):
    return dict(handler=h,key=key.keycode,ctrl=key.ctrl,alt=key.alt,shift=key.shift)


