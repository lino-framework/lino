"""
This is an alternative for reportlab/lib/styles.py
The original version of styles.py is copyright ReportLab Inc. 2000
v 1.15 2002/07/24 19:56:37 andy_robinson Exp $

Changes made by Luc Saffre <luc.saffre@gmx.net> 

- I rewrote PropertySet because I wanted true inheritance.

- Besides this I thought it useful that one can also access the Styles
  in a StyleSheet using "attribute" syntax. For example on can now
  write::

     stylesheet.Normal.spaceAfter = 6

  which is equivament to the classic syntax::

     stylesheet["Normal"].spaceAfter = 6

- keepWithNext was missing in defaults attribute list


"""

from reportlab.lib import colors
from reportlab.lib import pagesizes
from reportlab.lib.units import inch,mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

from lino.misc.pset import PropertySet, StyleSheet
# from sdoc.lists import ListStyle, NumberedListStyle
# from lino.sdoc.tables import TableModel



class ParagraphStyle(PropertySet):
    defaults = {
        'fontName':'Times-Roman',
        'fontSize':10,
        'leading':12,
        'leftIndent':0,
        'rightIndent':0,
        'firstLineIndent':0,
        'alignment':TA_LEFT,
        'spaceBefore':0,
        'spaceAfter':0,
        'keepWithNext':False,    # added by LS
        'allowSplitting' : True,
        'bulletFontName':'Times-Roman',
        'bulletFontSize':10,
        'bulletIndent':0,
        'textColor': colors.black,
        'backColor':None,
        'wrap':True # added by LS
        }


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

# added by LS



class DocumentStyle(PropertySet):
    defaults = {
        'pagesize':pagesizes.A4,
        'showBoundary':0,
        'leftMargin':inch,
        'rightMargin':inch,
        'rightMargin':inch,
        'topMargin':inch,
        'bottomMargin':inch,
        'header':None,
        'footer':None,
        'innerMargin':None,
        'outerMargin':None,
        }

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
   sheet.define("Document",DocumentStyle())
   sheet.define("Normal",ParagraphStyle(
      fontName='Times-Roman',
      fontSize=10,
      spaceBefore=2,
      spaceAfter=2,
      leading=12
      ))

   sheet.define("Number",sheet.Normal.child(alignment=TA_RIGHT))
   sheet.define("Heading1",sheet.Normal.child(
      fontName = 'Times-Bold',
      fontSize=18,
      leading=22,
      spaceAfter=6))

   sheet.define("Heading2",sheet.Normal.child(
      fontName = 'Times-Bold',
      fontSize=14,
      leading=18,
      spaceBefore=12,
      spaceAfter=6))

   sheet.define("Heading3",sheet.Normal.child(
      fontName = 'Times-BoldItalic',
      fontSize=12,
      leading=14,
      spaceBefore=12,
      spaceAfter=6))

   sheet.define("Code",sheet.Normal.child(
      fontName='Courier',
      wrap=False,
      fontSize=8,
      leading=8.8,
      firstLineIndent=0,
      leftIndent=36))

   sheet.define("Wrapped",sheet.Normal.child(wrap=False,
															alignment=TA_LEFT))
   return sheet


   #tool = DocumentTool(doc)

   #s.define('TitlePageHeader',tool.TitlePageHeader)

   #return s


   
