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


from time import sleep

#from lino.console.console import TaskAborted
from lino.console.console import UserAborted, OperationFailed

if False:
    
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

def _(s):
    return s    


#class TaskSummary:
    
class Job:
    
    #summaryClass=TaskSummary

    def __init__(self):
        self.count_errors = 0
        self.count_warnings = 0
        
    def getStatus(self):
        # may override
        s = _("%d warnings") % (self.count_warnings) 
        s += ". " + _("%d errors") % (self.count_errors) + "."
        return s

    
    #def summary(self):
    #def lines(self):
    def getSummary(self):
        # may override
        return [
            _("%d warnings") % self.count_warnings,
            _("%d errors") % self.count_errors ]

    def getLabel(self):
        raise NotImplementedError

    def run(self,sess,*args,**kw):
        raise NotImplementedError

    
    
class Task:
    #maxval=0

    """

    This represents a progress bar in a GUI.  But it works also in a
    console UI.
    
    task.begin()
    task.increment()
    """
    
    def __init__(self,sess,label=None,maxval=0):
        self.session=sess
        if label is None:
            label=_("Working")
        self.label=label
        #sess.status(label)
        #if maxval is not None:
        #self.job=job
        #self._label=label
        self.maxval=maxval
        self._done=False
        self._abortRequested=False
        self.percentCompleted=0
        self.curval=0
        

    def loop(self,looper,*args,**kw):
        # called from BaseSession.run_task()
        
        self.session.toolkit.onTaskBegin(self)
        #okay=True
        #retval=None
        #success=False
        try:
            retval=looper(self,*args,**kw)
            self._done = True
            #success=True
            self.percentCompleted = 100
            self.session.toolkit.onTaskDone(self)
            return retval
            
        except UserAborted,e:
            # may raise during Toolkit.onTaskBreathe
            #assert e.task == self
            #self.abort()
            self._done = True
            self.session.toolkit.onTaskAbort(self)
            raise OperationFailed(str(e))
            
        except Exception,e:
            # some uncaught exception occured
            #self.abort()
            self._done = True
            self.session.toolkit.onTaskAbort(self)
            self.session.exception(e)
            #self=False
            raise OperationFailed(str(e))

        #if not success:
        #    raise OperationFailed(self)

        #if self.count_errors+self.count_warnings != 0:
        #    pass

        return self
        
##         if showSummary:
##             l=job.getSummary(self)
##             if len(l):
##                 sess.notice("\n".join(l))

        #self.session=None
        
    def requestAbort(self):
        self._abortRequested=True
            
##     def abortRequested(self):
##         return self._abortRequested


    def sleep(self,n=1.0):
        sleepStep=0.1
        while n > 0:
            self.breathe()
            n-=sleepStep
            if n == 0: return
            sleep(sleepStep)

        
    def breathe(self):
        self.session.toolkit.onTaskBreathe(self)
        if self._abortRequested:
            if self.session.confirm(
                _("Are you sure you want to abort?")):
                raise UserAborted()
            self._abortRequested=False
            self.session.toolkit.onTaskResume(self)


    def increment(self,n=1):
        self.curval += n
        if self._done: return
        if self.maxval != 0:
            pc = int(100*self.curval/self.maxval)
            if pc == self.percentCompleted:
                return
            self.percentCompleted = pc
        self.session.toolkit.onTaskIncrement(self)
        self.breathe()

    #def taskStatus(self,msg,*args,**kw):
    def status(self,msg,*args,**kw):
        if msg is not None:
            msg = self.session.buildMessage(msg,*args,**kw)
        self.session.setStatusMessage(msg)
        self.session.toolkit.onTaskStatus(self)
        self.breathe()
        
##     def done(self,msg=None,*args,**kw):
##         if self._done: return
##         if msg is not None:
##             msg = self.session.buildMessage(msg,*args,**kw)

    def abort(self,msg=None):
    #def taskAbort(self,msg=None):
        if msg is None:
            msg = _("Aborted")
        if not self._done:
            self._done = True
            self.session.toolkit.onTaskAbort(self,msg)
            
##     def error(self,*args,**kw):
##     #def taskError(self,*args,**kw):
##         self.count_errors += 1
##         self.session.error(*args,**kw)

##     def warning(self,*args,**kw):
##     #def taskWarning(self,*args,**kw):
##         self.count_warnings += 1
##         self.session.warning(*args,**kw)
        

##     def getMaxVal(self):
##         # may override
##         return 0

##     def begin(self,label=None,maxval=0):
##         self._label=label
##         self.maxval=maxval
        
    def setMaxVal(self,n):
        self.maxval=n

    #def setLabel(self,s):
    #    self.label=s

    #def setStatus(self):
    def showStatus(self):
        raise "eine Task soll keinen Job haben"
    
##     def showStatus(self):
##         self.session.setStatusMessage(self.job.getStatus())


        
    def query(self,*args,**kw):
        raise "Is this still used?"
        #return self.session.query(*args,**kw)

    #def getLabel(self):
    #    return self.job.getLabel(self)
    
    def getLabel(self):
        return self.label
    
##     def getLabel(self):
##         raise NotImplementedError

##     def run(self):
##         raise NotImplementedError

    

    

class BugDemo(Task):
    maxval=10
    label="Let's see what happens if an exception occurs..."
    
##     def getLabel(self):
##         return "Let's see what happens if an exception occurs..."

    def run(self):
        for i in range(self.maxval,0,-1):
            self.increment()
            self.status("%d seconds left",i)
            self.sleep(1)
            
        self.thisWontWork()
            

## def run_task(sess,meth,label,maxval,*args,**kw):
##     task=Task(sess,label,maxval)
##     return task.run_in_session(meth,*args,**kw)
##     #meth(self,*args,**kw)

