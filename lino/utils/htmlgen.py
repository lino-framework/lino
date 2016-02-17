from builtins import str
from builtins import object
# Copyright 2011-2012 Luc Saffre
# License: BSD (see file COPYING for details)

import cgi

from django.utils.functional import Promise
from django.utils.encoding import force_text

from lino.utils.restify import restify


CONVERTERS = []


def py2html(v):
    #~ logger.debug("py2js(%r)",v)
    for cv in CONVERTERS:
        v = cv(v)
    if isinstance(v, Promise):
        v = force_text(v)
    if isinstance(v, HTML):
        return v.__html__()
    if callable(v):
        return "\n".join([ln for ln in v()])
    return cgi.escape(str(v))


class HTML(object):

    def __init__(self, html_code):
        self.html_code = html_code

    def __html__(self):
        return self.html_code


def LIST(tag, items):
    s = '\n'.join(['<li>%s</li>' % py2html(i) for i in items])
    return "<%s>%s</%s>" % (tag, s, tag)


def UL(items):
    return LIST('UL', items)


def OL(items):
    return LIST('OL', items)


def H(level, text):
    return "<h%d>%s</h%d>" % (level, cgi.escape(text), level)


def DIV(content):
    return "<DIV>%s</DIV>" % py2html(content)


def TH(content):
    return "<th>%s</th>" % py2html(content)


def TD(content):
    return "<TD>%s</TD>" % py2html(content)


class TABLE(object):

    """
    Renders as a simple table.
    
    """

    def __init__(self, headers, show_headers=True):
        self.headers = headers
        self.show_headers = show_headers

    def html_lines(self, rows):
        yield "<TABLE>"
        if self.show_headers:
            s = ''.join([TH(HTML(h)) for h in self.headers])
            yield "<TR>%s</TR>" % s

        for row in rows:
            s = ''.join([TD(HTML(cell)) for cell in row])
            yield "<TR>%s</TR>" % s
        yield "</TABLE>"
