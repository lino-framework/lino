# -*- coding: UTF-8 -*-
## Copyright 2012-2013 Luc Saffre
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
"""
Defines classes 
:class:`State`
:class:`Workflow`
:class:`ChangeStateAction`
"""

import sys

from django.utils.functional import Promise
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import string_concat
from django.utils.functional import lazy
from django.db import models

from lino.core import actions
from lino.core import actors
from lino.core import signals
#~ from lino.core import changes

from lino.utils import curry, unicode_string
from lino.core import choicelists



class State(choicelists.Choice):
    """
    A State is a specialized `Choice` that adds the `add_transition` method.
    `Choice.add_transition` declares or creates a `ChangeStateAction`
    which makes the object **enter this state**.
    """
    def add_transition(self,label=None,
        help_text=None,
        notify=False,
        #~ icon_file=None,
        icon_name=None,
        debug_permissions=None,
        **required):
        """
        `label` can be either a string or a subclass of ChangeStateAction
        """
        i = len(self.choicelist.workflow_actions)
        #~ i = len(self.choicelist._actions_list) # 20130531 
        #~ if label and issubclass(label,actions.Action):
        kw = dict()
        if help_text is not None:
            kw.update(help_text=help_text)
        #~ if icon_file is not None:
            #~ kw.update(icon_file=icon_file)
        if icon_name is not None:
            kw.update(icon_name=icon_name)
        kw.update(sort_index=10+i)
        if label and not isinstance(label,(basestring,Promise)):
            if required:
                raise Exception("Cannot specify requirements when using your own class")
            if notify:
                raise Exception("Cannot specify notify=True when using your own class")
            if debug_permissions:
                raise Exception("Cannot specify debug_permissions when using your own class")
            for a in self.choicelist.workflow_actions:
                if isinstance(a,label):
                    raise Exception("20130715 duplicate transition %s" % a)
            a = label(self,required,**kw)
        else:
            if notify:
                cl = NotifyingChangeStateAction
            else:
                cl = ChangeStateAction
            a = cl(self,required,label=label or self.text,**kw)
            if debug_permissions:
                a.debug_permissions = debug_permissions
        #~ name = 'mark_' + self.value
        name = 'wf' + str(i+1)
        a.attach_to_workflow(self.choicelist,name)
        #~ ba = self.choicelist.bind_action(a) # 20130531 why was this?
        #~ print 20130424, ba.actor, self, name, ba.action
        #~ """
        #~ TODO: `workflow_actions` is perhaps not nevessary: use Actor._actions_list instead
        #~ done 20130531
        #~ """
        self.choicelist.workflow_actions = self.choicelist.workflow_actions + [ a ]
        #~ self.choicelist.workflow_actions.append(a) 
        #~ yield name,a
        
        #~ if action_label is not None:
            #~ self.action_label = action_label
        #~ if help_text is not None:
            #~ self.help_text = help_text
        #~ self.required = required
        
    add_workflow = add_transition # backwards compat
        
        
    #~ def set_required(self,**kw):
        #~ from lino.core import perms
        #~ perms.set_required(self,**kw)
        


class Workflow(choicelists.ChoiceList):
    """
    A Workflow is a specialized ChoiceList used for 
    :attr:`lino.core.actors.Actor.workflow_state_field`.
    """
    workflow_actions = []
    
    item_class = State
    
    verbose_name = _("State")
    verbose_name_plural = _("States")
  
    #~ @classmethod
    #~ def add_statechange(self,newstate,action_label=None,states=None,**kw):
        #~ old = self.get_by_name()
        
    
    @classmethod
    def before_state_change(cls,obj,ar,kw,oldstate,newstate):
        pass

    @classmethod
    def after_state_change(cls,obj,ar,kw,oldstate,newstate):
        pass

    #~ @classmethod
    #~ def field(cls,*args,**kw):
        #~ if len(cls._fields) > 0:
            #~ raise Exception("Cannot use a Workflow for more than one field.")
        #~ return super(Workflow,cls).field(*args,**kw)
        
        
 #~ def set_required(self,**kw):
        #~ from lino.core import perms
        #~ perms.set_required(self,**kw)



class ChangeStateAction(actions.Action):
    """
    This is the class used when generating automatic 
    "state actions". For each possible value of the Actor's 
    :attr:`workflow_state_field` there will be an automatic action called 
    `mark_XXX`
    """
    
    #~ debug_permissions = True
    
    show_in_workflow = True
    
    
    def __init__(self,target_state,required,help_text=None,**kw):
        self.target_state = target_state
        #~ kw.update(label=getattr(target_state,'action_label',target_state.text))
        #~ kw.setdefault('label',target_state.text)
        #~ required = getattr(target_state,'required',None)
        #~ if required is not None:
        assert not kw.has_key('required')
        new_required = dict(self.required)
        new_required.update(required)
        if target_state.name:
            
            m = getattr(target_state.choicelist,'allow_transition',None)
            if m is not None:
                assert not required.has_key('allowed')
                def allow(action,user,obj,state):
                    return m(obj,user,target_state)
                new_required.update(allow=allow)
                
            m = getattr(target_state.choicelist,'allow_state_'+target_state.name,None)
            if m is not None:
                raise Exception("""
                
The allow_state_xxx magic is no longer allowed.
Because this is too magic. One day I needed about 4 hours
to find the explanation why some transition did not become 
visible, and it was because of a forgotten `allow_state_candidature`
method::
                
    @classmethod
    def allow_state_candidate(cls,self,user):
        if self.course:
            return True
        return False
        
    @classmethod
    def allow_state_change(cls,self,user,newstate):
        
                
                """)
                assert not required.has_key('allowed')
                def allow(action,user,obj,state):
                    return m(obj,user)
                new_required.update(allow=allow)
        kw.update(required=new_required)
        if self.help_text is None:
            if help_text is None:
                help_text = _("Mark this as %s") % target_state.text
        #~ help_text = getattr(target_state,'help_text',None)
        #~ if help_text is not None:
            kw.update(help_text=help_text)
        else:
            assert help_text is None
            
        super(ChangeStateAction,self).__init__(**kw)
        #~ logger.info('20120930 ChangeStateAction %s %s', actor,target_state)
        if self.icon_name:
            self.help_text = string_concat(self.label, '. ', self.help_text)
        
    #~ def full_name(self,actor):
        #~ if self.action_name is None or self.defining_actor is None:
            #~ return repr(self)
        #~ return self.defining_actor.actor_id + '.' + self.action_name
        
    def before_row_save(self,row,ar):
        pass
        
    def run_from_ui(self,ar,**kw):
        row = ar.selected_rows[0]
        #~ state_field_name = self.defining_actor.workflow_state_field.attname
        #~ state_field_name = row.workflow_state_field.attname
        state_field_name = ar.actor.workflow_state_field.attname
        #~ assert isinstance(state_field_name,basestring)
        #~ old = row.state
        old = getattr(row,state_field_name)
        
        watcher = signals.ChangeWatcher(row)
        
        self.target_state.choicelist.before_state_change(row,ar,kw,old,self.target_state)
        row.before_state_change(ar,kw,old,self.target_state)
        #~ row.state = self.target_state
        setattr(row,state_field_name,self.target_state)
        self.before_row_save(row,ar)
        row.save()
        self.target_state.choicelist.after_state_change(row,ar,kw,old,self.target_state)
        row.after_state_change(ar,kw,old,self.target_state)
        
        watcher.send_update(ar.request)
        
        return ar.success(**kw)
        
        
class NotifyingChangeStateAction(ChangeStateAction,actions.NotifyingAction):
    pass
