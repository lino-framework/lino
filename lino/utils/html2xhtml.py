# -*- coding: utf-8 -*-
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

ur"""
Defines the :func:`html2xhtml` function which converts 
HTML to valid XHTML. It is far from being perfect but
activaly being used in :mod:`lino.utils.appy_pod`.

>>> print(html2xhtml('''\
... <p>Hello,&nbsp;world!<br>Again I say: Hello,&nbsp;world!</p>
... <img src="foo.org">''')) #doctest: +NORMALIZE_WHITESPACE
<p>Hello, world!<br/>Again I say: Hello, world!</p>
<img src="foo.org"/>

(Note: the above contains non-breaking spaces `\xa0`)

>>> html = '''\
... <p style="font-family: &quot;Verdana&quot;;">Verdana</p>'''
>>> print(html2xhtml(html))
<p style='font-family: "Verdana";'>Verdana</p>

>>> print(html2xhtml('A &amp; B'))
A &amp; B

>>> print(html2xhtml('a &lt; b'))
a &lt; b

A `<div>` inside a `<span>` is not valid XHTML. 
But how to convert it?
Current solution is to simply remove the `<div>` 
tag (and it's corresponding `</div>`):

>>> print(html2xhtml('<p>foo<span>bar<div> oops </div>baz</span>bam</p>'))
<p>foo<span>bar oops baz</span>bam</p>

In HTML it was tolerated to not end certain tags.
For example, a string "<p>foo<p>bar<p>baz" should convert 
to  "<p>foo</p><p>bar</p><p>baz</p>". 
That's not yet implemented, but at least detected:

>>> print(html2xhtml('<p>foo<p>bar<p>baz'))
Traceback (most recent call last):
...
Exception: Unexpected end of document. Expected at least </p></p></p>


  

"""

from __future__ import print_function, unicode_literals

from xml.sax.saxutils import quoteattr

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

def attrs2xml(attrs):
    #~ return ' '.join(['%s="%s"' % a for a in attrs])
    return ' '.join(['%s=%s' % (k,quoteattr(v)) for k,v in attrs])
    
class TagEntry(object):
    def __init__(self,name,ignored=False):    
        self.name = name
        self.ignored = ignored

class MyHTMLParser(HTMLParser):
    def __init__(self,*args,**kw):
        HTMLParser.__init__(self,*args,**kw)
        self.result = ''
        self.context = []
        
    def handle_startendtag(self, tag, attrs):
        if not self.allow_tag_in_context(tag):
            return
            
        if attrs:
            self.handle_data('<%s %s/>' % (tag,attrs2xml(attrs)))
        else:
            self.handle_data('<%s/>' % tag)
        
    def handle_starttag(self, tag, attrs):
        if tag in ('br','img'):
            self.handle_startendtag(tag,attrs)
        else:
            if not self.allow_tag_in_context(tag):
                self.context.append(TagEntry(tag,True))
                return
            self.context.append(TagEntry(tag,False))
            if attrs:
                self.handle_data('<%s %s>' % (tag,attrs2xml(attrs)))
            else:
                self.handle_data('<%s>' % tag)

    def handle_endtag(self, tag):
        if len(self.context) > 0:
            expected = self.context.pop()
            if expected.name != tag:
                raise Exception("Invalid endtag. Expected </%s>, found <%s>" % (expected.name,tag))
        else:
            raise Exception("Unexpected endtag </%s> but context is empty" % tag)
        if not expected.ignored:
            self.handle_data('</%s>' % tag)
        
    def allow_tag_in_context(self,tag):
        if tag == 'div':
            for te in self.context:
                if te.name == 'span':
                    return False
        return True
        
    def handle_data(self, data):
        self.result += data
        
    def handle_entityref(self,name):
        """process a general entity reference of the form "&name;"."""
        #~ print "20121010 handle_entityref", repr(name)
        if name in ('lt','gt','amp','quot'):
            # 20120311 
            #~ self.handle_data('<![CDATA['+unichr(name2codepoint[name])+']]>')
            #~ 20121010 self.handle_data(unichr(name2codepoint[name]))
            self.handle_data("&%s;" % name)
            return
        self.handle_data(unichr(name2codepoint[name]))

def html2xhtml(html):
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
        raise Exception("Unexpected end of document. Expected at least %s" % expected)
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

    
