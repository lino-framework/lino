# -*- coding: UTF-8 -*-
## Copyright 2009-2013 Luc Saffre
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

import os
import cgi

from django import http
from django.db import models
from django.db import IntegrityError
from django.conf import settings
from django.views.generic import View
#~ from django.utils import simplejson as json
import json
from django.core import exceptions
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode

from lino import dd
#~ from lino.core.signals import pre_ui_delete

from lino.utils.xmlgen import html as xghtml
E = xghtml.E

from lino.utils.jsgen import py2js, js_code, id2js
from lino.utils import ucsv
from lino.utils import choosers
from lino.utils import isiterable
from lino.utils import dblogger
from lino.core import auth

from lino.core import actions
from lino.core import actors
from lino.core import dbtables
#~ from lino.core import changes
from lino.core import web
from lino.core.dbutils import navinfo

from lino.utils.media import TmpMediaFile


#~ from lino.ui import requests as ext_requests
from lino.core import constants as ext_requests
from . import elems as ext_elems

#~ from lino.ui.extjs3 import ext_elems

MAX_ROW_COUNT = 300



class HttpResponseDeleted(http.HttpResponse):
    status_code = 204
    

def requested_actor(app_label,actor):
    """
    Utility function which returns the requested actor, 
    either directly or (if specified name is a model) that 
    model's default table.
    """
    x = getattr(settings.SITE.modules,app_label)
    cl = getattr(x,actor)
    if not isinstance(cl,type):
        raise Exception("%s.%s is not a class" % (app_label,actor))
    if issubclass(cl,models.Model):
        return cl.get_default_table()
    if not issubclass(cl,actors.Actor):
        #~ raise http.Http404("%r is not an actor" % cl)
        raise Exception("%r is not an actor" % cl)
    return cl
    
#~ class Http403(Exception):
    #~ pass
    
def action_request(app_label,actor,request,rqdata,is_list,**kw):
    rpt = requested_actor(app_label,actor)
    action_name = rqdata.get(ext_requests.URL_PARAM_ACTION_NAME,None)
    #~ if action_name is None:
        #~ logger.info("20130731 action_name is None")
    if not action_name:
        if is_list: 
            action_name = rpt.default_list_action_name
        else:
            action_name = rpt.default_elem_action_name
    a = rpt.get_url_action(action_name)
    if a is None:
        raise http.Http404("%s has no url action %r (possible values are %s)" % (
            rpt,action_name,rpt.get_url_action_names()))
    user = request.subst_user or request.user
    if False: # 20130829
        if not a.get_view_permission(user.profile):
            raise exceptions.PermissionDenied(
                _("As %s you have no permission to run this action.") % user.profile)
            #~ return http.HttpResponseForbidden(_("As %s you have no permission to run this action.") % user.profile)
    ar = rpt.request(request=request,action=a,**kw)
    #~ ar.renderer = settings.SITE.ui.ext_renderer
    return ar
    
    
        
def json_response_kw(**kw):
    return json_response(kw)
    
def json_response(x,content_type='application/json'):
    s = py2js(x)
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
    if ar.actor.parameters:
        #~ rec.update(param_values=ar.ah.store.pv2dict(ar.ui,ar.param_values))
        rec.update(param_values=ar.actor.params_layout.params_store.pv2dict(ar.param_values))
    return rec

def elem2rec_detailed(ar,elem,**rec):
    """
    Adds additional information for this record, used only by detail views.
    
    The "navigation information" is a set of pointers to the next, previous, 
    first and last record relative to this record in this report. 
    (This information can be relatively expensive for records that are towards 
    the end of the report. 
    See `/blog/2010/0716`,
    `/blog/2010/0721`,
    `/blog/2010/1116`,
    `/blog/2010/1207`.)
    
    recno 0 means "the requested element exists but is not contained in the requested queryset".
    This can happen after changing the quick filter (search_change) of a detail view.
    
    """
    rh = ar.ah
    rec = elem2rec1(ar,rh,elem,**rec)
    if ar.actor.hide_top_toolbar:
        rec.update(title=unicode(elem))
    else:
        #~ print(ar.get_title())
        #~ print(dd.obj2str(elem))
        #~ print(repr(unicode(elem)))
        rec.update(title=ar.get_title() + u" » " + unicode(elem))
    rec.update(id=elem.pk)
    rec.update(disable_delete=rh.actor.disable_delete(elem,ar))
    if rh.actor.show_detail_navigator:
        rec.update(navinfo=navinfo(ar.data_iterator,elem))
    return rec
            



def delete_element(ar,elem):
    assert elem is not None
    msg = ar.actor.disable_delete(elem,ar)
    if msg is not None:
        rv = ar.error(None,msg,alert=True)
        return settings.SITE.ui.render_action_response(rv)
            
    #~ dblogger.log_deleted(ar.request,elem)
    
    #~ changes.log_delete(ar.request,elem)
    
    dd.pre_ui_delete.send(sender=elem,request=ar.request)
    
    try:
        elem.delete()
    except Exception,e:
        dblogger.exception(e)
        msg = _("Failed to delete %(record)s : %(error)s."
            ) % dict(record=dd.obj2unicode(elem),error=e)
        #~ msg = "Failed to delete %s." % element_name(elem)
        rv = ar.error(None,msg)
        return settings.SITE.ui.render_action_response(rv)
        #~ raise Http404(msg)
        
    
    return HttpResponseDeleted()
    
#CATCHED_AJAX_EXCEPTIONS = (Warning,IntegrityError,exceptions.ValidationError)
CATCHED_AJAX_EXCEPTIONS = (Warning,exceptions.ValidationError)

def ajax_error(e,rh,**kw):
    """
    Utility function that converts a catched exception 
    to a user-friendly error message.
    """
    if isinstance(e,exceptions.ValidationError):
        def fieldlabel(name):
            de = rh.actor.get_data_elem(name)
            #~ print 20130423, de
            return force_unicode(getattr(de,'verbose_name',name))
        #~ logger.info("20130418 ajax_error(%s",e.messages)
        #~ if isinstance(e.messages,dict):
        md = getattr(e,'message_dict',None)
        if md is not None:
            e = '<br>'.join(["%s : %s" % (fieldlabel(k),v) for k,v in md.items()])
        else:
            e = '<br>'.join(e.messages)
    kw = settings.SITE.ui.error(e,alert=True,**kw)
    return json_response(kw)

#~ def form2obj_and_save(self,request,rh,data,elem,is_new,include_rows): # **kw2save):
def form2obj_and_save(ar,data,elem,is_new,restful,file_upload=False): # **kw2save):
    """
    Parses the data from HttpRequest to the model instance and saves it.
    """
    #~ self = settings.SITE.ui
    request = ar.request
    rh = ar.ah
    #~ logger.info('20130321 form2obj_and_save %r', data)
    #~ print 'form2obj_and_save %r' % data
    
    #~ logger.info('20130418 before calling store.form2obj , elem is %s' % dd.obj2str(elem))
    # store normal form data (POST or PUT)
    #~ original_state = dict(elem.__dict__)
    if not is_new:
        watcher = dd.ChangeWatcher(elem)
    try:
        rh.store.form2obj(ar,data,elem,is_new)
        elem.full_clean()
    except CATCHED_AJAX_EXCEPTIONS as e:
        return ajax_error(e,rh)
        
    kw = dict(success=True)
    
    #~ except exceptions.ValidationError, e:
        #~ kw = settings.SITE.ui.error(e) 
        #~ return json_response(kw)
    
    #~ dirty = False
    #~ missing = object()
    #~ for k, v in original_state.iteritems():
        #~ if v != elem.__dict__.get(k, missing):
            #~ dirty = True
    #~ if not dirty:
    if is_new or watcher.is_dirty():
      
        elem.before_ui_save(ar)
        
        #~ if not is_new:
            #~ dblogger.log_changes(request,elem)
            
            
        kw2save = {}
        if is_new:
            kw2save.update(force_insert=True)
        else:
            kw2save.update(force_update=True)
            
        try:
            elem.save(**kw2save)
        except CATCHED_AJAX_EXCEPTIONS,e:
            return ajax_error(e,rh)
            #~ return views.json_response_kw(success=False,
                  #~ msg=_("There was a problem while saving your data:\n%s") % e)
                  
        if is_new:
            dd.pre_ui_create.send(elem,request=request)
            #~ changes.log_create(request,elem)
            kw.update(
                message=_("%s has been created.") % dd.obj2unicode(elem))
                #~ record_id=elem.pk)
        else:
            watcher.send_update(request)
            #~ watcher.log_diff(request)
            kw.update(message=_("%s has been updated.") % dd.obj2unicode(elem))
        
    else:
    
        kw.update(message=_("%s : nothing to save.") % dd.obj2unicode(elem))
        
    kw = elem.after_ui_save(ar,**kw)
        
    if restful:
        # restful mode (used only for Ext.ensible) needs list_fields, not detail_fields
        kw.update(rows=[rh.store.row2dict(ar,elem,rh.store.list_fields)])
    elif file_upload:
        kw.update(record_id=elem.pk)
        return json_response(kw,content_type='text/html')
    else: # 20120814 
        #~ logger.info("20120816 %r", ar.action)
        #~ if isinstance(ar.bound_action.action,actions.GridEdit):
        #~ if ar.bound_action.action.action_name in ('put','post'): # grid.on_afteredit
            #~ kw.update(rows=[rh.store.row2list(ar,elem)])
        #~ else:
            #~ kw.update(data_record=elem2rec_detailed(ar,elem))
        """
        TODO: in fact we need *either* `rows` (when this was called from a Grid) 
        *or* `data_record` (when this was called from a form). 
        But how to find out which one is needed?
        """
        kw.update(rows=[rh.store.row2list(ar,elem)])
        kw.update(data_record=elem2rec_detailed(ar,elem))
    #~ logger.info("20120208 form2obj_and_save --> %r",kw)
    return json_response(kw)
            





        

class AdminIndex(View):
    """
    Similar to PlainIndex
    """
    def get(self, request, *args, **kw):
        #~ logger.info("20130719 AdminIndex")
        settings.SITE.startup()
        ui = settings.SITE.ui
        if settings.SITE.user_model is not None:
            user = request.subst_user or request.user
            a = settings.SITE.get_main_action(user)
            if a is not None and a.get_view_permission(user.profile):
                kw.update(on_ready=ui.ext_renderer.action_call(request,a,{}))
        return http.HttpResponse(ui.ext_renderer.html_page(request,**kw))

class MainHtml(View):
    def get(self, request, *args, **kw):
        #~ logger.info("20130719 MainHtml")
        settings.SITE.startup()
        ui = settings.SITE.ui
        rv = ui.success(html=settings.SITE.get_main_html(request))
        return ui.render_action_response(rv)
        
class Authenticate(View):
    """
    This view is being used only when not remote http auth
    """
  
    def get(self, request, *args, **kw):
        action_name = request.GET.get(ext_requests.URL_PARAM_ACTION_NAME)
        if action_name == 'logout':
            username = request.session.pop('username',None)
            request.session.pop('password',None)
            #~ username = request.session['username']
            #~ del request.session['password']
            rv = dict(success=True,message="User %r logged out." % username)
            return settings.SITE.ui.render_action_response(rv)
        raise http.Http404()
            

    def post(self, request, *args, **kw):
        #~ from lino.core import auth
        #~ from django.contrib.sessions.backends.db import SessionStore
        #~ ss = SessionStore()
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username,password)
        if user is None:
            rv = settings.SITE.ui.error("Could not authenticate %r" % username)
            return settings.SITE.ui.render_action_response(rv)
        request.session['username'] = username
        request.session['password'] = password
        #~ request.session['password'] = request.GET.get('password')
        #~ auth.login(request,request.GET.get('username'), request.GET.get('password'))
        #~ ss.save()
        #~ logger.info("20130924 Now logged in as %r" % username)
        rv = settings.SITE.ui.success("Now logged in as %r" % username)
        return settings.SITE.ui.render_action_response(rv)
      

class RunJasmine(View):
    """
    """
    def get(self, request, *args, **kw):
        ui = settings.SITE.ui
        return http.HttpResponse(ui.ext_renderer.html_page(request,run_jasmine=True))

class EidAppletService(View):
    """
    """
    def post(self, request, *args, **kw):
        ui = settings.SITE.ui
        return ui.success(html='Hallo?')


class Callbacks(View):
    def get(self,request,thread_id,button_id):
        return settings.SITE.ui.callback_get(request,thread_id,button_id)
        


#~ if settings.SITE.user_model:
if settings.SITE.user_model and settings.SITE.use_tinymce:
  
    from jinja2 import Template as JinjaTemplate
    TextFieldTemplate = settings.SITE.modules.system.TextFieldTemplate

    class Templates(View):
      """
      Called by TinyMCE (`template_external_list_url 
      <http://www.tinymce.com/wiki.php/configuration:external_template_list_url>`_)
      to fill the list of available templates.
      
      """
      #~ def templates_view(self,request,
      def get(self,request,
          app_label=None,actor=None,pk=None,fldname=None,tplname=None,**kw):
        
          
          if request.method == 'GET':
            
              rpt = requested_actor(app_label,actor)
              elem = rpt.get_row_by_pk(pk)
              if elem is None:
                  raise http.Http404("%s %s does not exist." % (rpt,pk))
                  
              if tplname:
                  tft = TextFieldTemplate.objects.get(pk=int(tplname))
                  if settings.SITE.trusted_templates:
                      #~ return http.HttpResponse(tft.text)
                      template = JinjaTemplate(tft.text)
                      context = dict(request=request,instance=elem,**settings.SITE.modules)
                      return http.HttpResponse(template.render(**context))
                  else:
                      return http.HttpResponse(tft.text)
                  
                  
              #~ q = models.Q(user=request.user) | models.Q(user__group__in=request.user.group_set.all())
              teams = [o.group for o in request.user.users_membership_set_by_user.all()]
              flt = models.Q(team__isnull=True) | models.Q(team__in=teams)
              qs = TextFieldTemplate.objects.filter(flt).order_by('name')
                  
              #~ m = getattr(elem,"%s_templates" % fldname,None)
              #~ if m is None:
                  #~ q = models.Q(user=request.user) | models.Q(user=None)
                  #~ qs = TextFieldTemplate.objects.filter(q).order_by('name')
              #~ else:
                  #~ qs = m(request)
                  
              templates = []
              for obj in qs:
                  url = settings.SITE.build_admin_url('templates',
                      app_label,actor,pk,fldname,unicode(obj.pk))
                  templates.append([
                      unicode(obj.name),url,unicode(obj.description)])
              js = "var tinyMCETemplateList = %s;" % py2js(templates)
              return http.HttpResponse(js,content_type='text/json')
          raise http.Http404("Method %r not supported" % request.method)



def choices_for_field(request,actor,field):
    """
    Return the choices for the given field and the given web request 
    (whose requesting actor has already been identified and is given 
    as `actor`).
    """
    #~ logger.info("20120202 %r",field)
    chooser = choosers.get_for_field(field)
    if chooser:
        #~ logger.info('20120710 choices_view() : has chooser')
        qs = chooser.get_request_choices(request,actor)
        #~ qs = list(chooser.get_request_choices(ar,actor))
        #~ logger.info("20120213 %s",qs)
        #~ if qs is None:
            #~ qs = []
        assert isiterable(qs), \
              "%s.%s_choices() returned %r which is not iterable." % (
              actor.model,field.name,qs)
        if chooser.simple_values:
            def row2dict(obj,d):
                d[ext_requests.CHOICES_TEXT_FIELD] = unicode(obj)
                d[ext_requests.CHOICES_VALUE_FIELD] = obj
                return d
        elif chooser.instance_values:
            # same code as for ForeignKey
            def row2dict(obj,d):
                #~ d[ext_requests.CHOICES_TEXT_FIELD] = obj.get_choices_text(request,actor,field)
                d[ext_requests.CHOICES_TEXT_FIELD] = actor.get_choices_text(obj,request,field)
                d[ext_requests.CHOICES_VALUE_FIELD] = obj.pk
                return d
        else: # values are (value,text) tuples
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
                #~ d[ext_requests.CHOICES_TEXT_FIELD] = obj.get_choices_text(request,actor,field)
                d[ext_requests.CHOICES_TEXT_FIELD] = actor.get_choices_text(obj,request,field)
                d[ext_requests.CHOICES_VALUE_FIELD] = unicode(obj)
            return d
        
    elif isinstance(field,models.ForeignKey):
        m = field.rel.to
        #~ t = getattr(m,'_lino_choices_table',m.get_default_table())
        t = m.get_default_table()
        qs = t.request(request=request).data_iterator
        #~ logger.info('20120710 choices_view(FK) %s --> %s',t,qs)
        def row2dict(obj,d):
            #~ d[ext_requests.CHOICES_TEXT_FIELD] = obj.get_choices_text(request,actor,field)
            d[ext_requests.CHOICES_TEXT_FIELD] = actor.get_choices_text(obj,request,field)
            d[ext_requests.CHOICES_VALUE_FIELD] = obj.pk 
            return d
    else:
        raise http.Http404("No choices for %s" % fldname)
    return (qs,row2dict)
        

def choices_response(request,qs,row2dict,emptyValue):
    quick_search = request.GET.get(ext_requests.URL_PARAM_FILTER,None)
    if quick_search is not None:
        qs = dbtables.add_quick_search_filter(qs,quick_search)
        
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
    if emptyValue is not None: # 20121203
        empty = dict()
        empty[ext_requests.CHOICES_TEXT_FIELD] = emptyValue
        empty[ext_requests.CHOICES_VALUE_FIELD] = None
        rows.insert(0,empty)
    return json_response_kw(count=count,rows=rows) 
    #~ return json_response_kw(count=len(rows),rows=rows) 
    #~ return json_response_kw(count=len(rows),rows=rows,title=_('Choices for %s') % fldname)




  
class ActionParamChoices(View):
  
    def get(self,request,app_label=None,actor=None,an=None,field=None,**kw):
        actor = requested_actor(app_label,actor)
        ba = actor.get_url_action(an)
        if ba is None:
            raise Exception("Unknown action %r for %s" % (an,actor))
        field = ba.action.get_param_elem(field)
        qs, row2dict = choices_for_field(request,actor,field)
        if field.blank:
            emptyValue = '<br/>'
        else:
            emptyValue = None
        return choices_response(request,qs,row2dict,emptyValue)
      
class Choices(View):
  
    #~ def choices_view(self,request,app_label=None,rptname=None,fldname=None,**kw):
    def get(self,request,app_label=None,rptname=None,fldname=None,**kw):
        """
        Return a JSON object with two attributes `count` and `rows`,
        where `rows` is a list of `(display_text,value)` tuples.
        Used by ComboBoxes or similar widgets.
        If `fldname` is not specified, returns the choices for 
        the `record_selector` widget.
        """
        rpt = requested_actor(app_label,rptname)
        emptyValue = None
        if fldname is None:
            ar = rpt.request(request=request) # ,rpt.default_action)
            #~ rh = rpt.get_handle(self)
            #~ ar = ViewReportRequest(request,rh,rpt.default_action)
            #~ ar = dbtables.TableRequest(self,rpt,request,rpt.default_action)
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
            if field.blank:
                #~ logger.info("views.Choices: %r is blank",field)
                emptyValue = '<br/>'
            qs, row2dict = choices_for_field(request,rpt,field)
            
        return choices_response(request,qs,row2dict,emptyValue)
        
  
class Restful(View):
    """
    Used to collaborate with a restful Ext.data.Store.
    """
  
    def post(self,request,app_label=None,actor=None,pk=None):
        #~ ui = settings.SITE.ui
        rpt = requested_actor(app_label,actor)
        if pk is None:
            elem = None
        else:
            elem = rpt.get_row_by_pk(pk)
        ar = rpt.request(request=request)
            
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
        #~ ui = settings.SITE.ui
        rpt = requested_actor(app_label,actor)
        #~ a = rpt.default_action
        elem = rpt.get_row_by_pk(pk)
        ar = rpt.request(request=request)
        return delete_element(ar,elem)
      
    def get(self,request,app_label=None,actor=None,pk=None):
        #~ ui = settings.SITE.ui
        rpt = requested_actor(app_label,actor)
        #~ a = rpt.default_action
        assert pk is None, 20120814
        #~ if pk is None:
            #~ elem = None
        #~ else:
            #~ elem = rpt.get_row_by_pk(pk)
        ar = rpt.request(request=request)
        rh = ar.ah
        rows = [ 
          rh.store.row2dict(ar,row,rh.store.list_fields) 
            for row in ar.sliced_data_iterator ]
        kw = dict(count=ar.get_total_count(),rows=rows)
        kw.update(title=unicode(ar.get_title()))
        return json_response(kw)
        
    def put(self,request,app_label=None,actor=None,pk=None):
        #~ ui = settings.SITE.ui
        rpt = requested_actor(app_label,actor)
        #~ a = rpt.default_action
        elem = rpt.get_row_by_pk(pk)
        ar = rpt.request(request=request)
        rh = ar.ah
            
        data = http.QueryDict(request.body).get('rows') # raw_post_data before Django 1.4
        data = json.loads(data)
        a = rpt.get_url_action(rpt.default_list_action_name)
        ar = rpt.request(request=request,action=a)
        ar.renderer = settings.SITE.ui.ext_renderer
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
        ui = settings.SITE.ui
        rpt = requested_actor(app_label,actor)
        #~ if not ah.actor.can_view.passes(request.user):
            #~ msg = "User %s cannot view %s." % (request.user,ah.actor)
            #~ return http.HttpResponseForbidden()
        
        action_name = request.GET.get(ext_requests.URL_PARAM_ACTION_NAME,
          rpt.default_elem_action_name)
        ba = rpt.get_url_action(action_name)
        if ba is None:
            raise http.Http404("%s has no action %r" % (rpt,action_name))
            
        ar = ba.request(request=request)
        ar.renderer = ui.ext_renderer
        ah = ar.ah
        
        if pk and pk != '-99999' and pk != '-99998':
            elem = rpt.get_row_by_pk(pk)
            if elem is None:
                raise http.Http404("%s has no row with primary key %r" % (rpt,pk))
                #~ raise Exception("20120327 %s.get_row_by_pk(%r)" % (rpt,pk))
            ar.selected_rows = [elem]
        else:
            elem = None
        
        
        fmt = request.GET.get(ext_requests.URL_PARAM_FORMAT,ba.action.default_format)

        #~ if isinstance(a,actions.OpenWindowAction):
        if ba.action.opens_a_window:
          
            if fmt == ext_requests.URL_FORMAT_JSON:
                if pk == '-99999':
                    elem = ar.create_instance()
                    datarec = elem2rec_insert(ar,ah,elem)
                elif pk == '-99998':
                    elem = ar.create_instance()
                    datarec = elem2rec_empty(ar,ah,elem)
                else:
                    datarec = elem2rec_detailed(ar,elem)
                
                return json_response(datarec)
                
            after_show = ar.get_status(record_id=pk)
            
            tab = request.GET.get(ext_requests.URL_PARAM_TAB,None)
            if tab is not None: 
                tab = int(tab)
                after_show.update(active_tab=tab)
            
            return http.HttpResponse(ui.ext_renderer.html_page(request,ba.action.label,
              on_ready=ui.ext_renderer.action_call(request,ba,after_show)))
            
        if isinstance(ba.action,actions.RedirectAction):
            target = ba.action.get_target_url(elem)
            if target is None:
                raise http.Http404("%s failed for %r" % (ba,elem))
            return http.HttpResponseRedirect(target)
            
        if pk == '-99998':
            assert elem is None
            elem = ar.create_instance()
            ar.selected_rows = [elem]

        return settings.SITE.ui.run_action(ar)
                
        
    def post(self,request,app_label=None,actor=None,pk=None):
        ar = action_request(app_label,actor,request,request.POST,True)
        ar.renderer = settings.SITE.ui.ext_renderer
        elem = ar.actor.get_row_by_pk(pk)
        if elem is None:
            raise http.Http404("%s has no row with primary key %r" % (ar.actor,pk))
        if pk == '-99998':
            assert elem is None
            elem = ar.create_instance()
        ar.selected_rows = [elem]
        return settings.SITE.ui.run_action(ar)
        
    def put(self,request,app_label=None,actor=None,pk=None):
        data = http.QueryDict(request.body) # raw_post_data before Django 1.4
        ar = action_request(app_label,actor,request,data,False)
        ar.renderer = settings.SITE.ui.ext_renderer
        elem = ar.actor.get_row_by_pk(pk)
        if elem is None:
            raise http.Http404("%s has no row with primary key %r" % (actor,pk))
        return form2obj_and_save(ar,data,elem,False,False) # force_update=True)
            
    def delete(self,request,app_label=None,actor=None,pk=None):
        #~ ui = settings.SITE.ui
        rpt = requested_actor(app_label,actor)
        elem = rpt.get_row_by_pk(pk)
        if elem is None:
            raise http.Http404("%s has no row with primary key %r" % (rpt,pk))
        ar = rpt.request(request=request)
        return delete_element(ar,elem)


        
  
class ApiList(View):
    """
    - GET : List the members of the collection. 
    - PUT : Replace the entire collection with another collection. 
    - POST : Create a new entry in the collection where the ID is assigned automatically by the collection. 
      The ID created is included as part of the data returned by this operation. 
    - DELETE : Delete the entire collection.
    
    (Source: http://en.wikipedia.org/wiki/Restful)
    """

    def post(self,request,app_label=None,actor=None):
        #~ ui = settings.SITE.ui
        #~ rpt = requested_actor(app_label,actor)
        
        #~ action_name = request.POST.get(
            #~ ext_requests.URL_PARAM_ACTION_NAME,
            #~ rpt.default_list_action_name)
        #~ a = rpt.get_url_action(action_name)
        #~ if a is None:
            #~ raise http.Http404("%s has no url action %r" % (rpt,action_name))
        #~ ar = rpt.request(ui,request,a)
        
        ar = action_request(app_label,actor,request,request.POST,True)
        ar.renderer = settings.SITE.ui.ext_renderer
        #~ print 20121116, ar.bound_action.action.action_name
        if ar.bound_action.action.action_name in ['duplicate','post','poststay','insert']:
            rh = ar.ah
            elem = ar.create_instance()
            if rh.actor.handle_uploaded_files is not None:
                rh.actor.handle_uploaded_files(elem,request)
                file_upload = True
            else:
                file_upload = False
            return form2obj_and_save(ar,request.POST,elem,True,False,file_upload)
        return settings.SITE.ui.run_action(ar)
      
    def get(self,request,app_label=None,actor=None):
        #~ ar = action_request(app_label,actor,request,request.GET,limit=PLAIN_PAGE_LENGTH)
        ar = action_request(app_label,actor,request,request.GET,True)
        ar.renderer = settings.SITE.ui.ext_renderer
        rh = ar.ah
        
        #~ print 20120630, 'api_list_view'
        fmt = request.GET.get(
            ext_requests.URL_PARAM_FORMAT,
            ar.bound_action.action.default_format)
            
        #~ logger.info("20121203 views.ApiList.get() %s",ar.bound_action.full_name())
      
        if fmt == ext_requests.URL_FORMAT_JSON:
            #~ ar.renderer = ui.ext_renderer
            rows = [ rh.store.row2list(ar,row) for row in ar.sliced_data_iterator]
            #~ return json_response_kw(msg="20120124")
            #~ total_count = len(ar.data_iterator)
            total_count = ar.get_total_count()
            #~ if ar.create_rows:
            for row in ar.create_phantom_rows():
                d = rh.store.row2list(ar,row)
                rows.append(d)
                total_count += 1
            #~ 20120918
            kw = dict(count=total_count,
              rows=rows,
              success=True,
              no_data_text=ar.no_data_text, 
              #~ status=ar.get_status(ar.ui),
              title=unicode(ar.get_title()))
              #~ disabled_actions=rpt.disabled_actions(ar,None),
              #~ gc_choices=[gc.data for gc in ar.actor.grid_configs])
            if ar.actor.parameters:
                #~ kw.update(param_values=ar.actor.params_layout.params_store.pv2dict(settings.SITE.ui,ar.param_values))
                kw.update(param_values=ar.actor.params_layout.params_store.pv2dict(ar.param_values))
            return json_response(kw) 
                
        if fmt == ext_requests.URL_FORMAT_HTML:
            #~ ar.renderer = ui.ext_renderer
            #~ after_show = ar.get_status(ar.ui)
            after_show = ar.get_status()
            
            sp = request.GET.get(ext_requests.URL_PARAM_SHOW_PARAMS_PANEL,None)
            if sp is not None: 
                #~ after_show.update(show_params_panel=sp)
                after_show.update(show_params_panel=ext_requests.parse_boolean(sp))
            
            
            if isinstance(ar.bound_action.action,actions.InsertRow):
                elem = ar.create_instance()
                #~ print 20120630
                #~ print elem.national_id
                rec = elem2rec_insert(ar,rh,elem)
                after_show.update(data_record=rec)

            kw = dict(on_ready=
                ar.renderer.action_call(ar.request,ar.bound_action,after_show))
                #~ ui.ext_renderer.action_call(ar.request,ar.action,after_show))
            #~ print '20110714 on_ready', params
            kw.update(title=ar.get_title())
            return http.HttpResponse(ar.renderer.html_page(request,**kw))
        
        if fmt == 'csv':
            #~ response = HttpResponse(mimetype='text/csv')
            charset = settings.SITE.csv_params.get('encoding','utf-8')
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
            w = ucsv.UnicodeWriter(response,**settings.SITE.csv_params)
            w.writerow(ar.ah.store.column_names())
            if True: # 20130418 : also column headers, not only internal names
                column_names = None
                fields, headers, cellwidths = ar.get_field_info(column_names)
                w.writerow(headers)
                
            for row in ar.data_iterator:
                w.writerow([unicode(v) for v in rh.store.row2list(ar,row)])
            return response
            
        #~ if fmt in (ext_requests.URL_FORMAT_PDF,ext_requests.URL_FORMAT_ODT):
            #~ mf = TmpMediaFile(ar,fmt)
            #~ settings.SITE.makedirs_if_missing(os.path.dirname(mf.name))
            #~ ar.appy_render(mf.name)
            #~ return http.HttpResponseRedirect(mf.url)
            
        if fmt == ext_requests.URL_FORMAT_PRINTER:
            if ar.get_total_count() > MAX_ROW_COUNT:
                raise Exception(_("List contains more than %d rows") % MAX_ROW_COUNT)
            #~ ar.renderer = ui.ext_renderer
            response = http.HttpResponse(content_type='text/html;charset="utf-8"')
            doc = xghtml.Document(force_unicode(ar.get_title()))
            doc.body.append(E.h1(doc.title))
            t = doc.add_table()
            #~ settings.SITE.ui.ar2html(ar,t,ar.data_iterator)
            ar.dump2html(t,ar.data_iterator)
            doc.write(response,encoding='utf-8')
            return response
            
        return settings.SITE.ui.run_action(ar)
        #~ raise http.Http404("Format %r not supported for GET on %s" % (fmt,ar.actor))

      
class GridConfig(View):

    #~ def grid_config_view(self,request,app_label=None,actor=None):
    def put(self,request,app_label=None,actor=None):
        ui = settings.SITE.ui
        rpt = requested_actor(app_label,actor)
        #~ rpt = actors.get_actor2(app_label,actor)
        PUT = http.QueryDict(request.body) # raw_post_data before Django 1.4
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
            return settings.SITE.ui.error(None,msg,alert=True)
        #~ logger.info(msg)
        settings.SITE.ui.ext_renderer.build_site_cache(True)
        return settings.SITE.ui.success(msg)
        
MENUS = dict()        


def plain_response(ui,request,tplname,context):        
    u = request.subst_user or request.user
    menu = MENUS.get(u.profile,None)
    if menu is None:
        menu = settings.SITE.get_site_menu(ui,u.profile)
        url = settings.SITE.plain_prefix + '/'
        menu.add_url_button(url,label=_("Home"))
        menu = menu.as_html(ui,request)
        menu = E.tostring(menu)
        MENUS[u.profile] = menu
    context.update(menu=menu,E=E)
    web.extend_context(context)
    template = settings.SITE.jinja_env.get_template(tplname)
    
    response = http.HttpResponse(
        template.render(**context),
        content_type='text/html;charset="utf-8"')
    
    return response
            


class PlainList(View):
  
    def get(self,request,app_label=None,actor=None):
        ar = action_request(app_label,actor,request,request.GET,True)
        ar.renderer = settings.SITE.ui.plain_renderer
        context = dict(
          title=ar.get_title(),
          heading=ar.get_title(),
          #~ tbar = buttons,
          main=ar.as_html(),
        )
        return plain_response(settings.SITE.ui,request,'table.html',context)
        
        

class PlainElement(View):
    """
    Render a single record from :class:`lino.ui.PlainRenderer`.
    """
    def get(self,request,app_label=None,actor=None,pk=None):
        """
        GET : Retrieve a representation of the addressed member of the collection expressed in an appropriate MIME type.
        PUT : Update the addressed member of the collection or create it with the specified ID. 
        POST : Treats the addressed member as a collection and creates a new subordinate of it. 
        DELETE : Delete the addressed member of the collection. 
        
        (Source: http://en.wikipedia.org/wiki/Restful)
        """
        ui = settings.SITE.ui
        ar = action_request(app_label,actor,request,request.GET,False)
        ar.renderer = ui.plain_renderer
        
        context = dict(
          title=ar.get_action_title(),
          #~ menu = E.tostring(menu),
          #~ tbar = buttons,
          main = ar.as_html(pk),
        )
        #~ template = web.jinja_env.get_template('detail.html')
        
        return plain_response(ui,request,'detail.html',context)
        
        
class PlainIndex(View):
    """
    This is not a docstring
    Similar to AdminIndex
    """
    def get(self, request, *args, **kw):
        ui = settings.SITE.ui
        context = dict(
          title = settings.SITE.title,
          main = '',
        )
        if settings.SITE.user_model is not None:
            user = request.subst_user or request.user
        else:
            user = auth.AnonymousUser.instance()
        a = settings.SITE.get_main_action(user)
        if a is not None:
            if not a.get_view_permission(user.profile):
                raise exceptions.PermissionDenied("Action not allowed for %s" % user)
            kw.update(renderer=ui.plain_renderer)
            ar = a.request(request=request,**kw)
            #~ ar.renderer = ui.plain_renderer
            context.update(title=ar.get_title())
            # TODO: let ar generate main
            # context.update(main=ui.plain_renderer.action_call(request,a,{}))
        return plain_response(ui,request,'plain_index.html',context)
