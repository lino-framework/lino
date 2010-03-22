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
from lino.utils import actors

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
    
    
class Action:
    label = None
    name = None
    key = None
    needs_selection = False
    needs_validation = False
    
    def __init__(self):
        if self.name is None:
            self.name = self.__class__.__name__ # label
        if self.label is None:
            self.label = self.name #self.__class__.__name__
        
    def __str__(self):
        return self.name
        
    def run_in_dlg(self,dlg):
        raise NotImplementedError
        
    def before_run(self,dlg):
        pass

class RowsAction(Action):
    needs_selection = False
    needs_validation = False
    
    def before_run(self,dlg):
        if self.needs_selection and len(dlg.selected_rows) == 0:
            return _("No selection. Nothing to do.")

class DialogResponse:
    redirect = None
    alert_msg = None
    confirm_msg = None
    notify_msg = None
    refresh_menu = False
    refresh_caller = False
    close_caller = False
    show_window = None
    show_modal_window = None
    dialog_id = None
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
          show_window=self.show_window,
          show_modal_window=self.show_modal_window,
          dialog_id = self.dialog_id,
        )
      
running_dialogs = {}

def get_dialog(dialog_id):
    return running_dialogs.get(dialog_id,None)

class Dialog:
    """
    A Dialog is a conversation between client and server.
    Dialogs are initiated by a client request.
    Each `yield` of an `Action.run()` defines a response to the client, and execution continues only when the client has answered.
    See also `Lino.do_dialog()` in `lino.ui.extjs`.
    The current API is rather influenced by the possibilities of the ExtJS UI.
    """
    selected_rows = []
    params_def = ()
    modal_exit = None
    
    def __init__(self,ah,action,params):
        self.is_over = False
        self.ui = ah.ui
        #~ self.ah = actor.get_handle(ui)
        self.ah = ah
        self.params = params
        self.action = action # ah.actor.get_action(action_name)
        if not isinstance(action,Action):
            raise Exception("%s : %r is not an Action." % (self,action))
        self.running = None
        self.response = None
        
    def set_modal_exit(self,name):
        self.modal_exit = name
        #~ if name is None:
            #~ self.button_clicked = None
        #~ else:
            #~ self.button_clicked = self.ah.get_action(name)
        
    def __str__(self):
        return 'Dialog `%s.%s`' % (self.ah,self.action)
        
    def _open(self):
        if self.is_over:
            return
        self.response.dialog_id = hash(self)
        assert not running_dialogs.has_key(self.response.dialog_id)
        running_dialogs[self.response.dialog_id] = self
        
    def _close(self):
        self.is_over = True
        if self.response.dialog_id is None:
            return
        del running_dialogs[self.response.dialog_id]
        self.response.dialog_id = None
        
    def _start(self):
        msg = self.action.before_run(self)
        if msg:
            return DialogResponse(notify_msg=msg)
        lino.log.debug('Dialog._start() %s.%s(%r)',self.ah,self.action.name,self.params)
        self.running = self.action.run_in_dlg(self)
        r = self._step()
        self._open()
        return r
        
    #~ def before_step(self):
        #~ pass
        
    def _step(self):
        self.response = DialogResponse()
        #~ self.before_step()
        self.ah.before_step(self)
        try:
            dlg = self.running.next()
            assert dlg is self
        except StopIteration:
            self._close()
        return self.response
        
        
    def _abort(self):
        self._close()
        return DialogResponse(notify_msg=_("Client abort in %s") % self)
        
    """
    API used during `Action.run_in_dialog()`.
    """
        
    def get_user(self):
        raise NotImplementedError()
        
    def get_request(self,**kw):
        kw.update(user=self.get_user())
        return self.ah.request(**kw)
    
    def get_form(self,name):
        layout = actors.resolve_actor(name,self.ah.actor.app_label)
        lh = layout.get_handle(self.ui)
        fh = FormHandle(lh,self.ah)
        return fh # self.ah.get_form_handle(name)
        
    ## message methods to be used in yield statements
        
    def close_caller(self):
        self.response.close_caller = True
        return self
        
    def refresh_caller(self):
        self.response.refresh_caller = True
        return self
        
    def refresh_menu(self):
        self.response.refresh_menu = True
        return self
        
    def over(self):
        self.is_over = True
        return self
        
    def show_window(self,js):
        #~ assert js.strip().startswith('function')
        #~ self.response.show_window = py2js(js)
        self.response.show_window = js
        return self
        
    def show_modal_window(self,js):
        self.response.show_modal_window = js
        return self
        
    def show_modal_form(self,fh):
        self.ui.show_modal_form(self,fh)
        return self
        
    def redirect(self,url):
        self.response.redirect = url
        return self
        
    def confirm(self,msg,**kw):
        self.response.confirm_msg = msg
        return self
        
    def alert(self,msg,**kw):
        self.response.alert_msg = msg
        return self

    def exception(self,e):
        self.response.alert_msg = unicode(e)
        traceback.print_exc(e)
        return self

    def notify(self,msg):
        self.response.notify_msg = msg
        return self

    def cancel(self,msg=None):
        if msg is not None:
              self.notify(msg)
        return self.close_caller().over()
        
    def ok(self,msg=None):
        if msg is not None:
              self.notify(msg)
        return self.close_caller().over()



    
class Cancel(Action):
    label = _("Cancel")
    name = 'cancel'
    key = ESCAPE 
    
    def run_in_dlg(self,dlg):
        yield dlg.close_caller().over()

class OK(Action):
    needs_validation = True
    label = _("OK")
    name = "ok"
    key = RETURN

    def run_in_dlg(self,dlg):
        yield dlg.close_caller().over()


