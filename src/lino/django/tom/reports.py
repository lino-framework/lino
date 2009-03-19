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


import types
from StringIO import StringIO # cStringIO doesn't support Unicode
from textwrap import TextWrapper

from lino.reports.constants import *
from lino.misc.etc import assert_pure

from django.db import models
#from django import forms
from django.forms.models import modelform_factory, formset_factory
from django.forms.models import ModelForm,ModelFormMetaclass, BaseModelFormSet
from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.template.loader import select_template, Context


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



def again(request,**kw):
    req=request.GET.copy()
    for k,v in kw.items():
        req[k] = v
    return mark_safe(request.path + "?" + req.urlencode())


def hfill(s,align,width):
    if align == LEFT:
        return s.ljust(width)
    if align == RIGHT:
        return s.rjust(width)
    if align == CENTER:
        return s.center(width)
    raise ConfigError("hfill() : %s" % repr(align))

def vfill(lines,valign,height):
    n = height - len(lines) # negative if too many
    if n == 0: return
    if valign == TOP:
        if n > 0:
            for i in range(n):
                lines.append("")
        else:
            del lines[n:] # ?
    elif valign == BOTTOM:
        if n > 0:
            for i in range(-n):
                lines.insert(0,"")
        else:
            del lines[0:n] # ?
    elif valign == CENTER:
        raise NotImplementedError
    else:
        raise ConfigError("vfill() : %s" % repr(valign))
        
class Cell(object):
    def __init__(self,row,column,index):
        self.row = row
        self.column = column
        
    def __unicode__(self):
        return unicode(self.column.cell_value(self))
        
        
class Row(object):
    def __init__(self,rpt,request,queryset,instance,form,rownum):
        self.request = request
        self.rownum = rownum
        self.rpt = rpt
        self.instance = instance
        self.form=form
        self.queryset=queryset
      
    def __iter__(self):
        for col in self.rpt.columns:
            cell = Cell(self, col)
            yield cell
            
    def links(self):
        l=[]
        l.append('<a href="%s">page</a>' % self.get_url_path())
        l.append('<a href="%s">row</a>' % self.form.instance.get_url_path())
        #print "<br/>".join(l)
        return mark_safe("<br/>".join(l))

    def has_previous(self):
        return self.rownum > 1
    def has_next(self):
        #print "Row.has_next() : ", self.rownum, self.queryset.count()
        return self.rownum < self.queryset.count()
    def previous(self):
        return again(self.request,row=self.rownum-1)
        #~ req=self.request.GET.copy()
        #~ req["row"] = self.rownum-1
        #~ return mark_safe(self.request.path + "?" + req.urlencode())
    def next(self):
        return again(self.request,row=self.rownum+1)
        #return self.rownum+1
            
    def get_url_path(self):
        return again(self.request,row=self.rownum)
        
class Column(object):
    is_formfield = False
    def __init__(self, rpt, label,index):
        self.index = index
        self.width = None
        self.halign = LEFT
        self.valign = TOP
        self.label = label

    def getLabel(self):
        return self.label

    def get_urls(self,name):
        return []
        
    def format(self,value):
        return unicode(value)
  
    def getMinWidth(self):
        return 10
        #~ x=WIDTHS[self.field.__class__]
        #~ w=x[0]
        #~ w = max(w,len(self.getLabel()))
        #~ return w
        
    def getMaxWidth(self):
        return 100
        #~ x=WIDTHS[self.field.__class__]
        #~ return x[1]
        
class FieldColumn(Column):
    def __init__(self, rpt, field,index):
        Column.__init__(self,rpt,field.verbose_name,index)
        self.field = field
        self.name=field.name
        self.is_filter = isinstance(field,models.CharField)
        
    def cell_value(self,instance,form):
        return getattr(instance,self.field.name)
        

        
class FormFieldColumn(FieldColumn):
    is_formfield = True

    #~ def getCellValue(self,row_instance):
        #~ return getattr(row_instance,self.field.name)

    def cell_value(self,instance,form):
        return form[self.field.name]
        
        
class MethodColumn(Column):
    is_formfield = False
    is_filter = False
    def __init__(self, rpt, name,index):
        #print field.var_name
        Column.__init__(self,rpt,name,index)
        self.name = name
        
    def get_urls(self,name):
        return [ url(r'^%s/%s/$' % (name,self.name), 
            self.view) ]
            
    def cell_value(self,instance,form):
        meth=getattr(instance,self.name)
        return meth()
            
    #~ def view(self,request):
        #~ return render_to_response("tom/base_site.html",
          #~ dict(title=self.name))
      
#~ class RelatedColumn(ReadonlyColumn):
    #~ is_filter = False
    #~ def __init__(self, rpt, name, field):
        #~ #print field.var_name
        #~ Column.__init__(self,rpt,name)
        #~ self.field = field
        #~ self.name = name
        
    #~ def get_urls(self,name):
        #~ return [ url(r'^%s/%s/$' % (name,self.name), 
            #~ self.view) ]
            
    #~ def cell_value(self,cell):
        #~ return getattr(cell.row.form.instance,self.name)
            
    #~ def view(self,request):
        #~ return render_to_response("tom/base_site.html",
          #~ dict(title=self.name))
      
  
        

from django import forms

class ReportParameterForm(forms.Form):
    #~ pgn = forms.IntegerField(required=False,label="Page number") 
    #~ pgl = forms.IntegerField(required=False,label="Rows per page")
    flt = forms.CharField(required=False,label="Text filter")
    

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
    form_class = None
    label = None
    param_form = ReportParameterForm
    default_filter=''
    default_format='grid'
    #editable=True
    
    def __init__(self):
        self.groups = [] # for later
        self.totals = [] # for later
        if self.label is None:
            self.label = self.__class__.__name__
        #~ if self.form_class is None:
            #~ self.form_class = modelform_factory(self.queryset.model)
        
        
    def build_columns(self,rnd):
        columns = []
        meta = self.queryset.model._meta
        if self.columnNames:
            for colname in self.columnNames.split():
                try:
                    field,model,direct,m2m = meta.\
                      get_field_by_name(colname)
                    #print field, model, direct, m2m 
                except models.FieldDoesNotExist,e:
                    col = MethodColumn(self,colname,len(columns))
                else:
                    col = rnd.new_column(field,len(columns))
                columns.append(col)
        else:
            for field in meta.fields:
                col = rnd.new_column(field,len(columns))
                columns.append(col)
        return columns
                
    def getTitle(self):
        """
        returns None if this report has no title
        """
        return self.title
        
    def getLabel(self):
        return self.label
    
    def get_url_path(self):
        return self.rpt.get_url_path() + "/" + str(self.offset)

        
    ##
    ## public methods for user code
    ##

    def __unicode__(self):
        #return unicode(self.as_text())
        return unicode("%d row(s)" % self.queryset.count())
        
    def as_text(self, **kw):
        return TextReportRenderer(self,**kw).render()
        
    def as_form(self, **kw):
        return FormReportRenderer(self,**kw)

    #~ def get_urls_old(self,name):
        #~ urlpatterns = patterns('',
          #~ url(r'^%s$' % name, 
          #~ self.view))
        #~ urlpatterns += patterns('',
          #~ url(r'^%s/(?P<row>\d+)$' % name,
            #~ self.view_one))
        #~ return urlpatterns

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
        



class ReportRenderer:
    def __init__(self,report):
        self.report = report      
        self.columns = report.build_columns(self)


    def new_column(self,field,index):
        return FieldColumn(self,field,index)
        
    def getLabel(self):
        return self.report.getLabel()
        
    def getName(self):
        return self.report.__class__.__name__.lower()
        

class TextReportRenderer(ReportRenderer):
    
    def __init__( self,
                  report,
                  width=79,
                  columnWidths=None,
                  columnSep="|",
                  columnHeaderSep='-',
                  column_widths=None,
                  rowHeight=None,
                  flt=None):
        ReportRenderer.__init__(self,report)
        self.width=width
        self.columnWidths=columnWidths
        self.column_widths = column_widths
        self.rowHeight=rowHeight
        self.columnHeaderSep=columnHeaderSep
        self.columnSep=columnSep
        if flt is None:
            flt=self.report.default_filter
        self.flt=flt
                             
                             
  
    def computeWidths(self):
        
        """set total width or distribute available width to columns
        without explicit width. Note that these widths are to be
        interpreted as logical widths.

        """
        
        columnSepWidth=len(self.columnSep)
        if self.columnWidths is not None:
            i = 0
            for item in self.columnWidths.split():
                col = self.report.columns[i]
                if item.lower() == "d":
                    col.width = col.getMinWidth()
                elif item == "*":
                    col.width = None
                else:
                    col.width = int(item)
                i += 1
                
        if self.column_widths is not None:
            for col in self.columns:
                w=self.column_widths.get(col.name,None)
                if w is not None:
                    col.width=w

        if self.width is None:
            self.width = 0
            for col in self.columns:
                if col.width is None:
                    col.width=col.getMinWidth()
                self.width+=col.width
            return
            

        waiting = [] # columns waiting for automatic width
        used = 0 # how much width used up by columns with a width
        for col in self.columns:
            if col.width is None:
                waiting.append(col)
            else:
                used += col.width
                
        available=self.width - columnSepWidth*(len(self.columns)-1)

        if available <= 0:
            raise NotEnoughSpace()
        
        l=[]
        if len(waiting) > 0:
            
            # first loop: distribute width to those columns who need
            # less than available
            
            autoWidth = int((available - used) / len(waiting))
            for col in waiting:
                if col.getMaxWidth() is not None \
                      and col.getMaxWidth() < autoWidth:
                    col.width = col.getMaxWidth()
                    used += col.width
                else:
                    l.append(col)
                    
        if len(l) > 0:
            # second loop: 
            w = int((available - used) / len(l))
            assert w > 0
            for col in l:
                col.width = w
                used += w
         
        #elif self.width is None:
        #    self.width = totalWidth


    def render(self):
        writer=StringIO()
        self.computeWidths()
        wrappers = []
        for col in self.columns:
            wrappers.append(TextWrapper(col.width))
        width = self.width + len(self.columnSep)*(len(self.columns)-1)

        # renderHeader

        title=self.report.getTitle()
        if title is not None:
            writer.write(title+"\n")
            writer.write("="*len(title)+"\n")
            
        # wrap header labels:
        headerCells = []
        headerHeight=1
        i=0
        for col in self.columns:
            cell = wrappers[i].wrap(col.getLabel())
            headerCells.append(cell)
            headerHeight = max(headerHeight,len(cell))
            i+=1
            
        for cell in headerCells:
            vfill(cell,TOP,headerHeight)
            
        for i in range(headerHeight):
            writer.write(self._row_as_text(headerCells,i,self.columnSep))
                               
        l = [ self.columnHeaderSep * col.width
              for col in self.columns]
        writer.write("+".join(l) + "\n")
        
        queryset=self.report._build_queryset(flt=self.flt)
        #queryset=self.report.queryset
        #print queryset.count()
        for obj in queryset:
            wrappedCells = []
            for col in self.columns:
                v=col.cell_value(obj,None)
                if v is None:
                    v=''
                l = wrappers[col.index].wrap(col.format(v))
                if len(l) == 0:
                    wrappedCells.append([''])
                else:
                    wrappedCells.append(l)
            
            
            # find out rowHeight for this row
            if self.rowHeight is None:
                rowHeight = 1
                for linelist in wrappedCells:
                    rowHeight = max(rowHeight,len(linelist))
            else:
                rowHeight = self.rowHeight

            if rowHeight == 1:
                writer.write(self._row_as_text(wrappedCells,0,self.columnSep))
            else:
                # vfill each cell:
                for j in range(len(self.columns)):
                    vfill(wrappedCells[j],
                          self.columns[j].valign,
                          rowHeight)

                for i in range(rowHeight):
                    writer.write(self._row_as_text(
                        wrappedCells,i,self.columnSep))
        return writer.getvalue()



    def _row_as_text(self,cellValues,i,columnSep):
        l = []
        for j in range(len(self.columns)):
            assert_pure(cellValues[j][i])
            l.append(hfill(cellValues[j][i],
                           self.columns[j].halign,
                           self.columns[j].width))
        s=columnSep.join(l)
        return s.rstrip()+"\n"
        
        
        
class FormReportRenderer(ReportRenderer):

    page_length = 15
    extra=1
    can_delete=True
    can_order=False
    max_num=0
    start_page=1
    
    def __init__(self,
                 report,
                 editable=True):
        self.editable=editable
        ReportRenderer.__init__(self,report)
        
        # todo: instead of letting modelform_factory look up the fields again by 
        # their name, i should do it myself, formfields being then a list of 
        # fields and not of fieldnames.
        formfields = [col.field.name for col in self.columns if col.is_formfield]
        rowform_class = modelform_factory(report.queryset.model,
                                          fields=formfields)
                
        self.formset_class = formset_factory(rowform_class,
              BaseModelFormSet, extra=self.extra, 
              max_num=self.max_num,
              can_order=self.can_order, 
              can_delete=self.can_delete)
        self.formset_class.model = report.queryset.model
        
        
                  
    def new_column(self,field,index):
        if self.editable and field.editable and not field.primary_key:
            return FormFieldColumn(self,field,index)
        return FieldColumn(self,field,index)
        
    def get_urls(self,name):
        l = [ url(r'^%s$' % name, self.view) ]
        #for col in self.columns:
        #  l += col.get_urls(name)
        return l

    def view(self,request):
      
        params = self.report.param_form(request.GET)
        if params.is_valid():
            flt = params.cleaned_data['flt'] or self.report.default_filter
        else: 
            flt = self.report.default_filter
        qs = self.report._build_queryset(flt)
        
        context = dict(
            main_menu=settings.MAIN_MENU,
            report=self.report,
            title=self.report.label,
            params=params)
      
        row = request.GET.get('row')
        if row is None:
            return self.view_many(request,qs,context)
            
        return self.view_one(request,qs,context,row)
            


    def view_one(self,request,qs,context,row):
        rownum=int(row)
        try:
            obj=qs[rownum-1]
        except IndexError:
            rownum=qs.count()
            obj=qs[rownum-1]
        
        if request.method == 'POST':
            frm=self.form_class(request.POST,instance=obj)
            if frm.is_valid():
                frm.save()
        else:
            frm=self.form_class(instance=obj)      
        context.update(
            form=frm,
        )
        
        row = Row(self.report,request,qs,obj,frm,rownum)
        
        context.update(
            params=params,
            row=row,
            object=obj,
        )
        meta = self.queryset.model._meta
        l=[ 
           "tom/%s_form.html" % meta.db_table, 
           "tom/form.html"]
        t=select_template(l)
        return HttpResponse(t.render(Context(context)))
        
    def view_many(self,request,qs,context,row):
        
        pgn = request.GET.get('pgn')
        if pgn is None:
            pgn = self.report.start_page
        else:
            pgn=int(pgn)
        pgl = request.GET.get('pgl')
        if pgl is None:
            pgl = self.report.page_length
        else:
            pgl = int(pgl)
      
      
        paginator = Paginator(qs,pgl)
        try:
            page = paginator.page(pgn)
        except (EmptyPage, InvalidPage):
            page = paginator.page(paginator.num_pages)
        
        if request.method == 'POST':
            fs = self.formset_class(request.POST,queryset=page.object_list)
            if fs.is_valid():
                fs.save()
                
                if self.can_delete and fs.deleted_forms:
                    #print [unicode(form.instance) for form in fs.deleted_forms]
                    for form in fs.deleted_forms:
                        print "Deleted:", form.instance
                    # start from begin because paginator and page must reload
                    return HttpResponseRedirect(request.path)
                    
        else:
            fs = self.formset_class(queryset=page.object_list)
        context.update(formset=fs)
            
        rownum = page.start_index()
        rows = []
        if self.editable:
            for form in fs.forms:
                rows.append(Row(self,request,qs,form.instance,form,rownum))
                rownum += 1
        else:
            for obj in page.object_list:
                rows.append(Row,self,request,qs,obj,rownum)
                rownum += 1
          
        context.update(
            page=page,
            rows=rows,
        )
        return render_to_response("tom/grid.html",context)


    
    
    
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
    
def edit_instance(request,app,model,pk):
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
    )
    return render_to_response("tom/instance.html",context)
    
def urls(name=''):
    l=[url(r'^%s$' % name, index)]
    #~ l.append(url(r'^edit/(?P<name>\w+)$', edit_report))
    l.append(url(r'^edit/(?P<app>\w+)/(?P<model>\w+)/(?P<pk>\w+)$', edit_instance))
    #for rptname,rptclass in _report_classes.items():
    return patterns('',*l)
