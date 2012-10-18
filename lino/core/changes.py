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


from lino.core.modeltools import obj2str
from lino.core import fields #~ fields_list

#~ WATCH_SPECS = dict()

NOT_GIVEN = object()

class WatcherSpec:
    def __init__(self,ignored_fields,master_key):
        self.ignored_fields = ignored_fields
        self.master_key = master_key
    



class PseudoRequest:
    def __init__(self,user):
        self.user = user

class Watcher(object):
    def __init__(self,watched,is_new=False):
        self.original_state = dict(watched.__dict__)
        self.watched = watched
        self.is_new = is_new
        
    def is_dirty(self):
        if self.is_new: 
            return True
        for k,v in self.original_state.iteritems():
            if v != self.watched.__dict__.get(k, NOT_GIVEN):
                return True
        return False
        
    def log_changes(self,request):
      
        #~ cs = WATCH_SPECS.get(self.watched.__class__)
        cs = self.watched._change_watcher_spec
        
        #~ print 20120921, cs
        if cs is None:
            return
            
        #~ ignored_fields = self.watched._watch_changes_specs
        #~ ignored_fields            
        
        #~ watched_fields, options = cs
        
        if self.is_new:
            msg = u"%s created." % obj2str(self.watched,True)
            #~ msg = u"%s created by %s." % (obj2str(self.watched),request.user)
        else:
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
                
        from lino.models import Change, ChangeTypes
        
        if cs.master_key is None:
            master = self.watched
        else:
            #~ master = cs.master_key.value_from_object(self.watched)
            #~ master = getattr(self.watched,cs.master_key)
            master = getattr(self.watched,cs.master_key.name)
           
        #~ logger.info("20121018 %r",cs.master_key)
        #~ logger.info("20121018 watched is %r, master is %r ",self.watched,master)
        
        if master is None:
            return
            
        kw = dict()
        if self.is_new:
            kw.update(type=ChangeTypes.create)
        else:
            kw.update(type=ChangeTypes.update)

        #~ if not isinstance(master,models.Model):
            #~ raise Exception("20121018 %r is not a Model instance" % master)
        #~ if not isinstance(self.watched,models.Model):
            #~ raise Exception("20121018 %r is not a Model instance" % self.watched)
        Change(
            time=datetime.datetime.now(),
            user=request.user,
            #~ summary=self.watched._change_summary,
            master=master,
            object=self.watched,
            diff=msg,**kw).save()

def log_delete(request,obj):
    from lino.models import Change, ChangeTypes
    #~ cs = WATCH_SPECS.get(obj.__class__)
    cs = obj._change_watcher_spec
    if cs is None:
        return
    
    if cs.master_key is None:
        master = obj
    else:
        #~ master = cs.master_key.value_from_object(obj)
        #~ master = getattr(obj,cs.master_key)
        master = getattr(obj,cs.master_key.name)
        if master is None:
            return
    #~ if not isinstance(master,models.Model):
        #~ raise Exception("20121018 %r is not a Model instance" % master)
    #~ if not isinstance(obj,models.Model):
        #~ raise Exception("20121018 %r is not a Model instance" % obj)
    Change(
        type=ChangeTypes.delete,
        time=datetime.datetime.now(),
        user=request.user,
        #~ summary=obj._change_summary,
        master=master,
        object=obj).save()

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
    ignore = set(ignore)
    #~ cs = WATCH_SPECS.get(model)
    cs = model._change_watcher_spec
    if cs is not None:
        ignore |= cs.ignored_fields
    for f in model._meta.fields:
        if not f.editable:
            ignore.add(f.name)
    model._change_watcher_spec = WatcherSpec(ignore,master_key)
    #~ WATCH_SPECS[model] = WatcherSpec(ignore,master_key)
    
    #~ logger.info("20120924 %s ignore %s", model, ignore)
    #~ model._watch_changes_specs = (fields_spec,options)
    #~ else:
        #~ raise NotImplementedError()

