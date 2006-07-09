from lino.gendoc.html import PdfMaker

def body(doc):
    doc.h1("Third Test")
    doc.memo("""\
A test is a <em>test</em> and not a <em>final document</em>.

<ul>
<li>foo</li>
<li>bar</li>
<li>baz</li>
</ul>

A test is a <em>test</em> and not a <em>final document</em>.

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

A test is a <em>test</em> and not a <em>final document</em>.

About character formatting:

<em>emphasized</em> is same as <i>italic</i>.

<i>italic</i>, <b>bold</b> and <b><i>bold-italic</i></b>
are implemented using separate fonts.

Now the same text in underlined:
<u><i>italic</i>, <b>bold</b> and <b><i>bold-italic</i></b>
are implemented with a different font.</u>

And finally the same again in superscript:
<sup><i>italic</i>, <b>bold</b> and <b><i>bold-italic</i></b>
are implemented with a different font.</sup>


""")

PdfMaker().main(body)    
    

