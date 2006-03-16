#coding: latin1

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
import types

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
    
## def makedict(**kw): 
##     return kw

class CDATA:
    def __init__(self,text):
        self.text = unicode(text)
    def __xml__(self,wr):
        s = self.text.replace("&","&amp;")
        #wr(s.decode().encode("utf-8"))
        wr(s.encode("utf-8"))
        
class Element:
    elementname = None
    allowedAttribs = {}
    #defaultAttribs = {}
    def __init__(self,**kw):
        if self.elementname is None:
            raise InvalidRequest(
                "Cannot instantiate %s : no elementname" %
                str(self.__class__))
        self._attribs = {}
        self.setAttribs(**kw)
        
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
            raise AttributeError(
                "%s instance has no attribute '%s'" % (
                self.__class__.__name__, name))
        
    def __xml__(self,wr):
        wr("<"+self.elementname)
        #for k,v in self.defaultAttribs.items():
        #    wr(' %s=%s' % (self.allowedAttribs[k],quote(v)))
        for k,v in self._attribs.items():
            wr(' %s=%s' % (self.allowedAttribs[k],quote(v)))
        #wr('/>')
        wr('/>\n')
        
class TextElement(Element):
    "any element that may appear besides CDATA in a paragraph context"
    pass

class Container(Element):
    allowedChildren = (CDATA,Element)
    primaryKey = None
    def __init__(self,*content,**kw):
        Element.__init__(self,**kw)
        self.children = []
        for elem in content:
            #if type(elem) == types.StringType:
            if isinstance(elem,basestring):
                self.append(self.allowedChildren[0](elem))  
            else:
                self.append(elem)   
        
    def append(self,elem):
        #print self.allowedChildren
        for cl in self.allowedChildren:
            if isinstance(elem,cl):
                self.children.append(elem)
                return
        raise InvalidRequest(
            "%s not allowed in %s" %
            (str(elem.__class__),repr(self)))

    def peek(self,*key):
        if self.primaryKey is None:
            raise InvalidRequest(
                str(self.__class__)+" has no primaryKey")
        if len(self.primaryKey) != len(key):
            raise InvalidRequest(
                "Expected %d key elements but got %d" %
                len(self.primaryKey),len(key))
        for ch in self.children:
            i = 0
            found = True
            for k in key:
                if getattr(ch,self.primaryKey[i]) != k:
                    found = False
                    break
            if found: return ch
        raise InvalidRequest(str(key)+" no such child")
                
        
        
    def __xml__(self,wr):
        wr("<"+self.elementname)
        if len(self._attribs) > 0:
            for k,v in self._attribs.items():
                wr(' %s=%s' % (self.allowedAttribs[k],quote(v)))
        if len(self.children) == 0:
            wr('/>\n')
        else:
            wr('>')
            for child in self.children:
                child.__xml__(wr)
            wr("</"+self.elementname+">\n" )

class TextContainer(Container):
    
    """any conainer element that may appear besides TextElement and
    CDATA in a paragraph context"""
    
    pass

class Story(Container):            
            
    def table(self,doc,*args,**kw):
        t = Table(doc,*args,**kw)
        self.append(t)
        return t

##     def table(self,doc,name=None,styleName=None,**kw):
##         if name is None:
##             name = "Table"+str(len(doc.getTables())+1)
##         if styleName is None:
##             styleName = name
##             s = doc.addAutoStyle(name=styleName, family="table")
##         else:
##             s = doc.getStyle(styleName,"table")
##             # just to check existence
                                 
##         t = Table(doc,name=name, styleName=styleName)
##         if len(kw)>0:
##             s.addProperties(**kw)
##         self.append(t)
##         return t
        
    def p(self,*args,**kw):
        p = P(*args,**kw)
        self.append(p)
        return p
        
    def h(self,level,text,**kw):
        h = H(level,text,**kw)
        self.append(h)
        return h
    

class LineBreak(TextElement):
    elementname = "text:line-break"


class Text(TextContainer):
    elementname = "number:text"
    allowedChildren = (CDATA,)

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
    allowedChildren = (CDATA,TextElement,TextContainer)
    elementname = "text:p"
    allowedAttribs = dict(
        styleName='text:style-name')
        
    #~ def __init__(self,style="Default",*content,**kw):
        #~ kw['style'] = style
        #~ Container.__init__(self,*content,**kw)
        
    
class H(P):
    allowedChildren = (CDATA,)
    elementname = "text:h"
    allowedAttribs = dict(
        level='text:level',
        **P.allowedAttribs)
        
    def __init__(self,level,*content,**kw):
        kw['styleName'] = "Heading "+str(level)
        kw['level'] = level
        P.__init__(self,*content,**kw)
        
        
        
        




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
        
        
class PageLayout(Properties):
    """
    The attributes that you can associate with the <style:page-layout> element are: name and pageUsage.     
    The style:page-usage attribute specifies the type of pages that the page master should generate. 
    (all, left, right, mirrored.)
    """
    elementname = "style:page-layout"
    allowedAttribs = dict(
        name="style:name",
        pageUsage="style:page-usage")
        
        
class FootnoteSep(Element):
        elementname = "style:footnote-sep"
        allowedAttribs  = dict(
            width="style:width",
            distanceBeforeSep="style:distance-before-sep",
            distanceAfterSep="style:distance-after-sep",
            adjustment="style:adjustment",
            relWidth="style:rel-width",
            color="style:color",
            )


    
        
    

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


class Style(Container):
    elementname = "style:style"
    allowedChildren = (Properties,)
    allowedAttribs=dict(
        name="style:name",
        family="style:family",
        className="style:class",
        volatile="style:volatile",
        parentStyleName="style:parent-style-name",
        dataStyle="style:data-style-name",
        #displayName="style:display-name",
    )
    primaryKey = ('name','family')
    
    def addProperties(self,**kw):
        self.append(Properties(**kw))
    
    
class NumberStyle(Style):
    elementname = "number:number-style"
    allowedChildren = (Properties,Number,Text)
    
class DefaultStyle(Style):
    """
A default style specifies default formatting properties for a certain style family. These defaults are
used if a formatting property is neither specified by an automatic nor a common style. Default
styles exist for all style families that are represented by the <style:style> element specified in
section 13.1.
Default styles are represented by the <style:default-style> element. The only attribute
supported by this element is style:family. Its meaning equals the one of the same attribute for
the <style:style> element, and the same properties child elements are supported depending
on the style family.
[oospec-1.0, p. 386]
    """
    elementname = "style:default-style"
    allowedAttribs=dict(family="style:family")
    allowedChildren=(Properties,)

class FooterStyle(Style):
    elementname = "style:footer-style"
    
class HeaderStyle(Style):
    elementname = "style:header-style"

class CurrencyStyle(NumberStyle):
    elementname = "number:currency-style"










        
        
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
    allowedChildren = (P,Span,Container)
    elementname = "table:table-cell"
    allowedAttribs = dict(
        valueType="table:value-type",
        numberColumnsSpanned="table:number-columns-spanned",
        )
    
class TableRow(Container):
    allowedChildren = (TableCell,)
    elementname = "table:table-row"
    def __init__(self,table,*args,**kw):
        Container.__init__(self,*args,**kw)
        self._table = table

    def cell(self,*content,**kw):
        if len(self.children) == len(self._table.columns):
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
    allowedChildren = (TableRow,)
    elementname = "table:table-header-rows"

    

class Table(Container):
    elementname = "table:table"
    allowedChildren = (TableHeaderRows,TableColumn,TableRow)
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

    def h(self,level,text,**kw):
        return self.p(text,styleName="Heading",**kw)
    
    def p(self,text,**kw):
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
                
                





    
    
class Font(Element):
    elementname = "style:font-decl"
    #def __init__(self,name=None,fontFamily=None,fontFamilyGeneric=None,fontPitch=None):
    allowedAttribs = dict(
        name="style:name",
        fontFamily="fo:font-family",  
        fontFamilyGeneric="style:font-family-generic", # e.g. "modern", "roman"
        fontPitch="style:font-pitch", #  e.g. "fixed", "variable"
    )

class PageMaster(Style):
    """The <style:page-master> element specifies the physical properties of a page. This element
contains a <style:page-layout-properties> element which specifies the formatting
properties of the page and two optional elements that specify the properties of headers and
footers.
    """
    elementname = "style:page-master"
    allowedChildren = (Properties,FootnoteSep,HeaderStyle,FooterStyle)
    
    
class MasterPage(Container):
    """
    In text and spreadsheet documents, the <style:master-page> element contains the content
    of headers and footers. In these applications, a sequence of pages is generated by making use of
    a single master page or a set of master pages.
    
    Master pages are contained in the <office:master-styles>
    element. See also section 2.8.  You must have one master page
    element.
    
    """
    elementname = "style:master-page"
    allowedAttribs = dict(
        name="style:name",
        pageMasterName="style:page-master-name"
    )
    
"""

The header and footer elements specify the content of headers and
footers. They are contained within a master page element. The
<style:header> and <style:footer> elements contain the content of
headers and footers. The two additional elements, <style:header-left>
and <style:footer-left>, can be used to specify different content for
left pages, if appropriate. If the latter two elements are missing,
the content of the headers and footers on left and right pages is the
same.

The content of headers and footers is either:

- Standard text content, for example paragraphs, tables, or
  lists. Such headers and footers usually are supported by text
  documents.

- A sequence of any of the following elements; <style:region-left>,
  <style:regioncenter> and <style:region-reight>. These elements
  usually are supported by spreadsheet documents. Writer ignores them.

- Empty, which switches off the display of all headers or footers. It
  is not possible to switch off the display of headers or footers for
  left pages only.


[p. 390]
"""

class Region(Container):
    allowedChildren = (P, Table)
    
    
class RegionLeft(Region):
    elementname = "style:region-left"
class RegionCenter(Region):
    elementname = "style:region-center"
class RegionRight(Region):
    elementname = "style:region-right"
    
class HeaderOrFooter(Story):
    allowedChildren = (CDATA, Region, P, Table)
    allowedAttribs = dict(display="style:display")
    
    
class Header(HeaderOrFooter):
    elementname = "style:header"
    
class Footer(HeaderOrFooter):
    elementname = "style:footer"

class HeaderLeft(Header):
    elementname = "style:header-left"

class FooterLeft(Footer):
    elementname = "style:footer-left"



# second-level elements used in ifiles.py
class Fonts(Container):
        elementname = "office:font-decls"
        allowedChildren = (Font,)

class Styles(Container):
        elementname = "office:styles"
        allowedChildren = (Style,)
        
class AutoStyles(Container):
        elementname = "office:automatic-styles"
        allowedChildren = (Style,)
        
class MasterStyles(Container):
        elementname = "office:master-styles"
        allowedChildren = (Style,MasterPage)
        
            
class Body(Story):
    elementname = "office:body"
    
##     def __init__(self,doc):
##         Story.__init__(self)
##         self.doc = doc
        
##     def getTables(self):
##         raise NotImplementedError
            
## class TextBody(Body):
    
##     def __init__(self,doc):
##         Body.__init__(self,doc)

##     def table(self,*args,**kw):
##         t = Story.table(self,*args,**kw)
##         self.tables.append(t)
##         return t
        
## class SpreadsheetBody(Body):

