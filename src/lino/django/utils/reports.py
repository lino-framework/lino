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
from django.contrib.auth.decorators import login_required


#from django.forms.models import ModelForm,ModelFormMetaclass, BaseModelFormSet
#from django.shortcuts import render_to_response 
#from django.core.paginator import Paginator, EmptyPage, InvalidPage
#from django.http import HttpResponse, HttpResponseRedirect, Http404
#from django.utils.safestring import mark_safe
#from django.template.loader import render_to_string, get_template, select_template, Context

from lino.django.utils import layouts, render, perms
from lino.django.utils.editing import is_editing
from lino.django.utils.sites import lino_site


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


def base_attrs(cl):
    #~ if cl is Report or len(cl.__bases__) == 0:
        #~ return
    #~ myattrs = set(cl.__dict__.keys())
    for b in cl.__bases__:
        for k in base_attrs(b):
            yield k
        for k in b.__dict__.keys():
            yield k


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

class ReportMetaClass(type):
    def __new__(meta, classname, bases, classDict):
        cls = type.__new__(meta, classname, bases, classDict)
        if classname != 'Report':
            if cls.typo_check:
                myattrs = set(cls.__dict__.keys())
                for attr in base_attrs(cls):
                    myattrs.discard(attr)
                if len(myattrs):
                    print "[Warning]: %s defines new attribute(s) %s" % (cls,",".join(myattrs))
        
        #_report_classes[classname] = cls
        lino_site.register_report(cls)
        return cls




class Report:
    __metaclass__ = ReportMetaClass
    queryset = None 
    model = None
    order_by = None
    filter = None
    exclude = None
    title = None
    columnNames = None
    row_layout_class = None
    label = None
    param_form = ReportParameterForm
    #default_filter = ''
    name = None
    form_class = None
    master = None
    fk_name = None
    
    _page_layouts = None
    page_layouts = (layouts.PageLayout ,)
    
    can_view = perms.always
    can_add = perms.is_authenticated
    can_change = perms.is_authenticated

    typo_check = True
    
    #~ __slots__ = """
    #~ queryset model
    #~ order_by
    #~ filter
    #~ exclude
    #~ title
    #~ columnNames
    #~ row_layout_class
    #~ label
    #~ param_form
    #~ default_filter
    #~ name
    #~ form_class
    #~ master
    #~ fk_name
    #~ _page_layouts
    #~ page_layouts
    #~ can_view
    #~ can_add
    #~ can_change
    #~ """.split()
    
    
    def __init__(self,**kw):
        #~ self.groups = [] # for later
        #~ self.totals = [] # for later
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
        if self.row_layout_class is None:
            self.row_layout = layouts.RowLayout(self.model,
                                                self.columnNames)
        else:
            assert self.columnNames is None
            self.row_layout = self.row_layout_class(self.model)
        if self.master:
            self.fk = _get_foreign_key(self.master,
              self.model,self.fk_name)
        self._page_layouts = [
              layout(self.model) for layout in self.page_layouts]
                
        for k,v in kw.items():
            if not hasattr(self,k):
                print "[Warning] Ignoring attribute %s" % k
            setattr(self,k,v)
        
    def column_headers(self):
        #print "column_headers"
        #print self.layout
        for e in self.row_layout._main.elements:
            yield e.name
            
    def get_title(self,renderer):
        #~ if self.title is None:
            #~ return self.label
        return self.title or self.label
        
    def get_queryset(self,master_instance,flt=None):
        if self.queryset is not None:
            qs = self.queryset
        else:
            qs = self.model.objects.all()
        #~ if self.master:
            #~ fk = _get_foreign_key(self.master,self.model,self.fk_name)
            #~ self.fk.get_attname()
        if self.master is None:
            assert master_instance is None
        else:
            #print qs
            #print qs.model
            qs = qs.filter(**{self.fk.name:master_instance})
            #~ if self.fk.limit_choices_to:
                #~ qs = qs.filter(**self.fk.limit_choices_to)

        if self.order_by:
            qs = qs.order_by(*self.order_by.split())
        if self.filter:
            qs = qs.filter(**self.filter)
        if self.exclude:
            qs = qs.exclude(**self.exclude)
        if flt is not None:
            l = []
            q = models.Q()
            for field in self.model._meta.fields:
                if isinstance(field,models.CharField):
                    q = q | models.Q(**{
                      field.name+"__contains": flt})
            qs = qs.filter(q)
        return qs
        
    def getLabel(self):
        return self.label
    
    #~ def get_row_print_template(self,instance):
        #~ return instance._meta.db_table + "_print.html"
        
    #~ def page_layout(self,i=0):
        #~ if self._page_layouts is None:
            #~ self._page_layouts = [ 
              #~ l(self.model) for l in self.page_layouts]
        #~ return self._page_layouts[i]

    #~ def can_view(self,request,row=None):
        #~ return True
        
    #~ def can_add(self,request,row=None):
        #~ return True
        
    #~ def can_change(self,request,row=None):
        #~ return request.user.is_authenticated()
        
        
    #~ def __unicode__(self):
        #~ #return unicode(self.as_text())
        #~ return unicode("%d row(s)" % self.queryset.count())
    
    def get_urls(self,name):
        l = []
        l.append(url(r'^%s/(\d+)$' % name, self.view_one))
        l.append(url(r'^%s$' % name, self.view_many))
        l.append(url(r'^%s/(\d+)/pdf$' % name, self.pdf_one))
        l.append(url(r'^%s/pdf$' % name, self.pdf_many))
        l.append(url(r'^%s/(\d+)/print$' % name, self.print_one))
        l.append(url(r'^%s/print$' % name, self.print_many))
        return l

    #~ def view(self,request):
        #~ return self.view_many(request)
    def view_many(self,request):
        #~ msg = "Hello, "+unicode(request.user)
        #~ print msg
        #~ request.user.message_set.create(msg)
        if not self.can_view.passes(request):
            return render.sorry(request)
        if is_editing(request) and self.can_change.passes(request):
            r = render.EditManyReportRenderer(request,True,self)
        else:
            r = render.ViewManyReportRenderer(request,True,self)
        return r.render_to_response()
            
    def view_one(self,request,row,**kw):
        #print "Report.view_one()", request.path
        if not self.can_view.passes(request):
            return render.sorry(request)
        if is_editing(request) and self.can_change.passes(request):
            r = render.EditOneReportRenderer(row,request,True,self,**kw)
        else:
            r = render.ViewOneReportRenderer(row,request,True,self,**kw)
        return r.render_to_response()

    def pdf_one(self,request,row):
        if not self.can_view.passes(request):
            return render.sorry(request)
        return render.PdfOneReportRenderer(row,request,True,self).render()
        
    def pdf_many(self, request):
        if not self.can_view.passes(request):
            return render.sorry(request)
        return render.PdfManyReportRenderer(request,True,self).render()

    def print_many(self, request):
        if not self.can_view.passes(request):
            return render.sorry(request)
        return render.PdfManyReportRenderer(request,True,self).render(as_pdf=False)

    def print_one(self,request,row):
        if not self.can_view.passes(request):
            return render.sorry(request)
        return render.PdfOneReportRenderer(row,request,True,self).render(as_pdf=False)

    def as_text(self, *args,**kw):
        from lino.django.utils.renderers_text import TextReportRenderer
        return TextReportRenderer(self,*args,**kw).render()
        
    #~ def as_html(self, **kw):
        #~ return render.HtmlReportRenderer(self,**kw).render_to_string()
        
    def get_row_actions(self,renderer):
        l = []
        #l.append( ('dummy',self.dummy) )
        if self.can_change.passes(renderer.request):
            l.append( ('delete',self.delete_selected) )
        return l
            
    def delete_selected(self,renderer):
        for row in renderer.selected_rows():
            print "DELETE:", row.instance
            row.instance.delete()
        renderer.must_refresh()
        
        


#~ class SubReport(Report):
  
    #~ def __init__(self,master,fk_name=None):
    #~ fk = _get_foreign_key(master,self.model,fk_name)
  
    #~ def set_master(self,master):
        #~ self.master = master
        
    #~ def get_queryset(self):
        #~ return document.docitem_set.order_by("pos")
        