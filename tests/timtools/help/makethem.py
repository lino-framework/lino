## Copyright 2004-2009 Luc Saffre

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

from lino.timtools import CONSOLE_TARGETS
from lino.console.syscon import confirm
from lino.tools.tsttools import trycmd

def main(*args,**kw):
    msg = "Gonna rebuild the following files:\n"
    msg += ", ".join(["%s.help.txt" % ct for ct in CONSOLE_TARGETS])
    if confirm(msg+"\nAre you sure?"):
        for ct in CONSOLE_TARGETS:
            cmd = "lino %s --help > %s.help.txt" % (ct,ct)
            print cmd
            trycmd(cmd)
    

if __name__ == '__main__': 
    main()
