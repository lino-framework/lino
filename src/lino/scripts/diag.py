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


try:
    import win32file
except:
    win32file = None


from lino.ui import console

from lino.i18n import itr,_
itr("Start?",
   de="Arbeitsvorgang starten?",
   fr=u"Démarrer?")

def main(argv):
    console.copyleft(name="Lino/diag",
                     years='2005',
                     author='Luc Saffre')
    
    parser = console.getOptionParser(
        usage="usage: lino diag [options]",
        description="""\
writes some diagnostics about your computer.
""" )
    
##     parser.add_option("-s", "--simulate",
##                       help="""\
## simulate only, don't do it""",
##                       action="store_true",
##                       dest="simulate",
##                       default=False)
##     (options, args) = parser.parse_args(argv)

    (options, args) = parser.parse_args(argv)

    if len(args) != 0:
        parser.print_help() 
        sys.exit(-1)


    out = sys.stdout

    out.write("\nlocale.getdefaultlocale(): "
              + repr(locale.getdefaultlocale()))

    out.write("\ngetdefaultencoding() : "
              + sys.getdefaultencoding())
    out.write("\ngetfilesystemencoding() : "
              + sys.getfilesystemencoding())
    out.write("\nout.encoding : ")
    try:
        out.write(out.encoding)
    except AttributeError:
        out.write("(undefined)")
    out.write("\n")
    
    out.write(u"""

Do the following accented characters display correctly?

       A E I O U   a e i o u            
   ¨   Ä . Ï Ö Ü   ä ë ï ö ü
   ~   Ã . . Õ .   ã . . õ .            
   ´   Á É Í Ó Ú   á é í ó ú            
   `   À È Ì Ò Ù   à è ì ò ù
   ^   Â Ê Î Ô Û   â ê î ô û 

""")
    out.write("""
    Ännchen Müller machte große Augen.
    Cède à César les pâtes reçues.
    Tõesti, ma ütlen teile, see pole ükskõik.
    """)
 



if __name__ == '__main__':
    main(sys.argv[1:])
        

