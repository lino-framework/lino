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


from time import sleep

#from lino.console.console import TaskAborted
from lino.adamo.exceptions import UserAborted

if False:
    
    from lino.i18n import itr,_

    itr("Working",
       de=u"Arbeitsvorgang läuft",
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
    
## class Job:
    
##     #summaryClass=TaskSummary

##     def __init__(self):
##         self.count_errors = 0
##         self.count_warnings = 0
        
##     def getStatus(self):
##         # may override
##         s = _("%d warnings") % (self.count_warnings) 
##         s += ". " + _("%d errors") % (self.count_errors) + "."
##         return s

    
##     #def summary(self):
##     #def lines(self):
##     def getSummary(self):
##         # may override
##         return [
##             _("%d warnings") % self.count_warnings,
##             _("%d errors") % self.count_errors ]

##     def getLabel(self):
##         raise NotImplementedError

##     def run(self,sess,*args,**kw):
##         raise NotImplementedError


class UI:
    #def __init__(self,toolkit):
    #    self.toolkit=toolkit
        
    def buildMessage(self,msg,*args,**kw):
        assert len(kw) == 0, "kwargs not yet implemented"
        if len(args) == 0:
            return msg
        return msg % args
    
    def isInteractive(self):
        return True

    
    def loop(self,func,label,maxval=0,*args,**kw):
        "run func with a progressbar"
        if maxval == 0:
            task=Task(label)
        else:
            task=Progresser(label,maxval)
        task.toolkit=self.toolkit
        func(task,*args,**kw)
        #task.runfrom(self,*args,**kw)
        #task=Task(self,label,maxval)
        #task.loop(func,*args,**kw)
        return task

    def confirm(self,*args,**kw):
        return self.toolkit.show_confirm(self,*args,**kw)
    def decide(self,*args,**kw):
        return self.toolkit.show_decide(self,*args,**kw)
    def message(self,*args,**kw):
        return self.toolkit.show_message(self,*args,**kw)
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
    def showForm(self,*args,**kw):
        self.toolkit.show_form(self,*args,**kw)
    def showReport(self,*args,**kw):
        return self.toolkit.show_report(*args,**kw)
    def textprinter(self,*args,**kw):
        return self.toolkit.textprinter(self,*args,**kw)
    
##     def runfrom(self,ui,*args,**kw):
##         assert ui.toolkit is not None
##         self.toolkit=ui.toolkit
##         try:
##             self.run(*args,**kw)
##         except UserAborted,e:
##             bla

    def breathe(self):
        return self.toolkit.on_breathe(self)

    def runfrom(self,ui,*args,**kw):
        self.toolkit=ui.toolkit
        return self.run(*args,**kw)
        


    
    
class Task(UI):
    title=None
    label="Working"
    percentCompleted=0
    def __init__(self,label=None):
        #self._abortRequested=False
        if label is not None:
            self.label=label

    def requestAbort(self):
        if self.confirm( _("Are you sure you want to abort?"),
                         default=False):
            raise UserAborted()
        #self._abortRequested=False
        self.toolkit.onTaskResume(self)
        #self._abortRequested=True

    def getStatusLine(self):
        # may override but caution: called frequently
        return self.label
    
    def status(self,msg,*args,**kw):
        if msg is None:
            msg=''
        else:
            msg=self.buildMessage(msg,*args,**kw)
        self.label=msg
        return self.toolkit.show_status(self,msg)

    def getTitle(self):
        if self.title is None:
            return self.__class__.__name__
        return self.title

class Looper(Task):
    
    def __init__(self,f,label=None):
        Task.__init__(self,label)
        self.func=func
        
    def run(self,*args,**kw):
        return self.func(*args,**kw)
    
class Progresser(Task):

    """

    This represents a progress bar or some other progress indicator.
    
    task.begin()
    task.increment()
    """
    maxval=0
    
    def __init__(self,label=None,maxval=None):
        Task.__init__(self,label)
        if maxval is not None:
            self.maxval=maxval
        #self._done=False
        self.percentCompleted=0
        self.curval=0


    def runfrom(self,ui,*args,**kw):
        self.toolkit=ui.toolkit
        
        self.toolkit.onTaskBegin(self)
        #okay=True
        #retval=None
        #success=False
        try:
            retval=self.run(*args,**kw)
            #self._done = True
            #success=True
            self.percentCompleted = 100
            self.toolkit.onTaskDone(self)
            return retval
            
##         except UserAborted,e:
##             # may raise during Toolkit.onTaskBreathe
##             #assert e.task == self
##             #self.abort()
##             #self._done = True
##             self.toolkit.onTaskAbort(self)
##             raise #OperationFailed(str(e))
            
        except Exception,e:
            # some uncaught exception occured
            #self.abort()
            #self._done = True
            self.toolkit.onTaskAbort(self)
            #self.session.exception(e)
            #self=False
            raise #OperationFailed(str(e))

        #if not success:
        #    raise OperationFailed(self)

        #if self.count_errors+self.count_warnings != 0:
        #    pass

        #return self
        
##         if showSummary:
##             l=job.getSummary(self)
##             if len(l):
##                 sess.notice("\n".join(l))

        #self.session=None
        
            
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
        self.toolkit.on_breathe(self)
        #self.toolkit.onTaskBreathe(self)
##         if self._abortRequested:
##             if self.confirm(_("Are you sure you want to abort?")):
##                 raise UserAborted()
##             self._abortRequested=False
##             self.toolkit.onTaskResume(self)


    def increment(self,n=1):
        self.curval += n
        #if self._done: return
        if self.maxval != 0:
            pc = int(100*self.curval/self.maxval)
            if pc == self.percentCompleted:
                return
            self.percentCompleted = pc
        self.toolkit.onTaskIncrement(self)
        #self.breathe()

##     def status(self,msg,*args,**kw):
##         #self.session.status(msg,*args,**kw)
##         #self.breathe()
##         raise """\
## please replace "task.status()"
## with task.toolkit.status() and/or task.breathe()
## """
    
##     def status(self,msg,*args,**kw):
##         if msg is not None:
##             msg = self.session.buildMessage(msg,*args,**kw)
##         self.session.setStatusMessage(msg)
##         self.session.toolkit.onTaskStatus(self)
##         self.breathe()
        
##     def done(self,msg=None,*args,**kw):
##         if self._done: return
##         if msg is not None:
##             msg = self.session.buildMessage(msg,*args,**kw)

##     def abort(self,msg=None):
##         if msg is None:
##             msg = _("Aborted")
##         if not self._done:
##             self._done = True
##             self.toolkit.onTaskAbort(self,msg)
            
##     def error(self,*args,**kw):
##     #def taskError(self,*args,**kw):
##         self.count_errors += 1
##         self.session.error(*args,**kw)

##     def warning(self,*args,**kw):
##     #def taskWarning(self,*args,**kw):
##         self.count_warnings += 1
##         self.session.warning(*args,**kw)
        

##    def getMaxVal(self):
##        # may override
##        return 0

##     def begin(self,label=None,maxval=0):
##         self._label=label
##         self.maxval=maxval
        
    def setMaxVal(self,n):
        self.maxval=n

    #def setLabel(self,s):
    #    self.label=s

    #def setStatus(self):
##     def showStatus(self):
##         raise "eine Task soll keinen Job haben"
    
##     def showStatus(self):
##         self.session.setStatusMessage(self.job.getStatus())


        
##     def query(self,*args,**kw):
##         raise "Is this still used?"
        #return self.session.query(*args,**kw)

    #def getLabel(self):
    #    return self.job.getLabel(self)
    
##     def getLabel(self):
##         raise NotImplementedError

##     def run(self):
##         raise NotImplementedError

    

    

class BugDemo(Progresser):
    title="&Bug demo"
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

