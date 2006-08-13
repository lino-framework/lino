#coding: latin1

## Copyright 2005-2006 Luc Saffre.
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

def babel_message():

    s=u"""
Some sentences in different languages:
    
    Ännchen Müller machte große Augen.
    Cède à César les pâturages reçues.
    Tõesti, ma ütlen teile, see ei ole ükskõik.

Overview table with some accented characters:
    
        A E I O U   a e i o u            
    ¨   Ä \xcb Ï Ö Ü   ä ë ï ö ü
    ~   Ã . . Õ .   ã . . õ .            
    ´   Á É Í Ó Ú   á é í ó ú            
    `   À È Ì Ò Ù   à è ì ò ù
    ^   Â Ê Î Ô Û   â ê î ô û
    
"""
    
    try:
        out_encoding=repr(sys.stdout.encoding)
    except AttributeError:
        out_encoding="(undefined)"
        
    try:
        in_encoding=repr(sys.stdin.encoding)
    except AttributeError:
        in_encoding="(undefined)"

    s+="""
    
Some system settings related to encodings:

    locale.getdefaultlocale()   : %r
    sys.getdefaultencoding()    : %r
    sys.getfilesystemencoding() : %r
    sys.stdout.encoding : %s
    sys.stdin.encoding : %s
    
    """ % ( locale.getdefaultlocale(), 
    sys.getdefaultencoding(),
    sys.getfilesystemencoding(),
    out_encoding,
    in_encoding)

    return s
              

##     out.write("""
## Miscellaneous system settings:
## """)
##     l = sys.modules.keys()
##     l.sort()
    
##     out.write("modules: " + ' '.join(l)+"\n")

##     rpt = console.report()
##     rpt.addColumn(meth=lambda row: str(row[0]),
##                   label="key",
##                   width=12)
##     rpt.addColumn(meth=lambda row: repr(row[1]),
##                   label="value",
##                   width=40)
##     rpt.execute(d.items())    
    

class Diag(Application):
    name="Lino/diag"
    copyright="""\
Copyright (c) 2005-2006 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    url="http://lino.saffre-rumma.ee/diag.html"
    
    usage="usage: lino diag [options]"
    description="""\
writes some diagnostics about your computer.
""" 
    
    def run(self):
        if len(self.args) != 0:
            raise UsageError("no arguments please")
        #diag(sys.stdout)
        self.message(babel_message())


def main():
    Diag().main()
    
if __name__ == '__main__':
    main()
    
    
        

