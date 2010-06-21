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

import traceback
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode

import lino

class Hotkey:
    keycode = None
    shift = False
    ctrl = False
    alt = False
    inheritable = ('keycode','shift','ctrl','alt')
    def __init__(self,**kw):
        for k,v in kw.items():
            setattr(self,k,v)
            
    def __call__(self,**kw):
        for n in self.inheritable:
            if not kw.has_key(n):
                kw[n] = getattr(self,n)
            return Hotkey(**kw)
      
# ExtJS src/core/EventManager-more.js
RETURN = Hotkey(keycode=13)
ESCAPE = Hotkey(keycode=27)
PAGE_UP  = Hotkey(keycode=33)
PAGE_DOWN = Hotkey(keycode=34)
INSERT = Hotkey(keycode=44)
DELETE = Hotkey(keycode=46)
    
class ActionEvent(Exception):
    pass
    
class ValidationError(Exception):
    pass
    
#~ class MustConfirm(ActionEvent):
    #~ pass

#~ class ActionHandle:
    #~ def __init__(self,ui,action):
        #~ assert isinstance(action,Action)
        #~ self.ui = ui
        #~ self.action = action
        
    #~ def setup(self):
        #~ if self.ui is not None:
            #~ self.ui.setup_action(self)
        
    
    
class Action: # (base.Handled):
    #~ handle_class = ActionHandle
    #~ action_type = '?'
    opens_a_slave = False
    response_format = 'act' # ext_requests.FMT_RUN
    label = None
    name = None
    key = None
    needs_selection = False
    needs_validation = False
    #~ grid_button = True
    #~ hidden = False
    show_in_detail = True
    show_in_list = True
    
    def __init__(self,actor):
    #~ def __init__(self,ah):
        #~ self.ah = ah # actor handle of the actor who offers this action
        self.actor = actor # actor who offers this action
        if self.name is None:
            self.name = self.__class__.__name__ # label
        if self.label is None:
            self.label = self.name #self.__class__.__name__
        
        
    def __str__(self):
        return str(self.actor)+'.'+self.name

        
    def run_action(self,act):
        raise NotImplementedError
        
    def before_run(self,act):
        pass
        
        
        

class RowsAction(Action):
    needs_selection = False
    needs_validation = False
    
    def before_run(self,ar):
        if self.needs_selection and len(ar.selected_rows) == 0:
            return _("No selection. Nothing to do.")
            
            

class WindowAction(Action):
    #~ response_format = 'act' # ext_requests.FMT_RUN

    def run_action(self,ar):
        ar.show_action_window(self) 
        
                
class OpenWindowAction(WindowAction):
    pass
    #~ action_type = 'open_window'
    
    
class ToggleWindowAction(WindowAction):
    opens_a_slave = True
    #~ action_type = 'toggle_window'    
                
    
    
#~ class Cancel(Action):
    #~ label = _("Cancel")
    #~ name = 'cancel'
    #~ key = ESCAPE 
    
    #~ def run_in_dlg(self,dlg):
        #~ yield dlg.close_caller().over()

#~ class OK(Action):
    #~ needs_validation = True
    #~ label = _("OK")
    #~ name = "ok"
    #~ key = RETURN

    #~ def run_in_dlg(self,dlg):
        #~ yield dlg.close_caller().over()



class unused_ActionResponse:
    redirect = None
    alert_msg = None
    confirm_msg = None
    notify_msg = None
    refresh_menu = False
    refresh_caller = False
    close_caller = False
    #~ show_window = None
    js_code = None
    success = True # for Ext.form.Action.Submit
    errors = None # for Ext.form.Action.Submit
    
    def __init__(self,**kw):
        for k,v in kw.items():
            assert hasattr(self,k)
            setattr(self,k,v)
              
    
    def as_dict(self):
        return dict(
          success=self.success,
          redirect=self.redirect,
          alert_msg=self.alert_msg,
          notify_msg=self.notify_msg,
          confirm_msg=self.confirm_msg,
          refresh_menu=self.refresh_menu,
          refresh_caller=self.refresh_caller,
          close_caller=self.close_caller,
          #~ show_window=self.show_window,
          js_code=self.js_code,
        )

class ActionRequest:
    """
    An ActionRequest will be created for every request.
    
    """
    selected_rows = []
    
    def __init__(self,ah,action):
    #~ def __init__(self,actor,action,ui=None):
        #~ self.params = params
        if not isinstance(action,Action):
            raise Exception("%s : %r is not an Action." % (self,action))
        self.ah = ah # actor handle
        self.action = action # ah.actor.get_action(action_name)
        #~ self.actor = ah.actor
        self.ui = ah.ui
        self.response = dict(
          #~ redirect = None,
          #~ alert_msg = None,
          #~ confirm_msg = None,
          #~ notify_msg = None,
          #~ refresh_menu = False,
          #~ refresh_caller = False,
          #~ close_caller = False,
          #~ show_window = None,
          #~ js_code = None,
          success = True, # for Ext.form.Action.Submit
          errors = None, # for Ext.form.Action.Submit
        )
        
    def __str__(self):
        return 'ActionRequest `%s.%s`' % (self.ah,self.action)
        
    def run(self):
        msg = self.action.before_run(self)
        if msg:
            return dict(notify_msg=msg,success=False)
            #~ return ActionResponse(notify_msg=msg,success=False)
        lino.log.debug('ActionRequest %s.%s',self.ah,self.action.name)
        #~ lino.log.debug('ActionRequest._start() %s.%s(%r)',self.ah,self.action.name,self.params)
        #~ self.response = ActionResponse()
        try:
            #~ self.ui.run_action(self)
            self.action.run_action(self)
        except Exception,e:
            self.exception(e)
        return self.response
        
    """
    API used during `Action.run_action()`.
    """
        
    def get_user(self):
        raise NotImplementedError()
        
        
    ## message methods to be used in yield statements
    
        
    def close_caller(self):
        self.response.update(close_caller = True)
        return self
        
    def refresh_caller(self):
        self.response.update(refresh_caller = True)
        return self
        
    def refresh_menu(self):
        self.response.update(refresh_menu = True)
        return self
        
    #~ def show_report(self,rh):
        #~ return self.ui.show_report(self,rh)
        
    def show_action_window(self,action):
        return self.ui.show_action_window(self,action)
        
    #~ def show_detail(self):
        #~ return self.ui.show_detail(self)
        
    #~ def show_properties(self,lh):
        #~ return self.ui.show_properties(self)
        
    def unused_show_detail(self,row):
        assert self.ah.detail_link is not None
        self.ah.detail_link.row = row
        return self.ui.show_detail(self,row)
        
    def unused_show_window(self,js):
        #~ assert js.strip().startswith('function')
        #~ self.response.show_window = py2js(js)
        self.response.show_window = js
        return self
        
    def unused_show_modal_window(self,js):
        self.response.show_modal_window = js
        return self
        
    def redirect(self,url):
        self.response.update(redirect = url)
        return self
        
    def confirm(self,msg,**kw):
        self.response.update(confirm_msg = msg)
        return self
        
    def alert(self,msg,**kw):
        self.response.update(alert_msg = msg)
        return self

    def exception(self,e):
        self.response.update(success = False)
        self.response.update(alert_msg = unicode(e))
        traceback.print_exc(e)
        return self

    def notify(self,msg):
        self.response.update(notify_msg = msg)
        return self

    #~ def cancel(self,msg=None):
        #~ if msg is not None:
              #~ self.notify(msg)
        #~ return self.close_caller().over()
        
    #~ def ok(self,msg=None):
        #~ if msg is not None:
              #~ self.notify(msg)
        #~ return self.close_caller().over()



lino.log.debug(__file__+' : done')
