#~ ## Copyright 2009 Luc Saffre

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

import os
import traceback
#import types
import cgi
from textwrap import TextWrapper
from StringIO import StringIO # cStringIO doesn't support Unicode
import cStringIO


#from django.conf import settings
from django import forms
from django.db import models
from django.db.models.query import QuerySet
from django.template.loader import render_to_string
from django import template 
from django.shortcuts import render_to_response 
from django.forms.models import modelform_factory, modelformset_factory, inlineformset_factory
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.forms.models import ModelForm,ModelFormMetaclass, BaseModelFormSet
from django.db.models.manager import Manager

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.utils import simplejson
from django.template.loader import render_to_string, get_template, select_template, Context

try:
    # l:\snapshot\xhtml2pdf
    import ho.pisa as pisa
except ImportError:
    pisa = None


from lino.django.utils import layouts
#from lino.django.utils import reports
from lino.django.utils.requests import again, get_redirect, redirect_to
from lino.django.utils import editing, latex

IS_SELECTED = 'IS_SELECTED_%d'


def SPAN(text,style):
    #text = escape(text)
    return """<span class="textinput"
    style="%s">%s</span>
    """ % (style,text)
    
def HREF(href,text):
    text = escape(text)
    return mark_safe('<a href="%s">%s</a>' % (href,text))



def short_link(s):
    return "link"
    
    

    

class ReportRenderer:
    limit = None
    offset = None
    master_instance = None
    instance = None
    
    def __init__(self,report,
            master_instance=None,
            offset=None,limit=None,
            mode=None,
            **kw):
        #from lino.django.tom.reports import Report
        #assert isinstance(report,Report)
        self.report = report
        report.setup()
        self.name = report.name+"Renderer"
        self.mode = mode
        if mode == 'choice':
            self.store = report.choice_store
        else:
            self.store = report.store
        #self.layout = report.layouts[layout]
        #~ if report.master is None:
            #~ assert master_instance is None
        #~ else:
            #~ assert master_instance is None or isinstance(master_instance,report.master)
        #~ self.master_instance = master_instance
        if master_instance is not None:
            self.master_instance = master_instance
        #print self.__class__.__name__, "__init__()"
        #self.params = params
        self.queryset = report.get_queryset(master_instance,**kw)
        
        if isinstance(self.queryset,QuerySet):
            self.total_count = self.queryset.count()
        else:
            # a Report may override get_queryset() and return a list
            self.total_count = len(self.queryset)
        
        if offset is not None:
            self.queryset = self.queryset[int(offset):]
            self.offset = offset
            
        if limit is None:
            limit = report.page_length
        if limit is not None:
            self.queryset = self.queryset[:int(limit)]
            self.limit = limit
            
        self.page_length = report.page_length
        #self.column_headers = report.column_headers
        
        #~ if self.limit == 1:
            #~ #self.layout = self.report.page_layout
            #~ try:
                #~ self.instance = self.queryset[0]
            #~ except IndexError,e:
                #~ self.instance = self.report.create_instance(self)
        #~ else:
            #~ #self.layout = self.report.row_layout
            #~ self.column_headers = report.column_headers
            
        self.actions = self.report.get_row_actions(self)

    def get_title(self):
        return self.report.get_title(self)
        
    #~ def get_layout(self) :
        #~ raise NotImplementedError
        

    def obj2json(self,obj):
        d = {}
        for fld in self.store.fields:
            fld.write_to_form(obj,d)
            #d[e.name] = e.value2js(obj)
        return d
            
    def render_to_json(self):
        rows = [ self.obj2json(row) for row in self.queryset ]
        d = dict(count=self.total_count,rows=rows)
        s = simplejson.dumps(d,default=unicode)
        return s
        #print s
        #return HttpResponse(s, mimetype='text/html')
        

class ViewReportRenderer(ReportRenderer):
  
    #page_length = 10
    editing = 0
    selector = None
    #must_refresh = False
    offset = None
    sort_column = None
    sort_direction = None
    
    def __init__(self,request,report,*args,**kw):
      
        #~ if is_main:
        self.params = report.param_form(request.GET)
        if self.params.is_valid():
            kw.update(self.params.cleaned_data)
        pk = request.GET.get('master',None)
        if pk is not None:
            try:
                kw.update(master_instance=report.master.objects.get(pk=pk))
            except report.master.DoesNotExist,e:
                print "[Warning] There's no %s with %s=%r" % (
                  report.master.__name__,report.master._meta.pk.name,pk)
        sort = request.GET.get('sort',None)
        if sort:
            self.sort_column = sort
            sort_dir = request.GET.get('dir','ASC')
            if sort_dir == 'DESC':
                sort = '-'+sort
                self.sort_direction = 'DESC'
            kw.update(order_by=sort)
        
        #self.json = request.GET.get('json',False)
        
        offset = request.GET.get('start',None)
        if offset:
            kw.update(offset=offset)
        limit = request.GET.get('limit',None)
        if limit:
            kw.update(limit=limit)
        #~ layout = request.GET.get('layout',None)
        #~ if layout:
            #~ kw.update(layout=int(layout))
        mode = request.GET.get('mode',None)
        if mode:
            kw.update(mode=mode)

        #print "ViewReportRenderer.__init__() 1",report.name
        self.request = request
        ReportRenderer.__init__(self,report,*args,**kw)
        #print "ViewReportRenderer.__init__() 2",report.name
        #self.is_main = is_main
        request._lino_renderer = self
        

    def get_absolute_url(self,**kw):
        if self.master_instance is not None:
            kw.update(master_instance=self.master_instance)
        if self.limit != self.__class__.limit:
            kw.update(limit=self.limit)
        if self.offset is not None:
            kw.update(start=self.offset)
        if self.sort_column is not None:
            kw.update(sort=self.sort_column)
        if self.sort_direction is not None:
            kw.update(dir=self.sort_direction)
        #~ if self.layout.index != 0:
            #~ kw.update(layout=self.layout.index)
        if self.mode is not None:
            kw.update(mode=self.mode)
        return self.report.get_absolute_url(**kw)
        
        


        
class PdfManyReportRenderer(ViewReportRenderer):

    def render(self,as_pdf=True):
        template = get_template("lino/grid_print.html")
        context=dict(
          report=self,
          title=self.get_title(),
        )
        html  = template.render(Context(context))
        if not (pisa and as_pdf):
            return HttpResponse(html)
        result = cStringIO.StringIO()
        pdf = pisa.pisaDocument(cStringIO.StringIO(
          html.encode("ISO-8859-1")), result)
        if pdf.err:
            raise Exception(cgi.escape(html))
        return HttpResponse(result.getvalue(),mimetype='application/pdf')
        
    def rows(self):
        rownum = 1
        for obj in self.queryset:
            yield Row(self,obj,rownum,None)
            rownum += 1

  
class PdfOneReportRenderer(ViewReportRenderer):
    #detail_renderer = PdfManyReportRenderer

    def render(self,as_pdf=True):
        if as_pdf:
            return self.row.instance.view_pdf(self.request)
            #~ if False:
                #~ s = render_to_pdf(self.row.instance)
                #~ return HttpResponse(s,mimetype='application/pdf')
            #~ elif pisa:
                #~ s = as_printable(self.row.instance,as_pdf=True)
                #~ return HttpResponse(s,mimetype='application/pdf')
        else:
            return self.row.instance.view_printable(self.request)
            #~ result = as_printable(self.row.instance,as_pdf=False)
            #~ return HttpResponse(result)
