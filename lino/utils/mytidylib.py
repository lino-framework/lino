# -*- coding: utf-8 -*-
# Copyright 2011-2015 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""This is used only when libtidy is not available.

"""
# from future import standard_library
# standard_library.install_aliases()
from builtins import chr
# from builtins import object
# from __future__ import print_function, unicode_literals
from xml.sax.saxutils import quoteattr

from html.parser import HTMLParser
from html.entities import name2codepoint


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
            self.result += '<%s %s />' % (tag, attrs2xml(attrs))
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
            if tag == 'p':
                # avoid nested <p> tags
                if len(self.context) > 0:
                    if self.context[-1].name == 'p':
                        self.handle_endtag(tag)
                        self.result += '\n'
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
            self.write_endtag(tag)

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
        self.handle_data(chr(name2codepoint[name]))


def html2xhtml(html, **options):
    """
    Convert a HTML text to XHTML.
    Currently this is very basic and will be extended as needed.

    http://meiert.com/de/publications/translations/whatwg.org/html-vs-xhtml/
    http://de.selfhtml.org/html/xhtml/unterschiede.htm    
    """
    p = MyHTMLParser()
    p.feed(html)
    p.close()
    while len(p.context) > 0:
        e = p.context.pop()
        p.write_endtag(e.name)
        p.result += '\n'

    if len(p.context) > 0:
        expected = ''.join(["</%s>" % te.name for te in p.context])
        raise Exception("Unexpected end of document. Expected at least %s" %
                        expected)
    return p.result.rstrip()


