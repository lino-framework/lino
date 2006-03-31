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

## from lino.console.console import UserAborted, OperationFailed

import sys
from optparse import OptionParser
import textwrap

import lino

from lino.console import syscon
from lino.adamo.exceptions import UsageError, ApplicationError
from lino.console.task import Session

    
## class Session(UI):
##     """
    
## represents a user (usually a human sitting in front of a computer) who
## has chosen a toolkit and who runs some code (usually an application)

    
##     """
##     def __init__(self,user=None,pwd=None):
##         #UI.__init__(self,self.createToolkit())
##         #self.toolkit=None
##         self.user=user
##         self.pwd=pwd
##         self._ignoreExceptions = []
    


##     def abortRequested(self):
##         return self.toolkit.abortRequested()

##     def hasAuth(self,*args,**kw):
##         return True
            
##     def onLogin(self):
##         pass
    
##     def getUser(self):
##         return self.user

##     def login(self,user):
##         if self.user is not None:
##             self.logout()
##         self.user = user
##         self.onLogin()
        
##     def logout(self):
##         assert self.user is not None
##         self.user = None


##     def close(self):
##         pass

##     def exception(self,e,details=None):
##         if e.__class__ in self._ignoreExceptions:
##             return
##         self.toolkit.showException(self,e,details)

            


class Application(Session):
    
    name = None
    version=None # lino.__version__
    copyright=None
    url=None
    author=None
    usage = None
    description = None

    """
    
    vocabulary:
    
    main() processes command-line arguments ("get the
    instructions") runs the application and returns a system error
    code (usually forwarded to sys.exit())

    run() expects that all instructions are known and performs the
    actual task.
    
    
    """
    def __init__(self):
        #if session is None:
        #    session=syscon.getSystemConsole()
        #if self.name is None:
        #    self.name=self.__class__.__name__
        #self.toolkit=None 
        self.toolkit=syscon.getSystemConsole()
        #Session.__init__(self)
        #print "Application.__init__()", self    
        #self.setToolkit(toolkit)
        
    def setupApplication(self):
        pass
        

##     def createToolkit(self):
##         return syscon.getSystemConsole()

        
##     def parse_args(self,argv=None): #,**kw):
##         if self.author is not None:
##             self.copyleft(name=self.name,
##                           years=self.years,
##                           author=self.author)
##         p = OptionParser(
##             usage=self.usage,
##             description=self.description)
            
##         self.setupOptionParser(p)
        
##         if argv is None:
##             argv = sys.argv[1:]
        
##         options,args = p.parse_args(argv)
##         self.applyOptions(options,args)
##         return p
        
    def close(self):
        pass

    def __str__(self):
        if self.name is None:
            s = self.__class__.__name__
        else:
            s = self.name
            
        if self.version is not None:
            s += " version " + self.version
        return s
    
    def setupOptionParser(self,parser):
        pass

    def applyOptions(self,options,args):
        self.options=options
        self.args=args


    def aboutString(self):
        s = str(self)
        if self.author is not None:
            s += "\nAuthor: " +  self.author
        if self.copyright is not None:
            s += "\n"+self.copyright
            # "\nCopyright (c) %s %s." % (self.years, self.author)
            
        #from lino import __copyright__,  __url__
        #s += "\n\n" + __copyright__
        if self.url is not None:
            s += "\nHomepage: " + self.url
            
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
    
    def main(self,argv=None):
        """
        meant to be called

        if __name__ == '__main__':
            MyApplication().main()

        but lino.runscript calls it with argv=sys.argv[:2]
        (command-line arguments are shifted by one)

        """
        p = OptionParser(
            usage=self.usage,
            description=self.description)
        
        self.toolkit.setupOptionParser(p)
        self.setupOptionParser(p)

        if argv is None:
            argv = sys.argv[1:]

        try:
            options,args = p.parse_args(argv)
            self.applyOptions(options,args)
            #self.on_main()
            self.setupApplication()

            if self.name is not None and self.toolkit.isInteractive():
                self.notice(self.aboutString())
            
            return self.run()

        except UsageError,e:
            p.print_help()
            return -1
        except ApplicationError,e:
            self.error(str(e))
            return -1

    def run(self,*args,**kw):
        raise NotImplementedError

