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
    master_instance = None
    def __init__(self,report,master_instance=None,layout=None,**kw):
        #from lino.django.tom.reports import Report
        #assert isinstance(report,Report)
        self.report = report
        report.setup()
        self.name = report.name
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
        if self.limit is None:
            # ListRenderer gets report.page_length as limit, but DetailRenderer shows one row per page and has a fixed limit 1 that doesn't come from Report
            self.limit = report.page_length
        self.page_length = report.page_length
        self.column_headers = report.column_headers
        #self.slaves = report.slaves
        #self.pk = report.model._meta.pk
        
        self.layout = self.get_layout()
        #~ layout = self.get_layout()
        #~ self.layout = layout.renderer(self)
        
    def get_title(self):
        return self.report.get_title(self)
        
    def get_layout(self) :
        raise NotImplementedError
        
    def unused_get_slave(self,name):
        # self.layout is now a LayoutRenderer, not a Layout
        return self.layout.get_slave(name)
        
    def unused_as_ext_store(self):
      try:
        return self.layout.store.as_ext_value()
      except Exception,e:
          traceback.print_exc(e)
        
    def old_as_ext_store(self):
      try:
        s = """
        new Ext.data.Store({
          id: '%s',
        """ % self.report.name
        s += """
          proxy: new Ext.data.HttpProxy({
              url: '%s',
              method: 'GET'
            }),
        """ % self.get_absolute_url(json=True)  # self.json_url()
        #~ if self.master:
            #~ s += """
              #~ baseParams:{ 'params': { 'master': '1' } },
            #~ """
        s += """
          remoteSort: true,
          reader: new Ext.data.JsonReader(
            { totalProperty: 'count', 
              root: 'rows', 
              id: '%s',
        """ % self.report.model._meta.pk.name
        s += "fields: [ %s ]" % ",".join([repr(e.name) for e in self.ext_store_fields])
        s += " } " 
        s += "  )}) "
        return mark_safe(s)
      except Exception,e:
          traceback.print_exc(e)

    #~ def as_ext_colmodel_editing(self):
        #~ return self.as_ext_colmodel(editing=True)
        
    def old_as_ext_colmodel(self,editing=False):
      try:
        editing = self.report.can_change.passes(self.request)
        l = [e.ext_column(editing) for e in self.layout.leaves()]
        s = "new Ext.grid.ColumnModel([ %s ])" % ", ".join(l)
        return mark_safe(s)
      except Exception,e:
          traceback.print_exc(e)

    def obj2json(self,obj):
        d = {}
        for e in self.layout.ext_store_fields:
            #if d.has_key(e.name):
            #    print "Duplicate field %s was %r and becomes %r" % (e.name,d[e.name],e.value2js(obj))
            d[e.name] = e.value2js(obj)
        return d
            

class ViewReportRenderer(ReportRenderer):
  
    #page_length = 10
    editing = 0
    selector = None
    #must_refresh = False
    offset = None
    sort_column = None
    sort_direction = None
    
    def __init__(self,request,is_main,report,*args,**kw):
      
        if is_main:
            self.params = report.param_form(request.GET)
            if self.params.is_valid():
                kw.update(self.params.cleaned_data)
            pk = request.GET.get('master',None)
            if pk is not None:
                kw.update(master_instance=report.master.objects.get(pk=pk))
            sort = request.GET.get('sort',None)
            if sort:
                self.sort_column = sort
                sort_dir = request.GET.get('dir','ASC')
                if sort_dir == 'DESC':
                    sort = '-'+sort
                    self.sort_direction = 'DESC'
                kw.update(order_by=sort)
            
            self.json = request.GET.get('json',False)
                

        #print "ViewReportRenderer.__init__() 1",report.name
        self.request = request
        ReportRenderer.__init__(self,report,*args,**kw)
        #print "ViewReportRenderer.__init__() 2",report.name
        if isinstance(self.queryset,QuerySet):
            self.total_count = self.queryset.count()
        else:
            # a Report may override get_queryset() and return a list
            self.total_count = len(self.queryset)
        
        if is_main:
            offset = request.GET.get('start',None)
            if offset:
                self.offset = offset
            limit = request.GET.get('limit',self.limit)
            if limit:
                self.limit = limit
        
        if self.offset is not None:
            self.queryset = self.queryset[int(self.offset):]
        if self.limit is not None:
            self.queryset = self.queryset[:int(self.limit)]
            
        self.is_main = is_main
        
        if is_main and not self.editing:
            self._actions = self.report.get_row_actions(self)
        else:
            self._actions = ()

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
        return self.report.get_absolute_url(**kw)
        
        
    def render_to_response(self):
        url = get_redirect(self.request)
        if url is not None:
            return HttpResponseRedirect(url)
        if self.json:
            return self.json_reponse()
            
        from lino.django.utils.sites import lino_site
        context = lino_site.context(self.request,
          report = self,
          #layout = self.layout,
          layout = self.layout.renderer(self),
          title = self.get_title(),
          #form_action = self.again(editing=None),
        )
        if self.report.help_url is not None:
            context['help_url'] = self.report.help_url
        return render_to_response(self.template_to_reponse,
            context,
            context_instance=template.RequestContext(self.request))
        
    def json_reponse(self):
        rows = [ self.obj2json(row) for row in self.queryset ]
        d = dict(count=self.total_count,rows=rows)
        s = simplejson.dumps(d,default=unicode)
        #print s
        return HttpResponse(s, mimetype='text/html')
        
            
      
class ListViewReportRenderer(ViewReportRenderer):
  
    start_page = 1
    max_num = 0
    
    template_to_string = "lino/includes/grid.html"
    template_to_reponse = "lino/grid.html"
    
    def get_layout(self):
        return self.report.row_layout
        
        
    def must_refresh(self):
        redirect_to(self.request,self.again()) 
        
    
        

ListViewReportRenderer.detail_renderer = ListViewReportRenderer



class RowViewReportRenderer(ViewReportRenderer):
    "A ViewReportRenderer that renders a single Row."
    limit = 1
    detail_renderer = ListViewReportRenderer
    def __init__(self,*args,**kw):
        assert issubclass(self.detail_renderer,ListViewReportRenderer)
        #kw.update(limit=1)
        ViewReportRenderer.__init__(self,*args,**kw)
        if self.queryset.count() == 0:
            raise "No record found"
        if self.queryset.count() > 1:
            raise "Found more than one record"
        self.instance = self.queryset[0]
            
    def get_layout(self):
        return self.report.page_layout
        
    def get_absolute_url(self,**kw):
        kw['mode'] = 'detail'
        return ViewReportRenderer.get_absolute_url(self,**kw)
        
    
      
        
class ViewOneReportRenderer(RowViewReportRenderer):

    template_to_reponse = "lino/page.html"
    
        

    def get_title(self):
        return unicode(self.instance)


        
class PdfManyReportRenderer(ListViewReportRenderer):

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
        pdf = pisa.pisaDocument(cStringIO.StringIO(html.encode("ISO-8859-1")), result)
        if pdf.err:
            raise Exception(cgi.escape(html))
        return HttpResponse(result.getvalue(),mimetype='application/pdf')
        
    def rows(self):
        rownum = 1
        for obj in self.queryset:
            yield Row(self,obj,rownum,None)
            rownum += 1

def unused_render_to_pdf(obj):
    tplbases = [ obj._meta.db_table, "lino/page" ]
    tplnames = [ x + ".tex" for x in tplbases ]
    context = dict(
      #report=self,
      instance=obj,
      #title = unicode(obj),
      #title=u"%s - %s" % (self.get_title(),obj),
      #layout = layout
    )
    return latex.process_latex(tplnames,context)
    #~ template = select_template(tpls)
    #~ tex = template.render(Context(context))
    #~ tex = tex.encode("utf-8")
    #~ file('tmp.tex','w').write(tex)
    #~ os.system("pdflatex tmp.tex")
    #~ if not os.path.exists("tmp.pdf"):
        #~ raise Exception("tmp.pdf not created")
    #~ return "tmp.pdf"

def unused_as_printable(obj,as_pdf=True,model=None):
    #~ if model is None:
        #~ tn = obj._meta.db_table + "_print.html"
    #~ else:
        #~ tn = model._meta.db_table + "_print.html"
    tplnames = [ obj._meta.db_table, "lino/page" ]
    tpls = [ x + "_printable.html" for x in tplnames ]
    template = select_template(tpls)
    
    context = dict(
      #report=self,
      instance=obj,
      title = unicode(obj),
      #title=u"%s - %s" % (self.get_title(),obj),
      #layout = layout
    )
    html = template.render(Context(context))
    if not as_pdf:
        return html
    html = html.encode("ISO-8859-1")
    #file('tmp.html','w').write(html)
    result = cStringIO.StringIO()
    pdf = pisa.pisaDocument(cStringIO.StringIO(html), result)
    if pdf.err:
        raise Exception("pisa.pisaDocument.err is %r" % pdf.err)
    return result.getvalue()

  
class PdfOneReportRenderer(ViewOneReportRenderer):
    detail_renderer = PdfManyReportRenderer

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





class unused_ElementServer:
    def __init__(self,form):
        self.form = form # form may be None
        
    def old_render_field(self,elem):
        if self.form is None:
            return self.field_as_readonly(elem)
        try:
            bf = self.form[elem.name] # a BoundField instance
        except KeyError,e:
            return self.field_as_readonly(elem)
            
        if bf.field.widget.is_hidden:
            return self.field_as_readonly(elem)
        #field.setup_widget(bf.field.widget)
        
        widget = bf.field.widget
        if isinstance(widget,forms.widgets.Input):
            widget.attrs.update(size=elem.width)
        elif isinstance(widget,forms.Textarea):
            widget.attrs.update(cols=elem.width,
                                rows=elem.height)
        
        s = bf.as_widget()
        if elem.layout.show_labels and bf.label:
            if isinstance(bf.field.widget, forms.CheckboxInput):
                s = s + " " + bf.label_tag()
            else:
                s = bf.label_tag() + "<br/>" + s
        #print "render_field()", repr(bf.errors)
        s += unicode(bf.errors)
        return mark_safe(s)
        
    def get_value(self,elem):
        raise NotImplementedError

    def get_model_field(self,elem):
        raise NotImplementedError

    def old_field_as_readonly(self,elem,with_links=False):
        try:
            value = self.get_value(elem)
            model_field = self.get_model_field(elem)
            if model_field is None:
                if hasattr(value,"field"):
                    #print "it is a method"
                    field = value.field
                    value = value()
                    #print value
                    if field.verbose_name:
                        label = field.verbose_name
                    else:
                        label = elem.name.replace('_', ' ')
                    #print label
                    widget = field.formfield().widget
                    #print widget
                else:
                    #~ from lino.django.tom import reports
                    #~ if isinstance(value,reports.Report):
                        #~ return value.as_html()
                    #label = self.name
                    label = elem.name.replace('_', ' ')
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
                
            style = widget.attrs.get('style','')
            if elem.width is not None:
                style += "min-width:%dem;" % elem.width
            else:
                style += "width:100%;"
            if elem.height is not None:
                style += "min-height:%dem;" % (elem.height * 2)
                # TODO: 
                
            #print field_element.name, repr(value)
            
            if isinstance(widget, forms.CheckboxInput):
                if value:
                    s = "[X]"
                else: 
                    s = "[&nbsp;&nbsp;]"
                s = SPAN(s,style="width:2em;" )
                if elem.layout.show_labels:
                    s += " " + label
                return mark_safe(s)
                
            #~ if value is None: # or len(value) == 0:
                #~ value = '&nbsp;'
            #~ else:
                #~ value = unicode(value)
                
            if callable(value):
                value = value()
                
            if isinstance(value,Manager):
                value = "<br/>".join(
                  [HREF(get_instance_url(o),
                    unicode(o)) for o in value.all()])
            elif hasattr(value,'__iter__'):
                value = "<br/>".join(
                  [unicode(x) for x in value])
            elif value is None:
                value = '&nbsp;'
            elif with_links and isinstance(value,models.Model):
                url = get_instance_url(value)
                value = HREF(url,value)
            elif with_links and isinstance(model_field,models.URLField):
                value = HREF(value,short_link(value))
            else:
                value = unicode(value)
                if len(value) == 0:
                    value = '&nbsp;'
            s = SPAN(value,style)
            if elem.layout.show_labels:
                s = label + "<br/>" + s
            return mark_safe(s)
        except Exception, e:
            traceback.print_exc(e)
            raise
            
        
class unused_DialogRenderer(unused_ElementServer):
  
    def __init__(self,dialog,request):
        self.dialog = dialog
        self.request = request
        self.result = None
        if request.method == 'POST': 
            form = dialog.form_class(request.POST) 
            if form.is_valid(): 
                self.result = form.execute()
        else:
            form = dialog.form_class() 
        unused_ElementServer.__init__(form)
            
    def get_value(self,elem):
        return self.form[elem.name]

    def get_model_field(self,elem):
        return None

    def again(self,*args,**kw):
        return again(self.request,*args,**kw)
        
    def render_to_response(self,**kw):
        url = get_redirect(self.request)
        if url:
            #print "render_to_response() REDIRECT TO ", url
            return HttpResponseRedirect(url)
        from lino.django.utils.sites import lino_site
        context = lino_site.context(self.request,
          report = self,
          title = self.get_title(),
          #form_action = self.again(editing=None),
        )
        return render_to_response(self.template_to_reponse,
            context,
            context_instance=template.RequestContext(self.request))
        
        

        

class unused_Row(unused_ElementServer):
    def __init__(self,renderer,instance,number,dtl=None,form=None):
        unused_ElementServer.__init__(self,form)
        self.renderer = renderer
        self.report = renderer.report
        self.number = number
        self.instance = instance
        self.dtl = dtl
        
        return # remaining code not used with extjs
        #print "Row.__init__()", self.instance.pk
        self.inline_renderers = {}
        if dtl is not None:
            for name,inline in self.report._inlines.items():
                self.inline_renderers[name] = \
                  renderer.detail_renderer(renderer.request,
                    False,inline,self.instance)
      
        
    def as_html(self):
        return self.report.row_layout.bound_to(self).as_html()
            

    def unused_links(self):
        l = []
        #~ l.append('<a href="%s">%s</a>' % (
            #~ self.get_url_path(),unicode(self.instance)))
        if self.renderer.has_actions():
            l.append(unicode(
              self.renderer.selector[IS_SELECTED % self.number]))
        #print "<br/>".join(l)
        return mark_safe("<br/>".join(l))
        
        
        
    def management(self):
        return '' # not used with extjs
        #print "row_management", self.element
        try:
            l = []
            if self.renderer.editing:
                l.append("%d%s" % (self.number,self.pk_field()))
                if self.renderer.can_delete:
                    l.append(self.form["DELETE"])
            else:
                l.append(str(self.number))
                
            if self.renderer.has_actions():
                l.append(unicode(
              self.renderer.selector[IS_SELECTED % self.number]))

            return mark_safe("<br/>".join(l))
        except Exception,e:
            print "Exception in Row.management() %s:" % \
                 self.renderer.request.path
            traceback.print_exc()
            raise e
        

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
        if self.renderer.is_main:
            return self.renderer.again(str(self.number))
        return get_instance_url(self.instance)
        
        
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
        
    def render_inline(self,elem):
        return self.inline_renderers[elem.name].render_to_string()
            
    def get_value(self,elem):
      try:
        return getattr(self.instance,elem.name)
      except Exception,e:
        print "[TODO] No field %s in %s" % (elem.name,self.instance.__class__.__name__)

    def get_model_field(self,elem):
        try:
            return self.instance._meta.get_field(elem.name)
        except models.FieldDoesNotExist,e:
            return None


