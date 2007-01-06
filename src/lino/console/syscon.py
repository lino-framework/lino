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
import atexit

DEBUG=False

_syscon=None
_main=None

def getSystemConsole():
    global _syscon
    if _syscon is None:
        from lino.console.console import TtyConsole, Console
        if hasattr(sys.stdout,'isatty') and sys.stdout.isatty():
            _syscon=TtyConsole(sys.stdout, sys.stderr)
        else:
            _syscon=Console(sys.stdout, sys.stderr)
    return _syscon

def setSystemConsole(con):
    global _syscon
    _syscon=con


def setMainSession(sess):
    global _main
    _main=sess

def getMainSession():
    global _main
    if _main is None:
        from lino.console.application import Application
        _main=Application()
        _main.main()
    return _main
        
    

def shutdown():
    if _syscon is not None:
        _syscon.shutdown()

    if DEBUG:
        l = sys.modules.keys()
        l.sort()
        print "used modules: " + ' '.join(l)

atexit.register(shutdown)

def confirm(*args,**kw):
    return getMainSession().confirm(*args,**kw)
