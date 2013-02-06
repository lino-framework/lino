## Copyright 2011-2013 Luc Saffre
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

"""
  
This module contains also a utility function :func:`html2odf` 
which converts an HTML ElementTree object to 

>>> from lino.utils.xmlgen.html import E
>>> def test(e):
...     print(E.tostring(e))
...     print(toxml(html2odf(e)))
>>> test(E.p("This is a ",E.b("first")," test.")) #doctest: +NORMALIZE_WHITESPACE
<p>This is a <b>first</b> test.</p>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">This 
is a <text:span text:style-name="Bold Text">first</text:span> test.</text:p>

>>> test(E.p(E.b("This")," is another test.")) #doctest: +NORMALIZE_WHITESPACE
<p><b>This</b> is another test.</p>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"><text:span 
text:style-name="Bold Text">This</text:span> is another test.</text:p>

>>> test(E.td(E.p("This is another test."))) #doctest: +NORMALIZE_WHITESPACE
<td><p>This is another test.</p></td>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">This 
is another test.</text:p>

>>> test(E.td(E.p(E.b("This")," is another test."))) #doctest: +NORMALIZE_WHITESPACE
<td><p><b>This</b> is another test.</p></td>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"><text:span 
text:style-name="Bold Text">This</text:span> is another test.</text:p>

:func:`html2odf` converts bold text to a span with a 
style named "Bold Text". That's currently a hard-coded name, and the 
caller must make sure that a style of that name is defined in the 
document.

"""


import logging
logger = logging.getLogger(__name__)

import os

from appy.pod.renderer import Renderer as AppyRenderer

from lino.utils.restify import restify
from lino.utils.html2xhtml import html2xhtml
from lino.utils.xmlgen import etree
from lino.utils.xmlgen.html import E


from django.utils.encoding import force_unicode
from django.conf import settings


from cStringIO import StringIO
def toxml(node):
    buf = StringIO()
    node.toXml(0, buf)
    return buf.getvalue()


from odf.opendocument import OpenDocumentText
from odf.style import Style, TextProperties, ParagraphProperties
from odf.style import TableColumnProperties, TableRowProperties, TableCellProperties
#~ from odf.text import P
from odf.element import Text
from odf import text
from odf.table import Table, TableColumns, TableColumn, TableHeaderRows, TableRows, TableRow, TableCell

from cStringIO import StringIO
def toxml(node):
    buf = StringIO()
    node.toXml(0, buf)
    return buf.getvalue()


PTAGS = ('p','td')

def html2odf(e,ct=None,**ctargs):
    """
    Convert a :mod:`lino.utils.xmlgen.html` element 
    to an ODF text element.
    Currently it knows only P and B tags, 
    ignoring all other formatting.
    
    There's probably a better way to do this...
    """
    #~ print "20120613 html2odf()", e.tag, e.text
    if ct is None:
        ct = text.P(**ctargs)
        #~ if e.tag in PTAGS: 
            #~ oe = text.P(**ctargs)
        #~ else:
            #~ oe = text.P(**ctargs)
            #~ logger.info("20130201 %s",E.tostring(e))
            #~ raise NotImplementedError("<%s> without container" % e.tag)
    if isinstance(e,basestring):
        ct.addText(e)
        #~ oe = text.Span()
        #~ oe.addText(e)
        #~ yield oe
        return 
        
    if e.tag == 'b':
        oe = text.Span(stylename='Bold Text')
    elif e.tag == 'a':
        oe = text.Span(stylename='Bold Text')
    elif e.tag == 'img':
        return # ignore images
    elif e.tag in PTAGS: 
        oe = ct
    else:
        logger.info("20130201 %s",E.tostring(e))
        raise NotImplementedError("<%s> inside <%s>" % (e.tag,ct.tagName))
        #~ oe = text.Span()
            
    if e.text:
        oe.addText(e.text)
    for child in e:
        #~ html2odf(child,oe)
        html2odf(child,oe)
        #~ for oc in html2odf(child,oe):
            #~ # oe.addElement(oc)
            #~ oe.appendChild(oc)
    #~ if not True:
        #~ if e.tail:
            #~ oe.addText(e.tail)
    if oe is not ct:
        ct.appendChild(oe)
        #~ yield oe
    #~ if True:
    if e.tail:
        #~ yield e.tail
        #~ yield text.Span(text=e.tail)
        #~ yield Text(e.tail)
        ct.addText(e.tail)
    return ct


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

