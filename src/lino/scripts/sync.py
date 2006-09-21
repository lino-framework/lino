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

from lino.console.application import Application, \
     UsageError, UserAborted
from lino.tools.synchronizer import Synchronizer
from lino import __url__

class Sync(Application):

    name="Lino/sync"
    
    copyright="""\
Copyright (c) 2005-2006 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    
    url=__url__+"/sync.html"
    
    usage="usage: lino sync [options] SRC DEST"
    
    description="""\
where SRC and DEST are two directories to be synchronized.
""" 
    
    def setupOptionParser(self,parser):
        Application.setupOptionParser(self,parser)

##         parser.add_option(
##             "-s", "--simulate",
##             help="simulate only, don't do it",
##             action="store_true",
##             dest="simulate",
##             default=False)
        
        parser.add_option(
            "-u", "--unsafely",
            help="skip safety loop",
            action="store_false",
            dest="safely",
            default=True)
        
        parser.add_option(
            "-r", "--recurse",
            help="recurse into subdirs",
            action="store_true",
            dest="recurse",
            default=False)

        parser.add_option(
            "-p", "--progress",
            help="show progress bar",
            action="store_true",
            dest="showProgress",
            default=False)
    
    def run(self):

        job=Synchronizer()
        
        if len(self.args) == 2:
            job.addProject(
                self.args[0],self.args[1],self.options.recurse)

        
        elif len(self.args) == 1:
            #tasks=[]
            for ln in open(self.args[0]).readlines():
                ln=ln.strip()
                if len(ln):
                    if not ln.startswith("#"):
                        a=ln.split()
                        assert len(a) == 2
                        job.addProject(
                            a[0],a[1],self.options.recurse)
                        
        else:
            raise UsageError("needs 1 or 2 arguments")

        self.runtask(job,
                     showProgress=self.options.showProgress,
                     safely=self.options.safely)
                     

# Sync().main()

## if __name__ == '__main__':
##     consoleApplicationClass().main() # console,sys.argv[1:])
    
def main(*args,**kw):
    Sync().main(*args,**kw)

if __name__ == '__main__': main() 
