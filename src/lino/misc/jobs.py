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
itr("Success",
    de="Vorgang erfolgreich beendet.")


class JobAborted(Exception):
    pass



class BaseJob:
    
    def __init__(self):
        pass
        #self.init(*args,**kw)
        
    #def __init__(self,ui,label=None,status=None,maxval=0):
    def init(self,ui,label=None,maxval=0):
        self.ui = ui
        self._label = label
        self.curval = 0
        self.maxval = maxval
        self.pc = None
        self._done = False
        
        self.ui.onJobInit(self)

    def setMaxValue(self,n):
        self.maxval = n

    def getStatus(self):
        return _("Working")
    
    def getLabel(self):
        return self._label 
    
##     def update(self,msg,n=1):
##         # shortcut to call both status() and inc()
##         self.status(msg)
##         self.inc(n)
        
    def increment(self,n=1):
        self.curval += n
        if self._done:
            return
        if self.maxval != 0:
            pc = int(100*self.curval/self.maxval)
            if pc == self.pc:
                return
            self.pc = pc
        self.ui.onJobIncremented(self)
        
    def done(self,msg=None):
        if msg is None:
            msg = _("Success")
        if not self._done:
            self._done = True
            #if msg is not None:
            #    self._status = msg
            self.pc = 100
            #self.ui.onJobIncremented(self)
            self.ui.onJobDone(self,msg)
            #if msg is not None and self._label is not None:
            #    msg = self._label+": "+msg
            
    def summary(self):
        #self.info("%d increments",self.curval)
        pass

    def abort(self,msg=None):
        if msg is None:
            msg = _("Aborted")
##         if msg is not None:
##             self._status = msg
        if not self._done:
            self._done = True
            self.ui.onJobAbort(self,msg)
            #self.pc = 100
            #self.onInc()
            #self.onDone(msg)

            
##     def onInc(self):
##         pass
    
##     def onInit(self):
##         if self._label is not None:
##             self.ui.info(self._label)
        
##     def onDone(self,msg):
##         if msg is None:
##             self.ui.status("")
##         else:
##             self.ui.status(msg)
        


    def warning(self,*args,**kw):
        self.ui.warning(*args,**kw)
        
    def message(self,*args,**kw):
        self.ui.message(*args,**kw)
        
    def info(self,*args,**kw):
        self.ui.info(*args,**kw)
        
    def verbose(self,*args,**kw):
        self.ui.verbose(*args,**kw)
        
    def error(self,*args,**kw):
        self.ui.error(*args,**kw)
        
    def debug(self,*args,**kw):
        self.ui.debug(*args,**kw)
        
    def status(self,*args,**kw):
        self.ui.status(*args,**kw)
    
        

## class PurzelConsoleJob(Job):
##     # for StatusConsole

##     purzelMann = "|/-\\"


##     def status(self,msg,*args,**kw):
##         msg = self.ui._buildMessage(msg,*args,**kw)
##         self._status = msg
##         self._display_job(job)
        





class Job(BaseJob):
    # this is not to override but for use by ui.job()
    def init(self,*args,**kw):
        self._status = _("Working")
        BaseJob.init(self,*args,**kw)

    def getStatus(self):
        return self._status

    def status(self,msg,*args,**kw):
        self._status = self.ui.buildMessage(msg,*args,**kw)



class Task(BaseJob):
    # must override
    def __init__(self):
        self.count_errors = 0
        self.count_warnings = 0
        BaseJob.__init__(self)


    def start(self):
        # must override
        raise NotImplementedError

    def getStatus(self):
        # may override
        s = _("%d warnings") % (self.count_warnings) 
        s += ". " + _("%d errors") % (self.count_errors) + "."
        return s

    def summary(self):
        # may override
        self.info(_("%d warnings"),self.count_warnings)
        self.info(_("%d errors"), self.count_errors)

        

    def run(self,ui,*args,**kw):
        self.init(ui,*args,**kw)
        try:
            self.start()
            self.done()
        except JobAborted,e:
            self.abort(str(e))
        except KeyboardInterrupt,e:
            self.abort()
            
        

    def error(self,*args,**kw):
        self.count_errors += 1
        Job.error(self,*args,**kw)

    def warning(self,msg):
        self.count_warnings += 1
        Job.warning(self,*args,**kw)
        


