from lino.gendoc.maker import DocMaker

def body(doc):
    doc.h1("Third Example")
    doc.memo("""
    
This example is going to explain three important things about lists:

<ul>

<li>The individual list items are not renderd with a bullet.

<li>It is probably just a question of style.
I mean that I must define the right parameters in the stylesheet.

<li>But the question arises of whether I should implement cascading stylesheets or not.

</ul>

Ordered lists have similar problems:

<ol>

<li>The individual list items are not numbered.

<li>Yes, it is a pity.

</ol>

And to be short: lists in general aren't yet well implemented.

""")

DocMaker().main(body)    
    

