# -*- coding: utf-8 -*-
## Copyright 2011-2012 Luc Saffre 
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
Defines the :func:`html2xhtml` function used in :mod:`lino.utils.appy_pod`.

>>> print repr(html2xhtml('''\
... <p>Hello,&nbsp;world!<br>Again I say: Hello,&nbsp;world!</p>
... <img src="foo.org">'''))
u'<p>Hello,\xa0world!<br/>Again I say: Hello,\xa0world!</p>\n<img src="foo.org"/>'


>>> html = '''\
... <p style="font-family: &quot;Verdana&quot;;">Verdana</p>'''
>>> print repr(html2xhtml(html))
u'<p style=\'font-family: "Verdana";\'>Verdana</p>'

>>> print html2xhtml('A &amp; B')
A &amp; B

>>> print html2xhtml('a &lt; b')
a &lt; b


"""
from xml.sax.saxutils import quoteattr

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

def attrs2xml(attrs):
    #~ return ' '.join(['%s="%s"' % a for a in attrs])
    return ' '.join(['%s=%s' % (k,quoteattr(v)) for k,v in attrs])

class MyHTMLParser(HTMLParser):
    def __init__(self,*args,**kw):
        HTMLParser.__init__(self,*args,**kw)
        self.result = ''
        
    def handle_startendtag(self, tag, attrs):
        if attrs:
            self.handle_data('<%s %s/>' % (tag,attrs2xml(attrs)))
        else:
            self.handle_data('<%s/>' % tag)
        
    def handle_starttag(self, tag, attrs):
        if tag in ('br','img'):
            self.handle_startendtag(tag,attrs)
        else:
            if attrs:
                self.handle_data('<%s %s>' % (tag,attrs2xml(attrs)))
            else:
                self.handle_data('<%s>' % tag)

    def handle_endtag(self, tag):
        self.handle_data('</%s>' % tag)
        
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

    