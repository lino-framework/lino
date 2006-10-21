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
import locale

"""

"""

# In a normal Python installation the function setdefaultencoding() is
# deleted from module sys after executing sitecustomize.py

# If the Python process is "frozen" (running from a binary
# distribution produced by with py2exe or McMillan),
# sys.setdefaultencoding() has not been deleted, and site.py and
# sitecustomize.py haven't been executed.

# inspired by:
# http://pythonfacile.free.fr/python/unicode.html
# http://www.faqs.org/docs/diveintopython/kgp_unicode.html

## def setlocalencoding(encoding='cp850'):
##     if not hasattr(sys,'setdefaultencoding'):
##         return
##     import locale
##     loc = locale.getdefaultlocale()
##     if loc[1]:
##         print 'yes'
##         encoding=loc[1]
##     if sys.getdefaultencoding() != encoding:
##         #print "sys.setdefaultencoding(%s)" % repr(loc[1])
##         print "setting defaultencoding from", \
##               sys.getdefaultencoding(),"to",encoding
##         sys.setdefaultencoding(encoding)

def getlocalencoding():
    return locale.getdefaultlocale()[1]

def setlocalencoding():
    
    """Set system default encoding according to locale settings.

    This must be called during site.py because
    sys.setdefaultencoding() is no longer available.

      site.addsitedir(r"local\path\to\lino\trunk\src")
      from lino.customize import setlocalencoding
      setlocalencoding()

    
    """
    if sys.getdefaultencoding() != 'ascii': return
    if not hasattr(sys,'setdefaultencoding'): return
    loc=getlocalencoding()
    if loc and sys.getdefaultencoding() != loc:
        #print "setting defaultencoding from", \
        #      sys.getdefaultencoding(),"to",loc
        sys.setdefaultencoding(loc)


#print sys.getdefaultencoding()
#sys.stdout=rewriter(sys.stdout)
