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


    diag(sys.stdout)

def diag(out):    

    out.write("""
Non-ASCII characters are handled differently and might fail to display
correctly depending on the context and your computer settings.

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
    if False:
        out.write("""
  Graphic "box characters":
""")
        for e in ('cp850',):
            fn = e+".txt"
            for ln in file(fn).readlines():
                out.write("    " + ln.decode(e))
    
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
    out.write("\n")
    



if __name__ == '__main__':
    main(sys.argv[1:])
        

