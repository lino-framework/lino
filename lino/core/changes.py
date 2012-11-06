## Copyright 2012 Luc Saffre
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
:mod:`lino.core.changes` -- Watching database changes
------------------------------------------------------

This module contains utilities for logging changes in a Django database.

See also :doc:`/topics/changes`


"""

import logging
logger = logging.getLogger(__name__)
info = logger.info
warning = logger.warning
exception = logger.exception
error = logger.error
debug = logger.debug
#~ getLevel = logger.getLevel
#~ setLevel = logger.setLevel

import datetime

from django.conf import settings

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _


from lino.core.modeltools import obj2str, full_model_name
from lino.core import fields 
from lino.core import actions
from lino.utils import choicelists

#~ WATCH_SPECS = dict()

NOT_GIVEN = object()

class PseudoRequest:
    def __init__(self,username):
        self.username = username
        self._user = None
        
    def get_user(self):
        if self._user is None:
            if settings.LINO.user_model is not None:
                self._user = settings.LINO.user_model.objects.get(username=self.username)
        return self._user
    user = property(get_user)
        
class ChangeTypes(choicelists.ChoiceList):
    app_label = 'lino'
    label = _("Change Type")
add = ChangeTypes.add_item    
add('C',_("Create"),'create')
add('U',_("Update"),'update')
add('D',_("Delete"),'delete')
add('R',_("Remove child"),'remove_child')
add('A',_("Add child"),'add_child')

        

class WatcherSpec:
    #~ def __init__(self,ignored_fields,master_key):
    def __init__(self,ignored_fields,get_master):
        self.ignored_fields = ignored_fields
        #~ self.master_key = master_key
        self.get_master = get_master
    
def add_watcher_spec(model,ignore=[],master_key=None,**options):
    #~ if ignore is None:
        #~ model._change_watcher_spec = None
        #~ return
    #~ from lino import dd
    if isinstance(ignore,basestring):
        ignore = fields.fields_list(model,ignore)
    if isinstance(master_key,basestring):
        fld = fields.get_data_elem(model,master_key)
        if fld is None:
            raise Exception("No field %r in %s" % (master_key,model))
        master_key = fld
    if isinstance(master_key,fields.RemoteField):
        get_master = master_key.func
    elif master_key is None:
        def get_master(obj):
            return obj
    else:
        def get_master(obj):
            return getattr(obj,master_key.name)
    ignore = set(ignore)
    #~ cs = WATCH_SPECS.get(model)
    cs = model._change_watcher_spec
    if cs is not None:
        ignore |= cs.ignored_fields
    for f in model._meta.fields:
        if not f.editable:
            ignore.add(f.name)
    model._change_watcher_spec = WatcherSpec(ignore,get_master)
    #~ WATCH_SPECS[model] = WatcherSpec(ignore,master_key)
    
    #~ logger.info("20120924 %s ignore %s", model, ignore)
    #~ model._watch_changes_specs = (fields_spec,options)
    #~ else:
        #~ raise NotImplementedError()


def get_master(obj):
    
    #~ cs = WATCH_SPECS.get(self.watched.__class__)
    cs = obj._change_watcher_spec
    
    #~ print 20120921, cs
    if cs is None:
        return
    return cs.get_master(obj)
        
    #~ if cs.master_key is None:
        #~ return obj
    # master = cs.master_key.value_from_object(self.watched)
    # master = getattr(self.watched,cs.master_key)
    #~ return getattr(obj,cs.master_key.name)

def log_change(type,request,master,obj,msg=''):
    from lino.models import Change
    Change(
        type=type,
        time=datetime.datetime.now(),
        user=request.user,
        #~ summary=self.watched._change_summary,
        master=master,
        object=obj,
        diff=msg).save()


class Watcher(object):
    def __init__(self,watched):
        self.original_state = dict(watched.__dict__)
        self.watched = watched
        #~ self.is_new = is_new
        #~ self.request
        
    def is_dirty(self):
        #~ if self.is_new: 
            #~ return True
        for k,v in self.original_state.iteritems():
            if v != self.watched.__dict__.get(k, NOT_GIVEN):
                return True
        return False
        
    def log_diff(self,request):
        master = get_master(self.watched)
        if master is None:
            return
            
        #~ ignored_fields = self.watched._watch_changes_specs
        #~ ignored_fields            
        
        #~ watched_fields, options = cs
        
        #~ if self.is_new:
            #~ msg = u"%s created." % obj2str(self.watched,True)
            #~ msg = u"%s created by %s." % (obj2str(self.watched),request.user)
        #~ else:
        cs = self.watched._change_watcher_spec
        changes = []
        for k,old in self.original_state.iteritems():
            #~ if watched_fields is None or k in watched_fields:
            if not k in cs.ignored_fields:
                new = self.watched.__dict__.get(k, NOT_GIVEN)
                if old != new:
                    changes.append("%s : %s --> %s" % (k,obj2str(old),obj2str(new)))
        
        if len(changes) == 0:
            msg = '(no changes)'
        elif len(changes) == 1:
            msg = changes[0]
        else:
            msg = '- ' + ('\n- '.join(changes))
            
        log_change(ChangeTypes.update,request,master,self.watched,msg)
        
        
        

def log_delete(request,obj):
    """
    Calls :func:`log_change` with `ChangeTypes.delete`.
    
    Note that you must call this before actually deleting the object,
    otherwise mysql says ERROR: (1048, "Column 'object_id' cannot be null")
    """
    master = get_master(obj)
    if master is None:
        return
    log_change(ChangeTypes.delete,request,master,obj)
    
def log_create(request,obj):
    master = get_master(obj)
    if master is None:
        return
    log_change(ChangeTypes.create,request,master,obj,obj2str(obj,True))

def log_add_child(request,obj,child_model):
    master = get_master(obj)
    if master is None:
        return
    log_change(ChangeTypes.add_child,request,master,obj,full_model_name(child_model))

def log_remove_child(request,obj,child_model):
    master = get_master(obj)
    if master is None:
        return
    log_change(ChangeTypes.remove_child,request,master,obj,full_model_name(child_model))
