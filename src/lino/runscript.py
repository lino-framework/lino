## Copyright 2004-2006 Luc Saffre 

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

"""

This is a wrapper to the Lino scripts. Simply importing this module
examines the command-line arguments and call the appropriate script.

The auto-generated file lino.bat uses this wrapper


  python -c "from lino import runscript" %*

  (or)
  
  python -c "from lino import runscript" %1 %2 %3 %4 %5 %6 %7 %8 %9



"""

import sys

#from lino import scripts
#from lino.console import syscon
from lino.misc.my_import import my_import


def usage():
##     import os
    import lino
    
    print "Lino", lino.__version__
    print lino.__copyright__
    print "usage: lino COMMAND [...]"
    print "where COMMAND is one of:", ", ".join(scripts.__all__)
    
##     for fn in os.listdir(scripts.__path__):
##         if fn.endswith('.py'):
##             modname=fn[:-2]
##             mod = my_import("lino.scripts." + modname)
##             if mod.hasattr('consoleApplicationClass'):
##                 print modname

                
            
            


if len(sys.argv) <= 1:
    usage()
    sys.exit(-1)

## if not sys.argv[1] in scripts.__all__:
##     #usage()
##     print "error: unknown command '%s'" % sys.argv[1]
##     sys.exit(-1)

scriptName=sys.argv[1]
del sys.argv[1]
try:
    my_import("lino.scripts." + scriptName)
except ImportError,e:
    print "error: unknown lino script '%s'" % scriptName
    sys.exit(-1)

#mod = my_import("lino.scripts." + sys.argv[1])
#sys.exit(mod.consoleApplicationClass().main(sys.argv[2:]))
