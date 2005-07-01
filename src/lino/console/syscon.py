#coding: latin1

## Copyright 2003-2005 Luc Saffre 

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
import atexit
import codecs

from lino.console.console import TtyConsole
from lino.forms.session import Session

# if frozen (with py2exe or McMillan), sys.setdefaultencoding() has
# not been deleted.  And site.py and sitecustomize.py haven't been
# executed.

if hasattr(sys,'setdefaultencoding'):

    import locale
    loc = locale.getdefaultlocale()
    if loc[1]:
        #print "sys.setdefaultencoding(%s)" % repr(loc[1])
        sys.setdefaultencoding(loc[1])
    


#class JobAborted(Exception):
#    pass





"""

A Console instance represents the console and encapsulates some
often-used things that have to do with the console.

"""

try:
    import sound
except ImportError,e:
    sound = False

from lino.misc.jobs import Job #, PurzelConsoleJob

_syscon = None


# rewriter() inspired by a snippet in Marc-André Lemburg's Python
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

def setSystemConsole(c):
    g = globals()
    
    for funcname in (
        'isInteractive','isVerbose',
        #'run',
        'set', #'parse_args',
        ):
        g[funcname] = getattr(c,funcname)
        
    sess = Session(c)
    for funcname in (
        'debug',
        'notice','status','warning',
        'verbose', 'error','critical',
        'job',
        'exception',
        'message','confirm',
        'showReport',
        'textprinter',
        ):
        g[funcname] = getattr(sess,funcname)
        
    g['_syscon'] = c
    g['_session'] = sess


def getSystemConsole():
    return _syscon


def shutdown():
    if _syscon is not None:
        _syscon.shutdown()


if hasattr(sys.stdout,"encoding") \
      and sys.getdefaultencoding() != sys.stdout.encoding:
    sys.stdout = rewriter(sys.stdout)
    #sys.stderr = rewriter(sys.stderr)


setSystemConsole(TtyConsole(sys.stdout.write, sys.stderr.write))

atexit.register(shutdown)

