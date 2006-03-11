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

class Session:
    """
    
represents a user (usually a human sitting in front of a computer) who
has chosen a toolkit and who runs some code (usually an application)

    
    """
    def __init__(self,user=None,pwd=None):
        #self.toolkit=None
        self.user=user
        self.pwd=pwd
        self._ignoreExceptions = []
        self.toolkit=self.getToolkit()
    
    def buildMessage(self,msg,*args,**kw):
        assert len(kw) == 0, "kwargs not yet implemented"
        if len(args) == 0:
            return msg
        return msg % args
    
    def isInteractive(self):
        return True

    def abortRequested(self):
        return self.toolkit.abortRequested()

    def loop(self,func,label,maxval=0,*args,**kw):
        "run func with a progressbar"
        task=Task(self,label,maxval)
        task.loop(func,*args,**kw)
        return task

    def hasAuth(self,*args,**kw):
        return True
            
    def onLogin(self):
        pass
    
    def getUser(self):
        return self.user

    def login(self,user):
        if self.user is not None:
            self.logout()
        self.user = user
        self.onLogin()
        
    def logout(self):
        assert self.user is not None
        self.user = None


    def close(self):
        pass

    def confirm(self,*args,**kw):
        self.toolkit.show_confirm(self,*args,**kw)
    def decide(self,*args,**kw):
        self.toolkit.show_decide(self,*args,**kw)
    def message(self,*args,**kw):
        self.toolkit.show_message(self,*args,**kw)
    def notice(self,*args,**kw):
        return self.toolkit.show_notice(self,*args,**kw)
    def debug(self,*args,**kw):
        return self.toolkit.show_debug(self,*args,**kw)
    def warning(self,*args,**kw):
        return self.toolkit.show_warning(self,*args,**kw)
    def verbose(self,*args,**kw):
        return self.toolkit.show_verbose(self,*args,**kw)
    def error(self,*args,**kw):
        return self.toolkit.show_error(self,*args,**kw)
##     def critical(self,*args,**kw):
##         return self.toolkit.show_critical(*args,**kw)
    def status(self,*args,**kw):
        return self.toolkit.show_status(self,*args,**kw)
    def logmessage(self,*args,**kw):
        return self.toolkit.logmessage(self,*args,**kw)
    def showReport(self,*args,**kw):
        return self.toolkit.showReport(self,*args,**kw)
    def textprinter(self,*args,**kw):
        return self.toolkit.textprinter(self,*args,**kw)
    
    def exception(self,e,details=None):
        if e.__class__ in self._ignoreExceptions:
            return
        self.toolkit.showException(self,e,details)


            


class Application(Session):
    
    name = None
    version=lino.__version__
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
        if self.name is None:
            self.name=self.__class__.__name__

        Session.__init__(self)
            
        #self.setToolkit(toolkit)
        

        
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
    
    def setupOptionParser(self,parser):
        pass

    def applyOptions(self,options,args):
        self.options=options
        self.args=args


    def aboutString(self):
        if self.name is None:
            s = self.__class__.__name__
        else:
            s = self.name
            
        if self.version is not None:
            s += " version " + self.version
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

    def getToolkit(self):
        return syscon.getSystemConsole()

##     def beginSession(self,*args,**kw):
##         # to be overridden by Adamo Applications
##         return Session(*args,**kw)

    def main(self,argv=None,*args):
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
            
            if self.isInteractive():
                self.notice(self.aboutString())
            return self.run()

        except UsageError,e:
            p.print_help()
            return -1
        except ApplicationError,e:
            sess.error(str(e))
            return -1

    def run(self,*args,**kw):
        raise NotImplementedError

