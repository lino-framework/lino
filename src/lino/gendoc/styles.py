## Copyright 2003-2006 Luc Saffre.
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

"""
This is an alternative for reportlab/lib/styles.py
The original version of styles.py is copyright ReportLab Inc. 2000
v 1.15 2002/07/24 19:56:37 andy_robinson Exp $

Changes made by Luc Saffre:

- I rewrote PropertySet because I wanted true inheritance.

- Besides this I thought it useful that one can also access the Styles
  in a StyleSheet using "attribute" syntax. For example on can now
  write::

     stylesheet.Normal.spaceAfter = 6

  which is equivament to the classic syntax::

     stylesheet["Normal"].spaceAfter = 6

- keepWithNext was missing in defaults attribute list

- many more changes in 2006


"""

from reportlab.lib import colors
from reportlab.lib import pagesizes
from reportlab.lib.units import inch,mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

VA_MIDDLE="MIDDLE"
VA_CENTER="MIDDLE"
VA_TOP="TOP"
VA_BOTTOM="BOTTOM"

from lino.misc.pset import PropertySet, StyleSheet
# from sdoc.lists import ListStyle, NumberedListStyle
# from lino.sdoc.tables import TableModel



class FlowStyle(PropertySet):
    defaults = dict(
        leftIndent=0,
        rightIndent=0,
        spaceBefore=0,
        spaceAfter=0,
        backColor=None,
        keepWithNext=False,    
        pageBreakBefore=False, 
        pageBreakAfter=False,  
        )
    
class CharacterStyle(PropertySet):
    defaults = dict(
        fontName='Times-Roman',
        fontSize=10,
        textColor=colors.black,
        rise=False,
        underline=False,
        )
        
class ParagraphStyle(FlowStyle):
    defaults = dict(dict(
        leading=12,
        firstLineIndent=0,
        textStyle=None,
        alignment=TA_LEFT,
        allowSplitting = True,
        bulletFontName='Times-Roman',
        bulletFontSize=10,
        bulletIndent=0,
        wrap=True,
        **FlowStyle.defaults),**CharacterStyle.defaults)


class LineStyle(PropertySet):
    defaults = {
        'width':1,
        'color': colors.black
        }
    def prepareCanvas(self, canvas):
        """You can ask a LineStyle to set up the canvas for drawing
        the lines."""
        canvas.setLineWidth(1)
        #etc. etc.




class ListStyle(FlowStyle):
    defaults = dict(
        bulletWidth=12,
        bulletText= '-',
        **FlowStyle.defaults)
        
    def getBulletText(self,listInstance):
        return self.bulletText
      
class NumberedListStyle(ListStyle):
    defaults = dict(
        showParent=False,
        **ListStyle.defaults)
        
    def getBulletText(self,listInstance):
        text = str(listInstance.itemCount)+'.'
        if self.showParent:
            parent = listInstance.getParent()
            if parent is not None:
                text = parent.getBulletText() + text
        return text


class TableStyle(FlowStyle):
	defaults = dict(
		flowStyle=None,
		paraStyle=None,
		dataCellFormats=[],
		headerCellFormats= [],
		showHeaders=False,
		isgrowing=True,
		**FlowStyle.defaults)
	
	def formatTable(self,cmdName,*params):
		# self.dataCellFormats = list(self.dataCellFormats)
		addCellFormats(self.dataCellFormats,
							cmdName,
							(0,0),
							(-1,-1),
							*params)
		
	def formatHeader(self,cmdName,*params):
		# self.headerCellFormats = list(self.headerCellFormats)
		addCellFormats(self.headerCellFormats,
							cmdName,
							(0,0),
							(-1,0),
							*params)


class DocumentStyle(PropertySet):
    defaults = dict(
        pagesize=pagesizes.A4,
        showBoundary=0,
        leftMargin=inch,
        rightMargin=inch,
        topMargin=inch,
        bottomMargin=inch,
        header=None,
        footer=None,
        innerMargin=None,
        outerMargin=None,
        )

class FrameStyle(PropertySet):
    defaults = dict(
        halign=TA_LEFT,
        valign=VA_TOP,
        borderStyle=LineStyle(),
        borderStyleTop=None,
        borderStyleBottom=None,
        borderStyleRight=None,
        borderStyleLeft=None,
        padding=0,
        paddingTop=None,
        paddingBottom=None,
        paddingRight=None,
        paddingLeft=None,
        )
    
    
    
## class DocumentTool:
##    def __init__(self,doc):
##       self.doc = doc

##    def TitlePageHeader(self):
##       self.doc.beginTable(self.doc.styles.EmptyTable)
##       self.doc.formatParagraph(fontSize=8)
##       self.doc.formatTable("LINEBELOW",0.1,colors.black)
##       self.doc.p(self.doc.getTitle())
##       self.doc.endCell()
##       self.doc.formatParagraph(alignment=TA_RIGHT)
##       self.doc.p("Page %d" % self.doc.getPageNumber())
##       self.doc.endTable()

   

#
#
#

def getDefaultStyleSheet():
   sheet = StyleSheet()
   sheet.define("BODY",DocumentStyle())
   sheet.define("Header",FrameStyle(valign=VA_BOTTOM))
   sheet.define("Footer",FrameStyle(valign=VA_TOP))
   sheet.define("P",ParagraphStyle(
      fontName='Times-Roman',
      fontSize=10,
      spaceBefore=3,
      spaceAfter=3,
      leading=12
      ))

   sheet.define("TH",sheet.P.child(alignment=TA_CENTER))
   sheet.define("TD",sheet.P.child())
   sheet.define("TR",sheet.P.child())
   sheet.define("Verses",sheet.P.child(wrap=False))
   sheet.define("Right",sheet.P.child(alignment=TA_RIGHT))
   sheet.define("Center",sheet.P.child(alignment=TA_CENTER))
   sheet.define("H1",sheet.P.child(
      fontName = 'Times-Bold',
      keepWithNext=True,
      fontSize=18,
      leading=22,
      spaceAfter=6))

   sheet.define("H2",sheet.H1.child(
      fontSize=14,
      leading=18,
      spaceBefore=12,
      spaceAfter=6))

   sheet.define("H3",sheet.H2.child(
      fontSize=12,
      leading=14,
      spaceBefore=12,
      spaceAfter=6))

   sheet.define("PRE",sheet.P.child(
      fontName='Courier',
      wrap=False,
      fontSize=8,
      leading=8.8,
      firstLineIndent=0,
      leftIndent=36))

   #sheet.define("Wrapped",sheet.P.child(wrap=False,
   #                                          alignment=TA_LEFT))
   
   sheet.define('UL', ListStyle(bulletWidth=12))
   sheet.define('OL', NumberedListStyle(bulletWidth=12))

   sheet.define("LI",sheet.P.child(
       spaceBefore=1,
       spaceAfter=1,
       leftIndent=30,
       firstLineIndent=0,
       bulletText="\xe2\x80\xa2",
       bulletIndent=0))

   sheet.define("TABLE", TableStyle(
       leftIndent=20,
       rightIndent=50,
       dataCellFormats=[
       ('ALIGN',(0,0),(-1,-1),'LEFT'),
       ('VALIGN',(0,0),(-1,-1),'TOP'),
       ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
       ]))

   sheet.define("EmptyTable", TableStyle( dataCellFormats=[
       ('ALIGN',(0,0),(-1,-1),'LEFT'),
       ('VALIGN',(0,0),(-1,-1),'TOP'),
       ]))
		
   sheet.define("DataTable",TableStyle(dataCellFormats=[
       ('ALIGN',(0,0),(-1,-1),'LEFT'),
       ('VALIGN',(0,0),(-1,-1),'TOP'),
       ('LINEBELOW', (0,0), (-1,-1), 0.25, colors.black),
       ('BOX', (0,0), (-1,-1), 0.25, colors.black),
       # ('BACKGROUND', (0,0), (-1,-1), colors.grey),
       ]))

   
   return sheet

   #tool = DocumentTool(doc)

   #s.define('TitlePageHeader',tool.TitlePageHeader)

   #return s


   
