import os
from lino.gendoc.pdf import PdfDocument

d=PdfDocument()
d.body.h1("First Example")
d.body.memo("""\
A test is a test and not a final document.
A test is a test and not a final document.
A test is a test and not a final document.
A test is a test and not a final document.
A test is a test and not a final document.
""")

d.saveas("test.pdf")

os.system("start test.pdf")
