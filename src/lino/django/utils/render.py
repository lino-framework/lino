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
from django.db.models.manager import Manager

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string, get_template, select_template, Context

try:
    # l:\snapshot\xhtml2pdf
    import ho.pisa as pisa
except ImportError:
    pisa = None


#from lino.reports.constants import *
from lino.django.utils import layouts
from lino.django.utils.requests import again, get_redirect, redirect_to
#from lino.django.utils.editing import is_editing, stop_editing
from lino.django.utils import editing
from lino.django.utils.sites import site as lino_site


class ElementServer:
    def __init__(self,form):
        self.form = form # form may be None
        
    def render_field(self,elem):
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

    def field_as_readonly(self,elem):
        value = self.get_value(elem)
        model_field = self.get_model_field(elem)
        if model_field is None:
            if isinstance(value,Manager):
                try:
                    value = "<br/>".join(
                      [unicode(o) for o in value.all()])
                    label = elem.name
                    #widget=widget_for_value(value)
                    widget = forms.TextInput()
                except Exception, e:
                    print e
            # so it is a method
            elif hasattr(value,"field"):
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
                value = value()
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
            
        #print field_element.name, repr(value)
        
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
            if elem.layout.show_labels:
                s += " " + label
            return mark_safe(s)
            
        #~ if value is None: # or len(value) == 0:
            #~ value = '&nbsp;'
        #~ else:
            #~ value = unicode(value)
        
        
        style = widget.attrs.get('style','')
        if elem.width is not None:
            style += "min-width:%dem;" % elem.width
        else:
            style += "width:100%;"
        if elem.height is not None:
            style += "min-height:%dem;" % (elem.height * 2)
            # TODO: 
            
        if isinstance(widget, forms.SelectMultiple):
            s = "[ " + ",<br/>".join([unicode(o) for o in value.all()]) + " ]"
            s = SPAN(s,style)
        elif isinstance(widget, forms.Select):
            s = "[&nbsp;" + unicode(value) + "&nbsp;]"
            s = SPAN(s,style)
        else:
            if value is None:
                value = '&nbsp;'
            else:
                value = unicode(value)
                if len(value) == 0:
                    value = '&nbsp;'
            s = SPAN(value,style)
            
        if elem.layout.show_labels:
            s = label + "<br/>" + s
        return mark_safe(s)
        

        

class Row(ElementServer):
    def __init__(self,renderer,instance,number,dtl=None,form=None):
        ElementServer.__init__(self,form)
        self.renderer = renderer
        self.report = renderer.report
        self.number = number
        self.instance = instance
        self.dtl = dtl
        
        #print "Row.__init__()", self.instance.pk
        self.inline_renderers = {}
        if dtl is not None:
        #if renderer.is_main:
            for name,inline in self.report._page_layouts[dtl]._inlines.items():
                self.inline_renderers[name] = \
                  renderer.detail_renderer(renderer.request,
                    False,inline,self.instance)
      
    #~ def __getitem__(self,name):
        #~ if self.renderer.editing:
            #~ return self.form[name]
        #~ return getattr(self.instance,name)

        
    def as_html(self):
        try:
            #return r.render_to_string()
            return self.report.row_layout.bound_to(self).as_html()
        except Exception,e:
            print "Exception in Row.as_html():"
            traceback.print_exc()
            raise e

    def links(self):
        l = []
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
        
    def render_inline(self,elem):
        return self.inline_renderers[elem.name].render_to_string()
            
    def get_value(self,elem):
        return getattr(self.instance,elem.name)

    def get_model_field(self,elem):
        try:
            return self.instance._meta.get_field(elem.name)
        except models.FieldDoesNotExist,e:
            return None



class ReportRenderer:
    def __init__(self,report,master_instance=None,**params):
        #from lino.django.tom.reports import Report
        #assert isinstance(report,Report)
        self.report = report
        self.column_headers = report.column_headers
        #self.title = self.report.get_title()
        if report.master is None:
            assert master_instance is None
        else:
            assert master_instance is None or isinstance(master_instance,report.master)
        self.master_instance = master_instance
        #print self.__class__.__name__, "__init__()"
        #self.params = params
        self.queryset = report.get_queryset(master_instance,**params)
        

    def get_title(self):
        return self.report.get_title(self)
        
        
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
        


class ViewReportRenderer(ReportRenderer):
  
    editing = 0
    
    def __init__(self,request,is_main,report,*args,**kw):
        if is_main:
            self.params = report.param_form(request.GET)
            if self.params.is_valid():
                kw.update(self.params.cleaned_data)
        ReportRenderer.__init__(self,report,*args,**kw)
        self.request = request
        self.is_main = is_main


    def again(self,*args,**kw):
        return again(self.request,*args,**kw)
      
    #~ def can_change(self):
        #~ return self.report.can_change(self.request)
            
    def render_to_response(self,**kw):
        url = get_redirect(self.request)
        if url:
            #print "render_to_response() REDIRECT TO ", url
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
                pgn = int(pgn)
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

        
    #~ def position_string(self):
        #~ return  "Page %d of %d." % (self.page.number,
          #~ self.page.paginator.num_pages)
          
    def position_string(self):
        s = "Page %d of %d" % (self.page.number,self.page.paginator.num_pages)
        s += ' in <a href="%s">%s</a>.' % (
            self.again("",editing=None),self.report.get_title(self))
        return mark_safe(s)
        
          
        
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
        
        #~ s += """
        #~ <span class="current">%s</span>
        #~ """ % self.position_string()

        #if self.can_change():
        if self.editing:
            s += ' <a href="%s">%s</a>' % (
              self.again(editing=0),"show")
        else:
            s += ' <a href="%s">%s</a>' % (
              self.again(editing=1),"edit")
        s += ' <a href="%s">%s</a>' % (self.again('pdf'),"pdf")
        s += "</span>"
        s += ' <span class="position">%s</span>' % self.position_string()
        s += "</div>"
        return mark_safe(s)
        
        
    def rows(self):
        try:
            if self.master_instance is None:
                rownum = self.page.start_index()
                object_list = self.page.object_list
            else:
                rownum = 1
                object_list = self.queryset
            #rownum = self.page.start_index()
            print len(object_list)
            for obj in object_list:
                yield Row(self,obj,rownum,None)
                rownum += 1
        except Exception,e:
            traceback.print_exc(e)
            raise

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
        if self.is_main:
            tab = self.request.GET.get('tab')
            if tab is None:
                tab = 0
            else:
                tab = int(tab)
        self.row = Row(self,obj,rownum,tab)
        self.tab = tab
        layout = self.report._page_layouts[tab]
        self.layout = layout.bound_to(self.row)
        
    def tabs(self):
        if len(self.report._page_layouts) == 1:
            return ''
        s = '<ul class="tab">'
        i = 0
        for layout in self.report._page_layouts:
            title = layout.get_label()
            if i == self.tab:
                s += '<li class="tab_selected">%s</li>' % title
            else:
                href = self.again(tab=i)
                s += '<li><a href="%s">%s</a>' % (href,title)
            i += 1
        s += "</ul>"
        return mark_safe(s)
        
    def position_string(self):
        s = "Row %d of %d" % (self.row.number,self.queryset.count())
        s += ' in <a href="%s">%s</a>.' % (
            self.again("..",editing=None),self.report.get_title(self))
        return mark_safe(s)
        
        
      
        
class ViewOneReportRenderer(RowViewReportRenderer):

    template_to_string = "lino/includes/page_show.html"
    template_to_reponse = "lino/page_show.html"
    
    #~ def __init__(self,*args,**kw):
        #~ RowViewReportRenderer.__init__(self,*args,**kw)
        #~ layout = self.report._page_layouts[self.dtl]
        #~ self.layout = layout.bound_to(self.row)
            
        
    def navigator(self):
        s="""<div class="pagination"><span class="step-links">"""
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
        #if self.can_change():
        if self.editing:
            s += ' <a href="%s">%s</a>' % (
              self.again(editing=0),"show")
        else:
            s += ' <a href="%s">%s</a>' % (
              self.again(editing=1),"edit")
        s += ' <a href="%s">%s</a>' % (self.again('print'),"print")
        s += ' <a href="%s">%s</a>' % (self.again('pdf'),"pdf")
        s += '</span>'
        s += '<span class="position">%s</span>' % self.position_string()
        s += '</div>'
        return mark_safe(s)

    def get_title(self):
        return unicode(self.row.instance)
        



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
                #redirect_to(self.request,self.again(editing=None))
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
            yield Row(self,form.instance,rownum,None,form)
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
                #redirect_to(self.request,self.again(editing=None))
                #return HttpResponseRedirect(self.again(editing=None))
            else:
                print frm.errors
                editing.continue_editing(self.request)
        else:
            frm = self.report.form_class(instance=self.row.instance)
        self.form = frm
        
        self.row.form = frm
        
        #self.layout = self.report.page_layout().bound_to(self.row)
        
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
            yield Row(self,obj,rownum,None)
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



class DialogRenderer(ElementServer):
  
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
        ElementServer.__init__(form)
            
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
        context = lino_site.context(self.request,
          report = self,
          title = self.get_title(),
          form_action = self.again(editing=None),
        )
        return render_to_response(self.template_to_reponse,
            context,
            context_instance=template.RequestContext(self.request))
        
        
