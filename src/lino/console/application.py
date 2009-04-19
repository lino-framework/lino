#coding: latin1

## Copyright 2003-2009 Luc Saffre 

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

import os
import sys
from optparse import OptionParser
import textwrap

import lino

from lino.console import syscon
from lino.console.exceptions import UserAborted, OperationFailed, UsageError
from lino.console.task import Task

    
class Application(Task):

    """A Task that can be launched from a command line.

    User code will subclass Application, set class variables,
    implement a run() method and optinally override
    setupOptionParser().

    Usage examples

    docs/examples/appl1.py
    docs/examples/appl2.py

    """
    
    version = None 
    copyright = None
    url = None
    author = None
    usage = None
    description = None
    configfile = None
    configdefaults = {}

    """
    
    vocabulary:
    
    main() processes command-line arguments ("get the
    instructions") runs the application and returns a system error
    code (usually forwarded to sys.exit())

    run() expects that all instructions are known and performs the
    actual task.
    
    
    """
        
    def close(self):
        pass
    
    def setupOptionParser(self,p):
        self.toolkit.setupOptionParser(p)
        
        def set_lang(option, opt, value, parser):
            from lino import i18n
            i18n.setUserLang(value)
            
        p.add_option(
            "--lang",
            help="set user language to LANG",
            type="string",
            action="callback",
            callback=set_lang)
            
        if self.configfile is not None:
            p.add_option("--config",
                         help="""\
alternate configuration file instead of %s.""" % self.configfile,
                        action="store",
                        type="string",
                        dest="configfile",
                        metavar="FILE",
                        default=self.configfile)


    def applyOptions(self,options,args):
      
        """
        :attr:`Application.configfile` just specifies the default name. 
        If it is None, then there is no :cmd:`--config` option.
        If it is not None, then if has been set the default value for
        this option, so this is where we take the actual value to be
        used.
        """
        if self.configfile is not None:
            options._update_loose(self.configdefaults)
            if os.path.exists(options.configfile):
                self.verbose("Running configuration file %s", 
                  options.configfile)
                options.read_file(options.configfile,"loose")
                #execfile(options.configfile,self.configdefaults)
            else:
                self.verbose("Skip nonexisting configuration file %s",
                  options.configfile)
        self.options=options
        self.args=args

    def isInteractive(self):
        return self.toolkit.isInteractive()

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
        
        #~ if sys.modules.has_key('cherrypy'):
            #~ cherrypy = sys.modules['cherrypy']
            #~ using.append("CherryPy " + cherrypy.__version__)

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
    
    def start_running(self):
        self.toolkit.start_running(self)
        
    def stop_running(self):
        self.toolkit.stop_running()

    def get_description(self):
        return self.description


    def main(self,*args,**kw):
        """Process command-line arguments and run the application.

        """

        self.toolkit = syscon.getSystemConsole()
        syscon.setMainSession(self)
        
        desc = self.get_description()
        if desc is not None:
            desc=" ".join(desc.split())
        
        p = OptionParser(
            usage=self.usage,
            description=desc)
            
        self.setupOptionParser(p)

        argv = sys.argv[1:]
        
        try:
            poptions,pargs = p.parse_args(argv)
            self.applyOptions(poptions,pargs)
            self.start_running()
            ret=self.run(*args,**kw)
            self.stop_running()
            return ret

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

    def run(self,*args,**kw):
        pass

