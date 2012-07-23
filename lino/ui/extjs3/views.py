# -*- coding: UTF-8 -*-
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

from django import http
#~ from django.http import HttpResponse, Http404
from django.db import models
from django.conf import settings
from django.views.generic import View
from django.utils import simplejson as json
from django.core import exceptions
from django.utils.translation import ugettext as _

from lino import dd

from lino.utils.xmlgen import html as xghtml
from lino.utils.jsgen import py2js, js_code, id2js
from lino.utils import choosers
from lino.utils import isiterable
from lino.utils import dblogger

from lino.core import actions
from lino.core import actors
from lino.core.modeltools import obj2str, obj2unicode

from lino.ui import requests as ext_requests
from lino.ui.extjs3 import ext_elems



class HttpResponseDeleted(http.HttpResponse):
    status_code = 204
    


def requested_report(app_label,actor):
    x = getattr(settings.LINO.modules,app_label)
    cl = getattr(x,actor)
    if issubclass(cl,dd.Model):
        return cl._lino_default_table
    return cl
        
def json_response_kw(**kw):
    return json_response(kw)
    
def json_response(x,content_type='application/json'):
    #~ logger.info("20120208")
    #s = simplejson.dumps(kw,default=unicode)
    #return HttpResponse(s, mimetype='text/html')
    s = py2js(x)
    #~ logger.info("20120208 json_response(%r)\n--> %s",x,s)
    #~ logger.debug("json_response() -> %r", s)
    """
    Theroretically we should send content_type='application/json'
    (http://stackoverflow.com/questions/477816/the-right-json-content-type),
    but "File uploads are not performed using Ajax submission, 
    that is they are not performed using XMLHttpRequests. (...) 
    If the server is using JSON to send the return object, then 
    the Content-Type header must be set to "text/html" in order 
    to tell the browser to insert the text unchanged into the 
    document body." 
    (http://docs.sencha.com/ext-js/3-4/#!/api/Ext.form.BasicForm)
    See 20120209.
    """
    return http.HttpResponse(s, content_type=content_type)
    #~ return HttpResponse(s, content_type='text/html')
    #~ return HttpResponse(s, content_type='application/json')
    #~ return HttpResponse(s, content_type='text/json')
    
def elem2rec1(ar,rh,elem,**rec):
    rec.update(data=rh.store.row2dict(ar,elem))
    return rec

#~ def elem2rec_empty(ar,ah,**rec):
    #~ rec.update(data=dict())
    #~ rec.update(title='Empty detail')
    #~ return rec
    
def elem2rec_insert(ar,ah,elem):
    """
    Returns a dict of this record, designed for usage by an InsertWindow.
    """
    rec = elem2rec1(ar,ah,elem)
    #~ rec.update(title=_("Insert into %s...") % ar.get_title())
    rec.update(title=ar.get_action_title())
    rec.update(phantom=True)
    #~ rec.update(id=elem.pk) or -99999)
    return rec

def elem2rec_empty(ar,ah,elem,**rec):
    """
    Returns a dict of this record, designed for usage by an EmptyTable.
    """
    #~ rec.update(data=rh.store.row2dict(ar,elem))
    rec.update(data=elem._data)
    #~ rec = elem2rec1(ar,ah,elem)
    #~ rec.update(title=_("Insert into %s...") % ar.get_title())
    rec.update(title=ar.get_action_title())
    rec.update(id=-99998)
    #~ rec.update(id=elem.pk) or -99999)
    return rec

def elem2rec_detailed(ar,elem,**rec):
    """
    Adds additional information for this record, used only by detail views.
    
    The "navigation information" is a set of pointers to the next, previous, 
    first and last record relative to this record in this report. 
    (This information can be relatively expensive for records that are towards 
    the end of the report. 
    See :doc:`/blog/2010/0716`,
    :doc:`/blog/2010/0721`,
    :doc:`/blog/2010/1116`,
    :doc:`/blog/2010/1207`.)
    
    recno 0 means "the requested element exists but is not contained in the requested queryset".
    This can happen after changing the quick filter (search_change) of a detail view.
    
    """
    rh = ar.ah
    rec = elem2rec1(ar,rh,elem,**rec)
    if ar.actor.hide_top_toolbar:
        rec.update(title=unicode(elem))
    else:
        rec.update(title=ar.get_title() + u" » " + unicode(elem))
    #~ rec.update(title=ar.actor.get_detail_title(ar,elem))
    #~ rec.update(title=rh.actor.model._meta.verbose_name + u"«%s»" % unicode(elem))
    #~ rec.update(title=unicode(elem))
    rec.update(id=elem.pk)
    #~ if rh.actor.disable_delete:
    #~ rec.update(disabled_actions=rh.actor.disabled_actions(ar,elem))
    rec.update(disable_delete=rh.actor.disable_delete(elem,ar))
    if rh.actor.show_detail_navigator:
        first = None
        prev = None
        next = None
        last = None
        #~ ar = ext_requests.ViewReportRequest(request,rh,rh.actor.default_action)
        recno = 0
        #~ if len(ar.data_iterator) > 0:
        LEN = ar.get_total_count()
        if LEN > 0:
            if True:
                # this algorithm is clearly quicker on reports with a few thousand Persons
                id_list = list(ar.data_iterator.values_list('pk',flat=True))
                """
                Uncommented the following assert because it failed in certain circumstances 
                (see :doc:`/blog/2011/1220`)
                """
                #~ assert len(id_list) == ar.total_count, \
                    #~ "len(id_list) is %d while ar.total_count is %d" % (len(id_list),ar.total_count)
                #~ print 20111220, id_list
                first = id_list[0]
                last = id_list[-1]
                try:
                    i = id_list.index(elem.pk)
                except ValueError:
                    pass
                else:
                    recno = i + 1
                    if i > 0:
                        #~ prev = ar.queryset[i-1]
                        prev = id_list[i-1]
                    if i < len(id_list) - 1:
                        #~ next = ar.queryset[i+1]
                        next = id_list[i+1]
            else:
                first = ar.queryset[0]
                last = ar.queryset.reverse()[0]
                if ar.get_total_count() > 200:
                    #~ TODO: check performance
                    pass
                g = enumerate(ar.queryset) # a generator
                try:
                    while True:
                        index, item = g.next()
                        if item == elem:
                            if index > 0:
                                prev = ar.queryset[index-1]
                            recno = index + 1
                            index,next = g.next()
                            break
                except StopIteration:
                    pass
                if first is not None: first = first.pk
                if last is not None: last = last.pk
                if prev is not None: prev = prev.pk
                if next is not None: next = next.pk
        rec.update(navinfo=dict(
            first=first,prev=prev,next=next,last=last,recno=recno,
            message=_("Row %(rowid)d of %(rowcount)d") % dict(
              rowid=recno,rowcount=LEN)))
    return rec
            
    

  
    
    


def delete_element(ar,elem):
    assert elem is not None
    msg = ar.actor.disable_delete(elem,ar)
    if msg is not None:
        return settings.LINO.ui.error_response(None,msg)
            
    dblogger.log_deleted(ar.request,elem)
    
    try:
        elem.delete()
    except Exception,e:
        dblogger.exception(e)
        msg = _("Failed to delete %(record)s : %(error)s."
            ) % dict(record=obj2unicode(elem),error=e)
        #~ msg = "Failed to delete %s." % element_name(elem)
        return settings.LINO.ui.error_response(None,msg)
        #~ raise Http404(msg)
    return HttpResponseDeleted()
    

#~ def form2obj_and_save(self,request,rh,data,elem,is_new,include_rows): # **kw2save):
def form2obj_and_save(ar,data,elem,is_new,restful,file_upload=False): # **kw2save):
    """
    """
    #~ self = settings.LINO.ui
    request = ar.request
    rh = ar.ah
    #~ logger.info('20111217 form2obj_and_save %r', data)
    #~ print 'form2obj_and_save %r' % data
    
    #~ logger.info('20120228 before store.form2obj , elem is %s' % obj2str(elem))
    # store normal form data (POST or PUT)
    try:
        rh.store.form2obj(ar,data,elem,is_new)
    except exceptions.ValidationError,e:
        #~ raise
        return settings.LINO.ui.error_response(e)
       #~ return error_response(e,_("There was a problem while validating your data : "))
    #~ logger.info('20120228 store.form2obj passed, elem is %s' % obj2str(elem))
    
    elem.before_ui_save(ar)
    
    if not is_new:
        dblogger.log_changes(request,elem)
        
    try:
        elem.full_clean()
    except exceptions.ValidationError, e:
        return settings.LINO.ui.error_response(e) #,_("There was a problem while validating your data : "))
        
    kw2save = {}
    if is_new:
        kw2save.update(force_insert=True)
    else:
        kw2save.update(force_update=True)
        
    try:
        elem.save(**kw2save)
        
    #~ except Exception,e:
    except IntegrityError,e:
        return settings.LINO.ui.error_response(e) # ,_("There was a problem while saving your data : "))
        #~ return views.json_response_kw(success=False,
              #~ msg=_("There was a problem while saving your data:\n%s") % e)
    kw = dict(success=True)
    if is_new:
        dblogger.log_created(request,elem)
        kw.update(
            message=_("%s has been created.") % obj2unicode(elem))
            #~ record_id=elem.pk)
    else:
        kw.update(message=_("%s has been saved.") % obj2unicode(elem))
        
    kw = elem.after_ui_save(ar,**kw)
    #~ m = getattr(elem,"after_ui_save",None)
    #~ if m is not None:
        #~ kw = m(ar,**kw)
        
    if restful:
        # restful mode (used only for Ext.ensible) needs list_fields, not detail_fields
        kw.update(rows=[rh.store.row2dict(ar,elem,rh.store.list_fields)])
    elif file_upload:
        kw.update(record_id=elem.pk)
        return json_response(kw,content_type='text/html')
    else:
        kw.update(data_record=elem2rec_detailed(ar,elem))
    #~ logger.info("20120208 form2obj_and_save --> %r",kw)
    return json_response(kw)
            
        
    #~ return settings.LINO.ui.success_response(
        #~ _("%s has been saved.") % obj2unicode(elem),
        #~ rows=[elem])
    
        


class Index(View):

    def get(self, request, *args, **kw):
        ui = settings.LINO.ui
        #~ from lino.lino_site import lino_site
        #~ if settings.LINO.index_view_action:
            #~ kw.update(on_ready=self.ext_renderer.action_call(
              #~ settings.LINO.index_view_action))
        #~ logger.info("20120706 index_view() %s %r",request.user, request.user.profile)
        main = settings.LINO.get_main_action(request.subst_user or request.user)
        kw.update(on_ready=ui.ext_renderer.action_call(request,main))
        #~ kw.update(title=settings.LINO.modules.pcsw.Home.label)
        #~ kw.update(title=lino_site.title)
        #~ mnu = py2js(lino_site.get_site_menu(request.user))
        #~ print mnu
        #~ tbar=ext_elems.Toolbar(items=lino_site.get_site_menu(request.user),region='north',height=29)# renderTo='tbar')
        return http.HttpResponse(ui.html_page(request,**kw))
        #~ html = '\n'.join(self.html_page(request,main,konsole,**kw))
        #~ return HttpResponse(html)


class Templates(View):
  
    #~ def templates_view(self,request,
    def get(self,request,
        app_label=None,actor=None,pk=None,fldname=None,tplname=None,**kw):
      
        if request.method == 'GET':
            from lino.models import TextFieldTemplate
            if tplname:
                tft = TextFieldTemplate.objects.get(pk=int(tplname))
                return http.HttpResponse(tft.text)
                
            rpt = requested_report(app_label,actor)
                
            elem = rpt.get_row_by_pk(pk)

                
            if elem is None:
                raise http.Http404("%s %s does not exist." % (rpt,pk))
                
            #~ TextFieldTemplate.templates
            m = getattr(elem,"%s_templates" % fldname,None)
            if m is None:
                q = models.Q(user=request.user) | models.Q(user=None)
                #~ q = models.Q(user=request.user)
                qs = TextFieldTemplate.objects.filter(q).order_by('name')
            else:
                qs = m(request)
                
            templates = []
            for obj in qs:
                url = settings.LINO.ui.build_url('templates',
                    app_label,actor,pk,fldname,unicode(obj.pk))
                templates.append([
                    unicode(obj.name),url,unicode(obj.description)])
            js = "var tinyMCETemplateList = %s;" % py2js(templates)
            return http.HttpResponse(js,content_type='text/json')
        raise http.Http404("Method %r not supported" % request.method)
        
  
class Choices(View):
  
    #~ def choices_view(self,request,app_label=None,rptname=None,fldname=None,**kw):
    def get(self,request,app_label=None,rptname=None,fldname=None,**kw):
        """
        Return a JSON object with two attributes `count` and `rows`,
        where `rows` is a list of `(display_text,value)` tuples.
        Used by ComboBoxes or similar widgets.
        If `fldname` is not specified, returns the choices for the `jumpto` widget.
        """
        rpt = requested_report(app_label,rptname)
        #~ rpt = actors.get_actor2(app_label,rptname)
        ar = rpt.request(settings.LINO.ui,request,rpt.default_action)
        if fldname is None:
            #~ rh = rpt.get_handle(self)
            #~ ar = ViewReportRequest(request,rh,rpt.default_action)
            #~ ar = table.TableRequest(self,rpt,request,rpt.default_action)
            #~ rh = ar.ah
            #~ qs = ar.get_data_iterator()
            qs = ar.data_iterator
            #~ qs = rpt.request(self).get_queryset()
            def row2dict(obj,d):
                d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                d[ext_requests.CHOICES_VALUE_FIELD] = obj.pk # getattr(obj,'pk')
                return d
        else:
            """
            NOTE: if you define a *parameter* with the same name 
            as some existing *data element* name, then the parameter 
            will override the data element. At least here in choices view.
            """
            #~ field = find_field(rpt.model,fldname)
            field = rpt.get_param_elem(fldname)
            if field is None:
                field = rpt.get_data_elem(fldname)
            #~ logger.info("20120202 %r",field)
            chooser = choosers.get_for_field(field)
            if chooser:
                #~ logger.info('20120710 choices_view() : has chooser')
                qs = chooser.get_request_choices(ar,rpt)
                #~ qs = list(chooser.get_request_choices(ar,rpt))
                #~ logger.info("20120213 %s",qs)
                #~ if qs is None:
                    #~ qs = []
                assert isiterable(qs), \
                      "%s.%s_choices() returned %r which is not iterable." % (
                      rpt.model,fldname,qs)
                if chooser.simple_values:
                    def row2dict(obj,d):
                        #~ d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                        d[ext_requests.CHOICES_VALUE_FIELD] = unicode(obj)
                        return d
                elif chooser.instance_values:
                    # same code as for ForeignKey
                    def row2dict(obj,d):
                        d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                        d[ext_requests.CHOICES_VALUE_FIELD] = obj.pk # getattr(obj,'pk')
                        return d
                else:
                    def row2dict(obj,d):
                        d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj[1])
                        d[ext_requests.CHOICES_VALUE_FIELD] = obj[0]
                        return d
            elif field.choices:
                qs = field.choices
                def row2dict(obj,d):
                    if type(obj) is list or type(obj) is tuple:
                        d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj[1])
                        d[ext_requests.CHOICES_VALUE_FIELD] = obj[0]
                    else:
                        d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                        d[ext_requests.CHOICES_VALUE_FIELD] = unicode(obj)
                    return d
                
            elif isinstance(field,models.ForeignKey):
                m = field.rel.to
                t = getattr(m,'_lino_choices_table',m._lino_default_table)
                qs = t.request(settings.LINO.ui,request).data_iterator
                #~ logger.info('20120710 choices_view(FK) %s --> %s',t,qs)
                def row2dict(obj,d):
                    d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                    d[ext_requests.CHOICES_VALUE_FIELD] = obj.pk # getattr(obj,'pk')
                    return d
            else:
                raise http.Http404("No choices for %s" % fldname)
                
                
        #~ quick_search = request.GET.get(ext_requests.URL_PARAM_FILTER,None)
        #~ if quick_search is not None:
            #~ qs = table.add_quick_search_filter(qs,quick_search)
            
        count = len(qs)
            
        offset = request.GET.get(ext_requests.URL_PARAM_START,None)
        if offset:
            qs = qs[int(offset):]
            #~ kw.update(offset=int(offset))
        limit = request.GET.get(ext_requests.URL_PARAM_LIMIT,None)
        if limit:
            #~ kw.update(limit=int(limit))
            qs = qs[:int(limit)]
            
        rows = [ row2dict(row,{}) for row in qs ]
        return json_response_kw(count=count,rows=rows) 
        #~ return json_response_kw(count=len(rows),rows=rows) 
        #~ return json_response_kw(count=len(rows),rows=rows,title=_('Choices for %s') % fldname)
        
  
class Restful(View):
    """
    Used to collaborate with a restful Ext.data.Store.
    """
  
    def post(self,request,app_label=None,actor=None,pk=None):
        ui = settings.LINO.ui
        rpt = requested_report(app_label,actor)
        a = rpt.default_action
        if pk is None:
            elem = None
        else:
            elem = rpt.get_row_by_pk(pk)
        ar = rpt.request(ui,request,a)
            
        instance = ar.create_instance()
        # store uploaded files. 
        # html forms cannot send files with PUT or GET, only with POST
        if ar.actor.handle_uploaded_files is not None:
            ar.actor.handle_uploaded_files(instance,request)
            
        data = request.POST.get('rows')
        #~ logger.info("20111217 Got POST %r",data)
        data = json.loads(data)
        #~ data = self.rest2form(request,rh,data)
        return form2obj_and_save(ar,data,instance,True,True)
            
        
      
    def delete(self,request,app_label=None,actor=None,pk=None):
        ui = settings.LINO.ui
        rpt = requested_report(app_label,actor)
        a = rpt.default_action
        elem = rpt.get_row_by_pk(pk)
        ar = rpt.request(ui,request,a)
        return delete_element(ar,elem)
      
    #~ def restful_view(self,request,app_label=None,actor=None,pk=None):
    def get(self,request,app_label=None,actor=None,pk=None):
        ui = settings.LINO.ui
        rpt = requested_report(app_label,actor)
        a = rpt.default_action
        if pk is None:
            elem = None
        else:
            elem = rpt.get_row_by_pk(pk)
        ar = rpt.request(ui,request,a)
        rh = ar.ah
            
        rows = [ 
          rh.store.row2dict(ar,row,rh.store.list_fields) 
            for row in ar.sliced_data_iterator ]
        return json_response_kw(count=ar.get_total_count(),rows=rows)
        
    def put(self,request,app_label=None,actor=None,pk=None):
        ui = settings.LINO.ui
        rpt = requested_report(app_label,actor)
        a = rpt.default_action
        elem = rpt.get_row_by_pk(pk)
        ar = rpt.request(ui,request,a)
        rh = ar.ah
            
        data = http.QueryDict(request.raw_post_data).get('rows')
        data = json.loads(data)
        a = rpt.get_url_action(rpt.default_list_action_name)
        ar = rpt.request(ui,request,a)
        ar.renderer = ui.ext_renderer
        return form2obj_and_save(ar,data,elem,False,True) # force_update=True)
          
  
  
class ApiElement(View):
    #~ def api_element_view(self,request,app_label=None,actor=None,pk=None):
    def get(self,request,app_label=None,actor=None,pk=None):
        """
        GET : Retrieve a representation of the addressed member of the collection expressed in an appropriate MIME type.
        PUT : Update the addressed member of the collection or create it with the specified ID. 
        POST : Treats the addressed member as a collection and creates a new subordinate of it. 
        DELETE : Delete the addressed member of the collection. 
        
        (Source: http://en.wikipedia.org/wiki/Restful)
        """
        ui = settings.LINO.ui
        rpt = requested_report(app_label,actor)
        #~ if not ah.actor.can_view.passes(request.user):
            #~ msg = "User %s cannot view %s." % (request.user,ah.actor)
            #~ return http.HttpResponseForbidden()
        
        if pk and pk != '-99999' and pk != '-99998':
            elem = rpt.get_row_by_pk(pk)
            if elem is None:
                raise http.Http404("%s has no row with prmiary key %r" % (rpt,pk))
                #~ raise Exception("20120327 %s.get_row_by_pk(%r)" % (rpt,pk))
        else:
            elem = None
        
        #~ if request.method == 'DELETE':
            #~ ar = rpt.request(ui,request)
            #~ return delete_element(ar,elem)
            
        #~ if request.method == 'PUT':
            #~ if elem is None:
                #~ raise Http404('Tried to PUT on element -99999')
            #~ data = http.QueryDict(request.raw_post_data)
            #~ a = rpt.get_url_action(rpt.default_list_action_name)
            #~ ar = rpt.request(ui,request,a)
            #~ ar.renderer = ui.ext_renderer
            #~ return form2obj_and_save(ar,data,elem,False,False) # force_update=True)
            
        #~ if request.method == 'GET':
                    
        action_name = request.GET.get(ext_requests.URL_PARAM_ACTION_NAME,
          rpt.default_elem_action_name)
        a = rpt.get_url_action(action_name)
        if a is None:
            raise http.Http404("%s has no action %r" % (rpt,action_name))
            
        ar = rpt.request(ui,request,a)
        ar.renderer = ui.ext_renderer
        ah = ar.ah
        
        #~ fmt = request.GET.get('fmt',a.default_format)
        fmt = request.GET.get(ext_requests.URL_PARAM_FORMAT,a.default_format)

        #~ if isinstance(a,actions.OpenWindowAction):
        if a.opens_a_window:
          
            if fmt == ext_requests.URL_FORMAT_JSON:
                if pk == '-99999':
                    assert elem is None
                    elem = ar.create_instance()
                    datarec = elem2rec_insert(ar,ah,elem)
                elif pk == '-99998':
                    assert elem is None
                    elem = ar.create_instance()
                    datarec = elem2rec_empty(ar,ah,elem)
                else:
                    datarec = elem2rec_detailed(ar,elem)
                
                return json_response(datarec)
                
            #~ after_show = dict(data_record=datarec)
            #~ after_show = dict()
            #~ params = dict()
            after_show = ar.get_status(ui,record_id=pk)
            #~ bp = ui.request2kw(ar)
            
            #~ if a.window_wrapper.tabbed:
            #~ if rpt.get_detail().tabbed:
            #~ if rpt.model._lino_detail.get_handle(ui).tabbed:
            if True:
                tab = request.GET.get(ext_requests.URL_PARAM_TAB,None)
                if tab is not None: 
                    tab = int(tab)
                    after_show.update(active_tab=tab)
            #~ params.update(base_params=bp)
            
            return http.HttpResponse(ui.html_page(request,a.label,
              on_ready=ui.ext_renderer.action_call(request,a,after_show)))
            
        if isinstance(a,actions.RedirectAction):
            target = a.get_target_url(elem)
            if target is None:
                raise http.Http404("%s failed for %r" % (a,elem))
            return http.HttpResponseRedirect(target)
            
        if isinstance(a,actions.RowAction):
            #~ return a.run(ar,elem)
            if pk == '-99998':
                assert elem is None
                elem = ar.create_instance()
            
            try:
                rv = a.run(elem,ar)
                if rv is None:
                    return ui.success_response()
                return rv
            except actions.ConfirmationRequired,e:
                r = dict(
                  success=True,
                  confirm_message='\n'.join([unicode(m) for m in e.messages]),
                  step=e.step)
                return ui.action_response(r)
            except actions.Warning,e:
                r = dict(
                  success=False,
                  message=unicode(e),
                  alert=True)
                return ui.action_response(r)
            except Exception,e:
                if elem is None:
                    msg = unicode(e)
                else:
                    msg = _(
                      "Action \"%(action)s\" failed for %(record)s:") % dict(
                      action=a,
                      record=obj2unicode(elem))
                    msg += "\n" + unicode(e)
                msg += '.\n' + _(
                  "An error report has been sent to the system administrator.")
                logger.warning(msg)
                logger.exception(e)
                return settings.LINO.ui.error_response(e,msg)
          
        raise NotImplementedError("Action %s is not implemented)" % a)
                
              
        #~ return settings.LINO.ui.error_response(None,
            #~ "Method %r not supported for elements of %s." % (
                #~ request.method,ah.actor))
        #~ raise Http404("Method %r not supported for elements of %s" % (request.method,ah.actor))
        
    def put(self,request,app_label=None,actor=None,pk=None):
        ui = settings.LINO.ui
        rpt = requested_report(app_label,actor)
        elem = rpt.get_row_by_pk(pk)
        if elem is None:
            raise http.Http404("%s has no row with prmiary key %r" % (rpt,pk))
        data = http.QueryDict(request.raw_post_data)
        a = rpt.get_url_action(rpt.default_list_action_name)
        ar = rpt.request(ui,request,a)
        ar.renderer = ui.ext_renderer
        return form2obj_and_save(ar,data,elem,False,False) # force_update=True)
            
    def delete(self,request,app_label=None,actor=None,pk=None):
        ui = settings.LINO.ui
        rpt = requested_report(app_label,actor)
        elem = rpt.get_row_by_pk(pk)
        if elem is None:
            raise http.Http404("%s has no row with prmiary key %r" % (rpt,pk))
        ar = rpt.request(ui,request)
        return delete_element(ar,elem)
        
        
  
class ApiList(View):

    def post(self,request,app_label=None,actor=None):
        ui = settings.LINO.ui
        rpt = requested_report(app_label,actor)
        
        #~ action_name = request.GET.get(
        action_name = request.REQUEST.get(
            ext_requests.URL_PARAM_ACTION_NAME,
            rpt.default_list_action_name)
        a = rpt.get_url_action(action_name)
        if a is None:
            raise http.Http404("%s has no url action %r" % (rpt,action_name))
            
        ar = rpt.request(ui,request,a)
        ar.renderer = ui.ext_renderer
        rh = ar.ah
        
        #~ data = rh.store.get_from_form(request.POST)
        #~ instance = ar.create_instance(**data)
        #~ ar = ext_requests.ViewReportRequest(request,rh,rh.actor.list_action)
        #~ ar = ext_requests.ViewReportRequest(request,rh,rh.actor.default_action)
        elem = ar.create_instance()
        # store uploaded files. 
        # html forms cannot send files with PUT or GET, only with POST
        #~ logger.info("20120208 list POST %s",obj2str(elem,force_detailed=True))
        if rh.actor.handle_uploaded_files is not None:
            rh.actor.handle_uploaded_files(elem,request)
            file_upload = True
        else:
            file_upload = False
        return form2obj_and_save(ar,request.POST,elem,True,False,file_upload)
        #~ return form2obj_and_save(request,rh,request.POST,instance,True,ar)
      
    #~ def api_list_view(self,request,app_label=None,actor=None):
    def get(self,request,app_label=None,actor=None):
        """
        - GET : List the members of the collection. 
        - PUT : Replace the entire collection with another collection. 
        - POST : Create a new entry in the collection where the ID is assigned automatically by the collection. 
          The ID created is included as part of the data returned by this operation. 
        - DELETE : Delete the entire collection.
        
        (Source: http://en.wikipedia.org/wiki/Restful)
        """
        ui = settings.LINO.ui
        rpt = requested_report(app_label,actor)
        
        #~ action_name = request.GET.get(
        action_name = request.REQUEST.get(
            ext_requests.URL_PARAM_ACTION_NAME,
            rpt.default_list_action_name)
        a = rpt.get_url_action(action_name)
        if a is None:
            raise http.Http404("%s has no url action %r" % (rpt,action_name))
            
        ar = rpt.request(ui,request,a)
        ar.renderer = ui.ext_renderer
        rh = ar.ah
        
        #~ print 20120630, 'api_list_view'
        fmt = request.GET.get(
            ext_requests.URL_PARAM_FORMAT,
            ar.action.default_format)
      
        if fmt == ext_requests.URL_FORMAT_JSON:
            ar.renderer = ui.ext_renderer
            rows = [ rh.store.row2list(ar,row) for row in ar.sliced_data_iterator]
            #~ return json_response_kw(msg="20120124")
            #~ total_count = len(ar.data_iterator)
            total_count = ar.get_total_count()
            #~ if ar.create_rows:
            row = ar.create_phantom_row()
            if row is not None:
                d = rh.store.row2list(ar,row)
                rows.append(d)
                total_count += 1
            return json_response_kw(count=total_count,
              rows=rows,
              title=unicode(ar.get_title()),
              #~ disabled_actions=rpt.disabled_actions(ar,None),
              gc_choices=[gc.data for gc in rpt.grid_configs])
                
        if fmt == ext_requests.URL_FORMAT_HTML:
            ar.renderer = ui.ext_renderer
            after_show = ar.get_status(ui)
            if isinstance(ar.action,actions.InsertRow):
                elem = ar.create_instance()
                #~ print 20120630
                #~ print elem.national_id
                rec = elem2rec_insert(ar,rh,elem)
                after_show.update(data_record=rec)

            kw = dict(on_ready=
                ui.ext_renderer.action_call(ar.request,ar.action,after_show))
            #~ print '20110714 on_ready', params
            kw.update(title=ar.get_title())
            return http.HttpResponse(ui.html_page(request,**kw))
        
        if fmt == 'csv':
            #~ response = HttpResponse(mimetype='text/csv')
            charset = settings.LINO.csv_params.get('encoding','utf-8')
            response = http.HttpResponse(
              content_type='text/csv;charset="%s"' % charset)
            if False:
                response['Content-Disposition'] = \
                    'attachment; filename="%s.csv"' % ar.actor
            else:
                #~ response = HttpResponse(content_type='application/csv')
                response['Content-Disposition'] = \
                    'inline; filename="%s.csv"' % ar.actor
              
            #~ response['Content-Disposition'] = 'attachment; filename=%s.csv' % ar.get_base_filename()
            w = ucsv.UnicodeWriter(response,**settings.LINO.csv_params)
            w.writerow(ar.ah.store.column_names())
            for row in ar.data_iterator:
                w.writerow([unicode(v) for v in rh.store.row2list(ar,row)])
            return response
            
        #~ if fmt == ext_requests.URL_FORMAT_ODT:
            #~ if ar.get_total_count() > MAX_ROW_COUNT:
                #~ raise Exception(_("List contains more than %d rows") % MAX_ROW_COUNT)
            #~ target_parts = ['cache', 'odt', str(rpt) + '.odt']
            #~ target_file = os.path.join(settings.MEDIA_ROOT,*target_parts)
            #~ target_url = self.media_url(*target_parts)
            #~ ar.renderer = self.pdf_renderer
            #~ if os.path.exists(target_file):
                #~ os.remove(target_file)
            #~ logger.info(u"odfpy render %s -> %s",rpt,target_file)
            #~ self.table2odt(ar,target_file)
            #~ return http.HttpResponseRedirect(target_url)
        
        if fmt in (ext_requests.URL_FORMAT_PDF,ext_requests.URL_FORMAT_ODT):
            if ar.get_total_count() > MAX_ROW_COUNT:
                raise Exception(_("List contains more than %d rows") % MAX_ROW_COUNT)
        
            #~ from lino.utils.appy_pod import setup_renderer
            from lino.utils.appy_pod import Renderer
            #~ from appy.pod.renderer import Renderer
            
            tpl_leaf = "Table.odt" 
            #~ tplgroup = rpt.app_label + '/' + rpt.__name__
            tplgroup = None
            tplfile = find_config_file(tpl_leaf,tplgroup)
            if not tplfile:
                raise Exception("No file %s / %s" % (tplgroup,tpl_leaf))
                
            #~ target_parts = ['cache', 'appypdf', str(rpt) + '.odt']
            #~ target_parts = ['cache', 'appypdf', str(rpt) + '.pdf']
            target_parts = ['cache', 'appypdf', str(rpt) + '.' + fmt]
            target_file = os.path.join(settings.MEDIA_ROOT,*target_parts)
            target_url = ui.media_url(*target_parts)
            #~ ar.renderer = self.pdf_renderer
            ar.renderer = ui.ext_renderer # 20120624
            #~ body = ar.table2xhtml().toxml()
            """
            [NOTE] :doc:`/blog/2012/0211`:
            
            """
            #~ body = etree.tostring(self.table2xhtml(ar))
            #~ logger.info("20120122 body is %s",body)
            context = dict(
                ar=ar,
                title=unicode(ar.get_title()),
                #~ table_body=body,
                dtos=babel.dtos,
                dtosl=babel.dtosl,
                dtomy=babel.dtomy,
                babelattr=babel.babelattr,
                babelitem=babel.babelitem,
                tr=babel.babelitem,
                #~ iif=iif,
                settings=settings,
                #~ restify=restify,
                #~ site_config = get_site_config(),
                #~ site_config = settings.LINO.site_config,
                _ = _,
                #~ knowledge_text=fields.knowledge_text,
                )
            #~ lang = str(elem.get_print_language(self))
            if os.path.exists(target_file):
                os.remove(target_file)
            logger.info(u"appy.pod render %s -> %s (params=%s",
                tplfile,target_file,settings.LINO.appy_params)
            renderer = Renderer(tplfile, context, target_file,**settings.LINO.appy_params)
            #~ setup_renderer(renderer)
            #~ renderer.context.update(restify=debug_restify)
            renderer.run()
            return http.HttpResponseRedirect(target_url)
            
        if fmt == ext_requests.URL_FORMAT_PRINTER:
            if ar.get_total_count() > MAX_ROW_COUNT:
                raise Exception(_("List contains more than %d rows") % MAX_ROW_COUNT)
            #~ ar.renderer = self.pdf_renderer # 20120624
            ar.renderer = ui.ext_renderer
            
            if False:
                response = http.HttpResponse(content_type='text/html;charset="utf-8"')
                doc = xhg.HTML()
                doc.set_title(ar.get_title())
                t = ui.table2xhtml(ar)
                doc.add_to_body(t)
                xhg.Writer(response).render(doc)
                return response
            
            if True:
                response = http.HttpResponse(content_type='text/html;charset="utf-8"')
                doc = xghtml.Document(force_unicode(ar.get_title()))
                doc.body.append(xghtml.E.h1(doc.title))
                t = doc.add_table()
                ui.ar2html(ar,t)
                doc.write(response,encoding='utf-8')
                #~ xhg.Writer(response).render(doc)
                return response
            
            if False:
                from lxml.html import builder as html
                title = unicode(ar.get_title())
                doc = html.BODY(
                  html.HEAD(html.TITLE(title)),
                  html.BODY(
                    html.H1(title),
                    ui.table2xhtml(ar)
                  )
                )
                return http.HttpResponse(etree.tostring(doc),content_type='text/html;charset="utf-8"')
            
        raise http.Http404("Format %r not supported for GET on %s" % (fmt,rpt))

      
class GridConfig(View):

    #~ def grid_config_view(self,request,app_label=None,actor=None):
    def put(self,request,app_label=None,actor=None):
        ui = settings.LINO.ui
        rpt = actors.get_actor2(app_label,actor)
        PUT = http.QueryDict(request.raw_post_data)
        gc = dict(
          widths = [int(x) for x in PUT.getlist(ext_requests.URL_PARAM_WIDTHS)],
          columns = [str(x) for x in PUT.getlist(ext_requests.URL_PARAM_COLUMNS)],
          hiddens=[(x == 'true') for x in PUT.getlist(ext_requests.URL_PARAM_HIDDENS)],
          #~ hidden_cols=[str(x) for x in PUT.getlist('hidden_cols')],
        )
        
        filter = PUT.get('filter',None)
        if filter is not None:
            filter = json.loads(filter)
            gc['filters'] = [ext_requests.dict2kw(flt) for flt in filter]
        
        name = PUT.get('name',None)
        if name is None:
            name = ext_elems.DEFAULT_GC_NAME                 
        else:
            name = int(name)
            
        gc.update(label=PUT.get('label',"Standard"))
        try:
            msg = rpt.save_grid_config(name,gc)
        except IOError,e:
            msg = _("Error while saving GC for %(table)s: %(error)s") % dict(
                table=rpt,error=e)
            return settings.LINO.ui.error_response(None,msg)
        #~ logger.info(msg)
        settings.LINO.ui.build_site_cache(True)            
        return settings.LINO.ui.success_response(msg)
            
