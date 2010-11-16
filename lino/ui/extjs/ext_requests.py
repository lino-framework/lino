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

from django.db import models
from django.http import HttpResponse, Http404
from django.contrib.contenttypes.models import ContentType
#~ from django.contrib.contenttypes import generic
from django.utils import simplejson as json

import lino
from lino import actions
from lino import reports
#~ from lino import forms
#~ from lino.core import action_requests
from lino.utils import ucsv
#~ from lino.utils import choosers
#~ from lino.ui.extjs import ext_windows


#~ UNDEFINED = "nix"

CHOICES_TEXT_FIELD = 'text'
CHOICES_VALUE_FIELD = 'value'
CHOICES_HIDDEN_SUFFIX = "Hidden"


URL_PARAM_MASTER_TYPE = 'mt'
"""
The pk of the ContentType of the master model.
"""

URL_PARAM_MASTER_PK = 'mk'
"""
The pk of the master instance.
"""

# URL_PARAM_MASTER_GRID = 'mg'
URL_PARAM_FILTER = 'query'
URL_PARAM_CHOICES_PK = "ck"

POST_PARAM_SELECTED = 'selected'

#~ FMT_RUN = 'act'
#~ FMT_JSON = 'json'

def form_field_name(f):
    if isinstance(f,models.ForeignKey) or (isinstance(f,models.Field) and f.choices):
        return f.name + CHOICES_HIDDEN_SUFFIX
    else:
        return f.name
        
def dict2kw(d):
    newd = {}
    for k,v in d.items():
        newd[str(k)] = v
    return newd



def authenticated_user(user):
    if user.is_anonymous():
        return None
    return user
        
#~ class ActionRequest(actions.ActionRequest):
    
    #~ def __init__(self,request,ah,action):
        #~ self.request = request
        #~ actions.ActionRequest.__init__(self,ah,action,{})
        
    #~ def get_user(self):
        #~ return authenticated_user(self.request.user)
        
class ViewReportRequest(reports.ReportActionRequest):
    
    editing = 0
    selector = None
    sort_column = None
    sort_direction = None
    gc = None
    
    def __init__(self,request,rh,action,*args,**kw):
        reports.ReportActionRequest.__init__(self,rh.ui,rh.report,action)
        self.ah = rh
        self.request = request
        self.store = rh.store
        kw = self.parse_req(request,rh,**kw)
        self.setup(*args,**kw)
        
    def parse_req(self,request,rh,**kw):
        #~ gc_name = request.REQUEST.get('gc',None)
        #~ if gc_name:
            #~ self.gc = system.GridConfig.objects.get(rptname=self.report.actor_id,name=gc_name)
            
        master = kw.get('master',self.report.master)    
        if master is ContentType:
            mt = request.REQUEST.get(URL_PARAM_MASTER_TYPE)
            try:
                master = kw['master'] = ContentType.objects.get(pk=mt).model_class()
            except ContentType.DoesNotExist,e:
                raise ContentType.DoesNotExist("ContentType %r does not exist." % mt)
                
            #~ print kw
        if master is not None and not kw.has_key('master_instance'):
            pk = request.REQUEST.get(URL_PARAM_MASTER_PK,None)
            #~ print '20100406a', self.report,URL_PARAM_MASTER_PK,"=",pk
            #~ if pk in ('', '-99999'):
            if pk == '':
                pk = None
            if pk is None:
                kw['master_instance'] = None
            else:
                try:
                    kw['master_instance'] = master.objects.get(pk=pk)
                except ValueError,e:
                    raise Http404("Invalid primary key %r for %s",pk,master.__name__)
                except master.DoesNotExist,e:
                    # todo: ReportRequest should become a subclass of Dialog and this exception should call dlg.error()
                    raise Http404("There's no %s with primary key %r",master.__name__,pk)
            #~ print '20100212', self #, kw['master_instance']
        #~ print '20100406b', self.report,kw
        
        filter = request.REQUEST.get('filter',None)
        if filter is not None:
            filter = json.loads(filter)
            kw['gridfilters'] = [dict2kw(flt) for flt in filter]
        
        
        quick_search = request.REQUEST.get(URL_PARAM_FILTER,None)
        if quick_search:
            kw.update(quick_search=quick_search)
        offset = request.REQUEST.get('start',None)
        if offset:
            kw.update(offset=int(offset))
        limit = request.REQUEST.get('limit',None)
        if limit:
            kw.update(limit=int(limit))
        #~ else:
            #~ kw.update(limit=self.report.page_length)
            
        sort = request.REQUEST.get('sort',None)
        if sort:
            self.sort_column = sort
            sort_dir = request.REQUEST.get('dir','ASC')
            if sort_dir == 'DESC':
                sort = '-'+sort
                self.sort_direction = 'DESC'
            kw.update(order_by=sort)
        
        #~ layout = request.REQUEST.get('layout',None)
        #~ if layout:
            #~ kw.update(layout=int(layout))
            #~ kw.update(layout=rh.layouts[int(layout)])
            
        kw.update(user=request.user)
        
        if isinstance(self.action, actions.RowAction):
        #~ if self.action.needs_selection:
            kw.update(selected_rows = [
              self.ah.actor.model.objects.get(pk=pk) 
              for pk in request.REQUEST.getlist(POST_PARAM_SELECTED)])
            #~ selected = request.REQUEST.get(POST_PARAM_SELECTED,None)
            #~ if selected:
                #~ kw.update(selected_rows = [
                  #~ self.ah.actor.model.objects.get(pk=pk) for pk in selected.split(',') if pk])
        
        return kw
      
        
    def get_user(self):
        return authenticated_user(self.request.user)

    
    def unused_get_absolute_url(self,**kw):
        if self.master_instance is not None:
            kw.update(master_instance=self.master_instance)
        if self.sort_column is not None:
            kw.update(sort=self.sort_column)
        if self.sort_direction is not None:
            kw.update(dir=self.sort_direction)
        if self.layout is not self.rh.layouts[1]:
            kw.update(layout=self.layout.index)
        if self.limit != self.__class__.limit:
            kw.update(limit=self.limit)
        if self.offset is not None:
            kw.update(start=self.offset)
        return self.report.get_absolute_url(**kw)

    def row2list(self,row):
        return self.store.row2list(self.request,row)
        #~ l = []
        #~ for fld in self.store.fields:
            #~ l += fld.obj2list(self.request,row,d)
        #~ return l
      
    def row2dict(self,row):
        return self.store.row2dict(self.request,row)
        #~ d = {}
        #~ request = self.request
        #~ for fld in self.store.fields:
            #~ fld.obj2dict(request,row,d)
        #~ return d
 

#~ class ViewActionRequest(actions.ActionRequest):
    #~ def __init__(self,request,ah,action,*args,**kw):
        #~ self.request = request
        #~ actions.ActionRequest.__init__(self,ah,action,*args,**kw)
        
    #~ def handle_wc(self):
        #~ return self.action.handle_wc(self)
