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

from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
#~ from django.contrib.contenttypes import generic

import lino
#~ from lino import actions
from lino import reports
from lino import forms
from lino.core import action_requests
from lino.utils import ucsv
from lino.utils import chooser
#~ from lino.ui.extjs import ext_windows


#~ UNDEFINED = "nix"

CHOICES_TEXT_FIELD = 'text'
CHOICES_VALUE_FIELD = 'value'
CHOICES_HIDDEN_SUFFIX = "Hidden"


URL_PARAM_MASTER_TYPE = 'mt'
URL_PARAM_MASTER_PK = 'mk'
# URL_PARAM_MASTER_GRID = 'mg'
URL_PARAM_FILTER = 'query'
URL_PARAM_CHOICES_PK = "ck"

POST_PARAM_SELECTED = 'selected'


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
        

class BaseViewReportRequest(action_requests.ReportActionRequest):
    
    def __init__(self,request,rh,action,*args,**kw):
        action_requests.ReportActionRequest.__init__(self,rh,action)
        self.request = request
        self.store = rh.store
        #~ request._lino_request = self
        kw = self.parse_req(request,rh,**kw)
        self.setup(*args,**kw)
        
    def parse_req(self,request,rh,**kw):
        master = kw.get('master',self.report.master)
        if master is ContentType:
            mt = request.REQUEST.get(URL_PARAM_MASTER_TYPE)
            master = kw['master'] = ContentType.objects.get(pk=mt).model_class()
            #~ print kw
        if master is not None and not kw.has_key('master_instance'):
            pk = request.REQUEST.get(URL_PARAM_MASTER_PK,None)
            #~ print '20100406a', self.report,URL_PARAM_MASTER_PK,"=",pk
            if pk == '':
                pk = None
            if pk is None:
                kw['master_instance'] = None
            else:
                try:
                    kw['master_instance'] = master.objects.get(pk=pk)
                except master.DoesNotExist,e:
                    # todo: ReportRequest should become a subclass of Dialog and this exception should call dlg.error()
                    lino.log.warning(
                      "There's no %s with primary key %r",
                      master.__name__,pk)
            #~ print '20100212', self #, kw['master_instance']
        #~ print '20100406b', self.report,kw
        quick_search = request.REQUEST.get(URL_PARAM_FILTER,None)
        if quick_search:
            kw.update(quick_search=quick_search)
        offset = request.REQUEST.get('start',None)
        if offset:
            kw.update(offset=int(offset))
        limit = request.REQUEST.get('limit',None)
        if limit:
            kw.update(limit=int(limit))
        else:
            kw.update(limit=self.report.page_length)
            
        sort = request.REQUEST.get('sort',None)
        if sort:
            self.sort_column = sort
            sort_dir = request.REQUEST.get('dir','ASC')
            if sort_dir == 'DESC':
                sort = '-'+sort
                self.sort_direction = 'DESC'
            kw.update(order_by=sort)
        
        layout = request.REQUEST.get('layout',None)
        if layout:
            kw.update(layout=int(layout))
            #~ kw.update(layout=rh.layouts[int(layout)])
            
        kw.update(user=request.user)
        
        if self.action.needs_selection:
            selected = request.POST.get(POST_PARAM_SELECTED,None)
            if selected:
                kw.update(selected_rows = [
                  self.ah.actor.model.objects.get(pk=pk) for pk in selected.split(',') if pk])
        
        return kw
      
        
    def get_user(self):
        return authenticated_user(self.request.user)

    def get_absolute_url(self,**kw):
        if self.limit != self.__class__.limit:
            kw.update(limit=self.limit)
        if self.offset is not None:
            kw.update(start=self.offset)
        return self.report.get_absolute_url(**kw)
        

class CSVReportRequest(BaseViewReportRequest):
    extra = 0
    
    def get_absolute_url(self,**kw):
        kw['csv'] = True
        return BaseViewReportRequest.get_absolute_url(self,**kw)
        
    def parse_req(self,request,rh,**kw):
        quick_search = request.GET.get(URL_PARAM_FILTER,None)
        if quick_search:
            kw.update(quick_search=quick_search)
        return kw
        
    def render_to_csv(self):
        response = HttpResponse(mimetype='text/csv')
        w = ucsv.UnicodeWriter(response)
        names = [] # fld.name for fld in self.fields]
        fields = []
        for col in self.rh.list_layout._main.column_model.columns:
            names.append(col.editor.field.name)
            fields.append(col.editor.field)
        w.writerow(names)
        for row in self.queryset:
            values = []
            for fld in fields:
                # uh, this is tricky...
                meth = getattr(fld,'_return_type_for_method',None)
                if meth is not None:
                    v = meth(row)
                else:
                    v = fld.value_to_string(row)
                #lino.log.debug("20100202 %r.%s is %r",row,fld.name,v)
                values.append(v)
            w.writerow(values)
        return response

        
  
class ChoicesReportRequest(BaseViewReportRequest):
    extra = 0
    
    def __init__(self,request,rh,fldname,*args,**kw):
        self.fieldname = fldname
        BaseViewReportRequest.__init__(self,request,rh,rh.report.default_action,*args,**kw)
        
    def get_absolute_url(self,**kw):
        kw['choices_for_field'] = self.fieldname
        return BaseViewReportRequest.get_absolute_url(self,**kw)
        
    def setup_queryset(self):
        kw = {}
        for k,v in self.request.GET.items():
            kw[str(k)] = v
        chooser = self.rh.choosers[self.fieldname]
        qs = chooser.get_choices(**kw)
        if self.quick_search is not None:
            qs = reports.add_quick_search_filter(qs,self.quick_search)
        self.queryset = qs
        
    def row2dict(self,obj,d):
        d[CHOICES_TEXT_FIELD] = unicode(obj)
        #d['__unicode__'] = unicode(obj)
        d[CHOICES_VALUE_FIELD] = obj.pk # getattr(obj,'pk')
        #d[self.fieldname] = obj.pk 
        return d
          
  
class ViewReportRequest(BaseViewReportRequest):
  
    editing = 0
    selector = None
    sort_column = None
    sort_direction = None
    
    def get_absolute_url(self,**kw):
        if self.master_instance is not None:
            kw.update(master_instance=self.master_instance)
        if self.sort_column is not None:
            kw.update(sort=self.sort_column)
        if self.sort_direction is not None:
            kw.update(dir=self.sort_direction)
        if self.layout is not self.rh.layouts[1]:
            kw.update(layout=self.layout.index)
        return BaseViewReportRequest.get_absolute_url(self,**kw)

    def row2dict(self,row,d):
        #lino.log.debug('row2dict(%s)',row.__class__)
        #lino.log.debug('row2dict(%r)',row)
        if self.report.use_layouts:
            for fld in self.store.fields:
                fld.obj2json(row,d)
        else:
            self.report.row2dict(row,d)
        #lino.log.debug('  -> %r',kw)
        return d
 

