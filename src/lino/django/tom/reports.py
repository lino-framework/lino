## Copyright 2003-2009 Luc Saffre

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



from django.db import models
from django import forms
#from django.forms.models import ModelForm,ModelFormMetaclass, BaseModelFormSet
from django.conf.urls.defaults import patterns, url, include
#from django.shortcuts import render_to_response 
#from django.core.paginator import Paginator, EmptyPage, InvalidPage
#from django.http import HttpResponse, HttpResponseRedirect, Http404
#from django.utils.safestring import mark_safe
#from django.template.loader import render_to_string, get_template, select_template, Context

# l:\snapshot\xhtml2pdf
#import ho.pisa as pisa

#from lino.reports.constants import *
#import EditLayoutRenderer, ShowLayoutRenderer
from lino.django.tom import render


#~ from django import template

#~ register = template.Library()


# maps Django field types to a tuple of default paramenters
# each tuple contains: minWidth, maxWidth, is_filter
WIDTHS = {
    models.IntegerField : (2,10,False),
    models.CharField : (10,50,True),
    models.TextField :  (10,50,True),
    models.BooleanField : (10,10,True),
    models.ForeignKey : (5,40,False),
    models.AutoField : (2,10,False),
}



#~ def request_again(request,*args,**kw):
    #~ req=request.GET.copy()
    #~ for k,v in kw.items():
        #~ req[k] = v
    #~ pth=request.path
    #~ if len(args):
        #~ pth += "/" + "/".join(args)
    #~ s=req.urlencode()
    #~ if len(s):
        #~ pth += "?" + s
    #~ return mark_safe(pth)
    
    
    
        


class ReportParameterForm(forms.Form):
    #~ pgn = forms.IntegerField(required=False,label="Page number") 
    #~ pgl = forms.IntegerField(required=False,label="Rows per page")
    flt = forms.CharField(required=False,label="Text filter")
    #~ fmt = forms.ChoiceField(required=False,label="Format",choices=(
      #~ ( 'form', "editable form" ),
      #~ ( 'show', "read-only display" ),
      #~ ( 'text', "plain text" ),
    #~ ))
    

#        
#  Report
#        

#~ _report_classes = {}

#~ def get_report(name):
    #~ return _report_classes[name]
    
#~ def get_reports():
    #~ return _report_classes

#~ class ReportMetaClass(type):
    #~ def __new__(meta, classname, bases, classDict):
        #~ #print 'Class Name:', classname
        #~ #print 'Bases:', bases
        #~ #print 'Class Attributes', classDict
        #~ cls = type.__new__(meta, classname, bases, classDict)
        #~ _report_classes[classname] = cls
        #~ return cls




class Report(object):
  
    #~ __metaclass__ = ReportMetaClass
    
    queryset = None 
    title = None
    #width = None
    #columnWidths = None
    columnNames = None
    #rowHeight = None
    label = None
    param_form = ReportParameterForm
    default_filter=''
    #default_format='form'
    #editable=True
    name=None
    #path=None
    
    def __init__(self):
        self.groups = [] # for later
        self.totals = [] # for later
        if self.label is None:
            self.label = self.__class__.__name__
        if self.name is None:
            self.name = self.__class__.__name__.lower()
        #~ if self.title is None:
            #~ self.title = self.build_title()
        if self.queryset is None:
            self.queryset = self.get_queryset()
        
        
    def get_title(self):
        #~ if self.title is None:
            #~ return self.label
        return self.title or self.label
        
    def getLabel(self):
        return self.label
    
    def header_layout(self):
        pass
        
        
    def __unicode__(self):
        #return unicode(self.as_text())
        return unicode("%d row(s)" % self.queryset.count())
    
    def get_urls(self,name):
        #assert self.path is None, "you tried to install this Report instance to more than 1 url"
        #self.path = "/" + name
        l = []
        #l += [ url(r'^%s/edit$' % name, self.as_form) ]
        #l += [ url(r'^%s/text$' % name, self.as_text) ]
        #l += [ url(r'^%s/show$' % name, self.as_show) ]
        #l += [ url(r'^%s$' % name, self.view) ]
        #l += [ url(r'^%s' % name, self.view) ]
        #l += [ url(r'^%s$' % name, self.as_show) ]
        #~ l += [ url(r'^%s$' % name, ViewReportRenderer(self,name).view)]
        #~ l += [ url(r'^%s/edit$' % name, FormReportRenderer(self,name).view)]
        #~ l += [ url(r'^%s/pdf$' % name, PdfReportRenderer(self,name).view)]
        l += [ url(r'^%s$' % name, self.view_many)]
        l += [ url(r'^%s/(\d+)$' % name, self.view_one)]
        #l += [ url(r'^%s/edit$' % name, self.edit_view)]
        l += [ url(r'^%s/pdf$' % name, self.pdf_view_many)]
        l += [ url(r'^%s/(\d+)/pdf$' % name, self.pdf_view_one)]
        return l

    #~ def view(self, request):
        #~ if render.is_editing(request):
            #~ return render.EditReportRenderer(self).view(request)
        #~ return render.ViewReportRenderer(self).view(request)
            
    def view_many(self, request):
        if render.is_editing(request):
            r = render.EditManyReportRenderer(self,request)
        else:
            r = render.ViewManyReportRenderer(self,request)
        return r.render()
            
    def view_one(self, request,row):
        if render.is_editing(request):
            r = render.EditOneReportRenderer(self,request,row)
        else:
            r = render.ViewOneReportRenderer(self,request,row)
        return r.render()

    def pdf_view_one(self, request,row):
        return render.PdfOneReportRenderer(self,request,row).render()
        
    def pdf_view_many(self, request):
        return render.PdfManyReportRenderer(self,request).render()
        
    def as_text(self, **kw):
        return render.TextReportRenderer(self,**kw).render()
        
    def as_html(self, **kw):
        return render.HtmlReportRenderer(self,**kw).render()
        

    def _build_queryset(self,flt=None):
        qs=self.queryset
        if flt:
            l=[]
            q=models.Q()
            for col in self.columns:
                if col.is_filter:
                    q = q | models.Q(**{col.field.name+"__contains": flt})
            #print l
            qs = qs.filter(q)
        return qs
        



from django.conf import settings
from django.forms.models import modelform_factory, formset_factory
from django.shortcuts import render_to_response 
from lino.django.tom import layout as layouts


    
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
    form_class=modelform_factory(model_class)
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
      layout = layouts.EditLayoutRenderer(layouts.page_layout(obj),frm),
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

