## Copyright 2003-2007 Luc Saffre 

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

#from reportlab.lib.styles import getSampleStyleSheet
from reportlab import platypus
from reportlab.platypus.paraparser import ParaFrag
from reportlab.lib.fonts import ps2tt, tt2ps

from lino.gendoc import styles
from lino.gendoc import html
from lino.console.application import Application, UsageError

from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from lino.gendoc.styles import VA_MIDDLE, VA_TOP, VA_BOTTOM

epsilon = 0.001

class TableColumn:
    def __init__(self,label=None,width=None,style=None,weight=1):
        self.label = label
        self.width = width
        self.style = style
        self.weight=weight

    
def html2pdf(k,v):
    if k == "align":
        if v.lower() == "left": return "alignment",TA_LEFT
        if v.lower() == "right": return "alignment",TA_RIGHT
        if v.lower() == "center" : return "alignment",TA_CENTER
    elif k == "valign":
        if v.lower() == "top": return "vAlign",VA_TOP
        if v.lower() == "bottom": return "vAlign",VA_BOTTOM
        if v.lower() == "center": return "vAlign",VA_MIDDLE
    raise "html2pdf(%r,%r)" % (k,v)

class PdfDocument(html.Document):
    extension=".pdf"
    
    def __init__(self,stylesheet=None,**kw):
        if stylesheet is None:
            stylesheet=styles.getDefaultStyleSheet()
        html.Document.__init__(self,stylesheet=stylesheet,**kw)
            
    def saveas(self,filename,header=None,footer=None):
        #print "BODY:\n",self.body.toxml(),"\n"
        self.rldoc = platypus.SimpleDocTemplate(filename)
        # overwrites the default UL :
        #self.stylesheet.UL = BulletListStyle(bulletWidth=12)
        self.header=header
        self.footer=footer
        for k,v in self.getElementStyle(self.body).items():
            setattr(self.rldoc,k,v)
        
        story=[]
        for e in self.body.content:
            style=self.getElementStyle(e)
            if style.pageBreakBefore:
                if len(story) \
                   and story[-1].__class__ != platypus.PageBreak:
                    story.append(platypus.PageBreak())
            #print e.toxml()
            story += self.elem2flow(e,style,self.getDocumentWidth())
            if style.pageBreakAfter:
                if len(story) \
                   and story[-1].__class__ != platypus.PageBreak:
                    story.append(platypus.PageBreak())
        #print story
        #for fl in story:
        #   assert hasattr(fl,"wrapOn")
        self.rldoc.build(story,
                         onFirstPage=self.onEveryPage,
                         onLaterPages=self.onEveryPage)

    def getElementStyle(self,elem,stName=None,parent=None):
        if stName is None:
            stName=elem.xclass 
            if stName is None:
                stName=elem.tag()
        style=self.stylesheet[stName]
        d={}
        for k,v in elem._attribs.items():
            if v is not None:
                if k != 'xclass':
                    kk,vv=html2pdf(k,v)
                    d[kk]=vv
        if len(d):
            return style.child(**d)
        return style

    def makepar(self,txt,style,**kw):
        if style.wrap:
            return platypus.Paragraph(txt,style,**kw)
        return platypus.XPreformatted(txt,style,**kw)
        
    def elem2flow(self,elem,style,width):
        "Convert this element to an iteration of flowables."
        #print "elem2flow(%r)" % elem.__class__.__name__
        if isinstance(elem,html.PRE):
            assert len(elem.content) == 1
            yield platypus.Preformatted(
                elem.content[0].text, style)
            
        elif isinstance(elem,html.UL):
            for li in elem.content:
                istyle=self.getElementStyle(li,parent=elem)
                for fl in self.elem2flow(li,istyle,width):
                    yield fl
            
        elif isinstance(elem,html.LI):
            yield self.makepar(elem.toxml(),style)
            
        elif elem.__class__ is html.IMG:
            yield platypus.Image()
            
        elif isinstance(elem,html.TABLE):
            t=self.pdftable(elem,width,style)
            #pt=PdfTable(elem)
            #t=pt.buildTable(width,style)
            if t is None: return
            #print "gonna yield", t
            yield t
        
        #elif elem.fragmentable:
        elif isinstance(elem,html.Container):
            #print "fragmentable %s" % elem.__class__.__name__
            frags=[]
            for e in elem.content:
                if e.fragmentable:
                    #print "gonna elem2frags(%s)"% e.__class__.__name__
                    for f in self.elem2frags(e,style):
                        frags.append(f)
                elif e.flowable:
                    # found non-fragmentable element inside a flowable
                    if len(frags) > 0:
                        yield self.makepar("",style,frags=frags)
                    for ee in self.elem2flow(e,style,width):
                        yield ee
                    frags=[]
##                 if e.__class__ is html.IMG:
##                     yield self.makepar("",style,frags=frags)
##                     yield platypus.Image()
##                     frags=[]
                #elif e.__class__ is H1:
                #    yield self.makepar("",style,frags=frags)
            yield self.makepar("",style,frags=frags)
            
            #yield platypus.Table(data)
        else:
            raise "Cannot flow %r" % elem
##             yield self.makepar(str(elem),style)
        
    def elem2frags(self,elem,style):
        #print "elem2frags(%s)" % elem
        frag=ParaFrag()
        frag.text=''
        frag.fontName=style.fontName
        frag.fontSize=style.fontSize
        frag.textColor=style.textColor
        frag.rise=style.rise
        frag.underline=style.underline
        frag.strike=0 # added for reportlab 2.0
        frag.link=None # added for reportlab 2.0
        if elem.__class__ == html.CDATA:
            frag.text=" ".join(elem.text.split())
            if elem.text.startswith(" "):
                frag.text=" "+frag.text
            if elem.text.endswith(" "):
                frag.text+=" "
            
            #frag.text=elem.text
            yield frag
            return
        if elem.__class__ == html.BR:
            #frag.text='\n'
            frag.lineBreak=True
            yield frag
            return
        assert hasattr(elem,'content')
        if elem.__class__ in (html.EM,html.I):
            family, bold, italic = ps2tt(frag.fontName)
            frag.fontName=tt2ps(family,bold,1)
            #frag.fontName=frag.fontName+"-Italic"
        elif elem.__class__ == html.TT:
            family, bold, italic = ps2tt(frag.fontName)
            frag.fontName=tt2ps("Courier",bold,italic)
        elif elem.__class__ == html.B:
            family, bold, italic = ps2tt(frag.fontName)
            frag.fontName=tt2ps(family,1,italic)
        elif elem.__class__ == html.U:
            frag.underline=True
        elif elem.__class__ == html.SUP:
            frag.rise=True
        else:
            raise "Cannot handle <%s> inside a paragraph" \
                  % elem.tag()
##         for e in elem.content:
##             if e.__class__ == html.CDATA:
##                 frag.text += e.text
##             else:
##                 for ee in elem.content:
##                     for f in self.elem2frags(ee,frag):
##                         yield f
        
        for e in elem.content:
            for f in self.elem2frags(e,frag):
                yield f
        yield frag

    


    def getDocumentWidth(self):
        docstyle=self.getElementStyle(self.body)
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
        style = self.getElementStyle(self.body)
        textWidth = self.getDocumentWidth()

        x = style.leftMargin
        y = style.pagesize[1] - style.topMargin # headerHeight
            
        # x and y are the bottom left corner of the frame. The
        # canvas' (0,0) is not the paper's (0,0) but the bottom left
        # corner of the printable area

        self.drawFrame(canvas, style.header, x, y,
                       textWidth, style.topMargin,
                       style=self.stylesheet.Header)

        
        y = style.bottomMargin 
        self.drawFrame(canvas, style.footer, x, y,
                       textWidth, style.bottomMargin,
                       style=self.stylesheet.Footer)
        
    def drawFrame(self,canvas,func,x,y,
                  textWidth,availableHeight,style):
        if func is None:
            return
        story=self.createStory()
        func(story)
        #story = self.makeStory(func, textWidth)
        #if story is not None:
        pdfstory=[]
        for e in story.content:
            pdfstory += self.elem2flow(
                e,self.getElementStyle(e),textWidth)
            
        height = 0
        for e in pdfstory:
            unused,h = e.wrap(textWidth,availableHeight)
            height += h
            availableHeight -= h

        if style.valign == styles.VA_BOTTOM:
            pass
        elif style.valign == styles.VA_MIDDLE:
            y -= (height/2)
        elif style.valign == styles.VA_TOP:
            y -= height

        canvas.saveState()
        f = platypus.Frame(x,y,
                           textWidth,height,
                           leftPadding=0,
                           rightPadding=0,
                           bottomPadding=0,
                           topPadding=0) #showBoundary=True)
        f.addFromList(pdfstory,canvas)
        canvas.restoreState()


    def pdftable(self,element,width,style):
        assert element.__class__ is html.TABLE

        cellFormats = style.headerCellFormats \
                      + style.dataCellFormats
        
        colCount=0
        for tr in html.tablerows(element,2): # table body
            colCount=max(len(tr.content),colCount)

        columns=[]
        for elem in element.content:
            if elem.__class__ is html.COLGROUP:
                for col in elem.content:
                    if col.width[-1] == "*":
                        columns.append(TableColumn(
                            weight=int(col.width[:-1])))
                    elif col.width is not None:
                        raise NotImplementedError,"non-relative width"
                    else:
                        columns.append(TableColumn())

        if len(columns) == 0:
            for i in range(colCount):
                columns.append(TableColumn())
        else:
            assert colCount <= len(columns)

        # distribute free space to all columns whose width is None
        remainingWidth = width - style.leftIndent - style.rightIndent
        freeCount = 0   # number of columns whose width is None
        for col in columns:
            if col.width is None:
                freeCount += col.weight
            else:
                remainingWidth -= col.width
        if remainingWidth < 0:
            raise "remainingWidth %s is < 0" % repr(remainingWidth)

        if freeCount > 0:
            w = remainingWidth / freeCount

        colWidths = [] 
        for col in columns:
            if col.width is None:
                assert freeCount > 0 # of course
                colWidths.append(col.weight * w - epsilon)
            else:
                colWidths.append(col.width-epsilon)

        showHeaders=False
        i=0
        for tr in html.tablerows(element,0): # table header
            for th in tr.content:
                col=columns[i]
                col.label=[ e for e in self.elem2flow(
                    th,self.getElementStyle(th),colWidths[i])]
                if len(col.label)>0:
                    showHeaders=True
                    #print col.label
                i += 1


        rows=[]
        for tr in html.tablerows(element,2): # table body
            row=[]
            i=0 # column index
            for td in tr.content:
                l=[]
                l += self.elem2flow(
                    td, self.getElementStyle(td), colWidths[i])
                if len(l) == 1:
                    row.append(l[0])
                else:
                    row.append(l)
                i+=1
            rows.append(row)


        if showHeaders:
            headerData = []
            for col in columns:
                if col.label is None:
                    headerData.append("")
                else:
                    headerData.append(col.label)
            rows.insert(0,headerData)

        if len(rows) == 0:
            return

        t = platypus.Table(rows,colWidths)

        # note that Reportlab's TableStyle is only one part of gendoc's
        # TableStyle:

        # style of the table as a flowable:
        t.style = style
        # border formatting :
        t.setStyle(platypus.TableStyle(cellFormats))

        return t


        
        

## class PdfMaker(Application):

##     name="Lino/PdfMaker"

##     copyright="""\
## Copyright (c) 2006 Luc Saffre.
## This software comes with ABSOLUTELY NO WARRANTY and is
## distributed under the terms of the GNU General Public License.
## See file COPYING.txt for more information."""
    
##     url="http://lino.saffre-rumma.ee/pdfmaker.html"
    
##     usage="usage: %s [options] [FILE]"
    
##     description="""\

## PdfMaker creates a PDF file named FILE and then runs Acrobat Reader to
## view it. Default for FILE is "tmp.pdf".

## """

    

##     def run(self,body,ofname=None,**kw):
        
##         if True:
##             doc=PdfDocument()
##         else:
##             doc=html.HtmlDocument()
            
##         if ofname is None:
##             if len(self.args) > 0:
##                 ofname=self.args[0]
##             else:
##                 ofname="tmp"+doc.extension
##         try:
##             self.status("Preparing...")
##             #try:
##             body(doc.body)
##             #except ParseError,e:
##             #    raise

##             #print doc.body.toxml()
            
##             self.status("Writing %s...",ofname)
##             doc.saveas(ofname,**kw)
##             self.notice("%d pages." % doc.getPageNumber())
##             if self.isInteractive():
##                 self.showfile(ofname)

##         except IOError,e:
##             print e
##             return -1

