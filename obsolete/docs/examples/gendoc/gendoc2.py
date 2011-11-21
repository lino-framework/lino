from lino.gendoc.maker import DocMaker

def body(doc):
    doc.h1("Second Example")
    doc.memo("""
    
<tt>lino.gendoc</tt> has its own paragraph parser which replaces ReportLab's parser.

    """)
    doc.pre("""\
A test is a <em>test</em> and not a <em>final document</em>.
A test is a <em>test</em> and not a <em>final document</em>.
A test is a <em>test</em> and not a <em>final document</em>.
""")
    doc.memo("""\
A test is a <em>test</em> and not a <em>final document</em>.
A test is a <em>test</em> and not a <em>final document</em>.
A test is a <em>test</em> and not a <em>final document</em>.
""")

    doc.memo("""
    
About character formatting:
<em>emphasized</em> is same as <i>italic</i>.

<i>italic</i>, <b>bold</b> and <b><i>bold-italic</i></b>
are implemented using separate fonts, while
<sup>superscript</sup> simply raises the baseline.

Now the same text in underlined:
<u>
<i>italic</i>, <b>bold</b> and <b><i>bold-italic</i></b>
are implemented using separate fonts, while
<sup>superscript</sup> simply raises the baseline.
</u>

    """)
    

DocMaker().main(body)    
    

