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



class JobAborted(Exception):
    pass


uimeths = ('warning', 'message','info','error', 'verbose')


class Task:
    def __init__(self):
        self._todo = []
        self.count_errors = 0
        self.count_warnings = 0

##     def schedule(self,m,*args,**kw):
##         self._todo.append( (m,args,kw) )

    def getLabel(self):
        return _("Working")
    
    def run(self,ui):
        #self.ui = ui
        self.job = ui.job(self.getLabel())
##         for m in uimeths:
##             setattr(self,m,getattr(self.job,m))
        try:
            self.start()
            self.job.done()
        except JobAborted,e:
            self.job.aborted()
            
##         while len(self._todo) > 0:
##             # self.job.inc()
##             m,args,kw = self._todo.pop(0)
##             m(*args,**kw)

##     def setMaxValue(self,n):
##         self.job.setMaxValue(n)

    def message(self,msg):
        self.job.message(msg)

    def info(self,msg):
        self.job.info(msg)

    def status(self,msg):
        self.job.status(msg)

    def verbose(self,msg):
        self.job.verbose(msg)
        
    def error(self,msg):
        self.count_errors += 1
        self.job.error(msg)

    def warning(self,msg):
        self.count_warnings += 1
        self.job.warning(msg)
        

    def start(self):
        raise NotImplementedError



class Job:
    
    def __init__(self,pb,status=None,maxval=None):
        self.pb = pb
        for m in uimeths:
            setattr(self,m,getattr(pb,m))
        self.curval = 0
        self.maxval = maxval
        self._done = False
        if status is None:
            status = _("Working")
        self.pc = None
        self.status(status)

    def setMaxValue(self,n):
        self.maxval = n
        
    def status(self,msg=""):
        self._status = msg
        self.pb.onStatus(self)

    def info(self,msg):
        self.pb.info(msg)
        self.pb.onInc(self)
        
    def update(self,msg,n=1):
        self._status = msg
        self.inc(n)
        
    def inc(self,n=1):
        self.curval += n
        if self._done:
            return
        if self.maxval:
            pc = int(100*self.curval/self.maxval)
            if pc == self.pc:
                return
            self.pc = pc
        self.pb.onInc(self)
        
    def done(self,msg=None):
        if msg:
            self._status = msg
        if not self._done:
            self._done = True
            self.pc = 100
            self.pb.onInc(self)
            self.pb.onDone(self)

##     def __str__(self):
##         return self._title

            




class ProgressBar:

    """
    
    originally inspired by
    http://docs.python.org/mac/progressbar-objects.html
    
    and
    http://search.cpan.org/src/FLUFFY/Term-ProgressBar-2.06-r1/README
    
    and
    http://www.lpthe.jussieu.fr/~zeitlin/wxWindows/docs/wxwin_wxprogressdialog.html

    
    """
    def __init__(self,ui,label=None):
        
        self.ui = ui
        self._label = label
        self._jobs = []
        self.onInit()
        #self.status(status)

    def warning(self,msg):
        self.ui.warning(msg)
        
    def message(self,msg):
        self.ui.message(msg)
        
    def info(self,msg):
        self.ui.info(msg)
        
    def verbose(self,msg):
        self.ui.verbose(msg)
        
    def error(self,msg):
        self.ui.error(msg)
        
    def addJob(self,*args,**kw):
        job = Job(self,*args,**kw)
        self._jobs.append(job)
        self.onJob(job)
        return job
        
    def onInit(self):
        pass
    
    def onJob(self,job):
        self.onStatus(job)
    
    def onStatus(self,job):
        pass
    
    def onInc(self,job):
        pass

    def onDone(self,job):
        assert self._jobs[-1] == job, "%s != %s" % (
            str(job), str(self._jobs[-1]))
        del self._jobs[-1]
    

            
