## Copyright 2009-2010 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.


import traceback
#import types
import cgi
from textwrap import TextWrapper
from StringIO import StringIO # cStringIO doesn't support Unicode
import cStringIO

from django.db import models

#from lino.misc.etc import assert_pure

from lino import reports

LEFT = "LEFT"
RIGHT = "RIGHT"
CENTER = "CENTER"
TOP = "TOP"
BOTTOM = "BOTTOM"

class ConfigError(Exception):
    pass

class NotEnoughSpace(Exception):
    pass



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
      
  


class ColumnsReportRequest(reports.ReportActionRequest):
        
    def __init__(self,rh,*args,**kw):
        reports.ReportRequest.__init__(self,rh,*args,**kw)
        self.columns_by_name = {}
        columns = []
        meta = rh.report.model._meta
        if rh.report.column_names:
            for colname in rh.report.column_names.split() :
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
                    dtlrep = rh.report.list_layout._inlines.get(fieldname,None)
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
        
        
    def new_column(self,*args):
        return FieldColumn(self,*args)
        

class TextReportRequest(ColumnsReportRequest):
    def __init__( self,
                  rh,
                  master_instance=None,
                  width=79,
                  columnWidths=None,
                  columnSep="|",
                  columnHeaderSep='-',
                  column_widths=None,
                  rowHeight=None,
                  **params):
        self.width = width
        self.columnWidths = columnWidths
        self.column_widths = column_widths
        self.rowHeight = rowHeight
        self.columnHeaderSep = columnHeaderSep
        self.columnSep = columnSep
        #~ if flt is None:
            #~ flt = report.default_filter
        #~ self.flt = flt
        ColumnsReportRequest.__init__(self,rh,master_instance,**params)
                             
  
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
        
        l = []
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
        
        #queryset = self.report.get_queryset(master_instance=None,flt=self.flt)
        #queryset=self.report.queryset
        #print queryset.count()
        for obj in self.queryset:
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
            #assert_pure(cellValues[j][i])
            l.append(hfill(cellValues[j][i],
                           self.columns[j].halign,
                           self.columns[j].width))
        s=columnSep.join(l)
        return s.rstrip()+"\n"
        
    def detail_to_string(self,dtlrep,instance):
        r = TextReportRequest(dtlrep,instance)
        return r.render()
      
