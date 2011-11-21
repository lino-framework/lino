#coding: latin1
from lino.gendoc.maker import DocMaker

def body(doc):
    doc.h1("Fourth Example")
    
    doc.h2("Using manual line breaks")
    
    doc.memo("""

    It seems quite hard to implement manual line breaks with
    reportlab.platypus.  <br/>This is for later.  <br/>For now we just
    ignore them.

    Fortunately there is a workaround that should help in most cases:
    You can avoid automatic word wrapping by using
    <tt>verses()</tt>.
    
    The <tt>verses()</tt> method
    is similar to
    <tt>memo()</tt>,
    except that it creates 
    XPreformatted paragraph instances instead of the
    standard Paragraph.

    """)
    
    doc.verses('''
    There was a young man in Japan
    Who wrote verses that never would scan.
    When asked how this was
    He said "It's because
    I always try to put as many words into the last line as I possibly can."
    ''')
    



    
    doc.h2("Styles")
    
    doc.memo("""

    The <tt>heading()</tt>, <tt>pre()</tt> and <tt>memo()</tt> methods
    have an optional second argument: the name of a <em>Style</em> to
    be used.  For the moment let's just play around with some of them.
    
    """)
    doc.memo("This text is aligned right",style="Right")
    
    doc.memo("""
    You can also get formatting by using the HTML syntax.
    This works at least in one case...
    """)
    
    doc.memo("This text is also aligned right",align="right")
    doc.memo("This one is aligned center",align="center")
    
DocMaker().main(body)    
   

