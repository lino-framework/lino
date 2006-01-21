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

import sys
from optparse import OptionParser
import textwrap

import lino

from lino.console import syscon


class UsageError(Exception):
    pass
class ApplicationError(Exception):
    pass


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
    def __init__(self): #,console=None):
        if self.name is None:
            self.name=self.__class__.__name__
        self._sessions = []
            

        
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
        

    
    def setupOptionParser(self,parser):
        pass

    def applyOptions(self,options,args):
        self.options=options
        self.args=args

    def addProgramMenu(self,sess,frm):
        m = frm.addMenu("system","&Programm")
        m.addItem("logout",label="&Beenden",action=frm.close)
        m.addItem("about",label="Inf&o").setHandler(sess.showAbout)

        def buggy(task):
            for i in range(10,0,-1):
                task.increment()
                sess.status("%d seconds left",i)
                task.sleep(1)

            thisWontWork()
        
        m.addItem("bug",label="&Bug demo").setHandler(
            sess.loop,buggy,"Bug demo")
        #m.addItem(label="show &Console").setHandler(self.showConsole)
        return m


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
            
        credits = []
        credits.append("Python %d.%d.%d %s" % sys.version_info[0:4])
        credits.append('Lino ' + lino.__version__)

        if sys.modules.has_key('wx'):
            wx = sys.modules['wx']
            credits.append("wxPython " + wx.__version__)
    
        if sys.modules.has_key('pysqlite2'):
            from pysqlite2.dbapi2 import version
            #sqlite = sys.modules['pysqlite2']
            credits.append("PySQLLite " + version)
    
        if sys.modules.has_key('reportlab'):
            reportlab = sys.modules['reportlab']
            credits.append("Reportlab PDF library "+reportlab.Version)

        if sys.modules.has_key('win32print'):
            win32print = sys.modules['win32print']
            credits.append("Python Windows Extensions")
        
        if sys.modules.has_key('cherrypy'):
            cherrypy = sys.modules['cherrypy']
            credits.append("CherryPy " + cherrypy.__version__)

        if sys.modules.has_key('PIL'):
            credits.append("PIL")

        s += "\nCredits: " + "\n".join(
            textwrap.wrap(", ".join(credits),76))
        
        if False:
            s += "\n".join(
                textwrap.wrap(
                " ".join([ k for k in sys.modules.keys()
                           if not k.startswith("lino.")]),76))
            
        return s
    
        
        
    def main(self,argv=None):
        """
        meant to be called
        
            if __name__ == '__main__':
                MyApplication().main()
                
        but lino.runscript calls it with args=sys.argv[:2] (command-line
        arguments are shifted by one)
        
        """

##                 name=self.name,
##                 version=self.version,
            
        p = OptionParser(
            usage=self.usage,
            description=self.description)

        sess=syscon._session
        
        sess.setApplication(self)
        
        #sess.toolkit.setupOptionParser(p)
        sess.setupOptionParser(p)
        
        self.setupOptionParser(p)
        
        if argv is None:
            argv = sys.argv[1:]
        
        try:
            
            options,args = p.parse_args(argv)
            self.applyOptions(options,args)
            if syscon.isInteractive():
                syscon.notice(self.aboutString())
                #if self.copyright is not None:
                #    syscon.notice(self.copyright)
            return self.run(sess)
        
        except UsageError,e:
            p.print_help()
            return -1
        except ApplicationError,e:
            syscon.error(str(e))
            return -1

    def run(self,sess):
        self.showMainForm(sess)
        
    def showMainForm(self,sess):
        pass


    def addSession(self,sess):
        #sess = self._sessionFactory(self,toolkit,**kw)
        #sess = Session(toolkit)
        self._sessions.append(sess)
        #self.onOpenSession(sess)
        #return sess

    def removeSession(self,sess):
        #self.onCloseSession(sess)
        self._sessions.remove(sess)

    def onOpenSession(self,sess):
        self.showMainForm(sess)

    def onCloseSession(self,sess):
        pass


    def shutdown(self):
        for sess in self._sessions:
            #syscon.debug("Killing session %r",sess)
            sess.close()
        
        
