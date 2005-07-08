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


from lino.i18n import itr,_

itr("Working",
   de="Arbeitsvorgang läuft",
   fr="Travail en cours")
itr("%d warnings",
    de="%d Warnungen",
    fr="%d avertissements")
itr("%d errors" ,
    de="%d Fehler",
    fr="%d erreurs")
itr("Aborted",
    de="Vorgang abgebrochen")
itr("Are you sure you want to abort?",
    de="Arbeitsvorgang abbrechen?",
    fr="Interrompre le travail en cours?")

class TaskAborted(Exception):
    def __init__(self, task):
        self.task = task

class Task:

    def __init__(self):
        self.session=None
        self.percentCompleted=None
        self.curval=0
        self.maxval=0
        self.count_errors = 0
        self.count_warnings = 0
        self._done = False


    def run_in_session(self,sess):
        # don't override. Called by Session.runTask()
        assert self.session is None
        self.session=sess
        self.maxval=self.getMaxVal()
        self.percentCompleted=0
        
        self.session.toolkit.onTaskBegin(self)
        try:
            self.run()
            self.done()
        except TaskAborted,e:
            # may raise during Toolkit.onTaskBreathe
            assert e.task == self
            self.abort()
        except Exception,e:
            # some uncaught exception occured
            self.session.exception(e)
            self.abort()
        

    def increment(self,n=1):
        self.curval += n
        if self._done:
            return
        if self.maxval != 0:
            pc = int(100*self.curval/self.maxval)
            if pc == self.percentCompleted:
                return
            self.percentCompleted = pc
        self.session.toolkit.onTaskIncrement(self)
        self.breathe()

    def breathe(self):
        if self.session.toolkit.abortRequested():
            if self.session.confirm(
                _("Are you sure you want to abort?")):
                raise TaskAborted(self)
            self.session.toolkit.onTaskResume(self)
        self.session.toolkit.onTaskBreathe(self)

    def done(self,msg=None,*args,**kw):
        if self._done: return
        if msg is not None:
            msg = self.session.buildMessage(msg,*args,**kw)
        self._done = True
        self.percentCompleted = 100
        self.session.toolkit.onTaskDone(self,msg)

    def abort(self,msg=None):
        if msg is None:
            msg = _("Aborted")
        if not self._done:
            self._done = True
            self.session.toolkit.onTaskAbort(self,msg)
            
    def error(self,*args,**kw):
        self.count_errors += 1
        self.session.error(*args,**kw)

    def warning(self,*args,**kw):
        self.count_warnings += 1
        self.session.warning(*args,**kw)
        

    def getMaxVal(self):
        # may override
        return 0

    def getStatus(self):
        # may override
        s = _("%d warnings") % (self.count_warnings) 
        s += ". " + _("%d errors") % (self.count_errors) + "."
        return s


    def summary(self):
        # may override
        self.session.notice(_("%d warnings"),self.count_warnings)
        self.session.notice(_("%d errors"), self.count_errors)

        
    def run(self):
        raise NotImplementedError

    

class BugDemo(Task):

##     def __init__(self):
##         Task.__init__(self)
        
    def getMaxVal(self):
        return 10
    
    def run(self):
        for i in range(self.getMaxVal(),0,-1):
            self.session.status("%d seconds left",i)
            sleep(1)
            
        self.thisWontWork()
            
    def getLabel(self):
        return "Let's see what happens if an exception occurs..."


