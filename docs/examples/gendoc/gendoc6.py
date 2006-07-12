#coding: latin1
from lino.gendoc.pdf import PdfMaker
from lino.gendoc.styles import mm, TA_RIGHT

def footer(story):
    story.verses("""
    Rumma & Ko OÜ
    Tartu mnt 71-5
    10117 Tallinn
    """)

def header(story):
    story.memo("""
    <table class="EmptyTable">
    <tr><td>
    Bla, blabla, blablabla. Bla.
    </td>
    <td>
    Bla, blabla, blablabla. Bla.
    </td></tr>
    </table>
    """)

def body(story):
    story.document.stylesheet.BODY.update(
        showBoundary=True,
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

    This document has non-standard page margins,
    a header and a footer.


    """)
    story.par("Tallinn, 10. juuni 2006. a.",align="RIGHT")
    
PdfMaker().main(body)
