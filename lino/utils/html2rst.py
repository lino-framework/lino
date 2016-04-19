# This document is part of the Lino test suite. To test only this
# document, run::
#
#   $ python setup.py test -s tests.UtilsTests.test_html2rst

"""Convert a :mod:`lino.utils.xmlgen.html` element to a
reStructuredText string.

If `stripped` is `True`, output will be more concise and optimized
for console output, but possibly not valid reStructuredText.

Usage examples:

>>> from lino.utils.xmlgen.html import E
>>> e = E.p("This is a ", E.b("first"), " test.")
>>> print (html2rst(e, True))
This is a **first** test.
<BLANKLINE>

>>> e = E.p(E.b("This")," is another test.")
>>> print (html2rst(e, True))
**This** is another test.
<BLANKLINE>

>>> e = E.p(E.b("This")," is ",E.em("another")," test.")
>>> print (html2rst(e, True))
**This** is *another* test.
<BLANKLINE>

>>> url = "http://example.com"
>>> e = E.p(E.b("This")," is ",E.a("a link",href=url),".")
>>> print (html2rst(e, True))
**This** is `a link <http://example.com>`__.
<BLANKLINE>

>>> e = E.p("An empty bold text:",E.b(""))
>>> print (html2rst(e, True))
An empty bold text:
<BLANKLINE>

>>> e = E.ul(E.li("First"), E.li("Second"))
>>> print (html2rst(e, True))
<BLANKLINE>
First
Second
<BLANKLINE>

>>> e = E.h1("A header")
>>> print (html2rst(e, True))
========
A header
========
<BLANKLINE>

For images we render the ``alt`` text between brackets:

>>> e = E.img(src="http://example.com/images/1.jpg", alt="1")
>>> print (html2rst(e, True))
[img 1]

If there is no ``alt`` text, render the content of ``src``:

>>> e = E.img(src="http://example.com/images/1.jpg")
>>> print (html2rst(e, True))
[img http://example.com/images/1.jpg]


"""

from __future__ import unicode_literals

from atelier import rstgen

from lino.utils.xmlgen import etree

NEWLINE_TAGS = set(['p', 'thead', 'tr', 'li'])
IGNORED_TAGS = set(['tbody', 'table', 'div', 'span', 'br', 'ul', 'ol'])


def html2rst(e, stripped=False):
    """The html2rst function."""
    #~ print "20120613 html2odftext()", e.tag, e.text
    rst = ''
    if e.tag in ('p', 'li'):
        if not stripped:
            rst += '\n\n'

    elif e.tag in ('ul', 'ol'):
        rst += '\n'
    elif e.tag == 'br':
        if stripped:
            rst += '\n'
        else:
            rst += ' |br| \n'
    elif e.tag == 'b':
        rst += '**'
    elif e.tag == 'em' or e.tag == 'i':
        rst += '*'
    elif e.tag == 'a':
        rst += '`'

    if e.text:
        rst += e.text
    for child in e:
        rst += html2rst(child, stripped)

    if e.tag in NEWLINE_TAGS:
        if stripped:
            rst += '\n'
        else:
            rst += '\n\n'
    elif e.tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
        rst = rstgen.header(int(e.tag[1]), rst.strip()).strip()
        if stripped:
            rst += '\n'
        else:
            rst = '\n\n' + rst + '\n\n'
    elif e.tag == 'b':
        if rst == '**':
            rst = ''
        else:
            rst += '**'
    elif e.tag == 'em' or e.tag == 'i':
        if rst == '*':
            rst = ''
        else:
            rst += '*'
    elif e.tag == 'a':
        rst += ' <%s>`__' % e.get('href')
    elif e.tag == 'img':
        text = e.get('alt') or e.get('src')
        rst += '[img %s]' % text
    elif e.tag in ('td', 'th'):
        rst += ' '
    else:
        if e.tag not in IGNORED_TAGS:
            raise Exception("20150723 %s" % e.tag)

    if e.tail:
        rst += e.tail

    return rst


# def html2rst(e):
#     return _html2rst(e).strip()


class RstTable(rstgen.Table):

    """\
A table containing elementtree HTML:

.. complextable::
  :header:

  Code <NEXTCELL> Result <NEXTROW>

  >>> from lino.utils.xmlgen.html import E
  >>> headers = [E.p("A ", E.b("formatted"), " header"), "A plain header"]
  >>> rows = [[1,2], [3,4]]
  >>> print (RstTable(headers).to_rst(rows))
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
            return html2rst(v, True).strip()
        return super(RstTable, self).format_value(v).strip()


