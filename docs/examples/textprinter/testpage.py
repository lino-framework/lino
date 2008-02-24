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


def doit(tp):
    for codepage in ("cp850","cp437"):
        tp.writeln("Codepage " + codepage)
        tp.writeln()
        for c in range(255):
            tp.write(' '+chr(c).decode(codepage)+' ')
            if c % 16 == 0:
                tp.writeln()
        tp.writeln()
        
    tp.close()


if __name__ == "__main__":

        if False:
            doit(PlainTextPrinter())

        # do it in a PDF document:
        doit(PdfTextPrinter(os.path.join(OUTDIR,"testpage.pdf"),
                            fontName="Liberation"))

        # do it in a HTML file:
        if False:
            doit(HtmlTextPrinter(os.path.join(OUTDIR,"testpage.html")))

        # do it on a Windows printer:
        if False:
            doit( Win32TextPrinter(
                printerName=PSPRINTER,
                spoolFile=os.path.join(OUTDIR,"testpage.ps")))


