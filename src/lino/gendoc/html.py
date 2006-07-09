#coding: iso-8859-1

## Copyright 2003-2006 Luc Saffre 

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

from lino.gendoc import gendoc # import WriterDocument
from lino.forms.forms import MenuContainer

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



class Resolver:
    def __init__(self,root,cl,i2name):
        self.root=root
        self.cl=cl
        self.i2name=i2name
        #self.qry2name=qry2name

    def href(self,fromLoc,toRow):
        return fromLoc.locto(self.i2name(toRow)) + fromLoc.extension
    #".html"

    
        


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


def rpt2name(rpt):
    raise "must go away"
    qry=rpt.ds
    return "/".join(
        [rpt.name] + [col.name for col in qry._masterColumns]) \
        +"/index"
                            
class StaticSite:
    def __init__(self,root):
        self.root = root
        self._resolvers=[]
        #self.addResolver(DataReport, rpt2name)
        
    def addResolver(self,tc,i2name):
        self._resolvers.append(Resolver(self,tc,i2name))

    def findResolver(self,cl):
        for rs in self._resolvers:
            if rs.cl == cl: return rs



    
class HtmlDocument(gendoc.WriterDocument,MenuContainer,Locatable):
    extension=""
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
        gendoc.WriterDocument.__init__(self)
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
        #self._reports=[]
        if content is not None:
            assert hasattr(content,"__html__")
            self._body=[content]
        else:
            self._body=[]
            
        if parent is None:
            self.site=StaticSite(self)
        else:
            self.site = parent.site
        

    def addChild(self,**kw):
        c = self.__class__(parent=self,**kw)
        #assert not self.childrenByName.has_key(c.name)
        self.children.append(c)
        #self.childrenByName[c.name] = c
        return c
    
    
    def getLineWidth(self):
        return 100
    
    def getColumnSepWidth(self):
        return 0
    
    def writeText(self,txt):
        self.write(escape(txt))
        
##     def writeLink(self,href,label=None,doc=None):
##         raise "replaced by renderLink()"
##         if label is None: label=href
##         self.write('<a href="'+href+'">')
##         self.writeText(label)
##         self.write('</a>')

    def writeColValue(self,col,value):
        if value is None:
            s = ""
        else:
            #root=self.getRoot()
            cl=col.getValueClass()
##             if cl is Query:
##                 for rpt in root._reports:
##                     if rpt.doesShow(value):
##                         name=rpt2name(rpt)
##                         href=self.urlto(name)
##                         self.writeLink(href,str(value)) 
##                         return
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
##             else:
            rs=self.findResolver(cl)
            if rs is not None:
                href=rs.href(self,value)
                label=col.format(value)
                self.writeLink(href,label)
                return

            self.writeText(col.format(value))

    def par(self,*args,**kw):
        self._body.append(P(*args,**kw))

    def pre(self,*args,**kw):
        self._body.append(PRE(*args,**kw))

    def header(self,level,*args,**kw):
        self._body.append(H(level,*args,**kw))

    def report(self,rpt):
        self._body.append(ReportElement(self,rpt))

        if rpt.ds.canSort() > 0:
            for col in rpt.columns:
                for pg in range(rpt.ds.lastPage):
                    if pg != 0 \
                          or col.datacol != rpt.ds.sortColumns[0]:
                        e=ReportElement(self,rpt,pg+1,col.datacol)
                        self.addChild(
                            name=rptname(self,
                                         rpt,
                                         pageNum=pg+1,
                                         sortColumn=col.datacol),
                            title=rpt.getTitle(),
                            content=e)

        
##     def addReportChild(self,rpt):
##         raise "must go away"
##         doc=self.addChild(name=rpt2name(rpt),
##                           title=rpt.getLabel())
##         doc.report(rpt)
##         return doc
        

    def beginDocument(self,wr):
        wr("<html><head><title>")
        wr(escape(self.title))
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

        if self.menuBar is not None:
            for menu in self.menuBar.menus:
                wr('<ul class="adminmenu">')
                for mi in menu.items:
                    #assert mi.action is not None
                    wr('<li>')
                    self.writeLink(
                        href=mi.action,
                        label=mi.getLabel())
                    wr('</li>')
                wr('</ul>')


        
        
    
    def endDocument(self,wr):
        wr("""\
        </body>
        </html>
        """)


    def writeDocument(self,wr):
        self.writer = wr
        self.beginDocument(wr)
        for elem in self._body:
            elem.__html__(self,wr)
        self.endDocument(wr)
        self.writer = None
        
def rptname(doc,rpt,sortColumn=None,pageNum=None):
    if pageNum is None: pageNum=rpt.pageNum
    if rpt.ds.canSort():
        if sortColumn is None: sortColumn=rpt.ds.sortColumns[0]
        if pageNum==1 and sortColumn==rpt.ds.sortColumns[0]:
            return doc.name
        return doc.name+"_"+str(pageNum)+"_"+sortColumn.name
    elif pageNum==1: return doc.name
    return doc.name+"_"+str(pageNum)


        
        
## class DataRowElement:
##     def __init__(self,row):
##         self.row=row
        
##     def __html__(self,doc):
##         wr=doc.write
        
##         wr('<table width="100%" cellpadding="3" cellspacing="3">')
            
            
##         # iterate...
##         rowno = 0
##         for col in self.row._query.getVisibleColumns():
##         #for cell in self.row:
##             rowno += 1
##             if rowno % 2 == 0:
##                 wr("<tr class=''>\n")
##             else:
##                 wr("<tr class='alternate'>\n")

##             wr('<td>')
##             doc.writeText(col.getLabel())
##             wr("</td>")
            
##             wr('<td>')
##             doc.writeColValue(col,col.getCellValue(self.row))
##             wr("</td>")
##             wr("</tr>\n")
        
##         wr("</table>")


class HtmlPage:
    def __init__(self,doc,cloneElement,cloneOptions):
        self.doc=doc
        self.cloneElement=cloneElement
        self.cloneOptions=cloneOptions

    def filename(self):
        raise NotImplemented
        
class ReportElement:
    def __init__(self,doc,rpt,pageNum=1,sortColumn=None):
        self.doc=doc
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
    
    def __html__(self,doc):
        rpt=self.rpt
        ds=rpt.ds
        pageNum=self.pageNum
        sortColumn=self.sortColumn
        #wr=self.doc.write
        # initialize...
        rpt.beginReport(self.doc)
        s=''
        def wr(s2):
            s+=s2

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
                    href=rptname(doc,rpt,
                                 sortColumn=sortColumn,
                                 pageNum=1)+doc.extension,
                    label=firstPageButton)
                
                doc.writeLink(
                    href=rptname(doc,rpt,
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
                    href=rptname(doc,rpt,
                                 sortColumn=sortColumn,
                                 pageNum=pageNum+1)+doc.extension,
                    label=nextPageButton)
                doc.writeLink(
                    href=rptname(doc,rpt,
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
                url=rptname(doc,rpt,
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
            
            #rptrow = rpt.processItem(doc,datarow)
            rptrow = rpt.processItem(datarow)
            
            i=0
            for col in rpt.columns:
            #for cell in rptrow.cells:
                wr('<td>')
                doc.writeColValue(col.datacol,rptrow.values[i])
                # cell.value)
                #wr('<th scope="row">')
                wr("</td>")
                i+=1
            wr("</tr>\n")
            
            
        # renderFooter
        
        wr("</table>")
        
        rpt.endReport(doc)

    
                    




class StaticHtmlDocument(HtmlDocument):
    extension=".html"
    def save(self,sess,targetRoot=".",simulate=False):
        filenames = []
        dirname = opj(targetRoot,
                      self.location.replace("/",os.path.sep))
        fn = opj(dirname, self.filename())
        filenames.append(fn)
        #print fn
        if simulate:
            sess.status("Would write %s...",fn)
            fd = StringIO()
        else:
            sess.status("Writing %s...",fn)
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
                sess.notice("Created directory %s",dirname)
            
            fd = file(fn,"wt")
            
        self.writeDocument(fd.write)
        fd.close()
        
        
##         for rs in self._resolvers:
##             for x in ui.query(rs.cl):
##                 ch=self.__class__(parent=self,
##                                   name=rs.i2name(x),
##                                   title=x.getLabel(),
##                                   content=DataRowElement(x))
##                 filenames += ch.save(ui,targetRoot,simulate)
                
        for ch in self.children:
            filenames += ch.save(sess,targetRoot,simulate)
        return filenames











    
                    

from lino.oogen.elements import CDATA, Element, Container, Story, InvalidRequest

class Fragment(Container):
    allowedAttribs=dict(xclass='class',
                        id='id',
                        style='style',
                        title='title')
class SPAN(Fragment):
    allowedContent = (CDATA,Fragment)

class B(SPAN): pass    
class EM(SPAN): pass    
class I(SPAN): pass
class U(SPAN): pass
class SUP(SPAN): pass
class TT(SPAN): pass    
class FONT(SPAN): pass    
    
class P(Fragment):
    allowedContent = (CDATA,SPAN)
    allowedAttribs = dict(
        align="align",
        **SPAN.allowedAttribs)
    
class H(P):
    def __init__(self,level,*args,**kw):
        assert level > 0 and level <= 9
        self.level=level
        Container.__init__(self,*args,**kw)
        
    def tag(self):
        return self.__class__.__name__+str(self.level)
        


class PRE(P): pass

class LI(P):pass

class UL(Fragment): 
    allowedContent = (LI,)
    def li(self,*args,**kw):
        return self.append(LI(*args,**kw))

class OL(UL): 
    pass

class A(SPAN):
    allowedAttribs=dict(href="href",
                        **SPAN.allowedAttribs)
    
##     def __init__(self,href=None,label=None,doc=None):
##         if label is None: label=href
##         self.href=href
##         self.label=label
##         self.doc=doc
        
##     def __html__(self,doc,wr):
##         wr('<a href="'+self.href+'">')
##         wr(escape(self.label))
##         wr('</a>')

class TD(P): pass
class TH(P): pass
class TR(Fragment):
    allowedContent=(TD,TH)
    
class COL(Element):
    allowedAttribs=dict(span="span",width="width")

class COLGROUP(Fragment):
    allowedContent=(COL,)
    allowedAttribs=dict(span="span",width="width")

class TABLE(Fragment):
    allowedContent=(TR,COLGROUP,COL)
    


from HTMLParser import HTMLParser

class MemoParser(HTMLParser):

    def __init__(self,story):
        HTMLParser.__init__(self)
        self.story=story
        self.stack=[]
        self.buffer=""
        self.newpar=False # "start new par on next data"

##     def reset(self):
##         HTMLParser.reset(self)

    def _append(self,elem):
        self.stack[-1].append(elem)
        
    def handle_data(self,data):
        """process arbitrary data."""
        if data=='\n':
            self.newpar=True
            return
        if len(self.stack) == 0:
            self.stack.append(self.story.par())
            #print "pushed", self.stack[-1]
            self.newpar=False
        elif self.newpar:
            if self.stack[-1].__class__==P:
                popped=pop(self.stack)
                #print "popped",popped
            self.stack.append(self.story.par())
        self.newpar=False
        self.stack[-1].append(data)

    def handle_charref(self,name):
        """process a character reference of the form "&#ref;"."""
        print "handle_charref", name
        raise NotImplemented
        
    def handle_entityref(self,name):
        """process a general entity reference of the form "&name;"."""
        print "handle_entityref", name
        raise NotImplemented

    def starttag(self,tag,attrs):
        tag=tag.upper()
        cl=globals()[tag]
        return cl()
        
    def handle_startendtag(self,tag, attrs):
        self.handle_data(self.starttag(tag,attrs))

    def handle_starttag(self, tag, attrs):
        elem=self.starttag(tag,attrs)
        try:
            self._append(elem)
        except InvalidRequest,e:
            if self.stack[-1].__class__ is P \
               and elem.__class__ in(UL,OL,TABLE):
                popped=self.stack.pop()
                #print "popped",popped
                self.story.append(elem)
            else:
                raise
        self.stack.append(elem)
        

    def handle_endtag(self, tag):
        popped=self.stack.pop()
        if tag.upper() != popped.tag():
            if popped.__class__ is P:
                print "popped again"
                popped=self.stack.pop()
        assert tag.upper() == popped.tag(),\
               "Found </%s> (expected </%s>)" % (tag,popped.tag())


class HtmlStory(Story):
        
    def report(self,rpt):
        rpt.beginReport() # self.getDocument())
        header=[TH(col.getLabel()) for col in rpt.columns]
        t=TABLE(TR(*header))
        for row in rpt.rows(): # self.getDocument()):
            line=[TD(s) for (c,s) in row.cells()]
            t.append(TR(*line))

        rpt.endReport()
        return self.append(t)
        

    def table(self,*args,**kw):
        return self.append(TABLE(*args,**kw))

    def par(self,*args,**kw):
        return self.append(P(*args,**kw))

    def pre(self,*args,**kw):
        return self.append(PRE(*args,**kw))

    def heading(self,level,*args,**kw):
        return self.append(H(level,*args,**kw))

##     def write(self,txt):
##         self.parbuf += txt
        
##     def flush(self):
##         if len(self.parbuf)==0:
##             return
##         self.par(self.parbuf)
##         self.parbuf=""

    def memo(self,txt):
        p=MemoParser(self)
        p.feed(txt)
        p.close()
        
##         #self.parbuf=""
##         self.stack=[]
##         for line in txt.split('\n\n'):
##             if len(line) != 0:
##                 while True:
##                     pos = line.find('<')
##                     if pos == -1:
##                         break
##                     elif pos > 0:
##                         #self.write(line[:pos])
##                         self._append(line[:pos])
##                         line = line[pos:]

##                     pos = line.find('>')
##                     piece = line[:pos+1]
##                     tag = line[1:pos].upper()
##                     # print tag
##                     line = line[pos+1:]
                    
##                     if tag[0] != "/":
##                         if tag[-1] == "/":
##                             tag=tag[:-1]
##                             cl=globals()[tag]
##                             self._append(cl())
##                         else:
##                             cl=globals()[tag]
##                             elem=cl()
##                             try:
##                                 self._append(elem)
##                             except InvalidRequest,e:
##                                 if self.stack[-1].__class__ is P \
##                                    and cl in(UL,OL,TABLE):
##                                     #print "yes"
##                                     self.stack.pop()
##                                     self.append(elem)
##                                 else:
##                                     raise
##                             self.stack.append(elem)
##                     else:
##                         e=self.stack.pop()
##                         assert tag.endswith(e.tag()),\
##                                "Found %r  end with %r" % (
##                             tag,e.tag())

##                     #else:
##                     #    stack[-1].append(piece)

##                 self._append(line)

##     def _append(self,elem):
##         if len(self.stack) == 0:
##             self.stack=[self.par()]
##         self.stack[-1].append(elem)
        
    def ul(self,*args,**kw):
        return self.append(UL(*args,**kw))
    def ol(self,*args,**kw):
        return self.append(OL(*args,**kw))
    
    def getDocument(self):
        return None



class Document:

    def __init__(self,
                 title="Untitled",
                 date=None,
                 stylesheet=None):

        self.title = title
        self.date = date
        self.stylesheet = stylesheet
        self.body=HtmlStory(self)
        
        
class HtmlDocument(Document):
    
    def saveas(self,filename):
        f=file(filename,"wt")
        self.__xml__(f.write)
        f.close()

    def __xml__(self,wr):
        wr("<html><head><title>")
        wr(escape(self.title))
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
        self.body.__xml__(wr)
        wr("""\
        </body>
        </html>
        """)




#from reportlab.lib.styles import getSampleStyleSheet
from reportlab import platypus
from lino.gendoc import styles
from reportlab.platypus.paraparser import ParaFrag
from reportlab.lib.fonts import ps2tt, tt2ps

class TableColumn:
    def __init__(self,label=None,width=None,style=None,**kw):
        self.label = label
        self.width = width
        self.style = style

epsilon = 0.001

class PdfTable:
    
    def __init__(self,table):
        self.element=table
        self.rows=[]
        self.columns=[]
        colCount=0
        for elem in table.content:
            if elem.__class__ is TR:
                row=[]
                i=0 # column index
                for td in elem.content:
                    i+=1
                    if len(td.content) == 1:
                        row.append(str(td.content[0]))
                    else:
                        row.append([str(e) for e in td.content])
                colCount=max(i,colCount)
                self.rows.append(row)
            elif elem.__class__ is COL:
                self.columns.append(TableColumn())

        if len(self.columns) == 0:
            for i in range(colCount):
                self.columns.append(TableColumn())
        else:
            assert colCount <= len(columns)
            
        
    def buildTable(self,width,style):
        
        # distribute free space to all columns whose width is None
        remainingWidth = width - style.leftIndent - style.rightIndent
        freeCount = 0   # number of columns whose width is None
        for col in self.columns:
            if col.width is None:
                freeCount += 1
            else:
                remainingWidth -= col.width
        if remainingWidth < 0:
            raise "remainingWidth %s is < 0" % repr(remainingWidth)
        
        if freeCount > 0:
            w = remainingWidth / freeCount
            
        colWidths = [] 
        for col in self.columns:
            if col.width is None:
                assert freeCount > 0 # of course
                colWidths.append(w-epsilon)
            else:
                colWidths.append(col.width-epsilon)

        cellFormats = style.headerCellFormats \
                      + style.dataCellFormats

        if style.showHeaders:
            headerData = []
            for col in self.columns:
                if col.label is None:
                    headerData.append("")
                else:
                    headerData.append(col.label)
            self.rows.insert(0,headerData)

        if len(self.rows) == 0:
            return

        t = platypus.Table(self.rows,colWidths)
        
        # note that Reportlab' TableStyle is only one part of gendoc's
        # TableStyle:
        
        # style of the table as a flowable:
        t.style = style
        # border formatting :
        t.setStyle(platypus.TableStyle(cellFormats))
        
        return t

    


class PdfDocument(Document):        

            
    def saveas(self,filename,header=None,footer=None,
               **kw):
        self.rldoc = platypus.SimpleDocTemplate(filename)
        #self.stylesheet=getSampleStyleSheet()
        self.stylesheet=styles.getDefaultStyleSheet()
        # overwrites the default UL 
        #self.stylesheet.UL = BulletListStyle(bulletWidth=12)
        self.header=header
        self.footer=footer
        for k,v in kw.items():
            #self.body.stylesheet.Document.items():
            setattr(self.rldoc,k,v)
        
        story=[]
        for e in self.body.content:
            story += self.elem2flow(e,self.getDocumentWidth())
        #print story
        self.rldoc.build(story,
                         onFirstPage=self.onEveryPage,
                         onLaterPages=self.onEveryPage)
        
    def elem2flow(self,elem,width):
        #print "elem2flow()",elem
        stName=elem.xclass 
        if stName is None:
            stName=elem.tag()
        if isinstance(elem,PRE):
            yield platypus.XPreformatted(elem.toxml(),
                                         self.stylesheet[stName])
        elif isinstance(elem,UL):
            for li in elem.content:
                for fl in self.elem2flow(li,width):
                    yield fl
            
        elif isinstance(elem,LI):
            yield platypus.Paragraph(elem.toxml(),
                                     self.stylesheet[stName])
        elif isinstance(elem,P):
            frags=[]
            style=self.stylesheet[stName]
            for e in elem.content:
                for f in self.elem2frags(e,style):
                    frags.append(f)
            yield platypus.Paragraph("FRAGS",style,frags=frags)
            
        elif isinstance(elem,TABLE):
            pt=PdfTable(elem)
            t=pt.buildTable(width,self.stylesheet[stName])
            if t is None: return
            yield t
        
            #yield platypus.Table(data)
        else:
            yield platypus.XPreformatted(str(elem),
                                         self.stylesheet[style])
        
    def elem2frags(self,elem,style):
        frag=ParaFrag()
        frag.fontName=style.fontName
        frag.fontSize=style.fontSize
        frag.textColor=style.textColor
        frag.rise=style.rise
        frag.underline=style.underline
        if elem.__class__ == CDATA:
            frag.text=elem.text
            yield frag
            return
        frag.text=''
        if elem.__class__ in (EM,I):
            family, bold, italic = ps2tt(frag.fontName)
            frag.fontName=tt2ps(family,bold,1)
            #frag.fontName=frag.fontName+"-Italic"
        elif elem.__class__ == TT:
            family, bold, italic = ps2tt(frag.fontName)
            frag.fontName=tt2ps("Courier",bold,italic)
        elif elem.__class__ == B:
            family, bold, italic = ps2tt(frag.fontName)
            frag.fontName=tt2ps(family,1,italic)
        elif elem.__class__ == U:
            frag.underline=True
        elif elem.__class__ == SUP:
            frag.rise=True
        else:
            raise "Cannot handle <%s> inside a paragraph" \
                  % elem.tag()
        for e in elem.content:
            if e.__class__ == CDATA:
                frag.text += e.text
            else:
                for ee in elem.content:
                    for f in self.elem2frags(ee,frag):
                        yield f
##                 raise "<%s> not supported inside <%s>" % (
##                     e.tag(),elem.tag())
        yield frag

    


    def makeStory(self,func,textWidth):
        if func is not None:
            s=HtmlStory(self)
            func(s)
            return s

    def getDocumentWidth(self):
        docstyle=self.stylesheet.Document
        return docstyle.pagesize[0] \
                 - docstyle.rightMargin \
                 - docstyle.leftMargin \
                 - 12
        """ -12 because Frame takes 6 pt padding on each side
        """

    def getPageNumber(self):
        return self.rldoc.page
     
        
    def onEveryPage(self, canvas, rldoc):
        assert rldoc == self.rldoc
        style = self.stylesheet.Document
        textWidth = self.getDocumentWidth()

        x = style.leftMargin
        y = style.pagesize[1] - style.topMargin # headerHeight
            
        # x and y are the bottom left corner of the frame. The
        # canvas' (0,0) is not the paper's (0,0) but the bottom left
        # corner of the printable area
            
        self.drawFrame(canvas, self.header, x, y,
                       textWidth, style.topMargin, vAlign="BOTTOM")
        
        y = style.bottomMargin 
        self.drawFrame(canvas, self.footer, x, y,
                       textWidth, style.bottomMargin, vAlign="TOP")
        
    def drawFrame(self,canvas,func,x,y,
                  textWidth,availableHeight,vAlign="TOP"):
        story = self.makeStory(func, textWidth)
        if story is not None:
            height = 0
            for e in story:
                unused,h = e.wrap(textWidth,availableHeight)
                height += h
                availableHeight -= h

            if vAlign == "BOTTOM":
                pass
            elif vAlign == "MIDDLE":
                y -= (height/2)
            elif vAlign == "TOP":
                y -= height

            canvas.saveState()
            f = Frame(x,y,
                         textWidth,height,
                         leftPadding=0,
                         rightPadding=0,
                         bottomPadding=0,
                         topPadding=0)
                         #showBoundary=True)
            f.addFromList(story,canvas)
            canvas.restoreState() 
        
from lino.console.application import Application, UsageError

class PdfMaker(Application):

    name="Lino/PdfMaker"

    copyright="""\
Copyright (c) 2006 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    
    url="http://lino.saffre-rumma.ee/pdfmake.html"
    
    usage="usage: lino pdfmake [options] [FILE]"
    
    description="""\

PdfMaker creates a PDF file named FILE and then runs Acrobat Reader to
view it. Default for FILE is "tmp.pdf".

"""

    

    def run(self,body,ofname=None,**kw):
        if ofname is None:
            if len(self.args) > 0:
                ofname=self.args[0]
            else:
                ofname="tmp.pdf"
            
        doc=PdfDocument()

        try:
            self.status("Preparing...")
            #try:
            body(doc.body)
            #except ParseError,e:
            #    raise
            
            self.status("Writing %s...",ofname)
            doc.saveas(ofname,**kw)
            self.notice("%d pages." % doc.getPageNumber())
            if self.isInteractive():
                os.system("start "+ofname)

        except IOError,e:
            print e
            return -1

