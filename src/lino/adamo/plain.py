## Copyright Luc Saffre 2003-2004.

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


import re

from quixote.html import htmltext  # to be replaced by equivalent

from lino.adamo.row import BaseRow
from lino.adamo.datatypes import MemoType, UrlType, EmailType
from lino.misc.memo import MemoParser


class PlainRenderer:
    
    showRowCount = True

    def __init__(self, parent, db):
        if parent is not None:
            if db is None:
                db = parent.db
        self.db = db
        cmds = {
            'url' : self.cmd_url,
            'ref' : self.cmd_ref,
            'xe' : self.cmd_ref,
            'img' : self.cmd_img
            }
        
        self.memoParser = MemoParser(cmds)
        self.reportTemplates = (
            TableReportTemplate("Table"),
            ListReportTemplate("List"),
            )

    def setupRenderer(self):
        pass

    def cmd_img(self,s):
        s = s.split(None,1)
        return self.renderImage(*s)

    def cmd_ref(self,s):
        s = s.split(None,1)
        ref = s[0].split(':')
        if len(ref) != 2:
            return None
        try:
            if ref[0] == "MSX":
                ref[0] = "PAGES"
            elif ref[0] == "TPC":
                ref[0] = "TOPICS"
            elif ref[0] == "AUT":
                ref[0] = "AUTHORS"
            elif ref[0] == "NEW":
                ref[0] = "NEWS"
            elif ref[0] == "PUB":
                ref[0] = "PUBLICATIONS"
            area = getattr(self.db,ref[0])
        except AttributeError,e:
            return None
            #return str(e)
        s[0] = self.uriToTable(area._table)+"?id="+ref[1]
        return self.renderLink(*s)

    def cmd_url(self,s):
        s = s.split(None,1)
        return self.renderLink(*s)
    ##  if len(s) == 2:
    ##      return renderLink(s[0],label=s[1])
    ##  else:
    ##      return renderLink(s[0])

    def memo2html(self,txt):
        if txt is None:
            return ''
        txt = txt.strip()
        self.memoParser.parse(txt)
        return self.memoParser.html

    def renderImage(self,src,tags=None,label=None):
        if label is None:
            label = src
        s = '<img src="%s" alt="%s"' % (src,label)
        if tags is not None:
            s += tags
        s += ">"
        return s

    def renderLink(self,url,label=None):
        if label is None:
            label = url
        return '<a href="%s">%s</a>' % (url,label)

    def renderMenuBar(self,request,mb):
        s = ""
        if mb.getLabel():
            s += '<p class="toc"><b>%s</b> ' \
                  % self.formatLabel(mb.getLabel())
        for mnu in mb.getMenus():
            s += '<br><b>%s</b>: ' % self.formatLabel(mnu.getLabel())
            for mi in mnu.getItems():
                s += "<br>" + self.renderAction(mi,request)
        return s


    def formatLabel(self,label):
        p = label.find(self.db.schema.HK_CHAR)
        if p != -1:
            label = label[:p] + '<u>' + label[p+1] + '</u>' + label[p+2:]
        return str(htmltext(label))

    def renderValue(self,request,value,type):

        if value is None:
            return ""

        if hasattr(value,'asLabel'):
            return value.asLabel(self,request)

        if type is not None:
            if isinstance(type,MemoType):
                return self.memo2html(value)
            if isinstance(type,UrlType):
                return self.renderLink(value)
            if isinstance(type,EmailType):
                return self.renderLink('mailto:'+value,value)
        return str(htmltext(str(value)))

    def renderForm(self, request, row):
        #from lino.schemas.sprl.web import Page
        #if isinstance(row,Page):
        #body = row.asPreTitle(self,request)
        body = row.asPage(self,request)
        body += row.asFooter(self,request)
        #body += row.render_html(self,request,self.FMT_PAGE)
        return body

    def renderNavigator(self,request,ds,pageNum=None):
        return ''

    def renderReport(self, request, rpt, tpl=None, pageNum=None):
        if tpl is None:
            tpl = self.reportTemplates[0]
        if rpt.pageLen is None:
            limit = offset = None
            rowcount = 0
        else:
            if pageNum is None:
                pageNum=1
            elif pageNum < 0:
                pageNum = rpt.lastPage + pageNum - 1
            elif pageNum > rpt.lastPage:
                raise "pageNum > lastPage"
            rowcount = offset = rpt.pageLen*(pageNum-1) # +1
            limit = rpt.pageLen
            
        body = tpl.renderHeader(self,request,rpt,pageNum)
        for atomicRow in rpt.execute(offset=offset,limit=limit):
            rowcount += 1
            body += tpl.renderLine(self,request,rpt,pageNum,
                                          rowcount,atomicRow)

        body += tpl.renderFooter(self,request,rpt,pageNum)

        return body

    def urlToSelf(self,request,label,**options):
        return label

    def wholepage(self, request,
                      title,
                      body,
                      basepath='.',
                      preTitle='',
                      leftMargin=None):

        return title + "\n" + "="*len(title) + "\n" + body


class ReportTemplate:
    
    def __init__(self,label):
        self.label= label

class TableReportTemplate(ReportTemplate):
    
    def renderHeader(self,renderer,request,rpt,pageNum):
        body = ''
        if renderer.showRowCount:
            body += "#\t"
        for col in rpt.getColumns():
            body += col.getLabel() + "\t"
        body += '\n'            
        body += "-" * 40
        body += '\n'
        return body
    
    def renderLine(self,renderer,request,rpt,pageNum,
                        rowcount, atomicRow):
        body = ''
        values = rpt.atoms2values(atomicRow)
        if renderer.showRowCount:
            body += renderer.urlToSelf(request,
                                                label=str(rowcount),
                                                pl=1,
                                                pg=rowcount)
            body += "\t"

        sep = ""
        i = 0
        for col in rpt.getColumns():
            body += sep
            sep = "\t"
            type= getattr(col.queryCol.rowAttr,'type',None)
            body += renderer.renderValue(request,values[i],type)
            i += 1

        body += '\n'
        return body

    def renderFooter(self,renderer,request,rpt,pageNum):
        return "-" * 40 + "\n"

class ListReportTemplate(ReportTemplate):
    
    def renderHeader(self,renderer,request,rpt,pageNum):
        return '<ul>'
    def renderLine(self,renderer,request,rpt,pageNum,
                        rowcount, atomicRow):
        row = rpt.atoms2instance(atomicRow)
        return '<li>'+row.asParagraph(renderer,request)+'</li>'
    def renderFooter(self,renderer,request,rpt,pageNum):
        return '</ul>'
        

