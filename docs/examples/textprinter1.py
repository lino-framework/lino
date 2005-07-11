import os

from lino.console import syscon
from lino.textprinter.winprn import Win32TextPrinter
from lino.textprinter.pdfprn import PdfTextPrinter

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
        
syscon.parse_args()

# first on console:
d = syscon.textprinter()
doit(d)

# now on the printer:
if syscon.confirm("print it on default Windows printer?",
                  default=False):
    d = Win32TextPrinter()
    doit(d)

# and now on a PDF document:
filename = "test.pdf"
if syscon.confirm("start Acrobat Reader on %s?" % filename,
                  default=False):
    d = PdfTextPrinter(filename)
    doit(d)
    os.system("start "+filename)
        


