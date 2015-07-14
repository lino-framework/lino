# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""This module contains mainly a utility function :func:`html2odf` which
converts an ElementTree object generated using
:mod:`lino.utils.xmlgen.html` to a fragment of ODF.

>>> from lino.utils.xmlgen.html import E
>>> def test(e):
...     print E.tostring(e)
...     print toxml(html2odf(e))
>>> test(E.p("This is a ", E.b("first"), " test."))
... #doctest: +NORMALIZE_WHITESPACE
<p>This is a <b>first</b> test.</p>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">This
is a <text:span text:style-name="Strong Emphasis">first</text:span>
test.</text:p>

>>> test(E.p(E.b("This")," is another test."))
... #doctest: +NORMALIZE_WHITESPACE
<p><b>This</b> is another test.</p>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"><text:span
text:style-name="Strong Emphasis">This</text:span> is another test.</text:p>

>>> test(E.p(E.i("This")," is another test."))
... #doctest: +NORMALIZE_WHITESPACE
<p><i>This</i> is another test.</p>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"><text:span
text:style-name="Emphasis">This</text:span> is another test.</text:p>

>>> test(E.td(E.p("This is another test.")))
... #doctest: +NORMALIZE_WHITESPACE
<td><p>This is another test.</p></td>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">This
is another test.</text:p>

>>> test(E.td(E.p(E.b("This"), " is another test.")))
... #doctest: +NORMALIZE_WHITESPACE
<td><p><b>This</b> is another test.</p></td>
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"><text:span
text:style-name="Strong Emphasis">This</text:span> is another test.</text:p>

>>> test(E.ul(E.li("First item"),E.li("Second item"))) #doctest: +NORMALIZE_WHITESPACE
<ul><li>First item</li><li>Second item</li></ul>
<text:list xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" 
text:style-name="podBulletedList"><text:list-item><text:p 
text:style-name="podBulletItem">First item</text:p></text:list-item><text:list-item><text:p 
text:style-name="podBulletItem">Second item</text:p></text:list-item></text:list>

N.B.: the above chunk is obviously not correct since Writer doesn't display it.
(How can I debug a generated odt file? 
I mean if my content.xml is syntactically valid but Writer ...)
Idea: validate it against the ODF specification using lxml



:func:`html2odf` converts bold text to a span with a 
style named "Strong Emphasis". That's currently a hard-coded name, and the 
caller must make sure that a style of that name is defined in the 
document.

The text formats `<i>` and `<em>` are converted to a style "Emphasis".


Edge case:

>>> print toxml(html2odf("Plain string"))
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">Plain string</text:p>

>>> print toxml(html2odf(u"Ein schöner Text"))
... #doctest: +NORMALIZE_WHITESPACE
<text:p xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">Ein
schÃ¶ner Text</text:p>
"""

import logging
logger = logging.getLogger(__name__)

from StringIO import StringIO


def toxml(node):
    buf = StringIO()
    node.toXml(0, buf)
    return buf.getvalue()


from odf import text


#~ PTAGS = ('p','td','li')
PTAGS = ('p', 'td', 'div', 'table', 'tr')


def html2odf(e, ct=None, **ctargs):
    """
    Convert a :mod:`lino.utils.xmlgen.html` element to an ODF text element.
    Most formats are not implemented.
    There's probably a better way to do this...
    """
    sections_counter = 1
    #~ print "20120613 html2odf()", e.tag, e.text
    if ct is None:
        ct = text.P(**ctargs)
        #~ if e.tag in PTAGS:
            #~ oe = text.P(**ctargs)
        #~ else:
            #~ oe = text.P(**ctargs)
            #~ logger.info("20130201 %s",E.tostring(e))
            #~ raise NotImplementedError("<%s> without container" % e.tag)
    if isinstance(e, basestring):
        ct.addText(e)
        #~ oe = text.Span()
        #~ oe.addText(e)
        #~ yield oe
        return ct

    if e.tag == 'ul':
        ct = text.List(stylename='podBulletedList')
        ctargs = dict(stylename='podBulletItem')
        #~ ctargs = dict()

    text_container = None

    if e.tag == 'b':
        #~ oe = text.Span(stylename='Bold Text')
        oe = text.Span(stylename='Strong Emphasis')
    elif e.tag == 'a':
        oe = text.Span(stylename='Strong Emphasis')
        #~ oe = text.Span(stylename='Bold Text')
    elif e.tag in ('i', 'em'):
        oe = text.Span(stylename='Emphasis')
    elif e.tag == 'span':
        oe = text.Span()
    elif e.tag == 'br':
        oe = text.LineBreak()

    elif e.tag == 'h1':
        """
        <text:h text:style-name="Heading_20_1" text:outline-level="1">
        """
        oe = ct = text.H(stylename="Heading 1", outlinelevel=1)
    elif e.tag == 'h2':
        oe = ct = text.H(stylename="Heading 2", outlinelevel=2)
    elif e.tag == 'h3':
        oe = ct = text.H(stylename="Heading 3", outlinelevel=3)
    elif e.tag == 'div':
        oe = ct = text.Section(name="S" + str(sections_counter))

    elif e.tag == 'img':
        return  # ignore images
    elif e.tag == 'ul':
        oe = ct
    #~ elif e.tag in ('ul','ol'):
        #~ oe = text.List(stylename=e.tag.upper())
        #~ ctargs = dict(stylename=e.tag.upper()+"_P")
    elif e.tag == 'li':
        #~ oe = ct
        oe = text.ListItem()
        text_container = text.P(**ctargs)
        oe.appendChild(text_container)

    elif e.tag in PTAGS:
        oe = ct
        #~ if ct.tagName == 'p':
            #~ oe = ct
        #~ else:
            #~ oe = text.P(**ctargs)
    else:
        #~ logger.info("20130201 %s",E.tostring(e))
        raise NotImplementedError("<%s> inside <%s>" % (e.tag, ct.tagName))
        #~ oe = text.Span()

    if text_container is None:
        text_container = oe
    if e.text:
        text_container.addText(e.text)
    for child in e:
        #~ html2odf(child,oe)
        html2odf(child, text_container, **ctargs)
        #~ for oc in html2odf(child,oe):
            # ~ # oe.addElement(oc)
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
