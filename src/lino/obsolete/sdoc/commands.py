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

from reportlab.lib import colors
from reportlab.lib import pagesizes
# from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.rl_config import defaultPageSize

from reportlab.lib.pagesizes import *
from reportlab.lib.units import *
from reportlab.lib import colors
from reportlab.lib.enums import *


from lino.sdoc.tables import TableModel 
from lino.sdoc.lists import NumberedListStyle

from lino.sdoc.document import Document
from lino.sdoc import styles


# * # OL, TableHeader


document = None
stylesheet=None
#renderer = None
#outputfile = None
#inputfile = None

def setTitle(*args,**kw):
    return document.setTitle(*args,**kw)
def getTitle(*args,**kw):
    return document.getTitle(*args,**kw)

def setAuthor(*args,**kw):
    return document.setAuthor(*args,**kw)
def getAuthor(*args,**kw):
    return document.getAuthor(*args,**kw)

def getTextWidth(*args,**kw):
    return document.getTextWidth(*args,**kw)
def setFeeder(*args,**kw):
    return document.setFeeder(*args,**kw)

def getSourceFileName(*args,**kw):
    return document.getSourceFileName(*args,**kw)

def formatParagraph(*args,**kw):
    return document.formatParagraph(*args,**kw)

def getPageNumber():
    return document.renderer.getPageNumber()
def getOutputFileName():
    return document.renderer.getFilename()

def formatDocument(**kw):
    for k,v in kw.items():
        setattr(document.docstyle,k,v)



def p(*args,**kw): return document.p(*args,**kw)
def h1(*args,**kw): return document.h1(*args,**kw)
def h2(*args,**kw): return document.h2(*args,**kw)
def h3(*args,**kw): return document.h3(*args,**kw)
def pre(*args,**kw): return document.pre(*args,**kw)
def memo(*args,**kw): return document.memo(*args,**kw)
def img(*args,**kw): return document.img(*args,**kw)
def barcode(*args,**kw): return document.barcode(*args,**kw)
def addBackgroundPainter(*args,**kw):
	return document.addBackgroundPainter(*args,**kw)

def beginTable(*args,**kw): return document.beginTable(*args,**kw)
def endTable(*args,**kw): return document.endTable(*args,**kw)
def addColumn(*args,**kw): return document.addColumn(*args,**kw)
def beginCell(*args,**kw): return document.beginCell(*args,**kw)
def endCell(*args,**kw): return document.endCell(*args,**kw)
def beginRow(*args,**kw): return document.beginRow(*args,**kw)
def endRow(*args,**kw): return document.endRow(*args,**kw)
def restartRow(*args,**kw): return document.restartRow(*args,**kw)
def cell(*args,**kw): return document.cell(*args,**kw)
def tr(*args,**kw): return document.tr(*args,**kw)
def formatCell(*args,**kw): return document.formatCell(*args,**kw)
def formatRow(*args,**kw): return document.formatRow(*args,**kw)
def formatColumn(*args,**kw): return document.formatColumn(*args,**kw)
def formatTable(*args,**kw): return document.formatTable(*args,**kw)
def formatHeader(*args,**kw): return document.formatHeader(*args,**kw)

def beginList(*args,**kw): return document.beginList(*args,**kw)
def endList(*args,**kw): return document.endList(*args,**kw)
def li(*args,**kw): return document.li(*args,**kw)


def beginDocument(outputfile,
                  renderer,
                  source=None):
    global document
    global stylesheet
   
    document = Document(styles.getDefaultStyleSheet(), source)
    
    stylesheet = document.stylesheet
   
    # a renderer is allowed to change the name of outputfile
    renderer.open(outputfile)
    document.begin(renderer)



def endDocument(showOutput=False):
    document.end()
    document.renderer.close(showOutput)
   

