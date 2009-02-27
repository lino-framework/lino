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


#from lino.gendoc import gendoc # import WriterDocument

from xml.sax.saxutils import escape, unescape

from lino.gendoc.elements import \
     CDATA, Element, Container

class BR(Element):
    #flowable=True
    pass

class IMG(Element):
    flowable=True
    allowedAttribs=dict(src="src",
                        width="width",
                        height="height")



class Fragment(Container):
    fragmentable=True
    flowable=False
##     allowedAttribs=dict(id='id',
##                         lang='lang',
##                         title='title')
    allowedAttribs=dict(xclass='class',
                        id='id',
                        lang='lang',
                        style='style',
                        title='title')


class SPAN(Fragment):
    allowedContent = (CDATA,Fragment)

#class DIV(Fragment):
#    allowedContent = (CDATA,P,TABLE,SPAN,BR,IMG)
    

class B(SPAN): pass    
class EM(SPAN): pass    
class I(SPAN): pass
class U(SPAN): pass
class SUP(SPAN): pass
class TT(SPAN): pass    
class FONT(SPAN): pass

class LI(Fragment):
    flowable=True
    
    """Maybe P must be the first element because MemoParser wouln't
    otherwise handle empty lines inside a LI correctly.  To be
    tested."""

class UL(Fragment): 
    flowable=True
    allowedContent = (LI,)
    def li(self,*args,**kw):
        return self.append(LI(*args,**kw))

class OL(UL): 
    pass



class Cell(Fragment):
    allowedAttribs=dict(
        align="align",
        valign="valign",
        **Fragment.allowedAttribs)
class TD(Cell):
    pass
    
class TH(Cell):
    pass
    
class TR(Fragment):
    allowedContent=(TD,TH)
    
class COL(Element):
    allowedAttribs=dict(span="span",width="width")

class COLGROUP(Fragment):
    allowedContent=(COL,)
    allowedAttribs=dict(span="span",width="width")

class THEAD(Fragment):
    allowedContent=(TR,)
class TFOOT(Fragment):
    allowedContent=(TR,)
class TBODY(Fragment):
    allowedContent=(TR,)
    
class TABLE(Fragment):
    fragmentable=False
    flowable=True
    allowedContent=(TR,COLGROUP,THEAD,TFOOT,TBODY)
    
    def addrow(self,*cells):
        return self.append(TR(*[TD(e) for e in cells]))
    
def tablerows(table,area):
    """
    area is one of 0:THEAD, 1:TFOOT, 2:TBODY

    subdividing a table into areas is optional. if present, it must be
    in the specified order. if no areas specified, all TR elements are
    considered part of the TBODY.
    
    """
    for elem in table.content:
        if elem.__class__ is THEAD:
            if area == 0:
                for cell in elem.content:
                    yield cell
        elif elem.__class__ is TFOOT:
            if area == 1:
                for cell in elem.content:
                    yield cell
        elif elem.__class__ is TBODY:
            if area == 2:
                for cell in elem.content:
                    yield cell
        elif elem.__class__ is TR:
            if area == 2:
                yield elem
        elif elem.__class__ is COLGROUP:
            pass
        else:
            raise "unhandled element %s" % elem
        




class P(Fragment):
    fragmentable=False
    flowable=True
    allowedContent = (CDATA,SPAN,BR,IMG)
    allowedAttribs = dict(
        align="align",
        **SPAN.allowedAttribs)
    
class H(P):
    level=None
    def __init__(self,level,*args,**kw):
        assert level > 0 and level <= 9
        self.level=level
        Container.__init__(self,*args,**kw)
        
    def tag(self):
        return self.__class__.__name__+str(self.level)
        
class H1(P): pass

class PRE(P):
    allowedContent = (CDATA,)

class A(SPAN):
    allowedAttribs=dict(href="href",
                        **SPAN.allowedAttribs)


P.autoClosedByStart=(P,LI,UL,OL,TABLE)
P.autoClosedByEnd=(LI,UL,OL,TABLE,TD,TH,TR)
TD.autoClosedByStart=(TD,TH,TR)
TD.autoClosedByEnd=(TH,TR,TABLE)
TH.autoClosedByStart=(TD,TH,TR)
TH.autoClosedByEnd=(TD,TR,TABLE)
TR.autoClosedByStart=(TR,TABLE)
TR.autoClosedByEnd=(TABLE,)
LI.autoClosedByStart=(LI,)
LI.autoClosedByEnd=(UL,OL)

LI.allowedContent = TD.allowedContent \
                    = TH.allowedContent \
                    = (CDATA,P,BR,SPAN,IMG,TABLE)
    

    
class Story:
    """
    Implemented by BODY and Document
    """
    def format(self,**kw):
        raise NotImplementedError
            
    def append(self,*args,**kw):
        raise NotImplementedError
            
    def table(self,*args,**kw):
        return self.append(Table(self.getDocument(),*args,**kw))

    def par(self,*args,**kw):
        return self.append(P(*args,**kw))
        
    def heading(self,level,text,**kw):
        return self.append(H(level,text,**kw))
    def h1(self,txt,**kw): self.heading(1,txt,**kw)
    def h2(self,txt,**kw): self.heading(2,txt,**kw)
    def h3(self,txt,**kw): self.heading(3,txt,**kw)
    def getStyle(self,*args,**kw):
        return self.getDocument().getElementStyle(self,*args,**kw)

    def getPageNumber(self):
        return self.getDocument().getPageNumber()
    
    def memo(self,txt,style=None,**kw):
        from lino.gendoc.memo import MemoParser
        p=MemoParser(self,style,**kw)
        p.feed(txt)
        p.close()

    def report(self,rpt):
        rpt.beginReport()
        header=[TH(col.getLabel(),
                  align=col.datatype.halign,
                  valign=col.datatype.valign)
                for col in rpt.columns]
        t=TABLE()
        cols=[]
        for col in rpt.columns:
            cols.append(COL(width=str(col.width)+"*"))
        t.append(COLGROUP(*cols))
        t.append(THEAD(TR(*header)))
        # TFOOT if present must come before TBODY
        tbody=t.append(TBODY())
        for row in rpt.rows():
            line=[TD(s, align=col.datatype.halign,
                     valign=col.datatype.valign)
                  for (col,s) in row.cells()]
            tbody.append(TR(*line))
            
        rpt.endReport()
        #print t.toxml()
        return self.append(t)

    def par(self,txt,style=None,**kw):
        return self.append(P(txt,xclass=style,**kw))

    def pre(self,txt,style=None,**kw):
        return self.append(PRE(txt,xclass=style,**kw))

    def heading(self,level,txt,style=None,**kw):
        return self.append(H(level,txt,xclass=style,**kw))

    def verses(self,txt,style=None,**kw):
        if False:
            # this would be better, but reportlab cannot handle
            # manual line breaks
            t2=""
            for line in txt.splitlines():
                if len(line.strip()):
                    t2 += "<br/>"+line
                else:
                    t2 += '\n'
            return self.memo(txt,style,False,**kw)
        # so we must use a trick:
        if style is None:
            style="Verses"
        return self.memo(txt,style,**kw)

    def example(self,intro,code):
        self.memo(intro)
        self.h2("Code:")
        self.pre(code)
        self.h2("Result:")
        self.memo(code)
    
            
        
    def table(self,*args,**kw):
        return self.append(TABLE(*args,**kw))
    def ul(self,*args,**kw):
        return self.append(UL(*args,**kw))
    def ol(self,*args,**kw):
        return self.append(OL(*args,**kw))
    
    def getDocument(self):
        raise NotImplementedError

    
class BODY(Container,Story):
    allowedAttribs= dict(
        bgcolor='bgcolor',
        **Fragment.allowedAttribs)
        
    def __init__(self,doc,*args,**kw):
        self._document=doc
        Container.__init__(self,*args,**kw)

    def getDocument(self):
        return self._document

    def format(self,**kw):
        self.getDocument().format(self,**kw)



    
##     def __init__(self,href=None,label=None,doc=None):
##         if label is None: label=href
##         self.href=href
##         self.label=label
##         self.doc=doc
        
##     def __html__(self,doc,wr):
##         wr('<a href="'+self.href+'">')
##         wr(escape(self.label))
##         wr('</a>')

## def html2css(k,v):
##     if k == "align":
##         if v.lower() == "left": return "alignment",TA_LEFT
##         if v.lower() == "right": return "alignment",TA_RIGHT
##         if v.lower() == "center" : return "alignment",TA_CENTER
##     elif k == "valign":
##         if v.lower() == "top": return "vAlign",VA_TOP
##         if v.lower() == "bottom": return "vAlign",VA_BOTTOM
##         if v.lower() == "center": return "vAlign",VA_MIDDLE
##     raise "html2pdf(%r,%r)" % (k,v)


class FakeStyle:
    def update(self,**kw):
        pass


class Document(Story):
    extension=None
    def __init__(self,
                 title="Untitled",
                 date=None,
                 stylesheet=None):

        self.title=title
        self.date=date
        self.stylesheet=stylesheet
        self.body=self.createStory()

    def createStory(self):
        "also used in PdfDocument.drawFrame()"
        return BODY(self)

    def append(self,*args,**kw):
        return self.body.append(*args,**kw)
        
    def setTitle(self,title):
        self.title=title

    def getPageNumber(self):
        return 1
    
    def getDocument(self):
        return self

    def getStyle(self,*args,**kw):
        return self.getDocument().getElementStyle(self.body,*args,**kw)
    
    def getElementStyle(self,elem,name=None,parent=None):
        return FakeStyle()
    
##         stName=elem.xclass 
##         if stName is None:
##             stName=elem.tag()
##         style=self.stylesheet[stName]
##         d={}
##         for k,v in elem._attribs.items():
##             if v is not None:
##                 if k != 'xclass':
##                     kk,vv=html2css(k,v)
##                     d[kk]=vv
##         if len(d):
##             return style.child(**d)
##         return style
        
        
class HtmlDocument(Document):
    
    extension=".html"
    
    def saveas(self,filename,showOutput=False):
        f=file(filename,"wt")
        self.__xml__(f.write)
        f.close()


    def __xml__(self,wr):
        wr("<html><head>\n<title>")
        wr(escape(self.title))
        wr("""</title>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
""")
        if self.stylesheet is not None:
            wr('<link rel=stylesheet type="text/css" href="%s">\n'
               % self.urlto(self.stylesheet))
        wr('<meta name="KEYWORDS" content="">\n')
        wr('<meta name="GENERATOR" content="lino.gendoc">\n')
        wr('<meta name="author" content="">\n')
        wr('<meta name="date" content="%s">'%self.date)
        wr("<head>\n")
        self.body.__xml__(wr)
        wr("""\n</html>\n""")


