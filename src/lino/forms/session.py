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

from lino.console.console import AbstractToolkit

class BaseSession:
    
    def __init__(self,toolkit):
        self.statusMessage=None
        self._ignoreExceptions = []
        self.setToolkit(toolkit)
        
        
    def setToolkit(self,toolkit):
        #assert toolkit is not None
        assert isinstance(toolkit,AbstractToolkit),\
               repr(toolkit)+" is not a toolkit"
        self.toolkit = toolkit
        #self.toolkit.openSession(self)
        #assert toolkit.__class__.__name__.endswith("Console"), \
        #       toolkit.__class__.__name__
        
    def close(self):
        #self.toolkit.closeSession(self)
        pass
        
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
            assert type(msg) == type('')
            msg=self.buildMessage(msg,*args,**kw)
        self.statusMessage=msg
        return self.toolkit.showStatus(self,self.statusMessage)

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

    
    
##     def job(self,*args,**kw):
##         #job=self.toolkit.progresserFactory(self,*args,**kw)
##         #job=self.toolkit.jobFactory(self,*args,**kw)
##         return self.toolkit.createJob(self,*args,**kw)

        
        
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
        
    def runTask(self,task):
        task.run_in_session(self)

class Session(BaseSession):
    
    def __init__(self,toolkit=None):
        self._activeForm=None
        self._forms=[]
        BaseSession.__init__(self,toolkit)
        
        
    
    def form(self,*args,**kw):
        frm=self.toolkit.createForm(
            self,self._activeForm,*args,**kw)
        self._forms.append(frm)
        return frm
    

    def show(self,frm):
        assert frm in self._forms
        self._activeForm=frm
        frm.show()

    def setActiveForm(self,frm):
        self._activeForm = frm

