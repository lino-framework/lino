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
    
    
    
class Action: # (actors.Actor):
    label = None
    name = None
    key = None
    needs_selection = False
    needs_validation = False
    
    def __init__(self):
        #actors.Actor.__init__(self)
        if self.name is None:
            self.name = self.__class__.__name__ # label
        if self.label is None:
            self.label = self.name #self.__class__.__name__
        #self.report = report
        
        
    def run(self,context):
        raise NotImplementedError
        
class ActionContext:
    def __init__(self,ui,actor,action_name,*args,**kw):
        self.response = dict(success=True,must_reload=False,msg=None,stop_caller=False)
        self.ui = ui
        self.actor = actor
        self.action = actor.get_action(action_name)
        self._kw = kw
        self._args = args
        if not isinstance(self.action,Action):
            raise Exception("%s.get_action(%r) returned %r which is not an Action." % (actor,action_name,self.action))
        
    def run(self):
        if self.action.needs_selection and len(self.selected_rows) == 0:
            self.response.update(
              msg=_("No selection. Nothing to do."),
              success=False)
        else:
            lino.log.debug('ActionContext.run() : %s.%s(%r,%r)',self.actor,self.action.name,self._args,self._kw)
            try:
                self.action.run(self,*self._args,**self._kw)
            except ActionEvent,e:
                pass
            except Exception,e:
                traceback.print_exc(e)
                lino.log.exception(e)
                self.response.update(msg=force_unicode(e),success=False)
        return self.response
        
    def get_user(self):
        raise NotImplementedError()

    def refresh(self):
        self.response.update(must_reload=True)
        
    def refresh_menu(self):
        self.response.update(refresh_menu=True)
        
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
        self.response.update(stop_caller=True)
        
    def done(self,msg=_("OK")):
        self.setmsg(msg)
        self.response.update(stop_caller=True)
        
    def confirm(self,msg):
        #print "ActionContext.confirm()", msg
        self.confirms += 1
        if self.confirmed >= self.confirms:
            return
        self.response.update(confirm=msg,success=False)
        raise ActionEvent() # MustConfirm(msg)
        
    def show_window(self,**kw):
        self.response.update(window=kw)

    def js_eval(self,js):
        self.response.update(js_eval=js)

class InsertRow(Action):
    label = _("Insert")
    key = INSERT # (ctrl=True)
    
    def run(self,context):
        #if len(context.selected_rows) != 1:
        #    return context.error(_("More than one row selected."))
        context.confirm(_("Insert new row. Are you sure?"))
        rr = context.get_report_request()
        row = rr.create_instance()
        row.save()
        context.refresh()
        
  
class DeleteSelected(Action):
    needs_selection = True
    label = _("Delete")
    key = DELETE # (ctrl=True)
    
    def run(self,context):
        if len(context.selected_rows) == 1:
            context.confirm(_("Delete row %s. Are you sure?") % context.selected_rows[0])
        else:
            context.confirm(_("Delete %d rows. Are you sure?") % len(context.selected_rows))
        for row in context.selected_rows:
            #print "DELETE:", row
            row.delete()
        context.refresh()

    
class CancelDialog(Action):
    label = "Cancel"
    key = ESCAPE 
    
    def run(self,context):
        context.cancel()

class OK(Action):
    needs_validation = True
    label = "OK"
    key = RETURN

    def run(self,context):
        context.done()


class RunCommand(Action):
  
    def run(self,context,*args,**kw):
        context.actor.run(context,*args,**kw)

class Command(actors.Actor):
    default_action = RunCommand()
    
    def run(self,context):
        # override this in subclasses
        context.done()
      