# -*- coding: latin1 -*-

def doit(tp):
    tp.writeln("")
    tp.writeln("TextPrinter Test page")
    tp.writeln("")
    cols = int(tp.lineWidth() / 10) + 1
    tp.writeln("".join([" "*9+str(i+1) for i in range(cols)]))
    tp.writeln("1234567890"*cols)
    tp.writeln("")
    tp.writeln("Here is some \033b1bold\033b0 text.")
    tp.writeln("Here is some \033u1underlined\033u0 text.")
    tp.writeln("Here is some \033i1italic\033i0 text.")

    tp.writeln("Here is some more text.")
    tp.writeln(u"Ännchen Müller machte große Augen.")
    tp.write("And here")
    tp.write(" is some")
    tp.write(" frag")
    tp.writeln("mented text.")

    tp.writeln()
    tp.write("This is a very long line. ")
    tp.write("Just do demonstrate that TextPrinter ")
    tp.write("doesn't wrap paragraphs for you...")
    tp.write("Blabla bla. "*20)
    tp.writeln("Amen.")
    tp.close()
        

if __name__ == "__main__":
    # do it on sys.stdout:
    from lino.textprinter.plain import PlainTextPrinter
    doit(PlainTextPrinter())

    # do it in a PDF document:
    from lino.textprinter.pdfprn import PdfTextPrinter
    doit(PdfTextPrinter("tmp.pdf"))

    # do it in a HTML file:
    from lino.textprinter.htmlprn import HtmlTextPrinter
    doit(HtmlTextPrinter("tmp.html"))

    # do it on the default printer:
    if False:
        from lino.textprinter.winprn import Win32TextPrinter
        doit(Win32TextPrinter(self))


