
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

# doit() on sys.stdout:
from lino.textprinter.plain import PlainTextPrinter
d = PlainTextPrinter()
doit(d)

# doit() on a PDF document:
from lino.textprinter.pdfprn import PdfTextPrinter
filename = "textprinter1.pdf"
d = PdfTextPrinter(filename)
doit(d)

# doit() on the default printer:
if False:
    from lino.textprinter.winprn import Win32TextPrinter
    d = Win32TextPrinter()
    doit(d)


