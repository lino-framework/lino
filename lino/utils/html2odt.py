# -*- coding: utf-8 -*-
## Copyright 2003-2011 Luc Saffre 
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
"""
This is abandoned. See :doc:`/blog/2011/0523`
"""

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint


import types
#from xml.sax.saxutils import escape, unescape

from lino.utils import assert_pure

## from xml.sax import saxutils
## escape=saxutils.escape
## unescape=saxutils.unescape

# copied from twisted.web.microdom
ESCAPE_CHARS = (('&', '&amp;'),
                ('<', '&lt;'),
                ('>', '&gt;'),
                ('"', '&quot;'))

def escape(text):
    "Replace a few special chars with HTML entities."
    for ch, h in ESCAPE_CHARS:
        text=text.replace(ch, h)
    return text

def unescape(text):
    "Perform the exact opposite of 'escape'."
    for ch, h in ESCAPE_CHARS:
        text=text.replace(h, ch)
    return text


class InvalidRequest(Exception):
    pass


def quote(x):
    if type(x) == types.IntType:
        return '"'+str(x)+'"'
    if type(x) == types.BooleanType:
        return '"'+str(x).lower()+'"'
    #if type(x) == types.StringType:
    if isinstance(x,basestring):
        assert not '"' in x
        return '"'+x+'"'
    raise InvalidRequest("%s not handled" % str(type(x)))
    
class CDATA:
    fragmentable=True
    def __init__(self,text):
        assert_pure(text)
        self.text = text
        
    def __xml__(self,wr):
        #self.text.replace("&","&amp;").replace("<","&lt;"))
        #wr(escape(self.text).encode("iso-8859-1","xmlcharrefreplace"))
        wr(escape(self.text))

    def __str__(self):
        return self.text
        
class Element:
    fragmentable = False
    flowable = False
    elementname = None
    allowedAttribs = {}
    autoClosedByStart = []
    autoClosedByEnd = []
    #defaultAttribs = {}
    parent = None
    style = None
    def __init__(self,style=None,**kw):
        if style is not None:
            self.style=style
        if self.elementname is None:
            self.elementname=self.__class__.__name__
            #raise InvalidRequest(
            #    "Cannot instantiate %s : no elementname" %
            #    str(self.__class__))
        self._attribs = {}
        self.setAttribs(**kw)

    def setParent(self,parent):
        self.parent=parent
        
    def setAttribs(self,**kw):
        for k,v in kw.items():
            #assert not k in self.defaultAttribs.keys()
            try:
                xmlname = self.allowedAttribs[k]
            except KeyError,e:
                raise InvalidRequest(
                    "%s attribute not allowed for %s" % (
                    repr(k), self.__class__.__name__))
            self._attribs[k] = v
            
    def __getattr__(self,name):
        try:
            return self._attribs[name]
        except KeyError:
            if self.allowedAttribs.has_key(name):
                return None
            raise AttributeError(
                "%s instance has no attribute '%s'" % (
                self.__class__.__name__, name))
        
    def tag(self):
        return self.elementname
    
    def __xml__(self,wr):
        wr("<"+self.tag())
        for k,v in self._attribs.items():
            if v is not None:
                wr(' %s=%s' % (self.allowedAttribs[k],quote(v)))
        wr('/>')
        
    def toxml(self):
##         s=u""
##         def wr(x):
##             s.__add__(x)
##         self.__xml__(wr)
##         return s
        from timtools.misc.tsttools import UniStringIO
        u=UniStringIO()
##         from cStringIO import StringIO
##         b=StringIO()
##         def wr(s):
##             b.write(s.encode("utf-8"))
##         self.__xml__(wr)
        self.__xml__(u.write)
        return u.getvalue()

        
class Container(Element):
    allowedContent = (CDATA,Element)
    primaryKey = None
    def __init__(self,*content,**kw):
        Element.__init__(self,**kw)
        self.content = []
        for elem in content:
            #if type(elem) == types.StringType:
            self.append(elem)   
        
    def append(self,elem):
        #print self.allowedContent
        if isinstance(elem,basestring):
            e=self.allowedContent[0](elem)
            self.content.append(e)
            e.setParent=self
            return e
        for cl in self.allowedContent:
            if isinstance(elem,cl):
                self.content.append(elem)
                elem.setParent=self
                return elem
        raise InvalidRequest(
            "%s not allowed in %s" %
            (elem.__class__.__name__,self.__class__.__name__))

    def peek(self,*key):
        if self.primaryKey is None:
            raise InvalidRequest(
                str(self.__class__)+" has no primaryKey")
        if len(self.primaryKey) != len(key):
            raise InvalidRequest(
                "Expected %d key elements but got %d" %
                len(self.primaryKey),len(key))
        for ch in self.content:
            i = 0
            found = True
            for k in key:
                if getattr(ch,self.primaryKey[i]) != k:
                    found = False
                    break
            if found: return ch
        raise InvalidRequest(str(key)+" no such child")
                
        
        
    def __xml__(self,wr):
        wr("<"+self.tag())
        if len(self._attribs) > 0:
            for k,v in self._attribs.items():
                if v is not None:
                    wr(' %s=%s' % (self.allowedAttribs[k],quote(v)))
        if len(self.content) == 0:
            wr('/>')
        else:
            wr('>')
            for e in self.content:
                e.__xml__(wr)
            wr("</"+self.tag()+">" )






class TextElement(Element):
    "any element that may appear besides CDATA in a paragraph context"
    pass

class TextContainer(Container):
    
    """any conainer element that may appear besides TextElement and
    CDATA in a paragraph context"""
    
    pass

    

class LineBreak(TextElement):
    elementname = "text:line-break"


class Text(TextContainer):
    elementname = "number:text"
    allowedContent = (CDATA,)

class Span(Text):
    elementname = "text:span"
    
class SheetName(Text):
    elementname = "text:sheet-name"
class PageNumber(Text):
    elementname = "text:page-number"
class Title(Text):
    elementname = "text:title"
    
class Date(Text):
    elementname = "text:date"
    allowedAttribs=dict(
        dataStyleName="style:data-style-name",
        dateValue="text:date-value")

class Time(Text):
    elementname = "text:time"
    
    
        
        
class P(Container):
    allowedContent = (CDATA,TextElement,TextContainer)
    elementname = "text:p"
    allowedAttribs = dict(
        styleName='text:style-name')
        
    #~ def __init__(self,style="Default",*content,**kw):
        #~ kw['style'] = style
        #~ Container.__init__(self,*content,**kw)
        
    
class H(P):
    allowedContent = (CDATA,)
    elementname = "text:h"
    allowedAttribs = dict(
        level='text:level',
        **P.allowedAttribs)
        
    def __init__(self,level,*content,**kw):
        kw['styleName'] = "Heading "+str(level)
        kw['level'] = level
        P.__init__(self,*content,**kw)
        
        
def H1(*args,**kw): return H(1,*args,**kw)
def H2(*args,**kw): return H(2,*args,**kw)
def H3(*args,**kw): return H(3,*args,**kw)
        




"""
If you want to create documents in the same format as OpenOffice.org does, you should give each 
<style:style> an appropriate style:name and style:family attribute. Styles to be applied to characters 
should have a style:name of the form T followed by an integer and have a style:family of text. Styles to be 
applied to paragraphs or headings should have a style:name of the form P followed by an integer and have a 
style:family of paragraph.
(http://books.evc-cit.info/ch03.php)

Common and automatic styles have the same XML representation, but they are contained within
two distinct container elements, as follows:
● <office:styles> for common styles
● <office:automatic-styles> for automatic styles
Master styles are contained within a container element of its own:
● <style:master-styles>
(...)
A page layout describes the physical properties or geometry of a page, for example, page size,
margins, header height, and footer height.
A master page is a template for pages in a document. It contains a reference to a page layout
which specifies the physical properties of the page and can also contain static content that is
displayed on all pages in the document that use the master page. Examples of static content are
headers, footers, or background graphics.

_oospec-1.0: http://www.oasis-open.org/committees/download.php/6037/office-spec-1.0-cd-1.pdf

The style:name attribute identifies the name of the style. This attribute, combined with the
style family attribute, uniquely identifies a style. You cannot have two styles with the same
family and the same name.

The style:family attribute identifies the family of the style, for example, paragraph, text, or
frame. It might have one of the following values: paragraph, text, section, table, tablecolumn,
table-row, table-cell, table-page, chart, default, drawing-page, graphic, presentation, control and ruby.
[oospec-1.0, p. 381]

Table cell style can have an associated data style.
[oospec-1.0, p. 383]

A default style specifies default formatting properties for a certain style family. These defaults are
used if a formatting property is neither specified by an automatic nor a common style. Default
styles exist for all style families that are represented by the <style:style> element specified in
section 13.1.
Default styles are represented by the <style:default-style> element.
[oospec-1.0, p. 396]


"""
    
    
class Properties(Container):
    # <style:properties fo:font-style="italic" style:text-underline="single" style:text-underline-color="font-color" fo:font-weight="bold"/>
    # <style:properties fo:text-align="center" style:text-align-source="fix" fo:font-size="16pt" fo:font-style="italic" fo:font-weight="bold"/>
    # <style:properties fo:text-align="center" style:text-align-source="fix" fo:font-size="16pt" fo:font-style="italic" fo:font-weight="bold"/>
    # <style:properties fo:direction="ltr" style:rotation-angle="90"/>
    # <style:properties style:writing-mode="lr-tb"/>
    #~ <style:properties fo:min-height="0.751cm" fo:margin-left="0cm" fo:margin-right="0cm" fo:margin-top="0.25cm" 
    #~  fo:border="0.088cm solid #000000" fo:padding="0.018cm" fo:background-color="#c0c0c0">
    elementname="style:properties"
    allowedAttribs=dict(
        decimalPlaces="style:decimal-places",
        fontName="style:font-name",
        fontSize="fo:font-size",
        language="fo:language",
        country="fo:country",
        tabStopDistance="style:tab-stop-distance",
        fontWeight="fo:font-weight",
        fontStyle="fo:font-style",
        textUnderline="style:text-underline",
        textUnderlineColor="style:text-underline-color",
        textAlign="fo:text-align",
        textAlignSource="style:text-align-source",
        justifySingleWord="style:justify-single-word",
        direction="fo:direction",
        rotationAngle="style:rotation-angle",
        writingMode="style:writing-mode",
        minHeight="fo:min-height",
        marginLeft="fo:margin-left",
        marginRight="fo:margin-right",
        marginTop="fo:margin-top",
        marginBottom="fo:margin-bottom",
        border="fo:border",
        padding="fo:padding",
        backgroundColor="fo:background-color",
        pageWidth="fo:page-width",
        pageHeight="fo:page-height",
        numFormat="style:num-format",
        printOrientation="style:print-orientation",
        footnoteMaxHeight="style:footnote-max-height",
        useWindowFontColor="style:use-window-font-color",
        hyphenate="fo:hyphenate",
        hypenationRemainCharCount="fo:hyphenation-remain-char-count",
        hypenationPushCharCount="fo:hyphenation-push-char-count" ,
        hypenationLadderCount="fo:hyphenation-ladder-count",
        textAutospace="style:text-autospace",
        punctuationWrap="style:punctuation-wrap",
        lineBreak="style:line-break",
        columnWidth="style:column-width",
        **Element.allowedAttribs)

class TableProperties(Properties):
    allowedAttribs=dict(
        align="table:align",
        width="style:width",
        relWidth="style:rel-width",
        **Element.allowedAttribs)
        
        
    

class BackgroundImage(Element):
    #~ <style:background-image/>
    elementname="style:background-image"


class Number(Element):
    elementname="number:number"
    allowedAttribs=dict(
    minIntegerDigits="min-integer-digits",
    decimalPlaces="number:decimal-places",
    grouping="number:grouping",
    )
    

class CurrencySymbol(Text):
    # <number:currency-symbol number:language="fr" number:country="BE">EUR</number:currency-symbol>
    elementname = "number:currency-symbol"
    allowedAttribs=dict(
        language="number:language",
        country="number:country",
    )






        
        
class TableColumn(Element):
    elementname = "table:table-column"
    allowedAttribs = dict(
        styleName="table:style-name",
        numberColumnsRepeated="table:number-columns-repeated"
        )
    #def addProperties(self,**kw):
    def __init__(self,table,**kw):
        assert isinstance(table,Table)
        self.table = table
        name = table.name+"."+str(len(table.columns)+1)
        s = table.doc.addAutoStyle(name=name,family="table-column")
        if len(kw):
            s.addProperties(**kw)
        Element.__init__(self,styleName=s.name)

##     def addProperties(self,**kw):
##         self.append(Properties(**kw))
    
    
class TableCell(Container):
    allowedContent = (P,Span,Container)
    elementname = "table:table-cell"
    allowedAttribs = dict(
        valueType="table:value-type",
        numberColumnsSpanned="table:number-columns-spanned",
        )
    
class TableRow(Container):
    allowedContent = (TableCell,)
    elementname = "table:table-row"
    def __init__(self,table,*args,**kw):
        Container.__init__(self,*args,**kw)
        self._table = table

    def cell(self,*content,**kw):
        if len(self.content) == len(self._table.columns):
            s = self._table.column()
        elem = TableCell(valueType="string",*content,**kw)
##         for x in content:
##             if isinstance(x,TableCell):
##                 row.cell(cell)
##             else:
##                 row.cell(TableCell(cell))
        self.append(elem)
            
        #if len(kw):
        #    raise NotImplementedError
            #if kw.has_key('styleName')
            #s = self._table.doc.addAutoStyle(name="?",family="todo")
            # cell style? or paragraph style
        return elem

class TableHeaderRows(Container):
    allowedContent = (TableRow,)
    elementname = "table:table-header-rows"

    

class Table(Container):
    elementname = "table:table"
    allowedContent = (TableHeaderRows,TableColumn,TableRow)
    allowedAttribs = dict(
        name="table:name",
        styleName='table:style-name',
        #styleFamily='style:family',
    )
    #defaultAttribs = dict(styleFamily="table")
    
    
    def __init__(self,doc,name=None,styleName=None,**kw):

        if name is None:
            name = "Table"+str(len(doc.getTables())+1)
        if styleName is None:
            styleName = name
            s = doc.addAutoStyle(name=styleName,
                                 family="table")
            if len(kw)>0:
                if kw.has_key('width'):
                    if not kw.has_key('align'):
                        kw['align'] = 'center'
                s.append(TableProperties(**kw))
        else:
            assert len(kw) == 0
            s = doc.getStyle(styleName,"table")
            # just to check existence
                                 
        Container.__init__(self,name=name, styleName=styleName)

        self.doc = doc
        self.columns = []
        self._headerRows = None

    def heading(self,level,text,**kw):
        return self.p(text,styleName="Heading"+str(level),**kw)
    
    def par(self,text,**kw):
        r = self.row()
        p = P(text,**kw)
        r.cell(p,numberColumnsSpanned=str(len(self.columns)))
        #r.__xml__(sys.stdout.write)
        return p

    def column(self,**kw):
        assert self._headerRows is None
        col = TableColumn(self,**kw)
        self.columns.append(col)
        self.append(col)
        return col
    
##     def column(self,**kw):
##         name = self.name+"."+str(len(self.columns)+1)
##         s = self.doc.addAutoStyle(name=name,family="table-column")
##         if len(kw):
##             s.addProperties(**kw)
##         col = TableColumn(self,**kw)
##         self.columns.append(col)
##         self.append(col)
##         if len(kw):
##             col.addProperties(**kw)
##         return col
        
    def createTableRow(self,*cells,**kw):
        row = TableRow(self,**kw)
        for cell in cells:
            row.cell(cell)
##             if isinstance(cell,TableCell):
##                 row.cell(cell)
##             else:
##                 row.cell(TableCell(cell))
        return row

    def row(self,*cells,**kw):
        r = self.createTableRow(*cells,**kw)
        self.append(r)
        return r
        
    def headerRow(self,*cells,**kw):
        r = self.createTableRow(*cells,**kw)
        if not self._headerRows:
            self._headerRows = TableHeaderRows()
            self.append(self._headerRows)
        self._headerRows.append(r)





    
    
class MyHTMLParser(HTMLParser):

    def __init__(self,container,**kw):
        HTMLParser.__init__(self)
        self.container = container
        self.style = None
        self.kw = kw
        self.stack = []
        self.parsep = False

    def handle_data(self,data):
        """process arbitrary data."""
        #print "handle_data(%r) to %s"%(
        #    data,[e.tag() for e in self.stack])
        if len(self.stack) == 0:
            if len(data.strip()) == 0:
                return
            p = P(**self.kw)
            self._append(p)
            #self.autopar()
        tail = self.stack[-1]
        #print self.container.toxml()
        #print "%r -> %r" % (data, tail)
        #raw_input()
        if CDATA in tail.__class__.allowedContent:
            #print data.split('\n\n'), "to", \
            #      [e.tag() for e in self.stack],\
            #      self.parsep
            first=True
            #newpar=False
            for chunk in data.split('\n\n'):
                if first:
                    first = False
                else:
                    self.parsep = True
                if len(chunk.strip()) > 0:
                    if self.parsep:
                        self.parsep = False
                        self._append(
                            P(chunk,**self.kw))
                    else:
                        tail.append(chunk)
                elif not self.parsep:
                    tail.append(chunk)
                #newpar=True

        elif len(data.strip()) > 0:
            raise "cannot handle %r inside <%s>" % (data,tail.tag())

    def handle_charref(self,name):
        """process a character reference of the form "&#ref;"."""
        #print "handle_charref", name
        raise NotImplemented
    
        
    def handle_entityref(self,name):
        """process a general entity reference of the form "&name;"."""
        self.handle_data(unichr(name2codepoint[name]))
        #self.handle_data("&"+name+";")
        #print "handle_entityref", name
        #raise NotImplemented

    def _append(self,elem):
        while True:
            #print "_append(%s) to %s" % (
            #    elem.__class__.__name__,
            #    [e.__class__.__name__ for e in self.stack])
            if len(self.stack) == 0:
                if elem.flowable:
                    self.stack.append(elem)
                    self.container.append(elem)
                    return
                # create automagic paragraph
                # e.g. a memo that starts with "<tt>"
                p = P(**self.kw)
                self._append(p)
                # don't return but loop again
            try:
                self.stack[-1].append(elem)
                self.stack.append(elem)
                return 
            except InvalidRequest,e:
                #print "could not append <%s> to <%s>" % (
                #    elem.tag(),
                #    self.stack[-1].tag())
                if elem.__class__ in self.stack[-1].autoClosedByStart:
                    popped = self.stack.pop()
                    #print "<%s> automagically closes <%s>" % (
                    #    elem.tag(),
                    #    popped.tag())
                    # don't return but loop again
                else:
                    raise
        
        #print "<%s> was added to <%s>" %(elem.tag(),self.stack[-1].tag())
        
    def do_starttag(self,tag,attrs):
        tag = tag.upper()
        #~ cl = getattr(html,tag)
        cl = globals().get(tag)
        #print attrs
        d = {}
        for hk,hv in attrs:
            found = False
            for k,v in cl.allowedAttribs.items():
                if v == hk:
                    d[k] = hv
                    found = True
                    break
            if not found:
                raise "unhandled attribute %s" % k
        elem=cl(**d)
        if self.parsep: 
            self.parsep=False
            if not elem.flowable:
                #print "automagic P for nonflowable", elem.tag()
                self._append(P(**self.kw))
        self._append(elem)
        return elem
        
        
        
    def handle_startendtag(self,tag, attrs):
        elem=self.do_starttag(tag,attrs)
        self.stack.pop()

    def handle_starttag(self, tag, attrs):
        #print "found <%s>" % tag
        #print "handle_starttag(%s)"%tag
        elem = self.do_starttag(tag,attrs)
        if not isinstance(elem,Container):
            # tolerate <img> or <br> without endtag
            self.stack.pop()

    def handle_endtag(self, tag):
        #print "found </%s>" % tag
        while True:
            if len(self.stack) == 0:
                raise ParseError("stack underflow")
            popped = self.stack.pop()
            if tag.upper() == popped.tag():
                return
            cl = getattr(html,tag.upper())
            if cl in popped.autoClosedByEnd:
                pass
                #print "<%s> autoClosedBy </%s>" % (
                #    popped.tag(),tag.upper())
            else:
                raise "Found </%s>, expected </%s> (stack was %s)" % (
                    tag.upper(), popped.tag(),
                    [e.tag() for e in self.stack]+[popped.tag()]
                    )





def html2odt(html):
    story = []
    p = MyHTMLParser(story)
    p.feed(html)
    p.close()
    return '\n'.join([e.toxml() for e in story])



      
      
if __name__ == "__main__"	:
    html = '''
    <p>Hello,&nbsp;world!<br>Again I say: Hello,&nbsp;world!</p>
    <img src="foo.org">
    '''
    print html
    print html2odt(html)
    
