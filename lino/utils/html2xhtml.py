# -*- coding: utf-8 -*-
# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)

ur"""
Defines the :func:`html2xhtml` function which converts
HTML to valid XHTML. It is far from being perfect but
activaly being used in :mod:`lino.utils.appy_pod`.

>>> print(html2xhtml('''\
... <p>Hello,&nbsp;world!<br>Again I say: Hello,&nbsp;world!</p>
... <img src="foo.org">''')) #doctest: +NORMALIZE_WHITESPACE
<p>Hello,&nbsp;world!<br />
Again I say: Hello,&nbsp;world!</p>
<img src="foo.org" alt="" />


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

from __future__ import print_function, unicode_literals

from tidylib import tidy_fragment


def html2xhtml(html, **options):
    options.update(doctype='omit')
    options.update(show_warnings=0)
    options.update(indent=0)
    options.update(output_xml=1)
    document, errors = tidy_fragment(html, options=options)
    if errors:
        #~ raise Exception(repr(errors))
        raise Exception("Errors while processing %s\n==========\n%s" %
                        (html, errors))
    return document


# The remaining part is not used and just an illustration of how much
# time people can waste before realizing that they are reinventing the wheel.
from xml.sax.saxutils import quoteattr

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint


def attrs2xml(attrs):
    #~ return ' '.join(['%s="%s"' % a for a in attrs])
    return ' '.join(['%s=%s' % (k, quoteattr(v)) for k, v in attrs])


INLINE_TAGS = frozenset("""
a abbr acronym b bdo big br cite code dfn 
em s i img input kbd label q samp select small
span strong sub sup textarea tt var
""".split())


def is_inline_tag(tag):
    return tag in INLINE_TAGS


class TagEntry(object):

    def __init__(self, name, ignored=False):
        self.name = name
        self.ignored = ignored


class MyHTMLParser(HTMLParser):

    def __init__(self, *args, **kw):
        HTMLParser.__init__(self, *args, **kw)
        self.result = ''
        self.context = []
        self.inline_stack = []
        self.is_inline = False

    def write_startendtag(self, tag, attrs):
        if attrs:
            self.result += '<%s %s/>' % (tag, attrs2xml(attrs))
        else:
            self.result += '<%s/>' % tag

    def write_starttag(self, tag, attrs):
        if attrs:
            self.result += '<%s %s>' % (tag, attrs2xml(attrs))
        else:
            self.result += '<%s>' % tag

    def write_endtag(self, tag):
        self.result += '</%s>' % tag

    def before_tag(self, tag):
        if is_inline_tag(tag):
            if not self.is_inline:
                for itag, iattrs in self.pending_inline_tags():
                    self.handle_starttag(itag, iattrs)

                self.is_inline = True
        elif self.is_inline:
            self.is_inline = False

    def handle_startendtag(self, tag, attrs):
        if not self.allow_tag_in_context(tag):
            return
        self.write_startendtag(tag, attrs)

    def handle_starttag(self, tag, attrs):
        if tag in ('br', 'img'):
            self.handle_startendtag(tag, attrs)
        else:
            if not self.allow_tag_in_context(tag):
                self.context.append(TagEntry(tag, True))
                return
            self.context.append(TagEntry(tag, False))
            self.write_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if len(self.context) > 0:
            expected = self.context.pop()
            if expected.name != tag:
                raise Exception("Invalid endtag. Expected </%s>, found <%s>" %
                                (expected.name, tag))
        else:
            raise Exception("Unexpected endtag </%s> but context is empty" %
                            tag)
        if not expected.ignored:
            self.write_enddtag(tag)

    def allow_tag_in_context(self, tag):
        if tag == 'div':
            for te in self.context:
                if te.name == 'span':
                    return False
        return True

    def handle_data(self, data):
        self.result += data

    def handle_entityref(self, name):
        """process a general entity reference of the form "&name;"."""
        #~ print "20121010 handle_entityref", repr(name)
        if name in ('lt', 'gt', 'amp', 'quot'):
            # 20120311
            #~ self.handle_data('<![CDATA['+unichr(name2codepoint[name])+']]>')
            #~ 20121010 self.handle_data(unichr(name2codepoint[name]))
            self.handle_data("&%s;" % name)
            return
        self.handle_data(unichr(name2codepoint[name]))


def unused_html2xhtml(html):
    """
    Convert a HTML text to XHTML.
    Currently this is very basic and will be extended as needed.
    
    http://meiert.com/de/publications/translations/whatwg.org/html-vs-xhtml/
    http://de.selfhtml.org/html/xhtml/unterschiede.htm    
    """
    p = MyHTMLParser()
    p.feed(html)
    p.close()
    if len(p.context) > 0:
        expected = ''.join(["</%s>" % te.name for te in p.context])
        raise Exception("Unexpected end of document. Expected at least %s" %
                        expected)
    return p.result


#~ if __name__ == "__main__"	:
    #~ print html2xhtml('''
    #~ <p><span style="background-color: rgb(255, 255, 255); " id="ext-gen416">
    #~ Also ich probier mal.<br/>Schreibe ein bisschen Text.<br/><br/></span>
    #~ <h1 id="ext-gen418"><span style="background-color: rgb(255, 255, 255); ">
    #~ <span style="font-size: 32px; font-weight: bold; " id="ext-gen408">Aufzählungen:</span></span></h1>
    #~ <ol><li>Eins</li><li>Zwei</li><li>Drei</li><li>Vier</li><li>Fünf</li></ol><span style="background-color: rgb(255, 255, 255); "><br/><div id="ext-gen420"><span style="border-collapse: collapse; -webkit-border-horizontal-spacing: 2px; -webkit-border-vertical-spacing: 2px;">
    #~ Aber für :field:`notes</span><span style="border-collapse: collapse; -webkit-border-horizontal-spacing:
    #~ 2px; -webkit-border-vertical-spacing: 2px;">.Note.body`
    #~ gilt das nicht.&nbsp;</span><span style="border-collapse: collapse; -webkit-border-horizontal-spacing: 2px; -webkit-border-vertical-spacing: 2px; ">Dafür ist er ideal. Auch der Ausdruck funktioniert einfach,&nbsp;</span><span style="border-collapse: collapse; -webkit-border-horizontal-spacing: 2px; -webkit-border-vertical-spacing: 2px; ">indem ich in&nbsp;</span><span style="border-collapse: collapse; -webkit-border-horizontal-spacing: 2px; -webkit-border-vertical-spacing: 2px; "><a href="https://github.com/VinylFox/ExtJS.ux.HtmlEditor.Plugins" target="_self">appy.pod</a></span></div><div id="ext-gen420"><span style="border-collapse: collapse; -webkit-border-horizontal-spacing: 2px; -webkit-border-vertical-spacing: 2px; ">die folgende Formel verwende::</span></div><div><span style="border-collapse: collapse; -webkit-border-horizontal-spacing: 2px; -webkit-border-vertical-spacing: 2px; "><br/></span></div></span><blockquote class="webkit-indent-blockquote" style="margin: 0 0 0 40px; border: none; padding: 0px;"><span style="background-color: rgb(255, 255, 255); "><div><span style="border-collapse: collapse; -webkit-border-horizontal-spacing: 2px; -webkit-border-vertical-spacing: 2px;">&nbsp; do text</span></div></span><span style="background-color: rgb(255, 255, 255); "><div><span style="border-collapse: collapse; -webkit-border-horizontal-spacing: 2px; -webkit-border-vertical-spacing: 2px;">&nbsp; from xhtml(self.body)</span></div></span></blockquote><span style="background-color: rgb(255, 255, 255); "><div><span style="border-collapse: collapse; -webkit-border-horizontal-spacing: 2px; -webkit-border-vertical-spacing: 2px;">&nbsp;&nbsp;</span></div><div style="border-collapse: collapse; -webkit-border-horizontal-spacing: 2px; -webkit-border-vertical-spacing: 2px; "><br/></div></span></p>
    #~ ''')
def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
