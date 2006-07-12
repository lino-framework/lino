from lino.gendoc.pdf import PdfMaker

def body(doc):
    doc.h1("Fifth Example")
    doc.h2("Tables")

    doc.example("""
    
The following table summarizes the relationship between foo, bar and
baz:

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
    
The same table using the DataTable style:

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
    
Now an almost illegally simple table.
This is valid HTML, though not very modern:

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

    
PdfMaker().main(body)    
    

