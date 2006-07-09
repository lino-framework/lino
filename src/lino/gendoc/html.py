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

