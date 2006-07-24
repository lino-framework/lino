#coding: latin1

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

## import sys

## import lino

## from lino.console import syscon

import sys
from optparse import OptionParser
import textwrap

import lino

from lino.adamo.exceptions import UserAborted, OperationFailed
from lino.adamo.exceptions import UsageError #, ApplicationError

from lino.console import syscon
from lino.console.task import Session

    
class Application(Session):
    
    version=None # lino.__version__
    copyright=None
    url=None
    author=None
    usage=None
    description = None

    """
    
    vocabulary:
    
    main() processes command-line arguments ("get the
    instructions") runs the application and returns a system error
    code (usually forwarded to sys.exit())

    run() expects that all instructions are known and performs the
    actual task.
    
    
    """
        
##     def setupApplication(self):
##         pass
        

    def close(self):
        pass

    def setupOptionParser(self,parser):
        pass

    def applyOptions(self,options,args):
        self.options=options
        self.args=args
        if self.name and self.isInteractive():
            self.notice(self.aboutString())

    def isInteractive(self):
        return self.toolkit.isInteractive()

    #def beforeRun(self):
            

    def aboutString(self):
        s = str(self)
        if self.version is not None:
            s += " version " + self.version
        #if self.description is not None:
        #    s += "\n" +  self.description.strip()
        if self.url is not None:
            s += "\nHomepage: " + self.url
        if self.author is not None:
            s += "\nAuthor: " +  self.author
        if self.copyright is not None:
            s += "\n"+self.copyright
            
        using = []
        using.append('Lino ' + lino.__version__)
        using.append("Python %d.%d.%d %s" % sys.version_info[0:4])

        if sys.modules.has_key('wx'):
            wx = sys.modules['wx']
            using.append("wxPython " + wx.__version__)
    
        if sys.modules.has_key('pysqlite2'):
            from pysqlite2.dbapi2 import version
            #sqlite = sys.modules['pysqlite2']
            using.append("PySQLLite " + version)
    
        if sys.modules.has_key('reportlab'):
            reportlab = sys.modules['reportlab']
            using.append("Reportlab PDF library "+reportlab.Version)

        if sys.modules.has_key('win32print'):
            win32print = sys.modules['win32print']
            using.append("Python Windows Extensions")
        
        if sys.modules.has_key('cherrypy'):
            cherrypy = sys.modules['cherrypy']
            using.append("CherryPy " + cherrypy.__version__)

        if sys.modules.has_key('PIL'):
            using.append("PIL")

        s += "\nUsing " + "\n".join(
            textwrap.wrap(", ".join(using),76))
        
        if False:
            s += "\n".join(
                textwrap.wrap(
                " ".join([ k for k in sys.modules.keys()
                           if not k.startswith("lino.")]),76))
            
        return s
    
        
            

##     def setToolkit(self,toolkit):
##         #assert isinstance(toolkit,AbstractToolkit),\
##         #       repr(toolkit)+" is not a toolkit"
##         self.toolkit = toolkit

##     def beginSession(self,*args,**kw):
##         # to be overridden by Adamo Applications
##         return Session(*args,**kw)

##     def on_main(self):
##         # GuiApplication overrides this to launch the GUI toolkit
##         pass
    
    #def main(self,argv=None):
    def main(self,*args,**kw):
        """Process command-line arguments and run the application.

        This is meant to be called

        if __name__ == '__main__':
            MyApplication().main()

        """
        self.toolkit=syscon.getSystemConsole()
        
        desc=self.description
        if desc is not None:
            desc=" ".join(desc.split())
##             paras=[]
##             for para in self.description.split('\n\n'):
##                 paras.append(" ".join(para.split()))
##             desc="\n\n".join(paras)
        
        p = OptionParser(
            usage=self.usage,
            description=desc)
        
        self.toolkit.setupOptionParser(p)
        self.setupOptionParser(p)

        #if argv is None:
        argv = sys.argv[1:]

        try:
            poptions,pargs = p.parse_args(argv)
            self.applyOptions(poptions,pargs)
            #self.beforeRun()
            #self.on_main()
            #self.setupApplication()
            return self.run(*args,**kw)

        except UsageError,e:
            self.error("Usage error: "+str(e))
            p.print_help()
            return -1
        except UserAborted,e:
            self.verbose(str(e))
            return -1
        except OperationFailed,e:
            self.error(str(e))
            return -2
##         except ApplicationError,e:
##             self.error(str(e))
##             return -1

    def run(self,*args,**kw):
        raise NotImplementedError

