## Copyright 2004-2005 Luc Saffre 

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
  
  python -c "from lino import runscript" %1 %2 %3 %4 %5 %6 %7 %8 %9



"""

import sys

#from lino.ui import console
from lino.misc.my_import import my_import

mod = my_import("lino.scripts." + sys.argv[1])
app = mod.consoleApplicationClass()

sys.exit(app.main(sys.argv[2:]))
