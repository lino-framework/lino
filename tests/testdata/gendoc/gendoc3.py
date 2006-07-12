from lino.gendoc.pdf import PdfMaker

def body(doc):
    doc.h1("Third Example")
    doc.memo("""\
This example is going to explain three important truths:

<ul>
<li>foo</li>
<li>bar</li>
<li>baz</li>
</ul>

<ol>
<li>foo</li>
<li>bar</li>
<li>baz</li>
</ol>

Lists aren't yet well implemented...

""")

PdfMaker().main(body)    
    

