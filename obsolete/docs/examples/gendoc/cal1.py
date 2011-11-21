#coding: latin1

# Copyright 2007 Luc Saffre

import time
import datetime

from lino.gendoc.maker import DocMaker
from lino.gendoc import html
from lino.gendoc.styles import mm, TA_RIGHT

today = time.strftime("%d.%m.%Y")

def header(story):
    story.memo("""
    <table class="EmptyTable">
    <tr><td align="left">
    lk %d
    <td align="right">
    %s
    </table>
    """ % (story.getPageNumber(),today))

## def footer(story):
##     story.memo(u"""
##     <table class="EmptyTable">
##     <tr><td align="left">
##     Taizé laulud
##     <td align="right">
##     Eestikeelsed tekstid
##     </table>
##     """)

## FORMAT= 2

def body(story):
    
##     story.getStyle().update(
##         #showBoundary=True,
##         leftMargin=10*mm,
##         rightMargin=5*mm,
##         topMargin=11*mm,
##         bottomMargin=(148+9)*mm, # 297/2 = 148
##         #footer=footer,
##         #header=header,
##         )

##     story.getStyle("P").update(
##         fontSize=18,
##         leading=20,
##         spaceBefore=5)


    def cell(date=None,offset=0):
        if date is None:
            text=""
        else:
            date += datetime.timedelta(offset)
            text=str(date)
        t=html.TABLE(style="EmptyTable")
        t.addrow(text,"")
        return t
    
    date=datetime.date(2007,1,1)
    t=story.table(style="EmptyTable")
    t.addrow(cell(date),cell(date,4))
    t.addrow(cell(date,1),cell(date,5))
    t.addrow(cell(date,2),cell(date,6))
    t.addrow(cell(date,3),cell())

    
DocMaker().main(body)
