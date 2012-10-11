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

NOT_GIVEN = object()


class PseudoRequest:
    def __init__(self,user):
        self.user = user

class Watcher(object):
    def __init__(self,watched,is_new):
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
      
        cs = self.watched._watch_changes_specs
        
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
            master = getattr(self.watched,cs.master_key)
            if master is None:
                return
                
        kw = dict()
        if self.is_new:
            kw.update(type=ChangeTypes.create)
        else:
            kw.update(type=ChangeTypes.update)

        Change(
            time=datetime.datetime.now(),
            user=request.user,
            summary=self.watched._change_summary,
            master=master,
            object=self.watched,
            diff=msg,**kw).save()

def log_delete(request,obj):
    from lino.models import Change, ChangeTypes
    cs = obj._watch_changes_specs
    if cs is None:
        return
    
    if cs.master_key is None:
        master = obj
    else:
        master = getattr(obj,cs.master_key)
        if master is None:
            return
    Change(
        type=ChangeTypes.delete,
        time=datetime.datetime.now(),
        user=request.user,
        summary=obj._change_summary,
        master=master,
        object=obj).save()

