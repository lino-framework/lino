#coding: latin1

## Copyright 2005 Luc Saffre 

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
#itr("Success",
#    de="Vorgang erfolgreich beendet")



class JobAborted(Exception):
    def __init__(self, job):
        self.job = job




class BaseJob:
    
    def init(self,sess,maxval=0):
        self.session = sess
        assert maxval is not None
        self.maxval = maxval
        self.curval = 0
        self.pc = None
        self._done = False
        self.session.toolkit.onJobInit(self)

    def setMaxValue(self,n):
        self.maxval = n

    def getStatus(self):
        return _("Working")
    
    def getLabel(self):
        raise NotImplementedError
    
    def confirmAbort(self):
        return self.session.confirm("Are you sure you want to abort?")
        
    def increment(self,n=1):
        self.curval += n
        if self._done:
            return
        if self.maxval != 0:
            pc = int(100*self.curval/self.maxval)
            if pc == self.pc:
                return
            self.pc = pc
        #self.ui.onJobIncremented(self)
        self.refresh()

    def refresh(self):
        self.session.toolkit.onJobRefresh(self)
        
    def done(self,msg=None,*args,**kw):
        if self._done: return
        if msg is not None:
            msg = self.session.buildMessage(msg,*args,**kw)
        self._done = True
        #if msg is not None:
        #    self._status = msg
        self.pc = 100
        #self.ui.onJobIncremented(self)
        self.session.toolkit.onJobDone(self,msg)
        #if msg is not None and self._label is not None:
        #    msg = self._label+": "+msg
            
    def summary(self):
        #self.notice("%d increments",self.curval)
        pass

    def abort(self,msg=None):
        if msg is None:
            msg = _("Aborted")
##         if msg is not None:
##             self._status = msg
        if not self._done:
            self._done = True
            self.session.toolkit.onJobAbort(self,msg)
            #self.pc = 100
            #self.onInc()
            #self.onDone(msg)
            
        #raise JobAborted(msg)

            

    def warning(self,*args,**kw):
        self.session.warning(*args,**kw)
        
    def message(self,*args,**kw):
        self.session.message(*args,**kw)
        
    def notice(self,*args,**kw):
        self.session.notice(*args,**kw)
        
    def verbose(self,*args,**kw):
        self.session.verbose(*args,**kw)
        
    def error(self,*args,**kw):
        self.session.error(*args,**kw)
        
    def debug(self,*args,**kw):
        self.session.debug(*args,**kw)
        
    def status(self,*args,**kw):
        self.session.status(*args,**kw)
    
        

## class PurzelConsoleJob(Job):
##     # for StatusConsole

##     purzelMann = "|/-\\"


##     def status(self,msg,*args,**kw):
##         msg = self.ui._buildMessage(msg,*args,**kw)
##         self._status = msg
##         self._display_job(job)
        


class Job(BaseJob):
    
    """user code should not override this but instanciate it using
    Session.job(). subclassed by lino.forms.wx"""
    
    def init(self,session,label=None,*args,**kw):
        self._label = label
        self._status = _("Working")
        BaseJob.init(self,session,*args,**kw)

    def getLabel(self):
        return self._label
    
    def getStatus(self):
        return self._status

    def status(self,msg,*args,**kw):
        self._status = self.session.buildMessage(msg,*args,**kw)
        self.refresh()

class TaskJob(BaseJob):
    def init(self,sess,task):
        self.getStatus = task.getStatus
        self.getLabel = task.getLabel
        BaseJob.init(self,sess,maxval=task.maxval)


class Task:

    def __init__(self,*args,**kw):
        self.configure(*args,**kw)


    def run(self,session,*args,**kw):
        # don't override
        #self.reconfigure(*args,**kw)
        self.job=TaskJob()
        self.job.init(session,self)
        #self.job = session.job(self.getLabel(),self.maxval)
        try:
            self.start()
            self.job.done()
        except JobAborted,e:
            # may raise during Toolkit.onJobRefresh
            assert e.job == self.job
            self.job.abort()
        except Exception,e:
            session.exception(e)
            self.job.abort()
##             # some uncaught exception occured
##             print e
##             self.job.abort(repr(e))
            
            
    def configure(self,maxval=0):
        # may override
        self.maxval=maxval
        self.count_errors = 0
        self.count_warnings = 0

##     def reconfigure(self,*args,**kw):
##         self.configure(*args,**kw)

    def start(self):
        raise NotImplementedError

    def getStatus(self):
        # may override
        s = _("%d warnings") % (self.count_warnings) 
        s += ". " + _("%d errors") % (self.count_errors) + "."
        return s


    def summary(self):
        # may override
        self.notice(_("%d warnings"),self.count_warnings)
        self.notice(_("%d errors"), self.count_errors)

        

    def error(self,*args,**kw):
        self.count_errors += 1
        self.job.error(*args,**kw)

    def warning(self,*args,**kw):
        self.count_warnings += 1
        self.job.warning(*args,**kw)
        
    def status(self,*args,**kw):
        self.job.status(*args,**kw)
        


