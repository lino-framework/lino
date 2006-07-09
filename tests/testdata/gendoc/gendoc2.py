from lino.gendoc.html import PdfMaker

def body(doc):
    doc.h1("Second Test")
    doc.par("""\
A test is a <em>test</em> and not a <em>final document</em>.
A test is a <em>test</em> and not a <em>final document</em>.
A test is a <em>test</em> and not a <em>final document</em>.
""")
    doc.memo("""\
Note that <tt>doc.par()</tt> does not interpret any markup while <tt>doc.memo()</tt> does.
""")

PdfMaker().main(body)    
    

