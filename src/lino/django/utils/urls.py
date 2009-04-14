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


from django.conf import settings
from django.db import models
from django.forms.models import modelform_factory
from django.shortcuts import render_to_response 
from django.conf.urls.defaults import patterns, url, include

from lino.django.utils import layouts

    
def index(request):
    context=dict(
      main_menu=settings.MAIN_MENU,
      title="foo"
    )
    return render_to_response("tom/index.html",context)
    
#~ def edit_report(request,name,*args,**kw):
    #~ rptclass = _report_classes[name]
    #~ rpt = rptclass(*args,**kw)
    #~ return rpt.view(request)
    

    
def view_instance(request,app,model,pk):
    model_class = models.get_model(app,model)
    #print model_class
    obj = model_class.objects.get(pk=pk)
    form_class = modelform_factory(model_class)
    if request.method == 'POST':
        frm=form_class(request.POST,instance=obj)
        if frm.is_valid():
            frm.save()
    else:
        frm=form_class(instance=obj)
    
    context=dict(
      title=unicode(obj),
      form=frm,
      main_menu = settings.MAIN_MENU,
      layout = layouts.LayoutRenderer(obj.page_layout(),frm,
        editing=True),
    )
    return render_to_response("tom/instance.html",context)
    
def view_instance_method(request,app,model,pk,meth):
    model_class = models.get_model(app,model)
    obj = model_class.objects.get(pk=pk)
    m = getattr(obj,meth)
    #action_dict = obj.get_actions()
    #m = action_dict[meth_name]
    actor = m()
    return actor.view(request)
    
def urls(name=''):
    l=[url(r'^%s$' % name, index)]
    l.append(
      url(r'^instance/(?P<app>\w+)/(?P<model>\w+)/(?P<pk>\w+)$',
          view_instance))
    l.append(
      url(r'^instance/(?P<app>\w+)/(?P<model>\w+)/(?P<pk>\w+)/(?P<meth>\w+)$',
          view_instance_method))
    return patterns('',*l)

