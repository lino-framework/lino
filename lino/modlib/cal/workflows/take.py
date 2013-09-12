# -*- coding: UTF-8 -*-
## Copyright 2011-2013 Luc Saffre
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

Importing this from within one of your :xfile:`models.py` modules 
will add the "Take" action.

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.utils.translation import ugettext_lazy as _



from lino import dd


from lino.modlib.cal.workflows import (TaskStates,
    EventStates,GuestStates)


class TakeAssignedEvent(dd.Action):
    label = _("Take")
    show_in_workflow = True
    
    #~ icon_file = 'cancel.png'
    icon_name = 'flag_green'
    #~ required = dict(states='new assigned',owner=False)
    required = dd.required(owner=False)
    help_text=_("Take responsibility for this event.")
  
    def get_action_permission(self,ar,obj,state):
        if obj.assigned_to != ar.get_user():
            return False
        return super(TakeAssignedEvent,self).get_action_permission(ar,obj,state)
        
    def run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
        ar.confirm(self.help_text,_("Are you sure?"))
        obj.user = ar.get_user()
        obj.assigned_to = None
        #~ kw = super(TakeAssignedEvent,self).run(obj,ar,**kw)
        obj.save()
        kw.update(refresh=True)
        return kw
    
  
if False:
      
  class AssignEvent(dd.ChangeStateAction):
    label = _("Assign")
    required = dict(states='suggested draft published',owner=True)
    
    icon_name = 'flag_blue'
    help_text=_("Assign responsibility of this event to another user.")
    
    parameters = dict(
        to_user=dd.ForeignKey(settings.SITE.user_model),
        remark = dd.RichTextField(_("Remark"),blank=True),
        )
    
    params_layout = dd.Panel("""
    to_user
    remark
    """,window_size=(50,15))
    
    @dd.chooser()
    #~ def to_user_choices(cls,user):
    def to_user_choices(cls):
        return settings.SITE.user_model.objects.exclude(profile='') # .exclude(id=user.id)
      
    def action_param_defaults(self,ar,obj,**kw):
        kw = super(AssignEvent,self).action_param_defaults(ar,obj,**kw)
        kw.update(
            remark=unicode(_("I made up this event for you. %s")) 
                % ar.user)
        return kw
    
    
    def run_from_ui(self,ar,**kw):
        obj = ar.selected_rows[0]
        obj.user = ar.action_param_values.to_user
        kw = super(AssignEvent,self).run_from_ui(ar,**kw)
        #~ obj.save()
        kw.update(refresh=True)
        return kw
    


    
@dd.receiver(dd.pre_analyze)
def take_workflows(sender=None,**kw):
    
    site = sender
    
    site.modules.cal.Event.take = TakeAssignedEvent()

