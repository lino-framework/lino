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

## from lino.console.application import Application

## class RunPy(Application):

##     name="Lino runpy"
    
##     copyright="""\
## Copyright (c) 2005-2006 Luc Saffre.
## This software comes with ABSOLUTELY NO WARRANTY and is
## distributed under the terms of the GNU General Public License.
## See file COPYING.txt for more information."""
    
##     url="http://lino.saffre-rumma.ee/runpy.html"
    
##     usage="usage: runpy [options] PYFILE"
    
##     description="""\
## where PYFILE is a Python script to execute.
## """ 
    
##     def run(self):

##         for arg in self.args:
##             execfile(arg)


## #RunPy().main()

## ## # lino.runscript expects a name consoleApplicationClass
## ## consoleApplicationClass = Lino

## ## if __name__ == '__main__':
## ##     consoleApplicationClass().main()
    
## def main(*args,**kw):
##     RunPy().main(*args,**kw)

import sys

def main():
    #print sys.argv
    filename=sys.argv[1]
    del sys.argv[1]
    execfile(filename,{})

if __name__ == '__main__': main()
