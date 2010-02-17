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

from lino import actions
from lino import reports
from lino.utils import ucsv

from django.contrib.contenttypes.models import ContentType
#~ from django.contrib.contenttypes import generic

#~ UNDEFINED = "nix"

CHOICES_TEXT_FIELD = 'text'
CHOICES_VALUE_FIELD = 'value'
CHOICES_HIDDEN_SUFFIX = "Hidden"


URL_PARAM_MASTER_TYPE = 'mt'
URL_PARAM_MASTER_PK = 'mk'
# URL_PARAM_MASTER_GRID = 'mg'
URL_PARAM_FILTER = 'query'
URL_PARAM_CHOICES_PK = "ck"



def authenticated_user(user):
    if user.is_anonymous():
        return None
    return user
        
      
#~ class ActionContext(actions.ActionContext):
    #~ def __init__(self,request,*args,**kw):
        #~ actions.ActionContext.__init__(self,*args,**kw)
        #~ self.request = request
        #~ self.confirmed = self.request.POST.get('confirmed',None)
        #~ if self.confirmed is not None:
            #~ self.confirmed = int(self.confirmed)
        #~ self.confirms = 0
        #~ #print 'ActionContext.__init__()', self.confirmed, self.selected_rows
        
    #~ def get_user(self):
        #~ return authenticated_user(self.request.user)
        
    #~ def get_report_request(self):
        #~ raise NotImplementedError()
        
#~ class GridActionContext(ActionContext):
    #~ def __init__(self,request,*args,**kw):
        #~ ActionContext.__init__(self,request,*args,**kw)
        #~ assert isinstance(self.actor,reports.Report)
        #~ selected = self.request.POST.get('selected',None)
        #~ if selected:
            #~ self.selected_rows = [
              #~ self.actor.model.objects.get(pk=pk) for pk in selected.split(',') if pk]
        #~ else:
            #~ self.selected_rows = []
        
    #~ def get_report_request(self):
        #~ raise "what's about kw and ReportRequest.setup() here?"
        #~ rh = self.actor.get_handle(self.ui)
        #~ return ViewReportRequest(self.request,rh)


class Dialog(actions.Dialog):
    def __init__(self,request,*args,**kw):
        actions.Dialog.__init__(self,*args,**kw)
        self.request = request
        
        self.confirmed = self.request.POST.get('confirmed',None)
        
    def get_user(self):
        return authenticated_user(self.request.user)
        
    def get_report_request(self):
        raise NotImplementedError()
        
class GridDialog(Dialog):
    def __init__(self,request,*args,**kw):
        Dialog.__init__(self,request,*args,**kw)
        assert isinstance(self.actor,reports.Report)
        selected = self.request.POST.get('selected',None)
        if selected:
            self.selected_rows = [
              self.actor.model.objects.get(pk=pk) for pk in selected.split(',') if pk]
        else:
            self.selected_rows = []



class BaseViewReportRequest(reports.ReportRequest):
    
    def __init__(self,request,rh,*args,**kw):
        reports.ReportRequest.__init__(self,rh)
        self.request = request
        self.store = rh.store
        request._lino_request = self
        kw = self.parse_req(request,rh,**kw)
        self.setup(*args,**kw)
        
    def parse_req(self,request,rh,**kw):
        quick_search = request.GET.get(URL_PARAM_FILTER,None)
        if quick_search:
            kw.update(quick_search=quick_search)
        offset = request.GET.get('start',None)
        if offset:
            kw.update(offset=int(offset))
        limit = request.GET.get('limit',None)
        if limit:
            kw.update(limit=int(limit))
        else:
            kw.update(limit=self.report.page_length)
        kw.update(user=request.user)
        return kw
      
    def get_absolute_url(self,**kw):
        if self.limit != self.__class__.limit:
            kw.update(limit=self.limit)
        if self.offset is not None:
            kw.update(start=self.offset)
        return self.report.get_absolute_url(**kw)
        
    def render_to_json(self):
        rows = [ self.obj2json(row) for row in self.queryset ]
        total_count = self.total_count
        #lino.log.debug('%s.render_to_json() total_count=%d extra=%d',self,total_count,self.extra)
        # add extra blank row(s):
        for i in range(0,self.extra):
            row = self.create_instance()
            rows.append(self.obj2json(row))
            total_count += 1
        return dict(count=total_count,rows=rows)
        

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
        for col in self.rh.row_layout._main.column_model.columns:
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
        #self.recipient_report = rh.report
        self.fieldname = fldname
        fld, remote, direct, m2m = rh.report.model._meta.get_field_by_name(fldname)
        #fld = rpt.model._meta.get_field_by_name(fldname)
        assert direct
        self.rec_field = fld
        #called_rpt = reports.get_model_report(fld.rel.to)
        #rh = rpt.get_handle(ui)
        BaseViewReportRequest.__init__(self,request,rh,*args,**kw)
        
    #~ def parse_req(self,request,rh,**kw):
        #~ kw = BaseViewReportRequest.parse_req(self,request,rh,**kw)
        #~ kw['extra'] = 0
        #~ return kw
          
    def get_queryset(self,**kw):
        pk = self.request.GET.get(URL_PARAM_CHOICES_PK,None)
        return self.report.get_field_choices(self.rec_field,pk,**kw)
        #return self.report.get_queryset(self,master_instance=self.master_instance,**kw)
        
    def get_absolute_url(self,**kw):
        kw['choices_for_field'] = self.fieldname
        return BaseViewReportRequest.get_absolute_url(self,**kw)
        
    def obj2json(self,obj,**kw):
        kw[CHOICES_TEXT_FIELD] = unicode(obj)
        #kw['__unicode__'] = unicode(obj)
        kw[CHOICES_VALUE_FIELD] = obj.pk # getattr(obj,'pk')
        #kw[self.fieldname] = obj.pk 
        return kw
          
    #~ rh = 
    #~ req = ChoicesReportRequest(rpt,request)
    #~ pk = request.GET.get(URL_PARAM_CHOICES_PK,None)
    #~ choices_filter = rpt.get_field_choices(pk)
    #~ qs = rpt.get_queryset
    #~ choices = rpt.get_choice_field
    #~ model = models.get_model(app_label,modname)
    #~ field = model._meta.get_field_by_name(fldname)
    #~ get_field_choices
    #~ rpt = field._lino_choices_report
    #~ #kw['colname'] = request.POST['colname']
    #~ return json_report_view_(request,rpt,**kw)
        
  
class ViewReportRequest(BaseViewReportRequest):
  
    editing = 0
    selector = None
    sort_column = None
    sort_direction = None
    
    def parse_req(self,request,rh,**kw):
        kw = BaseViewReportRequest.parse_req(self,request,rh,**kw)
        if rh.report.master is not None and not kw.has_key('master_instance'):
            pk = request.GET.get(URL_PARAM_MASTER_PK,None)
            #~ if pk == UNDEFINED:
                #~ pk = None
            if pk == '':
                pk = None
            if pk is None:
                kw.update(master_instance=None)
            else:
                if rh.report.master is ContentType:
                    mt = request.GET.get(URL_PARAM_MASTER_TYPE)
                    master_model = ContentType.objects.get(pk=mt).model_class()
                else:
                    master_model = rh.report.master
                try:
                    m = master_model.objects.get(pk=pk)
                except master_model.DoesNotExist,e:
                    lino.log.warning(
                      "There's no %s with primary key %r",
                      master_model.__name__,pk)
                else:
                    kw.update(master_instance=m)
            #~ print '20100212', self #, kw['master_instance']
        sort = request.GET.get('sort',None)
        if sort:
            self.sort_column = sort
            sort_dir = request.GET.get('dir','ASC')
            if sort_dir == 'DESC':
                sort = '-'+sort
                self.sort_direction = 'DESC'
            kw.update(order_by=sort)
        
        layout = request.GET.get('layout',None)
        if layout:
            kw.update(layout=rh.layouts[int(layout)])
        return kw
        
        
    def get_user(self):
        return authenticated_user(self.request.user)

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

    def obj2json(self,obj,**kw):
        #lino.log.debug('obj2json(%s)',obj.__class__)
        #lino.log.debug('obj2json(%r)',obj)
        for fld in self.store.fields:
            fld.obj2json(obj,kw)
        #lino.log.debug('  -> %r',kw)
        return kw
 

