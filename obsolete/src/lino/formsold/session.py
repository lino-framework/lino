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

import time
import types

from lino.forms.base import AbstractToolkit
from lino.console.task import Task

class BaseSession:
    
    def __init__(self,toolkit):
        self.statusMessage=None
        self._ignoreExceptions = []
        self.setToolkit(toolkit)
        self._logfile = None
        self._logfile_stack = []
        
    def configure(self, logfile=None):
        if logfile is not None:
            if self._logfile is not None:
                self._logfile.close()
            self._logfile = open(logfile,"a")

    def beginLog(self,filename):
        self._logfile_stack.append(self._logfile)
        self._logfile = open(filename,"a")

    def endLog(self):
        assert len(self._logfile_stack) > 0
        if self._logfile is not None:
            self._logfile.close()
        self._logfile = self._logfile_stack.pop()
            
    #def writelog(self,msg):
    def logmessage(self,msg):
        if self._logfile:
            #t = strftime("%a %Y-%m-%d %H:%M:%S")
            t = time.strftime("%H:%M:%S")
            self._logfile.write(t+" "+msg+"\n")
            self._logfile.flush()

        
    def setupOptionParser(self,p):
        self.toolkit.setupOptionParser(p)
        def set_logfile(option, opt_str, value, parser,**kw):
            self.configure(logfile=value)
        p.add_option("-l", "--logfile",
                     help="log a report to FILE",
                     type="string",
                     dest="logFile",
                     action="callback",
                     callback=set_logfile)

        
    def setToolkit(self,toolkit):
        #assert toolkit is not None
        assert isinstance(toolkit,AbstractToolkit),\
               repr(toolkit)+" is not a toolkit"
        self.toolkit = toolkit
        #self.toolkit.openSession(self)
        #assert toolkit.__class__.__name__.endswith("Console"), \
        #       toolkit.__class__.__name__
        
    def close(self):
        assert len(self._logfile_stack) == 0
        if self._logfile:
            self._logfile.close()
        
##     def open(self):
##         self.toolkit.openSession(self)
        
##     def stopRunning(self,msg):
##         self.error(msg)
##         self.toolkit.stopRunning(self)
        
    
    def exception(self,e,details=None):
        if e.__class__ in self._ignoreExceptions:
            return
        self.toolkit.showException(self,e,details)

    def buildMessage(self,msg,*args,**kw):
        assert len(kw) == 0, "kwargs not yet implemented"
        if len(args) == 0:
            return msg
        return msg % args
    

    def status(self,msg=None,*args,**kw):
        if msg is not None:
            #ssert type(msg) == type('')
            assert msg.__class__ in (types.StringType,
                                     types.UnicodeType)
            msg=self.buildMessage(msg,*args,**kw)
        self.statusMessage=msg
        return self.toolkit.showStatus(self,msg)

    def setStatusMessage(self,msg):
        self.statusMessage=msg
    
        
    def debug(self,*args,**kw):
        return self.toolkit.debug(self,*args,**kw)
        
    def warning(self,*args,**kw):
        return self.toolkit.warning(self,*args,**kw)

    def verbose(self,*args,**kw):
        return self.toolkit.verbose(self,*args,**kw)

    def notice(self,*args,**kw):
        return self.toolkit.notice(self,*args,**kw)

    def error(self,*args,**kw):
        return self.toolkit.error(self,*args,**kw)
    
    def critical(self,*args,**kw):
        return self.toolkit.critical(self,*args,**kw)

    def showReport(self,*args,**kw):
        #print self.toolkit
        return self.toolkit.showReport(self,*args,**kw)

    def textprinter(self,*args,**kw):
        return self.toolkit.textprinter(self,*args,**kw)

    
    def message(self,*args,**kw):
        return self.toolkit.message(self,*args,**kw)
    def confirm(self,*args,**kw):
        return self.toolkit.confirm(self,*args,**kw)
    def decide(self,*args,**kw):
        return self.toolkit.decide(self,*args,**kw)

    def isInteractive(self):
        return self.toolkit.isInteractive()
        
    def isVerbose(self):
        return self.toolkit.isVerbose()
        
##     def runTask(self,task):
##         raise "replaced by runJob"

    #def runTask(self,task):
    #    task.run_in_session(self

    def run(self,sessfunc,*args,**kw):
        return sessfunc(self,*args,**kw)

    def loop(self,func,label,maxval=0,*args,**kw):
        task=Task(self,label,maxval)
        task.loop(func,*args,**kw)
        return task
    
    

class Session(BaseSession):
    
    def __init__(self,toolkit,app=None):
        #self._activeForm=None
        self.app=app
        #self._forms=[]
        BaseSession.__init__(self,toolkit)
        
        
    
    def form(self,*args,**kw):
        frm=self.toolkit.createForm(self,*args,**kw)
        #frm=self.toolkit.createForm(
        #    self,self._activeForm,*args,**kw)
        #self._forms.append(frm)
        return frm
    

    def showForm(self,ctrl):
        frm=self.form(label=ctrl.formLabel)
        ctrl.setupForm(frm)
        frm.show()
        
    def showAbout(self):
        frm = self.form(label="About",doc=self.app.aboutString())
        frm.addOkButton()
        frm.show()
        
##     def showForm(self,frm):
##         #assert frm in self._forms
##         self._activeForm=frm
##         #frm.show()

    def showMainForm(self):
        self.app.showMainForm(self)

    def setApplication(self,app):
        #assert self.app is None
        self.app = app
