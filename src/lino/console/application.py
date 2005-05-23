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

from lino import __version__, __author__

from lino.console.console import CLI
from lino.console import syscon

class UsageError(Exception):
    pass
class ApplicationError(Exception):
    pass

class Application(CLI):
    
    name = None
    years = None
    author = None
    
    """
    
    vocabulary:
    
    main() processes command-line arguments ("get the
    instructions") runs the application and returns a system error
    code (usually forwarded to sys.exit())

    run() expects that all instructions are known and performs the
    actual task.
    
    
    """
    def __init__(self,console=None):
        if console is None:
            console = syscon.getSystemConsole()
        self.console = console
        if self.name is not None:
            self.copyleft(name=self.name,
                             years=self.years,
                             author=self.author)

        
    def setupOptionParser(self,parser):
        self.console.setupOptionParser(parser)

    def applyOptions(self,options,args):
        self.options=options
        self.args=args

    def addProgramMenu(self,frm):
        m = frm.addMenu("&Programm")
        m.addItem(label="&Beenden",action=frm.close)
        m.addItem(label="Inf&o").setHandler(self.showAbout)
        #m.addItem(label="show &Console").setHandler(self.showConsole)
        return m


    def copyleft(self,name="Lino",
                 version=__version__,
                 years="2002-2005",
                 author=__author__):
        self.console.notice("""\
%s version %s.
Copyright (c) %s %s.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information.""" % (
            name, version, years, author))


    def showAbout(self):
        frm = self.form(label="About",doc=self.aboutString())
        frm.addOkButton()
        frm.show()
        
        
    def aboutString(self):
        s = self.name
        if self.version is not None:
            s += " version " + self.version
        if self.author is not None:
            s += "Copyright (c) %s %s." % self.years, self.author
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
        
        try:
            self.parse_args(argv)
            #options,args = p.parse_args(argv)
            #self.applyOptions(options,args)
            return self.run(self.console)
        
        except UsageError,e:
            p.print_help()
            return -1
        except ApplicationError,e:
            self.console.error(str(e))
            return -1

    def run(self,ui):
        raise NotImplementedError
        


