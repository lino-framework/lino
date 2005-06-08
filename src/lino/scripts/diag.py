#coding: latin1

## Copyright 2005 Luc Saffre.
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
import os
import locale

from lino.console.application import Application, UsageError

class Diag(Application):
    name="Lino/diag"
    years='2005'
    author='Luc Saffre'
    
    usage="usage: lino diag [options]"
    description="""\
writes some diagnostics about your computer.
""" 
    
    def run(self,sess):
        if len(self.args) != 0:
            raise UsageError("no arguments please")

        diag(sys.stdout)
        sess.message("")

def diag(out):    

    out.write("""
Some sentences in different languages:
    
    Ännchen Müller machte große Augen.
    Cède à César les pâtes reçues.
    Tõesti, ma ütlen teile, see pole ükskõik.

Overview table with all accented characters:
    
        A E I O U   a e i o u            
    ¨   Ä . Ï Ö Ü   ä ë ï ö ü
    ~   Ã . . Õ .   ã . . õ .            
    ´   Á É Í Ó Ú   á é í ó ú            
    `   À È Ì Ò Ù   à è ì ò ù
    ^   Â Ê Î Ô Û   â ê î ô û
""")
    
    out.write("""
Some system settings related to encodings:
""")    
    out.write("\n    locale.getdefaultlocale(): "
              + repr(locale.getdefaultlocale()))

    out.write("\n    getdefaultencoding() : "
              + sys.getdefaultencoding())
    out.write("\n    getfilesystemencoding() : "
              + sys.getfilesystemencoding())
    out.write("\n    sys.stdout.encoding : ")
    try:
        out.write(sys.stdout.encoding)
    except AttributeError:
        out.write("(undefined)")
    out.write("\n    sys.stdin.encoding : ")
    try:
        out.write(sys.stdin.encoding)
    except AttributeError:
        out.write("(undefined)")
    out.write("\n")

    out.write("""
Miscellaneous system settings:
""")
    l = sys.modules.keys()
    l.sort()
    
    out.write("modules: " + ' '.join(l)+"\n")

##     rpt = console.report()
##     rpt.addColumn(meth=lambda row: str(row[0]),
##                   label="key",
##                   width=12)
##     rpt.addColumn(meth=lambda row: repr(row[1]),
##                   label="value",
##                   width=40)
##     rpt.execute(d.items())    
    


consoleApplicationClass = Diag

if __name__ == '__main__':
    consoleApplicationClass().main() 
    
        

