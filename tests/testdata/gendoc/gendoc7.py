#coding: latin1
from lino.gendoc.pdf import PdfMaker
from lino.reports.reports import ListReport,LEFT,RIGHT

class InvoiceReport(ListReport):
    data=(
        ("pcd.fsc","Fujitsu-Siemens Esprimo","1","756,50"),
        ("mon.lcd.fsc",'Fujitsu-Siemens Monitor 19"',"1","370,80"),
        )
    def setupReport(self):
        self.addColumn(label="Item no.",width=11)
        self.addColumn(label="Description"),
        #self.addColumn( label="Qty", width=3),
        #self.addColumn(label="Unit price", width=12),
        self.addColumn(label="Price", width=12,halign=RIGHT),

def body(story):
    #story.document.stylesheet.define()
    story.h1("Seventh Example")
    story.h2("Reports")
    story.memo("""


    """)
    story.par("Tallinn, 10. juuni 2006. a.",align="RIGHT")

    story.report(InvoiceReport())
    
PdfMaker().main(body)
