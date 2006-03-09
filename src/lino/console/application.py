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
import textwrap

import lino


class Application:
    
    name = None
    version=lino.__version__
    copyright=None
    url=None
    #years = None
    author=None
    usage = None
    description = None

    #toolkits="console"
    
    #_sessionFactory=Session
    
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
        #self._sessions = []
        #self.session=session
            
        self._ignoreExceptions = []
        self.toolkit=None
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
    
        
        
    
            
    def confirm(self,*args,**kw):
        self.toolkit.confirm(*args,**kw)
    def decide(self,*args,**kw):
        self.toolkit.decide(*args,**kw)
    def message(self,*args,**kw):
        self.toolkit.message(*args,**kw)
    def notice(self,*args,**kw):
        return self.toolkit.notice(*args,**kw)
    def debug(self,*args,**kw):
        return self.toolkit.debug(*args,**kw)
    def warning(self,*args,**kw):
        return self.toolkit.warning(*args,**kw)
    def verbose(self,*args,**kw):
        return self.toolkit.verbose(*args,**kw)
    def error(self,*args,**kw):
        return self.toolkit.error(*args,**kw)
    def critical(self,*args,**kw):
        return self.toolkit.critical(*args,**kw)
    def status(self,*args,**kw):
        return self.toolkit.status(*args,**kw)
    def logmessage(self,*args,**kw):
        return self.toolkit.logmessage(*args,**kw)
    def showReport(self,*args,**kw):
        return self.toolkit.showReport(*args,**kw)
    def loop(self,*args,**kw):
        return self.toolkit.loop(*args,**kw)

##     def showAbout(self):
##         self.message(self.app.aboutString(),title="About")
        
    def textprinter(self,*args,**kw):
        return self.toolkit.textprinter(self,*args,**kw)

    def setToolkit(self,toolkit):
        #assert isinstance(toolkit,AbstractToolkit),\
        #       repr(toolkit)+" is not a toolkit"
        self.toolkit = toolkit

    def exception(self,e,details=None):
        if e.__class__ in self._ignoreExceptions:
            return
        self.toolkit.showException(self,e,details)

