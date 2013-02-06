## Copyright 2009-2012 Luc Saffre
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
Defines the :class:`Dialog` class.
"""
raise Exception("No longer used")

import logging
logger = logging.getLogger(__name__)

from django.utils.translation import ugettext as _

from lino.ui import base
from lino.core import actors
from lino.core import actions

class DialogHandle(base.Handle): 
    """
    
    """
    def __init__(self,ui,frame):
        #~ assert issubclass(frame,Frame)
        self.actor = frame
        base.Handle.__init__(self,ui)

    def get_actions(self,*args,**kw):
        return self.actor.get_actions(*args,**kw)
        
    def __str__(self):
        return "%s on %s" %(self.__class__.__name__,self.actor)


class OK(actions.Action):
    label = _("OK")

class Cancel(actions.Action):
    label = _("Cancel")

class Dialog(actors.Actor): 
    """
    Deserves more documentation.
    """
    _handle_class = DialogHandle
    
    @classmethod
    def get_default_action(self):
        return None # actions.BoundAction(self,actions.GridEdit())
        
    
    
    ok = OK()
    cancel = Cancel()