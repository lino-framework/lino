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
from django.forms.models import modelform_factory
from django.conf.urls.defaults import patterns, url, include
from django.forms.models import _get_foreign_key

#from django.forms.models import ModelForm,ModelFormMetaclass, BaseModelFormSet
#from django.shortcuts import render_to_response 
#from django.core.paginator import Paginator, EmptyPage, InvalidPage
#from django.http import HttpResponse, HttpResponseRedirect, Http404
#from django.utils.safestring import mark_safe
#from django.template.loader import render_to_string, get_template, select_template, Context

# l:\snapshot\xhtml2pdf
#import ho.pisa as pisa

from lino.django.tom import render
from lino.django.utils import layouts
from lino.django.utils.requests import is_editing


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




class Report:
  
    #~ __metaclass__ = ReportMetaClass
    
    queryset = None 
    model = None
    order_by = None
    title = None
    #width = None
    #columnWidths = None
    columnNames = None
    #rowHeight = None
    label = None
    param_form = ReportParameterForm
    default_filter = ''
    #default_format='form'
    #editable=True
    name = None
    #path=None
    form_class = None
    #row_print_template = "tom/"
    #detail_reports = ''
    master = None
    fk_name = None
    _page_layout = None
    page_layout_class = layouts.PageLayout
    
    def __init__(self):
        self.groups = [] # for later
        self.totals = [] # for later
        if self.label is None:
            self.label = self.__class__.__name__
        if self.name is None:
            self.name = self.__class__.__name__.lower()
        #~ if self.title is None:
            #~ self.title = self.build_title()
        #~ if self.queryset is None:
            #~ self.queryset = self.get_queryset()
        if self.model is None:
            self.model = self.queryset.model
        if self.form_class is None:
            self.form_class = modelform_factory(self.model)
        self.row_layout = layouts.RowLayout(self.model,
                                            self.columnNames)
        if self.master:
            self.fk = _get_foreign_key(self.master,
              self.model,self.fk_name)
        
        self.details = self.inlines()
         
    def column_headers(self):
        #print "column_headers"
        #print self.layout
        for e in self.row_layout._main.elements:
            yield e.name
            
    def inlines(self):
        return {}
         
    def get_title(self,renderer):
        #~ if self.title is None:
            #~ return self.label
        return self.title or self.label
        
    def get_queryset(self,master_instance):
        if self.queryset is not None:
            qs = self.queryset
        else:
            qs = self.model.objects.all()
        #~ if self.master:
            #~ fk = _get_foreign_key(self.master,self.model,self.fk_name)
            #~ self.fk.get_attname()
        if self.master is not None:
            qs = qs.filter(**{self.fk.name:master_instance})
            #~ if self.fk.limit_choices_to:
                #~ qs = qs.filter(**self.fk.limit_choices_to)

        if self.order_by:
            qs = qs.order_by(*self.order_by.split())
        return qs
        
    def getLabel(self):
        return self.label
    
    def get_row_print_template(self,instance):
        return instance._meta.db_table + "_print.html"
        
    def page_layout(self):
        #model = self.__class__
        if self._page_layout is None:
            self._page_layout = self.page_layout_class(
                self.model)
        return self._page_layout
            
        
    #~ def __unicode__(self):
        #~ #return unicode(self.as_text())
        #~ return unicode("%d row(s)" % self.queryset.count())
    
    def get_urls(self,name):
        l = []
        l.append(url(r'^%s$' % name, self.view_many))
        l.append(url(r'^%s/(\d+)$' % name, self.view_one))
        l.append(url(r'^%s/pdf$' % name, self.pdf_view_many))
        l.append(url(r'^%s/(\d+)/pdf$' % name, self.pdf_view_one))
        l.append(url(r'^%s/(\d+)/print$' % name, self.print_one_view))
        return l

    def view(self,request):
        return self.view_many(request)
        
    def view_many(self,request):
        if is_editing(request):
            r = render.EditManyReportRenderer(request,True,self)
        else:
            r = render.ViewManyReportRenderer(request,True,self)
        return r.render_to_response()
            
    def view_one(self,request,row):
        if is_editing(request):
            r = render.EditOneReportRenderer(row,request,True,self)
        else:
            r = render.ViewOneReportRenderer(row,request,True,self)
        return r.render_to_response()

    def pdf_view_one(self,request,row):
        return render.PdfOneReportRenderer(row,request,True,self).render()
        
    def pdf_view_many(self, request):
        return render.PdfManyReportRenderer(request,True,self).render()

    def print_one_view(self,request,row):
        return render.RowPrintReportRenderer(row,request,True,self).render()

    def as_text(self, *args,**kw):
        return render.TextReportRenderer(self,*args,**kw).render()
        
    #~ def as_html(self, **kw):
        #~ return render.HtmlReportRenderer(self,**kw).render_to_string()
        


#~ class SubReport(Report):
  
    #~ def __init__(self,master,fk_name=None):
    #~ fk = _get_foreign_key(master,self.model,fk_name)
  
    #~ def set_master(self,master):
        #~ self.master = master
        
    #~ def get_queryset(self):
        #~ return document.docitem_set.order_by("pos")
        