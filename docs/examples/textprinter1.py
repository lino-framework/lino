from lino.console.application import Application
from lino.textprinter.plain import PlainTextPrinter
from lino.textprinter.pdfprn import PdfTextPrinter
from lino.textprinter.winprn import Win32TextPrinter

def doit(d):
    d.writeln("")
    d.writeln("lino.textprinter Test page")
    d.writeln("")
    cols = int(d.lineWidth() / 10) + 1
    d.writeln("".join([" "*9+str(i+1) for i in range(cols)]))
    d.writeln("1234567890"*cols)
    d.writeln("")
    d.writeln("Here is some \033b1bold\033b0 text.")
    d.writeln("Here is some \033u1underlined\033u0 text.")
    d.writeln("Here is some \033i1italic\033i0 text.")
    d.endDoc()

class Test(Application):
    def run(self):
        # do it on sys.stdout:
        d = PlainTextPrinter(self)
        doit(d)

        # do it on a PDF document:
        filename = "textprinter1.pdf"
        d = PdfTextPrinter(self,filename)
        doit(d)
        self.showfile(filename)

        # do it on the default printer:
        if False:
            d = Win32TextPrinter(self)
            doit(d)

if __name__ == "__main__":
    Test().main()
