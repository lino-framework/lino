# -*- coding: UTF-8 -*-
# Adapted copy from lxml\src\lxml\html\builder.py
# --------------------------------------------------------------------
# The ElementTree toolkit is
# Copyright (c) 1999-2004 by Fredrik Lundh
# Modifications in this file are
# Copyright (c) 2012-2016 Luc Saffre
# --------------------------------------------------------------------

# This document is part of the Lino test suite. To test only this
# document, run::
#
#   $ python setup.py test -s tests.UtilsTests.test_xmlgen_html

"""Defines an ElementTree Builder for generating HTML documents.

Usage:

>>> from lino.utils.xmlgen.html import E
>>> html = E.html(
...            E.head( E.title("Hello World") ),
...            E.body(
...              E.h1("Hello World !"),
...              class_="main"
...            )
...        )

>>> print (E.tostring_pretty(html))
<html>
<head>
<title>Hello World</title>
</head>
<body class="main">
<h1>Hello World !</h1>
</body>
</html>


>>> kw = dict(title=u'Ein süßes Beispiel')
>>> kw.update(href="foo/bar.html")
>>> btn = E.button(type='button', class_='x-btn-text x-tbar-upload')
>>> html = E.a(btn, **kw)
>>> print (E.tostring_pretty(html))
<a href="foo/bar.html" title="Ein s&#252;&#223;es Beispiel">
<button class="x-btn-text x-tbar-upload" type="button" />
</a>

You can also do the opposite, i.e. parse HTML:

>>> html = E.raw('''<a href="foo/bar.html"
... title="Ein s&#252;&#223;es Beispiel">
... <button class="x-btn-text x-tbar-upload" type="button" />
... </a>''')
>>> print(E.tostring_pretty(html))
<a href="foo/bar.html" title="Ein s&#252;&#223;es Beispiel">
<button class="x-btn-text x-tbar-upload" type="button" />
</a>


>>> print(E.tostring(E.raw(
...     '<ul type="disc"><li>First</li><li>Second</li></ul>')))
<ul type="disc"><li>First</li><li>Second</li></ul>

"""

from __future__ import unicode_literals
from builtins import str
from builtins import object

import types
from xml.etree import ElementTree as ET
from lxml.etree import HTML

from lino.utils import join_elems
from lino.utils.xmlgen import Namespace
from lino.utils.html2rst import html2rst
# from htmlentitydefs import name2codepoint

# ENTITIES = {}
# ENTITIES.update((x, unichr(i)) for x, i in name2codepoint.iteritems())


# def CreateParser():
#     """Every string that is being parsed must get its own parser instance.
#     This is because "Due to limitations in the Expat library used by
#     pyexpat, the xmlparser instance returned can only be used to parse
#     a single XML document. Call ParserCreate for each document to
#     provide unique parser instances. (`docs.python.org
#     <https://docs.python.org/2/library/pyexpat.html>`_)

#     """
#     p = ET.XMLParser()
#     # PARSER.entity.update(htmlentitydefs.entitydefs)
#     p.entity = ENTITIES
#     assert 'otilde' in p.entity
#     assert 'eacute' in p.entity
#     assert 'nbsp' in p.entity
#     return p

# class RAW_HTML_STRING(unicode):
#     pass


class HtmlNamespace(Namespace):
    """The HTML namespace.
    This is instantiated as ``E``.
    """

    def tostring(self, v, *args, **kw):
        # if isinstance(v, types.GeneratorType):
        if isinstance(v, (types.GeneratorType, list, tuple)):
            return "".join([self.tostring(x, *args, **kw) for x in v])
        if self.iselement(v):
            # kw.setdefault('method', 'html')
            return super(HtmlNamespace, self).tostring(v, *args, **kw)
        return str(v)

    def to_rst(self, v, stripped=True):
        if isinstance(v, types.GeneratorType):
            return "".join([self.to_rst(x, stripped) for x in v])
        if self.iselement(v):
            return html2rst(v, stripped)
        return str(v)

    # def raw(self, raw_html):
    #     return RAW_HTML_STRING(raw_html)

    def raw(self, raw_html):
        """Parses the given string into an HTML Element.

        It the string contains a a single top-level element, then this
        element is returned. Otherwise return thewrapping ``body``
        element.

        """
        # print 20151008, raw_html

        # the lxml parser wraps `<html><body>...</body></html>` around
        # the snippet, but we don't want it.
        root = HTML(raw_html)[0]
        if len(root) == 1:
            return root[0]
        return root
        # try:
        #     return self.fromstring(raw_html, parser=CreateParser())
        # except ET.ParseError as e:
        #     raise Exception("ParseError {0} in {1}".format(e, raw_html))


E = HtmlNamespace(None, """
a
abbr
acronym
address
alt
applet
area
b
base
basefont
bdo
big
blockquote
body
br
button
caption
center
cite     
code     
col      
colgroup 
dd       
del      
dfn      
dir      
div      
dl       
dt       
em       
fieldset 
font     
form     
frame    
frameset 
h1     
h2     
h3     
h4     
h5
h6
head
height
hr     
html   
i      
iframe 
img    
input  
ins    
isindex 
kbd 
label 
legend 
li 
link 
map 
menu 
meta 
name
noframes 
noscript 
object 
ol 
optgroup 
option 
p
param 
pre 
q 
s 
samp
script
select
small
span
strike
strong
style
sub
sup
table
tbody
td
textarea
tfoot
th
thead
title
tr
tt
u
ul
var

class
id
bgcolor
cellspacing
width
align
valign
href
type
rel
target
value
onclick
src
rows
data-toggle
tabindex
placeholder
""")


def table_header_row(*headers, **kw):
    return E.tr(*[E.th(h, **kw) for h in headers])


def table_body_row(*cells, **kw):
    return E.tr(*[E.td(h, **kw) for h in cells])


class Table(object):
    """A pythonic representation of a ``<table>`` with ``<head>``,
    ``<foot>`` and ``<body>``.

    """
    def __init__(self):
        self.clear()

    def clear(self):
        self.head = []
        self.foot = []
        self.body = []
        self.attrib = dict()

    def add_header_row(self, *args, **kw):
        e = table_header_row(*args, **kw)
        self.head.append(e)
        return e

    def add_footer_row(self, *args, **kw):
        e = table_body_row(*args, **kw)
        self.foot.append(e)
        return e

    def add_body_row(self, *args, **kw):
        e = table_body_row(*args, **kw)
        self.body.append(e)
        return e

    def as_element(self):
        children = []
        if self.head:
            children.append(E.thead(*self.head))
        if self.foot:
            children.append(E.tfoot(*self.foot))
        if self.body:
            children.append(E.tbody(*self.body))
        return E.table(*children, **self.attrib)


class Document(object):
    """A pythonic representation of a ``<body>`` with a ``<title>`` and
    some ``<head>`` tags for stylesheets.

    """

    def __init__(self, title, stylesheets=None):
        self.title = title
        self.body = []
        self.stylesheets = stylesheets or []

    def add_stylesheet(self, url):
        self.stylesheets.append(url)

    def add_table(self):
        t = Table()
        self.body.append(t)
        return t

    def write(self, *args, **kw):
        ET.ElementTree(self.as_element()).write(*args, **kw)

    def as_element(self):
        body = []
        for e in self.body:
            if isinstance(e, Table):
                body.append(e.as_element())
            else:
                body.append(e)
        headers = []
        for css in self.stylesheets:
            headers.append(E.link(rel="stylesheet", type="text/css", href=css))
        headers.append(E.title(self.title))

        return E.html(
            E.head(*headers),
            E.body(*body)
        )


def lines2p(lines, min_height=0, **attrs):
    """Convert the given list of text lines `lines` into a paragraph
(``<p>``) with one ``<br>`` between each line. If optional
`min_height` is given, add empty lines if necessary.

    Examples:

    >>> print(E.tostring(lines2p(['first', 'second'])))
    <p>first<br />second</p>

    >>> print(E.tostring(lines2p(['first', 'second'], min_height=5)))
    <p>first<br />second<br /><br /><br /></p>

    If `min_height` is specified, and `lines` contains more items,
    then we don't truncate:

    >>> print(E.tostring(lines2p(['a', 'b', 'c', 'd', 'e'], min_height=4)))
    <p>a<br />b<br />c<br />d<br />e</p>

    This also works:

    >>> print(E.tostring(lines2p([], min_height=5)))
    <p><br /><br /><br /><br /></p>

    """
    while len(lines) < min_height:
        lines.append('')
    lines = join_elems(lines, E.br)
    return E.p(*lines, **attrs)


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
