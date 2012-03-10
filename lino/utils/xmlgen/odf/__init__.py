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
`Open Document <http://lists.oasis-open.org/archives/tc-announce/201201/msg00001.html>` 
files and chunks thereof.

ODF chunks for :term:`appy.pod`
-------------------------------

>>> mystory = text.p("Hello world!")
>>> print etree.tostring(mystory,pretty_print=True) #doctest: +ELLIPSIS
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">Hello world!</text:p>
<BLANKLINE>

Here is an example of what we want to do with such a chunk of ODF:

>>> from appy.pod.renderer import Renderer
>>> template_file = os.path.abspath(os.path.dirname(__file__))
>>> template_file = os.path.join(template_file,"Template.odt")
>>> target_file = "tmp.odt"
>>> if os.path.exists(target_file):
...     os.remove(target_file)
>>> def body():
...     return etree.tostring(mystory)
>>> context = dict(body=body,self=target_file)
>>> renderer = Renderer(template_file, context, target_file)
>>> renderer.run()
>>> if False: os.startfile(target_file)


The file `Template.odt` contains control codes for 
:term:`appy.pod` as documented in 
http://appyframework.org/podWritingAdvancedTemplates.html
with basically one single instruction::

  do text
  from body()


Validating
----------

What if we want to make sure that our chunk is syntactivally correct?

>>> validate(mystory) #doctest: +ELLIPSIS
Traceback (most recent call last):
...
SimpleException: ... Did not expect element p there

In order to validate our chunk of XML, we need to wrap it 
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
SimpleException: ... Element document failed to validate attributes

That's almost good, except for a little detail.
That error comes because we didn't specify a namespace for 
the attruibutes (`version` and `mimetype`).
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

An alternative approach might be:

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

text = xg.Namespace('text',"urn:oasis:names:tc:opendocument:xmlns:text:1.0")
table = xg.Namespace('table',"urn:oasis:names:tc:opendocument:xmlns:table:1.0")
office = xg.Namespace('office',"urn:oasis:names:tc:opendocument:xmlns:office:1.0",
  used_namespaces=[text,table])


rng_tree = etree.parse(rngpath('OpenDocument-v1.2-os-schema.rng'))
validator = etree.RelaxNG(rng_tree)
if False:
    for prefix,url in rng_tree.getroot().nsmap.items():
        if prefix is not None:
            assert not globals().has_key(prefix)
            globals()[prefix] = xg.Namespace(prefix,url)


def validate(root):
    if not validator.validate(root):
        raise xg.SimpleException(validator.error_log.last_error)


#~ class OpenDocument(xg.Namespace):
    #~ rng_filename = rngpath('OpenDocument-v1.2-os-schema.rng')
    #~ used_namespaces = [ iic ]
#~ odf = OpenDocument()


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

