#coding: latin1

## Copyright 2003-2005 Luc Saffre 

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

from lino import __version__, __author__

#from lino.console.console import CLI
from lino.console import syscon

#from lino.forms.session import Session


class UsageError(Exception):
    pass
class ApplicationError(Exception):
    pass



from lino.misc.jobs import Task
from time import sleep

class BugDemo(Task):

    def __init__(self,maxval=10):
        Task.__init__(self,maxval=10)
    
    def start(self):
        for i in range(self.maxval,0,-1):
            self.status("%d seconds left",i)
            sleep(1)
            
        self.thisWontWork()
            
    def getLabel(self):
        return "Let's see what happens if an exception occurs..."



#class Application(CLI):
class Application:
    
    name = None
    years = None
    author=None
    version=__version__
    usage = None
    description = None

    toolkits="console"
    
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
            

        
    def parse_args(self,argv=None): #,**kw):
        if self.author is not None:
            self.copyleft(name=self.name,
                          years=self.years,
                          author=self.author)
        p = OptionParser(
            usage=self.usage,
            description=self.description)
            
        self.setupOptionParser(p)
        
        if argv is None:
            argv = sys.argv[1:]
        
        options,args = p.parse_args(argv)
        self.applyOptions(options,args)
        return p
        

    
    def setupOptionParser(self,parser):
        pass

    def applyOptions(self,options,args):
        self.options=options
        self.args=args

    def addProgramMenu(self,sess,frm):
        m = frm.addMenu("system","&Programm")
        m.addItem("logout",label="&Beenden",action=frm.close)
        m.addItem("about",label="Inf&o").setHandler(sess.showAbout)
        m.addItem("bug",label="&Bug demo").setHandler(BugDemo().run,
                                                      sess)
        #m.addItem(label="show &Console").setHandler(self.showConsole)
        return m


    def copyleft(self,name="Lino",
                 version=__version__,
                 years="2002-2005",
                 author=__author__):
        syscon.notice("""\
%s version %s.
Copyright (c) %s %s.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information.""" % (
            name, version, years, author))

        
    def aboutString(self):
        s = self.name
        if self.version is not None:
            s += " version " + self.version
        if self.author is not None:
            s += "\nCopyright (c) %s %s." % (self.years, self.author)
        from lino import __copyright__,  __url__
        s += "\n\n" + __copyright__
        s += "\n\nHomepage:\n" + __url__
        s += "\n\nCredits:\n"
        s += "Python %d.%d.%d %s\n" % sys.version_info[0:4]

        if sys.modules.has_key('wx'):
            wx = sys.modules['wx']
            s += "wxPython " + wx.__version__ + "\n"
    
        if sys.modules.has_key('sqlite'):
            sqlite = sys.modules['sqlite']
            s += "PySQLLite " + sqlite.version + "\n"
    
        if sys.modules.has_key('reportlab'):
            reportlab = sys.modules['reportlab']
            s += "The Reportlab PDF generation library " + \
                           reportlab.Version + "\n"

        if sys.modules.has_key('win32print'):
            win32print = sys.modules['win32print']
            s += "Python Windows Extensions " + "\n"
        
        return s
    
        
        
    def main(self,argv=None):
        """
        meant to be called
        
            if __name__ == '__main__':
                MyApplication().main()
                
        but lino.runscript calls it with args=sys.argv[:2] (command-line
        arguments are shifted by one)
        
        """

##         p = OptionParser(
##             usage=self.usage,
##             description=self.description)
            
##         self.setupOptionParser(p)
        
        #toolkit=syscon.getSystemConsole()
        try:
            #toolkit=syscon.getSystemConsole()
            #toolkit.addApplication(self)
            #sess = Session(toolkit)
            #self.openSession(sess)
            #raise "... was wenn Schema mehr als eine db hat?"
            #self.startup(toolkit)
            #syscon.setSystemSession(self._sessions[0])
            #syscon.setSystemSession(sess)
            p=self.parse_args(argv)
            return self.run(syscon._session)
        
        except UsageError,e:
            p.print_help()
            return -1
        except ApplicationError,e:
            syscon.error(str(e))
            return -1

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
        
    def run(self,sess):
        raise NotImplementedError
    
