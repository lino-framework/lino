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

import traceback
#import types
import cgi
from textwrap import TextWrapper
from StringIO import StringIO # cStringIO doesn't support Unicode
import cStringIO


#from django.conf import settings
from django import forms
from django.db import models
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django import template 
from django.shortcuts import render_to_response 
from django.forms.models import modelform_factory, modelformset_factory, inlineformset_factory
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.forms.models import ModelForm,ModelFormMetaclass, BaseModelFormSet


from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string, get_template, select_template, Context

try:
    # l:\snapshot\xhtml2pdf
    import ho.pisa as pisa
except ImportError:
    pisa = None


from lino.reports.constants import *
from lino.django.utils import layouts
from lino.misc.etc import assert_pure
from lino.django.utils.requests import again, get_redirect, redirect_to
#from lino.django.utils.editing import is_editing, stop_editing
from lino.django.utils import editing
from lino.django.utils.sites import site as lino_site


    

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
        






#~ class Cell(object):
    #~ def __init__(self,row,column):
        #~ assert row is not None
        #~ self.row = row
        #~ self.column = column
        
    #~ def __unicode__(self):
        #~ value = self.column.cell_value(
          #~ self.row.instance,self.row.form)
        #~ if value is None:
            #~ return ''
        #~ return mark_safe(unicode(value))
        
        
class Row(object):
    def __init__(self,renderer,instance,number,form=None):
        self.renderer = renderer
        self.report = renderer.report
        self.number = number
        self.instance = instance
        self.form = form
        
        self.inline_renderers = {}
        if renderer.is_main:
            for name,inline in self.report._inlines.items():
                self.inline_renderers[name] = \
                  renderer.detail_renderer(renderer.request,
                    False,inline,self.instance)
        
        
      
    def __getitem__(self,name):
        if self.renderer.editing:
            return self.form[name]
        return getattr(self.instance,name)

        #~ col = self.renderer.find_column(name)
        #~ return Cell(self, col)
        
    def as_html(self):
        try:
            #return r.render_to_string()
            return self.report.row_layout.bound_to(self).as_html()
        except Exception,e:
            print "Exception in Row.as_html():"
            traceback.print_exc()
            raise e

    def links(self):
        l=[]
        if self.renderer.is_main:
            l.append('<a href="%s">page</a>' % self.get_url_path())
        if False:
            l.append('<a href="%s">instance</a>' % \
                self.instance.get_url_path())
        #print "<br/>".join(l)
        return mark_safe("\n".join(l))

    def has_previous(self):
        return self.number > 1
    def has_next(self):
        #print "Row.has_next() : ", self.rownum, self.queryset.count()
        return self.number < self.renderer.queryset.count()
    def previous(self):
        return self.renderer.again(row=self.number-1)
        #~ req=self.request.GET.copy()
        #~ req["row"] = self.rownum-1
        #~ return mark_safe(self.request.path + "?" + req.urlencode())
    def next(self):
        return self.renderer.again(row=self.number+1)
        #return self.rownum+1
            
    def get_url_path(self):
        return self.renderer.again(str(self.number))
        
    def pk_field(self):
        """
        Used in grid_edit.html
        BaseModelFormSet.add_fields() usually adds a hidden input for the pk, which must 
        get rendered somewhere on each row of the grid template.
        """
        pk = self.renderer.queryset.model._meta.pk
        if pk.auto_created or isinstance(pk, models.AutoField):
            return self.form[pk.name]
        return ""
        
        
        
    #~ def render_inline(self,inline):
        #~ dtlrep = self.report.details.get(name,None)
        #~ #dtlrep = getattr(self.report,name,None)
        #~ if dtlrep is None:
            #~ #print "%s has not detail %r" % (self.report,name)
            #~ return None
        #~ print self.__class__.__name__, ".render_detail()", name
        #~ return self.renderer.detail_to_string(inline,self.instance)
        #~ dtlrep = getattr(self.report,name,None)
        #~ if dtlrep is None:
            #~ #print "%s has not detail %r" % (self.report,name)
            #~ return None
        #~ try:
            #~ r = self.renderer.detail_renderer(self.renderer.request,False,dtlrep,self.instance)
            #~ return r.render_to_string()
        #~ except Exception,e:
            #~ #print e
            #~ traceback.print_exc()
            #~ raise e
            
    def render_field(self,field):
        r = self.inline_renderers.get(field.name,None)
        if r is not None:
            return r.render_to_string()
        if self.form is None:
            return self.field_as_readonly(field)
        try:
            bf = self.form[field.name] # a BoundField instance
        except KeyError,e:
            return self.field_as_readonly(field)
            
        if bf.field.widget.is_hidden:
            return self.field_as_readonly(field)
        #field.setup_widget(bf.field.widget)
        
        widget = bf.field.widget
        if isinstance(widget,forms.widgets.Input):
            widget.attrs.update(size=field.width)
        elif isinstance(widget,forms.Textarea):
            widget.attrs.update(cols=field.width,
                                rows=field.height)
        
        s = bf.as_widget()
        if field.layout.show_labels and bf.label:
            if isinstance(bf.field.widget, forms.CheckboxInput):
                s = s + " " + bf.label_tag()
            else:
                s = bf.label_tag() + "<br/>" + s
        #print "render_field()", repr(bf.errors)
        s += unicode(bf.errors)
        return mark_safe(s)
        
            
    def field_as_readonly(self,field_element):
        #instance = renderer.get_instance()
        value = getattr(self.instance,field_element.name)
        try:
            model_field = self.instance._meta.get_field(
              field_element.name)
        except models.FieldDoesNotExist,e:
            # so it is a method
            if hasattr(value,"field"):
                #print "it is a method"
                field = value.field
                value = value()
                #print value
                if field.verbose_name:
                    label = field.verbose_name
                else:
                    label = self.name.replace('_', ' ')
                #print label
                widget = field.formfield().widget
                #print widget
            else:
                value = value()
                #~ from lino.django.tom import reports
                #~ if isinstance(value,reports.Report):
                    #~ return value.as_html()
                label = self.name
                #widget=widget_for_value(value)
                widget = forms.TextInput()
        else:
            label = model_field.verbose_name
            form_field = model_field.formfield() 
            if form_field is None:
                form_field = forms.CharField()
                #return ''
            #print self.instance, field.name
            widget = form_field.widget
            
        def SPAN(text,style):
            return """<span class="textinput"
            style="%s">%s</span>
            """ % (style,text)
            
        if isinstance(widget, forms.CheckboxInput):
            if value:
                s = "[X]"
            else: 
                s = "[&nbsp;&nbsp;]"
            s = SPAN(s,style="width:2em;" )
            if field_element.layout.show_labels:
                s += " " + label
            return mark_safe(s)
            
        if value is None:
            value = '&nbsp;'
        #~ else:
            #~ value = unicode(value)
        #print self.name, value
        
        
        style = widget.attrs.get('style','')
        if field_element.width is not None:
            style += "width:%dem;" % field_element.width
        if field_element.height is not None:
            style += "height:%dem;" % (field_element.height * 2)
            # TODO: 
            
        if isinstance(widget, forms.Select):
            s = "[ " + unicode(value) + " ]"
            s = SPAN(s,style)
        else:
            s = SPAN(unicode(value),style)
            
        if field_element.layout.show_labels:
            s = label + "<br/>" + s
        return mark_safe(s)
        
    def old_field_as_readonly(self,field_element):
        #instance = renderer.get_instance()
        value = getattr(self.instance,field_element.name)
        try:
            model_field = self.instance._meta.get_field(
              field_element.name)
        except models.FieldDoesNotExist,e:
            # so it is a method
            if hasattr(value,"field"):
                #print "it is a method"
                field = value.field
                value = value()
                #print value
                if field.verbose_name:
                    label = field.verbose_name
                else:
                    label = self.name.replace('_', ' ')
                #print label
                widget = field.formfield().widget
                #print widget
            else:
                value = value()
                #~ from lino.django.tom import reports
                #~ if isinstance(value,reports.Report):
                    #~ return value.as_html()
                label = self.name
                #widget=widget_for_value(value)
                widget = forms.TextInput()
        else:
            label = model_field.verbose_name
            form_field = model_field.formfield() 
            if form_field is None:
                form_field = forms.CharField()
                #return ''
            #print self.instance, field.name
            widget = form_field.widget
        if value is None:
            value = ''
        #~ else:
            #~ value = unicode(value)
        #print self.name, value
        if isinstance(widget, forms.CheckboxInput):
            if value:
                s = "[X]"
            else: 
                s = "[&nbsp;&nbsp;]"
            if field_element.layout.show_labels:
                s += " " + label
        elif isinstance(widget, forms.Select):
            s = "[ " + unicode(value) + " ]"
            if field_element.layout.show_labels:
                s = label + "<br/>" + s
        else:
            field_element.setup_widget(widget)
            s = widget.render(field_element.name,value,
              attrs={"readonly":"readonly","class":"readonly"})
            if field_element.layout.show_labels:
                s = label + "<br/>" + s
        return mark_safe(s)
        




class Column:
    is_formfield = False
    def __init__(self,renderer,label,index,picture=None):
        self.index = index
        self.width = None
        self.halign = LEFT
        self.valign = TOP
        self.label = label
        self.picture = picture

    def getLabel(self):
        return self.label

    def get_urls(self,name):
        return []
        
    def format(self,value):
        return unicode(value)
  
    def getMinWidth(self):
        return 10
        
    def getMaxWidth(self):
        return 100
        

class FieldColumn(Column):
    def __init__(self,rr,field,*args):
        Column.__init__(self,rr,field.verbose_name,*args)
        self.field = field
        self.name = field.name
        self.is_filter = isinstance(field,models.CharField)
        
    def cell_value(self,instance,form):
        return getattr(instance,self.field.name)
        

        
class FormFieldColumn(FieldColumn):
    is_formfield = True

    def cell_value(self,instance,form):
        return form[self.field.name]
        
        
class MethodColumn(Column):
    is_formfield = False
    is_filter = False
    def __init__(self,rr,name,*args):
        #print field.var_name
        Column.__init__(self,rr,name,*args)
        self.name = name
        
    #~ def get_urls(self,name):
        #~ return [ url(r'^%s/%s/$' % (name,self.name), 
            #~ self.view) ]
            
    def cell_value(self,instance,form):
        meth = getattr(instance,self.name)
        return unicode(meth())
        #~ label = unicode(meth())
        #~ html = '<a href="%s/%s">%s</a>' % (
          #~ instance.get_url_path(), self.name, label)
        #~ return mark_safe(html)
            
    #~ def view(self,request):
        #~ return render_to_response("tom/base_site.html",
          #~ dict(title=self.name))
          
          
class DetailColumn(Column):
    is_formfield = False
    is_filter = False
    def __init__(self,renderer,name,dtlrep,*args):
        #print field.var_name
        Column.__init__(self,renderer.report,name,*args)
        self.name = name
        self.renderer = renderer
        self.dtlrep = dtlrep
        #assert renderer.master is not None
        
    def cell_value(self,instance,form):
        return self.renderer.detail_to_string(self.dtlrep,instance)
        #~ try:
            #~ r = self.renderer.detail_renderer(self.renderer.request,False,self.dtlrep,instance)
            #~ return r.render_to_string()
        #~ except Exception,e:
            #~ #print e
            #~ traceback.print_exc()
            #~ raise e
          
      
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
      
  

class ReportRenderer:
    def __init__(self,report,master_instance=None):
        #print self.__class__.__name__, "__init__()"
        #from lino.django.tom.reports import Report
        #assert isinstance(report,Report)
        self.report = report
        self.column_headers = report.column_headers
        #self.title = self.report.get_title()
        if report.master is None:
            assert master_instance is None
        else:
            assert isinstance(master_instance,report.master)
        self.master_instance = master_instance
        

    def new_column(self,*args):
        return FieldColumn(self,*args)
        
    def get_title(self):
        return self.report.get_title(self)
        
    def _build_queryset(self,flt=None):
        qs = self.report.get_queryset(self.master_instance)
        if flt:
            l = []
            q = models.Q()
            for col in self.columns:
                if col.is_filter:
                    q = q | models.Q(**{
                      col.field.name+"__contains": flt})
            qs = qs.filter(q)
        return qs
        
    #~ def render_detail(self,name):
        #~ dtlrep = self.report.details.get(name,None)
        #~ if dtlrep is None:
            #~ #print "%s has not detail %r" % (self.report,name)
            #~ return None
        #~ from lino.django.tom.reports import Report
        #~ assert isinstance(dtlrep,Report),"getattr(%r,%r) is not a Report" % (self.report,name)
        #~ return self.detail_to_string(dtlrep,self.row.instance)
        #~ try:
            #~ r = self.detail_renderer(self.request,False,dtlrep,self.row.instance)
            #~ return r.render_to_string()
        #~ except Exception,e:
            #~ print "Exception in RowViewReportRenderer.render_detail()"
            #~ traceback.print_exc()
            #~ raise e
      
    #~ def column_headers(self):
        #~ for x in self.
        
class ColumnsReportRenderer(ReportRenderer):
        
    def __init__(self,report,*args,**kw):
        ReportRenderer.__init__(self,report,*args,**kw)
        self.columns_by_name = {}
        columns = []
        meta = report.model._meta
        if report.columnNames:
            for colname in report.columnNames.split() :
                a = colname.split(":")
                if len(a) == 1:
                    fieldname = colname
                    picture = None
                else:
                    fieldname = a[0]
                    picture = a[1]
                try:
                    field,model,direct,m2m = \
                      meta.get_field_by_name(fieldname)
                    #print field, model, direct, m2m 
                except models.FieldDoesNotExist,e:
                    dtlrep = report._inlines.get(fieldname,None)
                    if dtlrep != None:
                        col = DetailColumn(self,
                                           fieldname,
                                           dtlrep,
                                           len(columns),
                                           picture)
                    else:
                        col = MethodColumn(report,
                                           fieldname,
                                           len(columns),
                                           picture)
                else:
                    col = self.new_column(field,len(columns),picture)
                columns.append(col)
                self.columns_by_name[fieldname] = col
        else:
            for field in meta.fields:
                col = self.new_column(field,len(columns))
                columns.append(col)
                self.columns_by_name[field.name] = col
        self.columns = columns
        
        

class TextReportRenderer(ColumnsReportRenderer):
    def __init__( self,
                  report,
                  master_instance=None,
                  width=79,
                  columnWidths=None,
                  columnSep="|",
                  columnHeaderSep='-',
                  column_widths=None,
                  rowHeight=None,
                  flt=None):
        self.width = width
        self.columnWidths = columnWidths
        self.column_widths = column_widths
        self.rowHeight = rowHeight
        self.columnHeaderSep = columnHeaderSep
        self.columnSep = columnSep
        if flt is None:
            flt = report.default_filter
        self.flt = flt
        ColumnsReportRenderer.__init__(self,report,master_instance)
                             
  
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
        self.computeWidths()
        wrappers = []
        for col in self.columns:
            wrappers.append(TextWrapper(col.width))
        width = self.width + len(self.columnSep)*(len(self.columns)-1)

        writer=StringIO()
        
        # renderHeader

        title=self.get_title()
        if title is not None:
            writer.write(title+"\n")
            writer.write("="*len(title)+"\n")
            
        # wrap header labels:
        headerCells = []
        headerHeight = 1
        i = 0
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
        
        queryset = self._build_queryset(flt=self.flt)
        #queryset=self.report.queryset
        #print queryset.count()
        for obj in queryset:
            wrappedCells = []
            for col in self.columns:
                v = col.cell_value(obj,None)
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
        
    def detail_to_string(self,dtlrep,instance):
        r = TextReportRenderer(dtlrep,instance)
        return r.render()
      

#~ class HtmlReportRenderer(ColumnsReportRenderer):
  
    #~ def __init__( self,
                  #~ report,
                  #~ flt=None):
        #~ if flt is None:
            #~ flt=report.default_filter
        #~ self.flt=flt
        #~ ColumnsReportRenderer.__init__(self,report)
                             
  
    #~ def render_to_string(self):
        #~ s = "<table><tr>"
        #~ for col in self.columns:
            #~ s += "<th>%s</th>" % col.label
        #~ s += "</tr>"
        #~ queryset = self._build_queryset(flt=self.flt)
        #~ for obj in queryset:
            #~ s += "<tr>"
            #~ for col in self.columns:
                #~ v=col.cell_value(obj,None)
                #~ if v is None:
                    #~ v=''
                #~ s += "<td>%s</td>" % unicode(v)
            #~ s += "</tr>"
        #~ s += "</table>"
        #~ return mark_safe(s)


class ViewReportRenderer(ReportRenderer):
  
    editing = 0
    
    def __init__(self,request,is_main,*args,**kw):
        ReportRenderer.__init__(self,*args,**kw)
        self.request = request
        self.is_main = is_main
        #self.prefix = prefix
        flt = self.report.default_filter
        if is_main:
            self.params = self.report.param_form(request.GET)
            if self.params.is_valid():
                flt = self.params.cleaned_data.get('flt',
                    self.report.default_filter)
        self.queryset = self._build_queryset(flt)
        #self.main_menu = settings.MAIN_MENU


    def again(self,*args,**kw):
        return again(self.request,*args,**kw)
      
    def can_change(self):
        return self.report.can_change(self.request)
            
    def render_to_response(self,**kw):
        url = get_redirect(self.request)
        if url:
            return HttpResponseRedirect(url)
        context = lino_site.context(self.request,
          report = self,
          title = self.get_title(),
          form_action = self.again(editing=None),
        )
        return render_to_response(self.template_to_reponse,
          context,
          context_instance=template.RequestContext(self.request))
        
    def render_to_string(self):
        context=dict(
          report = self,
        )
        return render_to_string(self.template_to_string,context)
        
    #~ def detail_to_string(self,dtlrep,instance):
        #~ r = self.detail_renderer(self.request,False,dtlrep,instance)
        #~ return r.render_to_string()
        #~ except Exception,e:
            #~ print "Exception in RowViewReportRenderer.render_detail()"
            #~ traceback.print_exc()
            #~ raise e
            
      
class ViewManyReportRenderer(ViewReportRenderer):
  
    page_length = 15
    start_page = 1
    max_num = 0
    
    template_to_string = "lino/includes/grid_show.html"
    template_to_reponse = "lino/grid_show.html"      
    
    def __init__(self,*args,**kw) : 
        ViewReportRenderer.__init__(self,*args,**kw)
        if self.is_main:
            pgn = self.request.GET.get('pgn')
            if pgn is None:
                pgn = self.start_page
            else:
                pgn=int(pgn)
            pgl = self.request.GET.get('pgl')
            if pgl is None:
                pgl = self.page_length
            else:
                pgl = int(pgl)
          
            paginator = Paginator(self.queryset,pgl)
            try:
                page = paginator.page(pgn)
            except (EmptyPage, InvalidPage):
                page = paginator.page(paginator.num_pages)
            self.page=page

        #~ details = {}
        #~ for name in self.report.detail_reports.split():
            #~ def render(instance):
                #~ meth = getattr(instance,name)
                #~ dtlrep = meth()
                #~ return mark_safe(unicode(dtlrep))
            #~ details[name] = render
        #~ self.details = details
        
    #~ def render(self):
        #~ context=dict(
          #~ report=self,
          #~ main_menu=settings.MAIN_MENU,
          #~ title=self.report.get_title(),
        #~ )
        #~ return render_to_response("tom/grid_show.html",context)
    
        
    def position_string(self):
        return  "Page %d of %d." % (self.page.number,
          self.page.paginator.num_pages)
        
    def navigator(self):
        s="""
        <div class="pagination">
        <span class="step-links">
        """
        page = self.page
        #num_pages = self.page.paginator.num_pages
            
        text = "&#x25C4;Previous"
        if page.has_previous():
            s += '<a href="%s">%s</a>' % (
              self.again(pgn=page.number-1),text)
        else:
            s += text
        s += " "
        text = "Next&#x25BA;"
        if page.has_next():
            s += '<a href="%s">%s</a>' % (
              self.again(pgn=page.number+1),text)
        else:
            s += text
        s += " "
        
        s += """
        <span class="current">%s</span>
        """ % self.position_string()

        if self.can_change():
            if self.editing:
                s += ' <a href="%s">%s</a>' % (
                  self.again(editing=0),"show")
            else:
                s += ' <a href="%s">%s</a>' % (
                  self.again(editing=1),"edit")
        s += ' <a href="%s">%s</a>' % (self.again('pdf'),"pdf")
        s += """
        </span>
        </div>
        """     
        return mark_safe(s)
        
    def rows(self):
        if self.master_instance is None:
            rownum = self.page.start_index()
            object_list = self.page.object_list
        else:
            rownum = 1
            object_list = self.queryset
        #rownum = self.page.start_index()
        for obj in object_list:
            yield Row(self,obj,rownum)
            rownum += 1

ViewManyReportRenderer.detail_renderer = ViewManyReportRenderer



class RowViewReportRenderer(ViewReportRenderer):
    "A ViewReportRenderer that renders a single Row."
    detail_renderer = ViewManyReportRenderer
    def __init__(self,row,*args,**kw):
        assert issubclass(self.detail_renderer,ViewManyReportRenderer)
        ViewReportRenderer.__init__(self,*args,**kw)
        rownum = int(row)
        try:
            obj = self.queryset[rownum-1]
        except IndexError:
            rownum = self.queryset.count()
            if rownum == 0:
                raise Http404("queryset is empty")
            obj = self.queryset[rownum-1]
        self.row = Row(self,obj,rownum)
        
    def position_string(self):
        return  "Row %d of %d." % (self.row.number,self.queryset.count())
        
    #~ def get_title(self):
        #~ return u"%s - %s" % (self.report.get_title(self),self.instance)
        
      
        
class ViewOneReportRenderer(RowViewReportRenderer):

    template_to_string = "lino/includes/page_show.html"
    template_to_reponse = "lino/page_show.html"
    
    def __init__(self,*args,**kw):
        RowViewReportRenderer.__init__(self,*args,**kw)
        
        #~ details = {}
        #~ for name in self.report.detail_reports.split():
            #~ meth = getattr(self.row.instance,name)
            #~ dtlrep = meth()
            #~ r = self.detail_renderer(dtlrep,request,name,
                #~ self.row.instance,dtlrep.fk_name)
            #~ details[name] = lambda x: r.render_to_string()
        #~ self.details = details
        
        #~ self.layout = layouts.RowLayoutRenderer(self.row,
            #~ self.page_layout(),self.details)
            
        #~ self.layout = layouts.RowLayoutRenderer(self.row,
            #~ self.report.page_layout(),self.render_detail)
            
        self.layout = self.report.page_layout().bound_to(self.row)
            
        
    def navigator(self):
        s="""<div class="pagination"><span class="step-links">"""
        s += '<a href="%s">%s</a>' % (
          self.again("..",editing=None),self.get_title())

        page = self.row
        get_var_name = "row"

        text = "&#x25C4;Previous"
        if page.has_previous():
            s += '<a href="%s">%s</a>' % (
              self.again("../" +str(page.number-1)),
              text)
        else:
            s += text
        s += " "
        text = "Next&#x25BA;"
        if page.has_next():
            s += '<a href="%s">%s</a>' % (
              self.again("../" + str(page.number+1)),
              text)
              #self.again(**{get_var_name: page.number+1}),text)
        else:
            s += text
        s += " "
        s += '<span class="current">%s</span>' % self.position_string()
        if self.can_change():
            if self.editing:
                s += ' <a href="%s">%s</a>' % (
                  self.again(editing=0),"show")
            else:
                s += ' <a href="%s">%s</a>' % (
                  self.again(editing=1),"edit")
        s += ' <a href="%s">%s</a>' % (self.again('print'),"print")
        s += ' <a href="%s">%s</a>' % (self.again('pdf'),"pdf")
        s += """</span></div>"""     
        return mark_safe(s)




class EditReportRenderer:  # Mixin class
  
    editing = 1
    
    def new_column(self,field,*args):
        if field.editable and not field.primary_key:
            return FormFieldColumn(self,field,*args)
        return FieldColumn(self,field,*args)
        

class EditManyReportRenderer(EditReportRenderer,ViewManyReportRenderer):
    extra = 1
    can_delete = True
    can_order = False
    template_to_string = "lino/includes/grid_edit.html"
    template_to_reponse = "lino/grid_edit.html"
        
    def __init__(self,*args,**kw):
        ViewManyReportRenderer.__init__(self,*args,**kw)
        #print self.__class__.__name__,"__init__()"
        
        fs_args = {}
        if self.report.master is not None:
            formset_class = inlineformset_factory(
                  self.report.master,
                  self.report.model,
                  fk_name=self.report.fk_name,
                  extra=self.extra, 
                  max_num=self.max_num,
                  can_order=self.can_order, 
                  can_delete=self.can_delete)
            fs_args['instance'] = self.master_instance
        else:
            formset_class = modelformset_factory(
                  self.report.model,
                  extra=self.extra, 
                  max_num=self.max_num,
                  can_order=self.can_order, 
                  can_delete=self.can_delete)
            fs_args['queryset'] = self.page.object_list

        
        if self.request.method == 'POST':
            fs = formset_class(self.request.POST,**fs_args)
            if fs.is_valid():
                #print self.__class__.__name__, "valid"
                fs.save()
                if self.can_delete and fs.deleted_forms:
                    for form in fs.deleted_forms:
                        print "Deleted:", form.instance
                editing.stop_editing(self.request)
                """
                start from begin because paginator and page must reload
                e.g. if an instance has been added, it may now be at 
                a different row and the page count may have changed.
                """
                #return HttpResponseRedirect(self.again(editing=None))
                redirect_to(self.request,self.again(editing=None))
            else:
                print fs.errors
                editing.continue_editing(self.request)
        else:
            #print self.__class__.__name__, "not POST"
            fs = formset_class(**fs_args)
        self.formset = fs
        #print self.__class__.__name__, "__init__() done"
        

    def rows(self):
        if self.is_main:
            rownum = self.page.start_index()
        else:
            rownum = 1
        for form in self.formset.forms:
            yield Row(self,form.instance,rownum,form)
            rownum += 1

    
class EditOneReportRenderer(EditReportRenderer,ViewOneReportRenderer):
    detail_renderer = EditManyReportRenderer
    template_to_string = "lino/includes/page_edit.html"
    template_to_reponse = "lino/page_edit.html"      
  
    def __init__(self,*args,**kw):
        ViewOneReportRenderer.__init__(self,*args,**kw)
        if self.request.method == 'POST':
            frm = self.report.form_class(self.request.POST,
              instance=self.row.instance)
            if frm.is_valid():
                #print self.__class__.__name__, "valid"
                frm.save()
                editing.stop_editing(self.request)
                redirect_to(self.request,self.again(editing=None))
                #return HttpResponseRedirect(self.again(editing=None))
            else:
                print frm.errors
                editing.continue_editing(self.request)
        else:
            frm = self.report.form_class(instance=self.row.instance)
        self.form = frm
        
        # hack: no need to instanciate a new Row for this...
        self.row.form = frm
        
        self.layout = self.report.page_layout().bound_to(self.row)
        
        #self.row = Row(self,self.instance,self.rownum,frm)
        #print self.__class__.__name__, "__init__() done"

        
class PdfManyReportRenderer(ViewManyReportRenderer):

    def render(self):
        template = get_template("lino/grid_pdf.html")
        context=dict(
          report=self,
          title=self.get_title(),
        )
        html  = template.render(Context(context))
        if not pisa:
            return HttpResponse(html)
        result = cStringIO.StringIO()
        pdf = pisa.pisaDocument(cStringIO.StringIO(html.encode("ISO-8859-1")), result)
        if pdf.err:
            raise Exception(cgi.escape(html))
        return HttpResponse(result.getvalue(),mimetype='application/pdf')
        
    def rows(self):
        rownum = 1
        for obj in self.queryset:
            yield Row(self,obj,rownum)
            rownum += 1

class PdfOneReportRenderer(ViewOneReportRenderer):
    detail_renderer = PdfManyReportRenderer

    def render(self):
        template = get_template("lino/page_pdf.html")
        #self.row = Row(self,obj,rownum)
        obj = self.row.instance
        #~ layout = layouts.InstanceLayoutRenderer(obj,
          #~ self.report.page_layout(),render_detail=self.render_detail)
        context = dict(
          report=self,
          title=u"%s - %s" % (self.get_title(),obj),
          #layout = layout
        )
        html  = template.render(Context(context))
        if not pisa:
            return HttpResponse(html)
        result = cStringIO.StringIO()
        pdf = pisa.pisaDocument(cStringIO.StringIO(\
                html.encode("ISO-8859-1")), result)
        if pdf.err:
            raise Exception(cgi.escape(html))
        return HttpResponse(result.getvalue(),
            mimetype='application/pdf')


class RowPrintReportRenderer(RowViewReportRenderer):
    def render(self):
        tplname = self.report.get_row_print_template(self.row.instance)
        context = dict(instance=self.row.instance)
        return render_to_response(tplname,context)



def sorry(request):
    context = lino_site.context(request,
      title = "Sorry",
    )
    return render_to_response("lino/sorry.html",
      context,
      context_instance = template.RequestContext(request))
