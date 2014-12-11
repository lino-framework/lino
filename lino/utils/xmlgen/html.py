# -*- coding: UTF-8 -*-
# LS 20120430 adapted copy from lxml\src\lxml\html\builder.py
# --------------------------------------------------------------------
# The ElementTree toolkit is
# Copyright (c) 1999-2004 by Fredrik Lundh
# --------------------------------------------------------------------

# This document is part of the Lino test suite. To test only this
# document, run::
#
#   $ python setup.py test -s tests.UtilsTests.test_xmlgen_html



"""
A set of HTML generator tags for building HTML documents.

Usage::

    >>> from lino.utils.xmlgen.html import E
    >>> html = E.html(
    ...            E.head( E.title("Hello World") ),
    ...            E.body(
    ...              E.h1("Hello World !"),
    ...              class_="main"
    ...            )
    ...        )

    >>> print E.tostring_pretty(html)
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
    >>> btn = E.button(type='button',class_='x-btn-text x-tbar-upload')
    >>> html = E.a(btn,**kw)
    >>> print E.tostring_pretty(html)
    <a href="foo/bar.html" title="Ein s&#252;&#223;es Beispiel">
    <button class="x-btn-text x-tbar-upload" type="button" />
    </a>
    
"""

from __future__ import unicode_literals

from xml.etree import ElementTree as ET
from atelier import rstgen
from lino.utils import join_elems
from lino.utils.xmlgen import etree
from lino.utils.xmlgen import Namespace


def HtmlNamespace(Namespace):

    def tostring(self, element, *args, **kw):
        kw.setdefault('method', 'html')
        return super(HtmlNamespace, self).tostring(element, *args, **kw)


#~ E = Namespace("http://www.w3.org/1999/xhtml","""
E = Namespace(None, """
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


def _html2rst(e, **kw):
    #~ print "20120613 html2odftext()", e.tag, e.text
    rst = ''
    if e.tag in ('p', 'li'):
        rst += '\n\n'
    elif e.tag == 'br':
        rst += ' |br| \n'
    elif e.tag == 'b':
        rst += '**'
    elif e.tag == 'em':
        rst += '*'
    elif e.tag == 'a':
        rst += '`'

    #~ doesn't yet work:
    """
    """

    #~ if e.tag == 'a':
        #~ return '`%s <%s>`__' % (e.text,e.get('href'))

    if e.text:
        rst += e.text
    for child in e:
        rst += _html2rst(child)

    if e.tag == 'p':
        rst += '\n\n'
    elif e.tag == 'b':
        if rst == '**':
            rst = ''
        else:
            rst += '**'
    elif e.tag == 'em':
        if rst == '*':
            rst = ''
        else:
            rst += '*'
    elif e.tag == 'a':
        rst += ' <%s>`__' % e.get('href')
    #~ else:
        #~ rst += ' '

    if e.tail:
        rst += e.tail
    return rst


def html2rst(e):
    """
    Convert a :mod:`lino.utils.xmlgen.html` element 
    (e.g. a value of a :class:`DisplayField <lino.core.fields.DisplayField>`) 
    to an reStructuredText string.
    Currently it knows only P and B tags, 
    ignoring all other formatting.
    
    Usage example:
    
    >>> from lino.utils.xmlgen.html import E, html2rst
    >>> e = E.p("This is a ", E.b("first"), " test.")
    >>> print html2rst(e)
    This is a **first** test.
    
    >>> e = E.p(E.b("This")," is another test.")
    >>> print html2rst(e)
    **This** is another test.
    
    >>> e = E.p(E.b("This")," is ",E.em("another")," test.")
    >>> print html2rst(e)
    **This** is *another* test.
    
    >>> url = "http://example.com"
    >>> e = E.p(E.b("This")," is ",E.a("a link",href=url),".")
    >>> print html2rst(e)
    **This** is `a link <http://example.com>`__.
    
    >>> e = E.p("An empty bold text:",E.b(""))
    >>> print html2rst(e)
    An empty bold text:
    """
    return _html2rst(e).strip()


class RstTable(rstgen.Table):

    """\
A table containing elementtree HTML:

.. complextable::
  :header: 

  Code <NEXTCELL> Result <NEXTROW>

  >>> from lino.utils.xmlgen.html import E, RstTable
  >>> headers = [E.p("A ", E.b("formatted"), " header"), "A plain header"]
  >>> rows = [[1,2], [3,4]]
  >>> print RstTable(headers).to_rst(rows)
  ======================== ================
   A **formatted** header   A plain header
  ------------------------ ----------------
   1                        2
   3                        4
  ======================== ================
  <BLANKLINE>

  <NEXTCELL>

  ======================== ================
   A **formatted** header   A plain header
  ------------------------ ----------------
   1                        2
   3                        4
  ======================== ================

    """

    def format_value(self, v):
        if etree.iselement(v):
            return html2rst(v)
        return super(RstTable, self).format_value(v)


def lines2p(lines, min_height=0, **attrs):
    """Examples:

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
