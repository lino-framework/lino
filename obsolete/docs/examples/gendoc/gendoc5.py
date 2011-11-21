from lino.gendoc.maker import DocMaker

def body(doc):
    doc.h1("Fifth Example")
    doc.h2("Tables")

    doc.example("""

The markup language of <tt>memo()</tt> supports tables using the same
markup syntax as HTML:

    ""","""
<table>
<tr>
<td>foo</td>
<td>bar</td>
<td>baz</td>
</tr>
<tr>
<td>A</td>
<td>B</td>
<td>C</td>
</tr>
</table>

    """)
    doc.example("""

You can specify the name of a table style as the <tt>class</tt> attribute of the <tt>&lt;table></tt> tag:

    ""","""
<table class="DataTable">
<tr>
<td>foo</td>
<td>bar</td>
<td>baz</td>
</tr>
<tr>
<td>A</td>
<td>B</td>
<td>C</td>
</tr>
</table>

    """)
    doc.example("""

You can omit closing tags if the parser can close them automatically.
This was valid HTML in the beginnings of the Internet, and modern
browsers still render it correctly:

    ""","""
    
<table>
<tr>
<td>foo
<td>bar
<td>baz
<tr>
<td>A
<td>B
<td>C
</table>
    
    """)

    
DocMaker().main(body)    
    

