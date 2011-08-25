## Copyright 2011 Luc Saffre
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

import logging
logger = logging.getLogger(__name__)

from lino.utils.restify import restify
from lino.utils.html2xhtml import html2xhtml


def setup_renderer(renderer):
    """
    Install additional functions into the specified `appy.pod` renderer.
    
    This may break with later versions of `appy.pod` since 
    it hacks on undocumented regions... but we wanted to be 
    able to insert rst formatted plain text using a simple comment 
    like this::
    
      do text
      from restify(self.body)
        
    Without this hack, users would have to write each time something 
    like::
    
      do text
      from xhtml(restify(self.body).encode('utf-8'))
        
      do text
      from xhtml(restify(self.body,output_encoding='utf-8'))
    

    """
    def restify_func(unicode_string,**kw):
        if not unicode_string:
            return ''
        
        html = restify(unicode_string,output_encoding='utf-8')
        #~ try:
            #~ html = restify(unicode_string,output_encoding='utf-8')
        #~ except Exception,e:
            #~ print unicode_string
            #~ traceback.print_exc(e)
        #~ print repr(html)
        #~ print html
        return renderer.renderXhtml(html,**kw)
        #~ return renderer.renderXhtml(html.encode('utf-8'),**kw)
    renderer.contentParser.env.context.update(restify=restify_func)
    def html_func(html,**kw):
        if not html:
            return ''
        #~ logger.debug("html_func() got:<<<\n%s\n>>>",html)
        #~ print __file__, ">>>"
        #~ print html
        #~ print "<<<", __file__
        html = html2xhtml(html)
        if isinstance(html,unicode):
            # some sax parsers refuse unicode strings. 
            # appy.pod always expects utf-8 encoding.
            # See /blog/2011/0622.
            html = html.encode('utf-8')
        return renderer.renderXhtml(html,**kw)
    renderer.contentParser.env.context.update(html=html_func)
    
    #~ def xhtml_func(xhtml,**kw):
        #~ if isinstance(xhtml,unicode):
            #~ html = html.encode('utf-8')
        #~ return renderer.renderXhtml(xhtml,**kw)
    #~ renderer.contentParser.env.context.update(xhtml=xhtml_func)



