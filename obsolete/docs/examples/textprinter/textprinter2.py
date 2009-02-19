import os
import glob

from lino.textprinter.plain import PlainTextPrinter
from lino.textprinter.pdfprn import PdfTextPrinter
from lino.textprinter.htmlprn import HtmlTextPrinter
from lino.textprinter.winprn import Win32TextPrinter

from lino import config

PSPRINTER=config.win32.get('postscript_printer')

OUTDIR=os.path.join(config.paths.get('webhome'),
                   "examples","textprinter")


def doit(inputfile,tp):
    print inputfile, "-->", tp.__class__.__name__
    tp.readfile(inputfile,encoding="cp850")
    tp.close()


if __name__ == "__main__":

    for fn in glob.glob("*.prn"):
        base,ext=os.path.splitext(fn)
        
        doit(fn,PlainTextPrinter())

        # do it in a PDF document:
        doit(fn,PdfTextPrinter(os.path.join(OUTDIR,base+".pdf")))

        # do it in a HTML file:
        doit(fn,HtmlTextPrinter(os.path.join(OUTDIR,base+".html")))

        # do it on a Windows printer:
        doit(fn,Win32TextPrinter(
            printerName=PSPRINTER,
            spoolFile=os.path.join(OUTDIR,base+".ps")))


