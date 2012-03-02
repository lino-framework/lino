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

raise Exception("No longer used since 20120301")

"""

First example:

>>> doc = HTML(HEAD(TITLE("Hello")),BODY(P("Hello, world!")))
>>> print doc.tostring(True,namespace=xhtml)
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
>>> doc.set_title("Two tables")
>>> p = doc.add_to_body(P("Here are two tables."))
>>> def add_table(cl):
...     t = cl()
...     doc.add_to_body(t)
...     t.add_header_row("Country", "Capital", "Population")
...     t.add_body_row("Belgium", "Brussels", "10.0M")
...     t.add_body_row("Estonia", "Tallinn", "1.1M")
>>> add_table(TABLE)
>>> add_table(HFBTABLE)
>>> print doc.tostring(True,namespace=xhtml)
<HTML xmlns="http://www.w3.org/1999/xhtml">
<HEAD>
<TITLE>Two tables</TITLE>
</HEAD>
<BODY>
<P>Here are two tables.</P>
<TABLE>
<TR>
<TH>Country</TH>
<TH>Capital</TH>
<TH>Population</TH>
</TR>
<TR>
<TD>Belgium</TD>
<TD>Brussels</TD>
<TD>10.0M</TD>
</TR>
<TR>
<TD>Estonia</TD>
<TD>Tallinn</TD>
<TD>1.1M</TD>
</TR>
</TABLE>
<TABLE>
<THEAD>
<TR>
<TH>Country</TH>
<TH>Capital</TH>
<TH>Population</TH>
</TR>
</THEAD>
<TBODY>
<TR>
<TD>Belgium</TD>
<TD>Brussels</TD>
<TD>10.0M</TD>
</TR>
<TR>
<TD>Estonia</TD>
<TD>Tallinn</TD>
<TD>1.1M</TD>
</TR>
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

Writer = xg.Writer

class HtmlContainer(xg.Container):
    style = xg.Attribute()
    bgcolor = xg.Attribute()
    width = xg.Attribute()

class xhtml(xg.Namespace):
  prefix = None
  url = "http://www.w3.org/1999/xhtml"
  
  class HTML(HtmlContainer):
    class HEAD(xg.Container):
        #~ class SCRIPT(xg.Javascript): pass
        class TITLE(xg.String):
            pass
    class BODY(HtmlContainer):
        class TEXT(xg.TEXT): pass            
        class P(HtmlContainer): pass
        class TABLE(HtmlContainer):
            border = xg.Attribute()
            cellspacing = xg.Attribute()
                
            class TR(HtmlContainer):
                class TD(HtmlContainer):
                  align = xg.Attribute()
                  valign = xg.Attribute()
                  bgcolor = xg.Attribute()
                  colspan = xg.Attribute()
                class TH(TD): pass
                  
            class COLGROUP(xg.Container): 
                class COL(xg.Container): 
                    width = xg.Attribute()
                    span = xg.Attribute()
                    
            class TBODY(xg.Container): pass
            class THEAD(xg.Container): pass
            class TFOOT(xg.Container): pass
              
            def add_header_row(self,*args,**kw):
                return self.add_child(table_header_row(*args,**kw))
                
            def add_body_row(self,*args,**kw):
                return self.add_child(table_body_row(*args,**kw))

                
        class HFBTABLE(TABLE):
            "Variant of TABLE that uses THEAD, TFOOT and TBODY elements"
            elementname = "TABLE"
            def add_header_row(self,*args,**kw):
                return self.find_node(self.THEAD).add_child(table_header_row(*args,**kw))
                
            def add_footer_row(self,*args,**kw):
                return self.find_node(self.TFOOT).add_child(table_body_row(*args,**kw))
                #~ tr = self.TR(*[self.TR.TH(h,**kw) for h in headers])

            def add_body_row(self,*args,**kw):
                return self.find_node(self.TBODY).add_child(table_body_row(*args,**kw))
                #~ tr = self.TR(*[self.TR.TD(h,**kw) for h in cells])
                #~ self.add_child(self.TBODY(*cells))

    def set_title(self,text):
        head = self.find_node(HEAD)
        title = head.find_node(HEAD.TITLE)
        title.value = TEXT(text)
        
    def add_to_body(self,node):
        body = self.find_node(BODY)
        return body.add_child(node)
  
HTML = xhtml.HTML
HEAD = xhtml.HTML.HEAD
TITLE = xhtml.HTML.HEAD.TITLE
BODY = xhtml.HTML.BODY
P = xhtml.HTML.BODY.P
TABLE = xhtml.HTML.BODY.TABLE
HFBTABLE = xhtml.HTML.BODY.HFBTABLE
#~ TR = xhtml.HTML.BODY.TABLE.TR
#~ TD = xhtml.HTML.BODY.TABLE.TR.TD
#~ TH = xhtml.HTML.BODY.TABLE.TR.TH
TEXT = xhtml.HTML.BODY.TEXT
#~ SCRIPT = xhtml.HTML.HEAD.SCRIPT

def table_header_row(*headers,**kw):
    return TABLE.TR(*[TABLE.TR.TH(h,**kw) for h in headers])
def table_body_row(*cells,**kw):
    return TABLE.TR(*[TABLE.TR.TD(h,**kw) for h in cells])
                  


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

