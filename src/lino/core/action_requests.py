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
from django.db import models

import lino
from lino import actions

class ActionResponse:
    redirect = None
    alert_msg = None
    confirm_msg = None
    notify_msg = None
    refresh_menu = False
    refresh_caller = False
    close_caller = False
    show_window = None
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
        )

class ActionRequest:
    """
    An ActionRequest will be created for every request.
    
    """
    selected_rows = []
    
    #~ def __init__(self,ah,action):
    def __init__(self,actor,action,ui=None):
        # TODO: ah parameter not needed here because it is now stored in action.ah
        #~ self.is_over = False
        #~ self.params = params
        self.actor = actor
        self.action = action # ah.actor.get_action(action_name)
        self.ui = ui
        self.ah = actor.get_handle(ui) # ah # actor handle
        if not isinstance(action,actions.Action):
            raise Exception("%s : %r is not an Action." % (self,action))
        self.response = None
        
    def __str__(self):
        return 'ActionRequest `%s.%s`' % (self.ah,self.action)
        
    def run(self):
        msg = self.action.before_run(self)
        if msg:
            return ActionResponse(notify_msg=msg,success=False)
        #~ lino.log.debug('ActionRequest._start() %s.%s',self.ah,self.action.name)
        #~ lino.log.debug('ActionRequest._start() %s.%s(%r)',self.ah,self.action.name,self.params)
        self.response = ActionResponse()
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
        self.response.close_caller = True
        return self
        
    def refresh_caller(self):
        self.response.refresh_caller = True
        return self
        
    def refresh_menu(self):
        self.response.refresh_menu = True
        return self
        
    def show_report(self,rh):
        return self.ui.show_report(self,rh)
        
    def show_action_window(self,action):
        return self.ui.show_action_window(self,action)
        
    def show_detail(self):
        return self.ui.show_detail(self)
        
    def show_properties(self,lh):
        return self.ui.show_properties(self)
        
    def unused_show_detail(self,row):
        assert self.ah.detail_link is not None
        self.ah.detail_link.row = row
        return self.ui.show_detail(self,row)
        
    def show_window(self,js):
        #~ assert js.strip().startswith('function')
        #~ self.response.show_window = py2js(js)
        self.response.show_window = js
        return self
        
    def unused_show_modal_window(self,js):
        self.response.show_modal_window = js
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
        self.response.success = False
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



