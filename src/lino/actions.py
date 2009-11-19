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

import traceback
from django.utils.translation import ugettext as _

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
      
RETURN = Hotkey(keycode=13)
ESCAPE = Hotkey(keycode=27)
PAGE_UP  = Hotkey(keycode=33)
PAGE_DOWN = Hotkey(keycode=34)
DELETE = Hotkey(keycode=46)
    
class ActionEvent(Exception):
    pass
    
#~ class MustConfirm(ActionEvent):
    #~ pass
    
class Action:
    label = None
    name = None
    key = None
    needs_selection = True
    
    def __init__(self):
        if self.label is None:
            self.label = self.__class__.__name__
        if self.name is None:
            self.name = self.label
        #self.report = report
        
        
    def unused_get_response(self,rptreq):
        context = rptreq.report.ui.ActionContext(self,rptreq)
        if self.needs_selection and len(context.selected_rows) == 0:
            context._response.update(
              msg="No selection. Nothing to do.",
              success=False)
        else:
            try:
                self.run(context)
            except ActionEvent,e:
                pass
            except Exception,e:
                traceback.print_exc(e)
                context._response.update(msg=str(e),success=False)
        return context._response

        
    def run(self,context):
        raise NotImplementedError

class ActionContext:
    def __init__(self,ui,action):
        self.ui = ui
        self.action = action
        
    def run(self):
        if self.action.needs_selection and len(self.selected_rows) == 0:
            self.response.update(
              msg="No selection. Nothing to do.",
              success=False)
        else:
            try:
                self.action.run(self)
            except ActionEvent,e:
                pass
            except Exception,e:
                traceback.print_exc(e)
                self.response.update(msg=str(e),success=False)
        return self.response

    def refresh(self):
        self.response.update(must_reload=True)
        
    def redirect(self,url):
        self.response.update(redirect=url)
        
    def setmsg(self,msg=None):
        if msg is not None:
            self.response.update(msg=msg)
        
    def error(self,msg=None):
        self.response.update(success=False)
        self.setmsg(msg)
        raise ActionEvent() # MustConfirm(msg)
        
    def cancel(self,msg=_("User abort")):
        self.response.update(success=False)
        self.setmsg(msg)
        self.response.update(close_dialog=True)
        
    def confirm(self,msg):
        #print "ActionContext.confirm()", msg
        self.confirms += 1
        if self.confirmed >= self.confirms:
            return
        self.response.update(confirm=msg,success=False)
        raise ActionEvent() # MustConfirm(msg)
        
    def show_window(self,**kw):
        self.response.update(window=kw)


class DeleteSelected(Action):
    label = "Delete"
    key = DELETE # (ctrl=True)
    
    def run(self,context):
        if len(context.selected_rows) == 1:
            context.confirm("Delete row %s. Are you sure?" % context.selected_rows[0])
        else:
            context.confirm("Delete %d rows. Are you sure?" % len(context.selected_rows))
        for row in context.selected_rows:
            #print "DELETE:", row
            row.delete()
        context.refresh()

    
class CancelDialog(Action):
    needs_selection = False
    label = "Cancel"
    key = ESCAPE 
    
    def run(self,context):
        context.cancel()

class OK(Action):
    needs_selection = False
    label = "OK"
    key = RETURN
