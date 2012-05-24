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

import logging
logger = logging.getLogger(__name__)

from lino.ui import base
from lino.core import actors
from lino.core import actions
from lino.mixins.printable import DirectPrintAction

class FrameHandle(base.Handle): 
    def __init__(self,ui,frame):
        #~ assert issubclass(frame,Frame)
        self.actor = frame
        base.Handle.__init__(self,ui)

    def get_actions(self,*args,**kw):
        return self.actor.get_actions(*args,**kw)
        
    def __str__(self):
        return "%s on %s" %(self.__class__.__name__,self.actor)



class Frame(actors.Actor): 
    """
    """
    _handle_class = FrameHandle
    #~ default_action_class = None
    editable = False
    
    @classmethod
    def do_setup(self):
        #~ logger.info("%s.__init__()",self.__class__)
        #~ if not self.__class__ is Frame:
        #~ if self.default_action_class:
            #~ self.default_action = self.default_action_class(self)
        if not self.label:
            self.label = self.default_action.label
            #~ self.default_action.actor = self
        super(Frame,self).do_setup()
        #~ self.set_actions([])
        #~ self.setup_actions()
        #~ if self.default_action:
            #~ self.add_action(self.default_action)


class EmptyTable(Frame):
    """
    A "Table" that has exactly one virtual row and thus is visible 
    only using a Detail view on that row.
    """
    #~ has_navigator = False
    #~ hide_top_toolbar = True
    hide_navigator = True
    default_list_action_name = 'show'
    default_elem_action_name =  'show'
    default_action = actions.ShowEmptyTable()
    do_print = DirectPrintAction()
    
    #~ @classmethod
    #~ def do_setup(self):
        #~ # logger.info("%s.__init__()",self.__class__)
        #~ # if not self.__class__ is Frame:
        #~ if self is not EmptyTable:
            #~ # assert self.default_action_class is None
            #~ # if self.label is None:
                #~ # raise Exception("%r has no label" % self)
            #~ # self.default_action = actions.ShowEmptyTable()
            #~ # self.default_action = self.add_action(actions.ShowEmptyTable())
            #~ super(Frame,self).do_setup()
            #~ # self.setup_actions()
            #~ # self.add_action(self.default_action)

    #~ @classmethod
    #~ def setup_actions(self):
        #~ super(EmptyTable,self).setup_actions()
        #~ from lino.mixins.printable import DirectPrintAction
        #~ self.add_action(DirectPrintAction())
        
            
    @classmethod
    def create_instance(self,req,**kw):
        #~ if self.known_values:
            #~ kw.update(self.known_values)
        if self.parameters:
            kw.update(req.param_values)

        #~ for k,v in req.param_values.items():
            #~ kw[k] = v
        #~ for k,f in self.parameters.items():
            #~ kw[k] = f.value_from_object(None)
        obj = actions.EmptyTableRow(self,**kw)
        kw = req.ah.store.row2dict(req,obj)
        obj._data = kw
        obj.update(**kw)
        return obj
    
    #~ @classmethod
    #~ def elem_filename_root(self,elem):
        #~ return self.app_label + '.' + self.__name__

    @classmethod
    def get_data_elem(self,name):
        de = super(EmptyTable,self).get_data_elem(name)
        if de is not None:
            return de
        a = name.split('.')
        if len(a) == 2:
            return getattr(getattr(settings.LINO.modules,a[0]),a[1])
