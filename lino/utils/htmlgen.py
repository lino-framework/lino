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

import cgi

from django.utils.functional import Promise
from django.utils.encoding import force_unicode

from lino.utils.restify import restify



CONVERTERS = []

def py2html(v):
    #~ logger.debug("py2js(%r)",v)
    for cv in CONVERTERS:
        v = cv(v)
    if isinstance(v,Promise):
        v = force_unicode(v)
    if isinstance(v,HTML):
        return v.__html__()
    if callable(v):
        return "\n".join([ln for ln in v()])
    return cgi.escape(unicode(v))

class HTML(object):
    def __init__(self,html_code):
        self.html_code = html_code
    def __html__(self):
        return self.html_code
      
def LIST(tag,items):
    s = '\n'.join(['<li>%s</li>' % py2html(i) for i in items])
    return "<%s>%s</%s>" % (tag,s,tag)
def UL(items): return LIST('UL',items)
def OL(items): return LIST('OL',items)
def H(level,text): return "<H%d>%s</H%d>" % (level,cgi.escape(text),level)
def DIV(content): return "<DIV>%s</DIV>" % py2html(content)
def TH(content): return "<th>%s</th>" % py2html(content)
def TD(content): return "<TD>%s</TD>" % py2html(content)



class TABLE:
    """
    Renders as a simple table.
    
    """
    def __init__(self,headers,show_headers=True):
        self.headers = headers
        self.show_headers = show_headers
        
    def html_lines(self,rows):
        yield "<TABLE>"    
        if self.show_headers:
            s = ''.join([TH(HTML(h)) for h in self.headers])
            yield "<TR>%s</TR>" % s
        
        for row in rows:
            s = ''.join([TD(HTML(cell)) for cell in row])
            yield "<TR>%s</TR>" % s
        yield "</TABLE>"    
          
