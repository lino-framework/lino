import os
import glob

from lino.textprinter.plain import PlainTextPrinter
from lino.textprinter.pdfprn import PdfTextPrinter
from lino.textprinter.htmlprn import HtmlTextPrinter
from lino.textprinter.winprn import Win32TextPrinter

from lino import config

PSPRINTER=config.get('win32','postscript_printer')

DLDIR=r"u:\htdocs\timwebs\lino\examples"


def doit(inputfile,p):
    print inputfile, "-->", p
    p.readfile(inputfile,encoding="cp850")
    p.close()


if __name__ == "__main__":

    for fn in glob.glob("*.prn"):
        base,ext=os.path.splitext(fn)
        
        doit(fn,PlainTextPrinter())

        # do it in a PDF document:
        doit(fn,PdfTextPrinter(os.path.join(DLDIR,base+".pdf")))

        # do it in a HTML file:
        doit(fn,HtmlTextPrinter(os.path.join(DLDIR,base+".html")))

        # do it on a Windows printer:
        doit(fn,Win32TextPrinter(
            printerName=PSPRINTER,
            spoolFile=os.path.join(DLDIR,base+".ps")))


