# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

u"""
Tools for generating 
`Open Document 
<http://lists.oasis-open.org/archives/tc-announce/201201/msg00001.html>`_ 
files and chunks thereof.


Generating validated chunks of ODF
----------------------------------

We instantiate a simple chunk of ODF...

>>> mystory = text.p("Hello world!")

... and look how it gets rendered:

>>> print etree.tostring(mystory,pretty_print=True) #doctest: +ELLIPSIS
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">Hello world!</text:p>
<BLANKLINE>

What if we want to make sure that our chunk is syntactically 
correct?

>>> validate(mystory) #doctest: +ELLIPSIS
Traceback (most recent call last):
...
Warning: ... Did not expect element p there

Yes, in order to validate our chunk of XML, we need to wrap it 
into a document:

>>> root = office.document(
...     office.body(
...       office.text(mystory)),
...     version="1.2",
...     mimetype="application/vnd.oasis.opendocument.text"
... )

>>> validate(root) #doctest: +ELLIPSIS
Traceback (most recent call last):
...
Warning: ... Element document failed to validate attributes

That's almost good, except for a little "detail":
when using Python syntax, we cannot specify a namespace 
for attributes (here `version` and `mimetype`).

How to specify the namespace of attributes? 

First attempt:

>>> OFFICE = "{"+office.targetNamespace+"}"
>>> attribs = {
...     OFFICE + 'version' : "1.2",
...     OFFICE + 'mimetype' : "application/vnd.oasis.opendocument.text",
... }
>>> root = office.document(
...     office.body(
...       office.text(
...         text.p("Hello world!")
...     )),
...     **attribs
... )
>>> validate(root) #doctest: +ELLIPSIS

This works, but is rather heavy to code.

Here is how we suggest to set attributes:

>>> office.update_attribs(root,
...     version="1.2",
...     mimetype="application/vnd.oasis.opendocument.text")
>>> validate(root)

This is functionally equivalent (but more easy to code) :

>>> root.set(office.version().tag,"1.2")
>>> root.set(office.mimetype().tag,"application/vnd.oasis.opendocument.text")

>>> print etree.tostring(root,pretty_print=True) #doctest: +ELLIPSIS
<office:document xmlns:...>
  <office:body>
    <office:text>
      <text:p>Hello world!</text:p>
    </office:text>
  </office:body>
</office:document>
<BLANKLINE>

There is also a shortcut function `validate_chunks` which does all this wrapping work:

>>> validate_chunks(text.p("Hello world!"))


Here an example of invalid tree:

>>> mystory = text.p("Foo",text.p("Bar"))
>>> validate_chunks(mystory) #doctest: +ELLIPSIS
Traceback (most recent call last):
...
Warning: ... Element p has extra content: text



ODF chunks for :term:`appy.pod`
-------------------------------

To understand why we want to generate such chunks of 
validated ODF, 
please read the first section of the following documentation page:
http://appyframework.org/podWritingAdvancedTemplates.html.
We have a file `Template.odt` with basically one single 
contains control code::

  do text
  from body()
  
And here is the body() function called there:

>>> mystory = text.p("Hello world!")

Here is an example on how to use it:

>>> print render_to_odt("xmlgen_odf_1.odt",
...   body=etree.tostring(mystory),
...   title="lino.utils.xmlgen.odf example 1")
File xmlgen_odf_1.odt has been created.


Examples
--------

>>> t = table.table(
...   table.makeattribs(name="Mytable",style_name="Mytable"),
...   table.table_column(table.makeattribs(style_name="A",number_columns_repeated="2")),
...   table.table_row(
...     table.table_cell(text.p("First"),table.makeattribs(value_type="string")),
...     table.table_cell(text.p("Second"),table.makeattribs(value_type="string")),
...   ),
...   table.table_row(
...     table.table_cell(text.p("Third"),table.makeattribs(value_type="string")),
...     table.table_cell(text.p("Fourth"),table.makeattribs(value_type="string")),
...   ),
... )
>>> validate_chunks(t)
>>> print render_to_odt("xmlgen_odf_2.odt",
...   body=etree.tostring(t),
...   title="lino.utils.xmlgen.odf example 2")
File xmlgen_odf_2.odt has been created.





"""


import os
from lxml import etree
from lino.utils import xmlgen as xg

def rngpath(*parts):
    p1 = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(p1,'relaxng',*parts)
    
"""    
<grammar xmlns="http://relaxng.org/ns/structure/1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:presentation="urn:oasis:names:tc:opendocument:xmlns:presentation:1.0" xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" xmlns:db="urn:oasis:names:tc:opendocument:xmlns:database:1.0" xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" xmlns:anim="urn:oasis:names:tc:opendocument:xmlns:animation:1.0" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:math="http://www.w3.org/1998/Math/MathML" xmlns:xforms="http://www.w3.org/2002/xforms" xmlns:grddl="http://www.w3.org/2003/g/data-view#" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" xmlns:smil="urn:oasis:names:tc:opendocument:xmlns:smil-compatible:1.0" datatypeLibrary="http://www.w3.org/2001/XMLSchema-datatypes">
"""

class Text(xg.Namespace):
    def setup_namespace(self):
        self.define_names("p")

text = Text('text',"urn:oasis:names:tc:opendocument:xmlns:text:1.0")
#~ text = xg.Namespace('text',"urn:oasis:names:tc:opendocument:xmlns:text:1.0")

class Table(xg.Namespace):
    def setup_namespace(self):
        self.define_names("""
        table
        name
        style-name
        number-columns-repeated
        table-row
        table-cell
        table-column
        """)
table = Table('table',"urn:oasis:names:tc:opendocument:xmlns:table:1.0")

class Style(xg.Namespace):
    def setup_namespace(self):
        self.define_names("""
        """)
style = Style('style',"urn:oasis:names:tc:opendocument:xmlns:style:1.0")

class Office(xg.Namespace):
    used_namespaces=[text,table,style]
    def setup_namespace(self):
        self.define_names("""
        document body text 
        version mimetype
        value-type
        """)

office = Office('office',"urn:oasis:names:tc:opendocument:xmlns:office:1.0")
#~ office = xg.Namespace('office',"urn:oasis:names:tc:opendocument:xmlns:office:1.0",
    #~ used_namespaces=[text,table])

table.value_type = office.value_type




rng_tree = etree.parse(rngpath('OpenDocument-v1.2-os-schema.rng'))
validator = etree.RelaxNG(rng_tree)

if False:
    for prefix,url in rng_tree.getroot().nsmap.items():
        if prefix is not None:
            assert not globals().has_key(prefix)
            globals()[prefix] = xg.Namespace(prefix,url)


def validate(root):
    if not validator.validate(root):
        raise xg.Warning(validator.error_log.last_error)

def validate_chunks(*chunks):
    root = office.document(
        office.makeattribs(
            version="1.2",
            mimetype="application/vnd.oasis.opendocument.text"),
        office.body(
          office.text(*chunks)),
    )
    validate(root)

#~ def validate_chunks(*chunks):
    #~ root = office.document(
        #~ office.body(
          #~ office.text(*chunks)),
    #~ )
    #~ office.update_attribs(root,
        #~ version="1.2",
        #~ mimetype="application/vnd.oasis.opendocument.text")
    #~ validate(root)
  


def render_to_odt(target_file,startfile=False,**context):
    """
    Render a chunk to an odt file using a default template.
    """
    from appy.pod.renderer import Renderer
    dir = os.path.abspath(os.path.dirname(__file__))
    template_file = os.path.join(dir,"Template.odt")
    #~ target_file = os.path.join(dir,"tmp.odt")
    if os.path.exists(target_file):
        os.remove(target_file)
    #~ context = dict(body=body,self="lino.utils.xmlgen.odf example")
    renderer = Renderer(template_file, context, target_file)
    renderer.run()
    if startfile: os.startfile(target_file)
    return "File %s has been created." % target_file


#~ class OpenDocument(xg.Namespace):
    #~ rng_filename = rngpath('OpenDocument-v1.2-os-schema.rng')
    #~ used_namespaces = [ iic ]
#~ odf = OpenDocument()


def unused_table2odt(headers,fields,widths,rows):
    """
    Not finished because I discovered the `ODFPY <https://joinup.ec.europa.eu/software/odfpy>`_ library    
    """
    sums  = [0 for col in fields]
      
    story = []
    story.append(office.automatic_styles())
    t = table.table(
      table.makeattribs(name="Mytable",style_name="Mytable"),
      table.table_column(table.makeattribs(style_name="A",number_columns_repeated="2")),
      table.table_row(
        table.table_cell(text.p("First"),table.makeattribs(value_type="string")),
        table.table_cell(text.p("Second"),table.makeattribs(value_type="string")),
      ),
      table.table_row(
        table.table_cell(text.p("Third"),table.makeattribs(value_type="string")),
        table.table_cell(text.p("Fourth"),table.makeattribs(value_type="string")),
      ),
    )
    validate_chunks(t)
      
    yield html.TR(*headers)
    
    recno = 0
    for row in rows:
        recno += 1
        cells = [TD(x) for x in row2cells(row,sums)]
        #~ yield html.TR(*cells,**cellattrs)
        yield html.TR(*cells)
            
    has_sum = False
    for i in sums:
        if i:
            has_sum = True
            break
    if has_sum:
        yield html.TR(
          *[html.TD(x,**cellattrs) for x in ar.ah.store.sums2html(ar,fields,sums)])



def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

