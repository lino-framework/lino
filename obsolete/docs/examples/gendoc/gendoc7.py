#coding: latin1
from lino.gendoc.maker import DocMaker
from lino.reports.reports import ListReport,LEFT,RIGHT


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


class InvoiceReport(ListReport):
    width=50
    data=(
        ("pcd.fsc",     "Fujitsu-Siemens Esprimo",     "756,50"),
        ("mon.lcd.fsc", 'Fujitsu-Siemens Monitor 19"', "370,80"),
        ("acc.cdr",     'CDRW 10 pcs',                 "12,20"),
        ("",            'Total',                       "1239,50"),
        )
    def setupReport(self):
        self.addColumn(label="Item no.",width=11)
        self.addColumn(label="Description"),
        #self.addColumn( label="Qty", width=3),
        #self.addColumn(label="Unit price", width=12),
        self.addColumn(label="Price", width=12,halign=RIGHT),

def body(story):
    story.getStyle().update(header=header,footer=footer)
    #story.document.stylesheet.define()
    story.h1("Seventh Example")
    story.h2("Invoice")
    story.memo("""


    """)
    story.par("Tallinn, 10. juuni 2006. a.",align="RIGHT")

    story.report(InvoiceReport())
    
DocMaker().main(body) #,header=header)
