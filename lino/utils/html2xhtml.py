# -*- coding: utf-8 -*-
# Copyright 2011-2016 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

# How to test this document:
#
#  $ python setup.py test -s tests.UtilsTests.test_tidy

r"""Defines the :func:`html2xhtml` function which converts HTML to
valid XHTML.

It uses Jason Stitt's `pytidylib
<http://countergram.com/open-source/pytidylib/docs/index.html>`__
module. This module requires the `HTML Tidy library
<http://tidy.sourceforge.net/>`__ to be installed on the system::

    $ sudo apt-get install tidy

Some examples:

>>> print(html2xhtml('''\
... <p>Hello,&nbsp;world!<br>Again I say: Hello,&nbsp;world!</p>
... <img src="foo.org" alt="Foo">'''))
... #doctest: +NORMALIZE_WHITESPACE -SKIP
<p>Hello,&nbsp;world!<br />
Again I say: Hello,&nbsp;world!</p>
<img src="foo.org" alt="Foo" />

Above test is currently skipped because tidylib output can slightly
differ (``alt="Foo">`` versus ``alt="Foo" >``) depending on the
installed version of tidylib.


>>> html = '''\
... <p style="font-family: &quot;Verdana&quot;;">Verdana</p>'''
>>> print(html2xhtml(html))
<p style="font-family: &quot;Verdana&quot;;">Verdana</p>

>>> print(html2xhtml('A &amp; B'))
A &amp; B

>>> print(html2xhtml('a &lt; b'))
a &lt; b

A `<div>` inside a `<span>` is not valid XHTML.
Neither is a `<li>` inside a `<strong>`.

But how to convert it?  Inline tags must be "temporarily" closed
before and reopended after a block element.

>>> print(html2xhtml('<p>foo<span class="c">bar<div> oops </div>baz</span>bam</p>'))
<p>foo<span class="c">bar</span></p>
<div><span class="c">oops</span></div>
<span class="c">baz</span>bam

>>> print(html2xhtml('''<strong><ul><em><li>Foo</li></em><li>Bar</li></ul></strong>'''))
<ul>
<li><strong><em>Foo</em></strong></li>
<li><strong>Bar</strong></li>
</ul>

In HTML it was tolerated to not end certain tags.
For example, a string "<p>foo<p>bar<p>baz" converts
to "<p>foo</p><p>bar</p><p>baz</p>".

>>> print(html2xhtml('<p>foo<p>bar<p>baz'))
<p>foo</p>
<p>bar</p>
<p>baz</p>




"""

# from __future__ import print_function, unicode_literals

WRAP_BEFORE = """\
<html>
<head>
<title></title>
</head>
<body>
"""

try:

    from tidylib import tidy_fragment

    # http://tidy.sourceforge.net/docs/quickref.html

    def html2xhtml(html, **options):
        options.update(doctype='omit')
        options.update(show_warnings=0)
        options.update(indent=0)
        # options.update(output_xml=1)
        options.update(output_xhtml=1)
        document, errors = tidy_fragment(html, options=options)
        if False:  # errors:
            # LS 20190905 disabled error checking, see my blog
            #~ raise Exception(repr(errors))
            raise Exception("Errors while processing %s\n==========\n%s" %
                            (html, errors))
        # if document.startswith(WRAP_BEFORE):
        #     document = document[len(WRAP_BEFORE):]
        #     document = document[:-15]
        return document.strip()

    HAS_TIDYLIB = True

except OSError:
    # happens on readthedocs.org and Travis CI: OSError: Could not
    # load libtidy using any of these names:
    # libtidy,libtidy.so,libtidy-0.99.so.0,cygtidy-0-99-0,tidylib,
    # libtidy.dylib,tidy

    # We can simply ignore it since it is just for building the docs.
    from lino.utils.mytidylib import html2xhtml
    # TODO: emulate it well enough so that at least the test suite passes

    HAS_TIDYLIB = False


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
