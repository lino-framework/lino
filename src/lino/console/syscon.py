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

from lino.console.console import TtyConsole, Console
#from lino.console.session import Session


#class JobAborted(Exception):
#    pass

DEBUG=False

## class UsageError(Exception):
##     pass

## class ApplicationError(Exception):
##     pass





if sys.stdout.isatty():
    _syscon=TtyConsole(sys.stdout, sys.stderr)
else:
    _syscon=Console(sys.stdout, sys.stderr)
    



## def parse_args(argv=None): #,**kw):
##     p = OptionParser()
##     _session.setupOptionParser(p)
        
##     if argv is None:
##         argv = sys.argv[1:]

##     return p.parse_args(argv)

##     #options,args = p.parse_args(argv)
##     #_session.toolkit.applyOptions(options,args)
##     #return p
        

    
def getSystemConsole():
    return _syscon
    #return _session

def setSystemConsole(con):
    #setToolkit(toolkit)
    global _syscon
    _syscon=con

## def run(app,argv=None):
##     """
##     meant to be called
    
##     if __name__ == '__main__':
##         syscon.run(MyApplication)
                
##     but lino.runscript calls it with args=sys.argv[:2] (command-line
##     arguments are shifted by one)
        
##     """
##     #app=appClass(_syscon)
##     app.setToolkit(_syscon)
##     #_syscon.startApplication(app)
##     p = OptionParser(
##         usage=app.usage,
##         description=app.description)
    
##     _syscon.setupOptionParser(p)
##     app.setupOptionParser(p)

##     if argv is None:
##         argv = sys.argv[1:]

##     try:
##         options,args = p.parse_args(argv)
##         app.applyOptions(options,args)
##         if _syscon.isInteractive():
##             _syscon.writeln(app.aboutString())
##         return app.run()

##     except UsageError,e:
##         p.print_help()
##         return -1
##     except ApplicationError,e:
##         _syscon.error(str(e))
##         return -1

    
    
    
def shutdown():
    #if _syscon is not None:
    #    _syscon.shutdown()

    if _syscon is not None:
        _syscon.shutdown()

    if DEBUG:
        l = sys.modules.keys()
        l.sort()
        print "used modules: " + ' '.join(l)

## if hasattr(sys.stdout,"encoding") \
##       and sys.stdout.encoding is not None \
##       and sys.getdefaultencoding() != sys.stdout.encoding:
##     #print sys.stdout.encoding
##     sys.stdout = rewriter(sys.stdout)
##     #sys.stderr = rewriter(sys.stderr)


## _session=Session(console)

## g = globals()
    
## for funcname in (
##     'debug',
##     'notice','status','warning',
##     'verbose', 'error','critical',
##     #'job',
##     'isInteractive','isVerbose',
##     'exception',
##     #'message','confirm',
##     'showReport',
##     'textprinter',
##     #'run',
##     'loop'
##     ):
##     g[funcname] = getattr(_session,funcname)
        


#setSystemConsole(TtyConsole(sys.stdout.write, sys.stderr.write))

## def getToolkit():
##     #return _session.toolkit
##     return _syscon


## def setToolkit(con):
##     #_session.setToolkit(toolkit)
##     _syscon=con


atexit.register(shutdown)

