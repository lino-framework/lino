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
from django.forms.models import modelform_factory
from django.forms.models import modelformset_factory
from django.conf.urls.defaults import patterns, url, include
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, InvalidPage



# maps Django field types to a tuple of default paramenters
# each tuple contains: minWidth, maxWidth, is_filter
WIDTHS = {
    models.IntegerField : (2,10,False),
    models.CharField : (10,40,True),
    models.TextField :  (10,40,True),
    models.ForeignKey : (5,40,False),
    models.AutoField : (2,10,False),
}


def urlparams(**kw):
    s=""
    for k,v in kw.items():
        s += "?"+k+"="+str(v)
    return s

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
        

class ReportColumn(object):
    
    def __init__(self, field,index):
        assert type(index) == int
        self.field = field
        self.width = None
        self.index=None
        self.halign=LEFT
        self.valign=TOP
        self.index=index
        self.is_filter = WIDTHS[self.field.__class__][2]

        
    def getCellValue(self,row_instance):
        return getattr(row_instance,self.field.name)

    def getMinWidth(self):
        x=WIDTHS[self.field.__class__]
        w=x[0]
        w = max(w,len(self.getLabel()))
        return w
        
    def getMaxWidth(self):
        x=WIDTHS[self.field.__class__]
        return x[1]
        
    def getLabel(self):
        return self.field.verbose_name

    def format(self,value):
        return unicode(value)
        

from django import forms

class ReportParameterForm(forms.Form):
    pgn = forms.IntegerField(required=False,label="Page number") 
    pgl = forms.IntegerField(required=False,label="Rows per page")
    flt = forms.CharField(required=False,label="Text filter")

#        
#  Report
#        
    
class Report:
    
    queryset = None 
    title = None
    width = None
    columnWidths = None
    columnNames = None
    rowHeight = None
    modelForm = None
    page_length = 15
    label = None
    param_form = ReportParameterForm
    
    def __init__(self):
        self.groups = [] # for later
        self.totals = [] # for later
        self.columns = []
        if self.label is None:
            self.label = self.__class__.__name__
        if self.modelForm is None:
            self.modelForm = modelform_factory(self.queryset.model)
        meta = self.queryset.model._meta
        for field_name in self.columnNames.split():
            field = meta.get_field_by_name(field_name)[0]
            self.columns.append(ReportColumn(field,len(self.columns)))

    def getTitle(self):
        """
        returns None if this report has no title
        """
        return self.title
        
    def getLabel(self):
        return self.label
    

    def computeWidths(self,columnSepWidth):
        
        """set total width or distribute available width to columns
        without explicit width. Note that these widths are to be
        interpreted as logical widths.

        """
        
        if self.columnWidths is not None:
            i = 0
            for item in self.columnWidths.split():
                col = self.columns[i]
                if item.lower() == "d":
                    col.width = col.getMinWidth()
                elif item == "*":
                    col.width = None
                else:
                    col.width = int(item)
                i += 1

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


        
    ##
    ## public methods for user code
    ##

    def __unicode__(self):
        return unicode(self.as_text())
        
        
    def as_text(self, columnSep='|',
                      lineWidth=79,
                      columnHeaderSep='-',
                      ):
        writer=StringIO()
        self.computeWidths(columnSepWidth=len(columnSep))
        wrappers = []
        for col in self.columns:
            wrappers.append(TextWrapper(col.width))
        width = self.width + len(columnSep)*(len(self.columns)-1)

        # renderHeader

        title=self.getTitle()
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
            writer.write(self._row_as_text(headerCells,i,columnSep))
                               
        l = [ columnHeaderSep * col.width
              for col in self.columns]
        writer.write("+".join(l) + "\n")
        

        for obj in self.queryset:
            wrappedCells = []
            for col in self.columns:
                v=col.getCellValue(obj)
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
                writer.write(self._row_as_text(wrappedCells,0,columnSep))
            else:
                # vfill each cell:
                for j in range(len(self.columns)):
                    vfill(wrappedCells[j],
                          self.columns[j].valign,
                          rowHeight)

                for i in range(rowHeight):
                    writer.write(self._row_as_text(
                        wrappedCells,i,columnSep))
        
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
        
    def get_urls(self,name):
        urlpatterns = patterns('',
          url(r'^%s$' % name, 
            self.view_list))
        urlpatterns += patterns('',
          url(r'^%s/(?P<row>\d+)$' % name,
            self.view_page))
        return urlpatterns
        

    def view_list(self,request):
        params = self.param_form(request.GET)
        if params.is_valid():
            pgn = params.cleaned_data['pgn'] or 1
            pgl = params.cleaned_data['pgl'] or self.page_length
            flt = params.cleaned_data['flt'] or ''
        else: 
            pgn = 1
            pgl = self.page_length
            flt = ''
            
        qs=self.queryset
        if flt:
            d={}
            for col in self.columns:
                if col.is_filter:
                    d[col.field.name+"__contains"]=flt
            print d
            qs = qs.filter(**d)
          
        paginator = Paginator(qs,pgl)
        
        try:
            page = paginator.page(pgn)
        except (EmptyPage, InvalidPage):
            page = paginator.page(paginator.num_pages)

        fsclass = modelformset_factory(self.queryset.model,
                                       fields=self.columnNames.split())
                                       
        if request.method == 'POST':
            fs = fsclass(request.POST,queryset=page.object_list)
            if fs.is_valid():
                fs.save()
        else:
            fs = fsclass(queryset=page.object_list)
            
        def get_again(**kw):
            kw.update(request.GET)
            return urlparams(kw)

        context = dict(
            params=params,
            report=self,
            page=page,
            formset=fs,
            get_again=get_again,
        )
        return render_to_response("tom/list.html",context)

    def view_page(self,request,row):
        obj=self.queryset[int(row)]
        if request.method == 'POST':
            frm=self.modelForm(request.POST,instance=obj)
            if frm.is_valid():
                frm.save()
        else:
            frm=self.modelForm(instance=obj)      
        context = dict(
            report=self,
            object=obj,
            form=frm,
        )
        return render_to_response("tom/page.html",context)    
        
