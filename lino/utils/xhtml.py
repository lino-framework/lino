# -*- coding: UTF-8 -*-
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

"""

First example:

>>> xg.set_default_namespace(xhtml)
>>> doc = HTML(HEAD(TITLE("Hello")),BODY(P("Hello, world!")))
>>> print doc.toxml(True)
<HTML xmlns="http://www.w3.org/1999/xhtml">
<HEAD>
<TITLE>Hello</TITLE>
</HEAD>
<BODY>
<P>Hello, world!</P>
</BODY>
</HTML>

Second example:

>>> doc = HTML()
>>> doc.set_title("A simple table")
>>> p = doc.add_to_body(P("Here is a table."))
>>> t = TABLE()
>>> doc.add_to_body(t)
>>> t.add_header_row("Country", "Capital", "Population")
>>> t.add_body_row("Belgium", "Brussels", "10.0M")
>>> t.add_body_row("Estonia", "Tallinn", "1.1M")
>>> print doc.toxml(True)
<HTML xmlns="http://www.w3.org/1999/xhtml">
<HEAD>
<TITLE>A simple table</TITLE>
</HEAD>
<BODY>
<P>Here is a table.</P>
<TABLE>
<THEAD>
<TH>Country</TH>
<TH>Capital</TH>
<TH>Population</TH>
</THEAD>
<TBODY>
<TD>Belgium</TD>
<TD>Brussels</TD>
<TD>10.0M</TD>
</TBODY>
<TBODY>
<TD>Estonia</TD>
<TD>Tallinn</TD>
<TD>1.1M</TD>
</TBODY>
</TABLE>
</BODY>
</HTML>
"""


import datetime

from appy.shared.dav import Resource
from appy.shared.xml_parser import XmlUnmarshaller

from lino.utils import d2iso
from lino.utils import IncompleteDate
from lino.utils import xmlgen as xg

class HtmlContainer(xg.Container):
    style = xg.Attribute()
    bgcolor = xg.Attribute()
    width = xg.Attribute()

class xhtml(xg.Namespace):
  url = "http://www.w3.org/1999/xhtml"
  
  class HTML(HtmlContainer):
    class HEAD(xg.Container):
        class TITLE(xg.String):
            pass
    class BODY(HtmlContainer):
        class TEXT(xg.TEXT): pass            
        class P(HtmlContainer): pass
        class TABLE(HtmlContainer):
            border = xg.Attribute()
            cellspacing = xg.Attribute()
            class COLGROUP(xg.Container): 
                class COL(xg.Container): 
                    width = xg.Attribute()
                    span = xg.Attribute()
                    
            class TBODY(xg.Container): 
                class TR(HtmlContainer):
                    class TD(HtmlContainer):
                      align = xg.Attribute()
                      valign = xg.Attribute()
                      bgcolor = xg.Attribute()
                    class TH(TD): pass
            class THEAD(TBODY): pass
            class TFOOT(TBODY): pass
              
            def add_header_row(self,*headers,**kw):
                cells = [self.THEAD.TR.TH(h,**kw) for h in headers]
                self.append(self.THEAD(*cells))

            def add_body_row(self,*cells,**kw):
                cells = [self.TBODY.TR.TD(h,**kw) for h in cells]
                self.append(self.TBODY(*cells))

    def set_title(self,text):
        head = self.find_node(HEAD)
        title = head.find_node(HEAD.TITLE)
        title.value = TEXT(text)
        
    def add_to_body(self,node):
        body = self.find_node(BODY)
        body.append(node)
  
HTML = xhtml.HTML
HEAD = xhtml.HTML.HEAD
TITLE = xhtml.HTML.HEAD.TITLE
BODY = xhtml.HTML.BODY
P = xhtml.HTML.BODY.P
TABLE = xhtml.HTML.BODY.TABLE
#~ TR = xhtml.HTML.BODY.TABLE.TR
#~ TD = xhtml.HTML.BODY.TABLE.TR.TD
#~ TH = xhtml.HTML.BODY.TABLE.TR.TH
TEXT = xhtml.HTML.BODY.TEXT

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

