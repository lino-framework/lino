## Copyright 2009 Luc Saffre

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

from urllib import urlencode

from django.http import Http404
from django.utils.safestring import mark_safe
from django.db import models
from django import template 
from django.conf.urls.defaults import patterns, url, include
from django.shortcuts import render_to_response 


def view_instance(request,db_table=None,pk=None):
    if db_table is None:
        return Http404
    from . import reports
    try:
        #rptclass = reports.model_reports[db_table]
        rpt = reports.model_reports[db_table]
    except KeyError,e:
        msg = """
        There is no Report defined for %s.
        """ % db_table
        return sorry(request,message=msg)
        
    #rpt = rptclass(filter=dict(pk__exact=pk))
    return rpt.view_one(request,1)

def unused_view_instance_slave(request,app_label=None,model_name=None,slave_name=None):
    pk = request.GET.get('master',None)
    if not pk:
        print "view_instance_slave with master=%s" % pk
        return sorry(request)
    #pk = params.master
    #print repr(pk)
    model = models.get_model(app_label,model_name)
    obj = model.objects.get(pk=pk)
    from . import reports
    rptclass = reports.get_slave(obj,slave_name)
    if not rptclass:
        print "no slave %s for model %s" % (slave,model)
        return sorry(request)
    rpt = rptclass(master_instance=obj)
    return rpt.json(request)

    
def list_view(request,app_label=None,rptname=None):
    app = models.get_app(app_label)
    rptclass = getattr(app,rptname)
    rpt = rptclass()
    return rpt.view_many(request)

def detail_view(request,app_label=None,rptname=None):
    app = models.get_app(app_label)
    rptclass = getattr(app,rptname,None)
    if rptclass is None:
        raise Http404("Application '%s' (%s) has no report '%s'" % (
          app_label, app.__file__, rptname))
    rpt = rptclass()
    return rpt.view_one(request)
    

def choices_view(request,app_label=None,model_name=None):
    model = models.get_model(app_label,model_name)
    rpt = model._lino_choices
    return rpt.view_many(request)

def field_choices_view(request,app_label=None,model_name=None,field_name=None):
    model = models.get_model(app_label,model_name)
    field = model.get_field(field)
    rpt = get_combo_report(field.rel.to)
    return rpt.view_many(request)





def sorry(request,message=None):
    if message is None:
        if request.user.is_authenticated():
            message = mark_safe("""
    Sorry %s, you have no access permission for this action.
    Consider logging in as another user.
    """ % request.user.username)
        else:
            message = mark_safe("""
    This action requires that you log in.
            """)
    from lino.django.utils.sites import lino_site
    context = lino_site.context(request,
      title = "Sorry",
      message = message,
    )
    return render_to_response("lino/sorry.html",
      context,
      context_instance = template.RequestContext(request))



def get_report_url(report,master_instance=None,
        json=False,save=False,mode=None,action=None,**kw):
    if json:
        url = "/json/"
    elif save:
        url = "/save/"
    elif action:
        url = "/action/"
    else:
        url = "/r/"
    url += report.app_label + "/" + report.name
    if action:
        url += "/" + action
    #~ app_label = report.__class__.__module__.split('.')[-2]
    #~ if mode == 'choices':
        #~ url = '/choices/%s/%s' % (app_label,report.model.__name__)
    #~ else:
        #~ url = '/%s/%s/%s' % (mode,app_label,report.__class__.__name__)
    #~ if master_instance is None:
        #~ master_instance = report.master_instance
    if master_instance is not None:
        kw['master'] = master_instance.pk
    if mode is not None:
        kw['mode'] = mode
    if len(kw):
        url += "?"+urlencode(kw)
    return url
        

def get_instance_url(o):
    if hasattr(o,'get_instance_url'):
        url = o.get_instance_url()
        if url is not None:
            return url
    return "/o/%s/%s" % (o._meta.db_table, o.pk)
        


def get_urls():
    from . import reports
    return patterns('',
        (r'^o/(?P<db_table>\w+)/(?P<pk>\w+)$', view_instance),
        #(r'^slave/(?P<app_label>\w+)/(?P<model_name>.+)/(?P<slave>.+)$', view_instance_slave),
        #(r'^r/(?P<rptname>\w+)$', reports.view_report_as_ext),
        #(r'^json/(?P<rptname>\w+)$', reports.view_report_as_json),
        #(r'^save/(?P<rptname>\w+)$', reports.view_report_save),
        (r'^r/(?P<app_label>\w+)/(?P<rptname>\w+)$', reports.view_report_as_ext),
        (r'^json/(?P<app_label>\w+)/(?P<rptname>\w+)$', reports.view_report_as_json),
        (r'^save/(?P<app_label>\w+)/(?P<rptname>\w+)$', reports.view_report_save),
        (r'^action/(?P<app_label>\w+)/(?P<rptname>\w+)/(?P<action>\w+)$', reports.view_action),
        #(r'^choices/(?P<app_label>\w+)/(?P<model_name>\w+)$', choices_view),
        #(r'^list/(?P<app_label>\w+)/(?P<rptname>\w+)$', list_view),
        #(r'^detail/(?P<app_label>\w+)/(?P<rptname>\w+)$', detail_view),
        #(r'^field_choices/(?P<app_label>.+)/(?P<model_name>.+)/(?P<field_name>.+)$', choices_view),
    )

