#coding: latin1

## Copyright 2003-2005 Luc Saffre 

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

import sys
import os
opj = os.path.join
from cStringIO import StringIO

from lino.gendoc.gendoc import WriterDocument
from lino.forms.base import MenuContainer

from lino.adamo.query import QueryColumn
from lino.adamo.query import Query


# from twisted.web.microdom
ESCAPE_CHARS = (('&', '&amp;'),
                ('<', '&lt;'),
                ('>', '&gt;'),
                ('"', '&quot;'))

def unescape(text):
    "Perform the exact opposite of 'escape'."
    for ch, h in ESCAPE_CHARS:
        text = text.replace(h, ch)
    return text

def escape(text):
    "replace a few special chars with HTML entities."
    for ch, h in ESCAPE_CHARS:
        text = text.replace(ch, h)
    return text 


firstPageButton = '[<<]'
lastPageButton = '[>>]'
prevPageButton = '[<]'
nextPageButton = '[>]'
beginNavigator = '''
<p class="nav">Navigator:
'''
endNavigator = "</p>"


END_PAGE = """
  </body>
  </html>
"""


class Resolver:
    def __init__(self,root,cl,i2name):
        self.root=root
        self.cl=cl
        self.i2name=i2name
        #self.qry2name=qry2name

    def href(self,fromLoc,toRow):
        return fromLoc.locto(self.i2name(toRow)) + fromLoc.extension
    #".html"

    
        
def rpt2name(rpt):
    qry=rpt.ds
    return "/".join(
        [rpt.name]+[col.name for col in qry._masterColumns])+"/index"
                            


class Locatable:
    # local URL. URL for a local resource
    extension=None
    def __init__(self,name,location=None,parent=None):
        pos=name.rfind("/")
        if pos != -1:
            assert location is None
            location=name[:pos]
            name=name[pos+1:]
            
        if location is None:
            if parent is None:
                location=""
            else:
                location = parent.location
        else:
            assert not location.endswith('/')
            assert not location.startswith('/')
            if parent is not None:
                location = parent.addloc(location)
            
        self.location=location
        if name.endswith(self.extension):
            name = name[:-len(self.extension)]
        self.name=name
        self.parent=parent
        
    def filename(self):
        return self.name + self.extension

    def dirname(self):
        return self.location.replace("/",os.path.sep)

    def getRoot(self):
        if self.parent is None:
            return self
        return self.parent.getRoot()

    def urlto(self,other):
        if self.location == other.location:
            return other.filename()
        return self.locto(other.location) + "/" + other.filename()
    
    def locto(self,dest):
        if self.location=="": return dest
        l1=self.location.split("/")
        if dest=="": return "/".join([".."]*len(l1))
        l2=dest.split("/")
        while len(l1) and len(l2) and l1[0] == l2[0]:
            del l1[0]
            del l2[0]
        #l= [".."]*(len(l1)-1) + l2
        l= [".."]*len(l1) + l2
        return "/".join(l)

    def addloc(self,location):
        if self.location == "":
            return location
        return self.location+"/"+location


class StyleSheet(Locatable): 
    extension=".css"


class HtmlDocument(WriterDocument,MenuContainer,Locatable):
    extension=".html"
    def __init__(self,
                 content=None,
                 title=None,
                 date=None,
                 name=None,
                 location=None,
                 parent=None,
                 stylesheet=None,
                 **kw):

        if name is None:
            name="index"
        
        Locatable.__init__(self,name,location,parent)
        WriterDocument.__init__(self)
        MenuContainer.__init__(self)
        
        
        if stylesheet is None:
            if parent is not None:
                stylesheet=parent.stylesheet
        else:
            assert type(stylesheet)==type('')
            stylesheet = StyleSheet(stylesheet,parent=self)

        self.stylesheet = stylesheet
        
        #self.content=content

        self.children = []
        #self.childrenByName = {}

        if title is None:
            title = self.filename()
        self.title = title
        self.date = date
        self._reports=[]
        self._resolvers=[]
        if content is not None:
            assert hasattr(content,"render")
            self._body=[content]
        else:
            self._body=[]

    def addChild(self,**kw):
        c = self.__class__(parent=self,**kw)
        #assert not self.childrenByName.has_key(c.name)
        self.children.append(c)
        #self.childrenByName[c.name] = c
        return c
    
    def addResolver(self,tc,i2name):
        self._resolvers.append(Resolver(self,tc,i2name))

    def addReportChild(self,rpt):
        doc=self.addChild(name=rpt2name(rpt),
                          title=rpt.getLabel())
        doc.report(rpt)
        return doc
        
    
    def getLineWidth(self):
        return 100
    
    def getColumnSepWidth(self):
        return 0
    
    def writeText(self,txt):
        self.write(escape(txt))
        
    def writeLink(self,href,label,doc=None):
        self.write('<a href="'+href+'">')
        self.writeText(label)
        self.write('</a>')

    def findResolver(self,cl):
        root=self.getRoot()
        for rs in root._resolvers:
            if rs.cl == cl: return rs

    def writeColValue(self,col,value):
        if value is None:
            s = ""
        else:
            root=self.getRoot()
            cl=col.getValueClass()
            if cl is Query:
                for rpt in root._reports:
                    if rpt.doesShow(value):
                        name=rpt2name(rpt)
                        href=self.urlto(name)
                        self.writeLink(href,str(value)) 
                        return
                #print "no report for", value
##                 cl=value.getLeadTable().__class__
##                 #print cl
##                 rs=self.findResolver(cl)
##                 if rs is not None:
##                     #print "bla"
##                     for row in value:
##                         href=rs.href(self,row)
##                         label=row.getLabel()
##                         self.writeLink(href,label) 
##                         self.writeText(", ")
##                     return
            else:
                rs=self.findResolver(cl)
                if rs is not None:
                    href=rs.href(self,value)
                    label=value.getLabel()
                    self.writeLink(href,label)
                    return

            self.writeText(col.format(value))

    def h(self,level,txt):
        self._body.append(H(level,txt))

    def report(self,rpt):
        self._reports.append(rpt)
        self._body.append(ReportElement(rpt))

    def beginDocument(self,wr):
        self.writer = wr
        wr("<html><head><title>")
        self.writeText(self.title)
        wr("""</title>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
""")
        if self.stylesheet is not None:
            wr('<link rel=stylesheet type="text/css" href="%s">\n'
               % self.urlto(self.stylesheet))
        wr('<meta name="KEYWORDS" content="">\n')
        wr('<meta name="GENERATOR" content="Lino">\n')
        wr('<meta name="author" content="">\n')
        wr('<meta name="date" content="%s">')
        wr("<head><body>\n")
        
    
    def endDocument(self):
        self.write(END_PAGE)
        self.writer = None


    def writeDocument(self,wr):
        self.beginDocument(wr)
        if self.menuBar is not None:
            for menu in self.menuBar.menus:
                self.write('<ul id="adminmenu">')
                for mi in menu.items:
                    #assert mi.action is not None
                    self.write('<li>')
                    self.writeLink(
                        href=mi.action,
                        label=mi.getLabel())
                    self.write('</li>')
                self.write('</ul>')


        for elem in self._body:
            elem.render(self)
        self.endDocument()

    
    def save(self,ui,targetRoot=".",simulate=False):
        filenames = []
        dirname = opj(targetRoot,
                      self.location.replace("/",os.path.sep))
        fn = opj(dirname, self.filename())
        filenames.append(fn)
        #print fn
        if simulate:
            ui.status("Would write %s...",fn)
            fd = StringIO()
        else:
            ui.status("Writing %s...",fn)
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
                ui.notice("Created directory %s",dirname)
            
            fd = file(fn,"wt")
            
        self.writeDocument(fd.write)
        fd.close()
        
        for rpt in self._reports:
            if rpt.ds.canSort() > 0:
                for col in rpt.columns:
                    for pg in range(rpt.ds.lastPage):
                        if pg != 0 or \
                           col.datacol != rpt.ds.sortColumns[0]:
                            e=ReportElement(rpt,pg+1,col.datacol)
                            ch=self.addChild(
                                name=rptname(rpt,
                                             pageNum=pg+1,
                                             sortColumn=col.datacol),
                                title=rpt.getLabel(),
                                content=e)
                
        
        #print len(subdocs)
        #raise "hier"
        #for ch in subdocs:
        #    filenames += ch.save(ui,targetRoot,simulate)

##         for rs in self._resolvers:
##             for x in ui.query(rs.cl):
##                 ch=self.__class__(parent=self,
##                                   name=rs.i2name(x),
##                                   title=x.getLabel(),
##                                   content=DataRowElement(x))
##                 filenames += ch.save(ui,targetRoot,simulate)
                
        for ch in self.children:
            filenames += ch.save(ui,targetRoot,simulate)
        return filenames


        
class H:
    def __init__(self,level,txt):
        assert level > 0 and level <= 9
        self.level=level
        self.text=txt
        
    def render(self,doc):
        tag = "H"+str(self.level)
        doc.write("<%s>" % tag)
        doc.writeText(self.text)
        doc.write("</%s>\n" % tag)


def rptname(rpt,sortColumn=None,pageNum=None):
    if pageNum is None: pageNum=rpt.pageNum
    if rpt.ds.canSort():
        if sortColumn is None: sortColumn=rpt.ds.sortColumns[0]
        if pageNum==1 and sortColumn==rpt.ds.sortColumns[0]:
            return rpt.name
        return str(pageNum)+"_"+sortColumn.name
    elif pageNum==1: return rpt.name
    return str(pageNum)
    
                    



        
        
class DataRowElement:
    def __init__(self,row):
        self.row=row
        
    def render(self,doc):
        wr=doc.write
        
        wr('<table width="100%" cellpadding="3" cellspacing="3">')
            
            
        # iterate...
        rowno = 0
        for cell in self.row:
            rowno += 1
            if rowno % 2 == 0:
                wr("<tr class=''>\n")
            else:
                wr("<tr class='alternate'>\n")

            wr('<td>')
            doc.writeText(cell.col.getLabel())
            wr("</td>")
            
            wr('<td>')
            doc.writeColValue(cell.col,cell.getValue())
            wr("</td>")
            wr("</tr>\n")
        
        wr("</table>")

        
class ReportElement:
    def __init__(self,rpt,pageNum=1,sortColumn=None):
        self.rpt=rpt
        self.pageNum=pageNum
        if rpt.canSort():
            if sortColumn is None:
                sortColumn=rpt.ds.sortColumns[0]
            else:
                assert isinstance(sortColumn,QueryColumn)
            self.sortColumn=sortColumn

    def rptname(self):
        if self.rpt.canSort():
            return str(self.pageNum)+"_"+self.sortColumn.name
        return str(self.pageNum)
    
    def render(self,doc):
        rpt=self.rpt
        ds=rpt.ds
        pageNum=self.pageNum
        sortColumn=self.sortColumn
        wr=doc.write
        # initialize...
        rpt.beginReport(doc)

        # title

        #if rpt.label is not None:
        #    self.h(1,rpt.label)


        # navigator

        if True: # flup.lastPage > 1:
            wr(beginNavigator)
                
            if pageNum is None:
                pageNum = 1
            elif pageNum < 0:
                pageNum = ds.lastPage + pageNum + 1
                # pg=-1 --> lastPage
                # pg=-2 --> lastPage-1
                
            if pageNum == 1:
                wr(firstPageButton)
                wr(prevPageButton)
            else:

                doc.writeLink(
                    href=rptname(rpt,
                                 sortColumn=sortColumn,
                                 pageNum=1)+doc.extension,
                    label=firstPageButton)
                
                doc.writeLink(
                    href=rptname(rpt,
                                 sortColumn=sortColumn,
                                 pageNum=pageNum-1)+doc.extension,
                    label=prevPageButton)

##                 ch=self.getChild(rptname(rpt,pageNum=pageNum-1))
##              self.link(uri=self.urito(ch),
##                           label=prevPageButton)



            wr(" [page %d of %d] " % (pageNum, ds.lastPage))
                
            if pageNum == ds.lastPage:
                wr(nextPageButton)
                wr(lastPageButton)
            else:
                doc.writeLink(
                    href=rptname(rpt,
                                 sortColumn=sortColumn,
                                 pageNum=pageNum+1)+doc.extension,
                    label=nextPageButton)
                doc.writeLink(
                    href=rptname(rpt,
                                 sortColumn=sortColumn,
                                 pageNum=ds.lastPage)+doc.extension,
                    label=lastPageButton)
                
                
##                 ch=self.getChild(rptname(rpt,pageNum=pageNum+1))
##              self.link(uri=self.urito(ch),
##                           label=nextPageButton)
##                 ch=self.getChild(rptname(rpt,pageNum=rpt.lastPage))
##              self.link(uri=self.urito(ch),
##                           label=lastPageButton)
                
            wr(' (%d rows)' % len(ds))
            wr(endNavigator)

        
        

        # renderHeader

        wr('<table width="100%" cellpadding="3" cellspacing="3">')
        wr('<tr>\n')
        for col in rpt.columns:
            wr('<th scope="col">')
            if col.datacol == sortColumn:
                doc.writeText(col.getLabel())
            else:
                url=rptname(rpt,
                            pageNum=pageNum,
                            sortColumn=col.datacol)+doc.extension
                doc.writeLink(
                    href=url,
                    label=col.getLabel(),
                    doc="Click here to sort by "+col.getLabel())
            wr('</th>\n')
            
        wr("</tr>\n")
            
            
        # iterate...
        rowno = 0
        for datarow in ds.child(pageNum=pageNum,
                                sortColumns=[sortColumn]):
            rowno += 1
            if rowno % 2 == 0:
                wr("<tr class=''>\n")
            else:
                wr("<tr class='alternate'>\n")
            
            rptrow = rpt.processItem(doc,datarow)

            for cell in rptrow.cells:
                wr('<td>')
                doc.writeColValue(cell.col.datacol,cell.value)
                #wr('<th scope="row">')
                wr("</td>")
            wr("</tr>\n")
            
            
        # renderFooter
        
        wr("</table>")
        
        rpt.endReport(self)

    
                    
