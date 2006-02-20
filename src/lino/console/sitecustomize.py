## Copyright 2003-2006 Luc Saffre 

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import sys
import codecs

"""

This module is intended to be used from your sitecustomize.py.

from lino.console import sitecustomize

"""

# inspired by:
# http://pythonfacile.free.fr/python/unicode.html
# http://www.faqs.org/docs/diveintopython/kgp_unicode.html


# the function setdefaultencoding() is deleted from module sys
# after executing sitecustomize.py

# If the Python process is "frozen" (running from a binary
# distribution produced by with py2exe or McMillan),
# sys.setdefaultencoding() has not been deleted, and site.py and
# sitecustomize.py haven't been executed.

if hasattr(sys,'setdefaultencoding'):
    import locale
    loc = locale.getdefaultlocale()
    if loc[1]:
        #print "sys.setdefaultencoding(%s)" % repr(loc[1])
        sys.setdefaultencoding(loc[1])
    
    else:
        encoding = 'cp850'
        #encoding = 'iso-8859-1'



# rewriter() inspired by a snippet in Marc-Andre Lemburg's Python
# Unicode Tutorial
# (http://www.reportlab.com/i18n/python_unicode_tutorial.html)

def rewriter(to_stream):
    if to_stream.encoding is None:
        return to_stream
    if to_stream.encoding == sys.getdefaultencoding():
        return to_stream

    (e,d,sr,sw) = codecs.lookup(to_stream.encoding)
    unicode_to_fs = sw(to_stream)

    (e,d,sr,sw) = codecs.lookup(sys.getdefaultencoding())
    
    class StreamRewriter(codecs.StreamWriter):

        encode = e
        decode = d

        def write(self,object):
            data,consumed = self.decode(object,self.errors)
            self.stream.write(data)
            return len(data)

    return StreamRewriter(unicode_to_fs)


sys.stdout=rewriter(sys.stdout)
