# -*- coding: UTF-8 -*-
## Copyright 2012 Luc Saffre
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

r"""
Experimental. Not maintained and not used within Lino.

This package contains mainly a copy of `odfpy.contrib.html2odt` 
(https://joinup.ec.europa.eu/software/odfpy). 
One modification by LS in the original files:

- :file:`html2odt.py` : changed import statement for `emptycontent`

The content of this file (:file:`__init__.py`) is my own derived work.

I wanted to use the HTML2ODTParser not for grabbing 
a complete HTML page and creating a full .odt file, 
but for converting a chunk of HTML into a chunk of ODF XML.

Example:

>>> html = '''This is<br>a <em>simple</em> <b>test</b>.'''
>>> print html2odt(html)
This is<text:line-break/>a <em>simple</em> test.

Note that the Parser ignores the ``<b>...</b>`` tag.
Seems that this simply isn't yet implemented.

"""

from lino.utils.html2odt.html2odt import HTML2ODTParser
from odf import element


class RawXML(element.Childless, element.Node):
    #~ nodeType = element.Node.ELEMENT_NODE
    nodeType = element.Node.TEXT_NODE
    def __init__(self, raw_xml):
        self.raw_xml = raw_xml
        #~ super(RawXML,self).__init__()
        
    def toXml(self,level,f):
        f.write(self.raw_xml)
            


def html2odt(data,encoding='iso8859-1',baseurl=''):
    p = HTML2ODTParser(encoding, baseurl)
    #~ failure = ""
    p.feed(data)
    text = p.result()  # Flush the buffer
    #~ return RawXML(text)
    return text


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()

