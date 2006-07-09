import os
from lino.gendoc.html import PdfDocument

d=PdfDocument()
d.body.h1("A test")
d.body.par("""\
A test is a test and not a final document.
A test is a test and not a final document.
A test is a test and not a final document.
A test is a test and not a final document.
A test is a test and not a final document.
""")

d.saveas("test.pdf")

os.system("start test.pdf")
