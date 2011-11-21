#coding: latin1
from lino.gendoc.maker import DocMaker
from lino.gendoc.styles import mm, TA_RIGHT

def footer(story):
    story.verses(u"""
    Rumma & Ko OÜ
    Tartu mnt 71-5
    10117 Tallinn
    """)

def header(story):
    story.memo("""
    <table class="EmptyTable">
    <tr><td align="left">
    (Left header)
    <td align="right">
    (Right header)
    </table>
    """)

def body(story):
    story.getStyle().update(
        #showBoundary=True,
        leftMargin=60*mm,
        rightMargin=30*mm,
        topMargin=40*mm,
        bottomMargin=40*mm,
        footer=footer,
        header=header,
        )
    #story.document.stylesheet.Footer.update(
    story.h1("Sixth Example")
    story.h2("Page setup")
    story.memo("""

This document has non-standard page margins, a header and a footer.

    """)
    story.par("This paragraph is aligned right",align="RIGHT")
    story.memo("Here is another paragraph.")
    
DocMaker().main(body)
