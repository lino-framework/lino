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


"""
    
originally inspired by
    http://docs.python.org/mac/progressbar-objects.html
    
and
    http://search.cpan.org/src/FLUFFY/Term-ProgressBar-2.06-r1/README
    
and
    http://www.lpthe.jussieu.fr/~zeitlin/wxWindows/docs/wxwin_wxprogressdialog.html


20050307 : decided to convert Console() for using logging module
  http://www.python.org/doc/current/lib/module-logging.html

The logging module misses a level for normal messages that are not
warnings.  (syslog calls them "notice", I called them message) "normal
but significant condition"

debug : only visible if -vv (very verbose)         10
info  : only visible if -v (verbose)               20
notice : normally visible (suppressed if -q)       
warning : normally visible (suppressed if -qq)     30
error : normally visible (suppressed if -qqq)      40
critical : never suppressed                        50

application example for sync.py:

in user code i must :
- replace info with notice
- replace verbose with info

logging.addLevelName(25,"NOTICE")


OTOH:

- the logging module is very heavy for DEBUG and INFO. These messages
  should go simply to stdout (or not). Why keep their timestamp and
  source line number for example?
  
  Idea: Console() never logs the "verbose" messages. In fact I keep my
  current Console concept but take their args/kw system.

- there is no solution formy status() method

  status() : displays a message that will be overwritten by the next
  message. If this is not possible, for example on a console that
  doesn't suport CR, these messages are forwarded to info().
  




message, confirm and decide are no "logging" methods.
they should maybe forward also to notice().
maybe not: user code must decide about this.

  
    
idea: make ProgressBar a subclass of Job!  If nested jobs are to be
managed in a single ProgressBar, then that's the UI who decides. 
Currently there is no visualisation of a job nesting level.

If I want support for nested jobs, then a job has a parent, instead.

Problem: PurzelStreamProgressBar must erase status line before writing
any output, then write the output, then rewrite the status. That's why
a ProgressBar is also a UI.

Maybe write \r only before next output? If there are other processes
writing to the stream (e.g. print messages), these will overwrite the
status bar only partially if they are short. In any case one should
avoid writing directly to the stream if there is also a
PurzelStreamProgressBar writing to it.

Console could split _stdout and _stderr into _debug, _verbose, _info,
_warnings and _error. Depending on the console's verbosity, some of
them would be noop writers.
Advantage: performance?

Disadvantage: how to capture? The current startDump()/stopDump() which
is very usful for tesst cases wouldn't be possible anymore.

There is a difference between filtering messages according to their
importance level, and deciding where they go.

"""



class JobAborted(Exception):
    pass


#uimeths = ('warning', 'message','info','error', 'verbose')


class Job:
    
    def __init__(self,ui,label=None,status=None,maxval=0):
        #self.pb = pb
        self._label = label
        self.ui = ui
        #for m in uimeths:
        #    setattr(self,m,getattr(pb,m))
        self.curval = 0
        self.maxval = maxval
        self.pc = None
        self._done = False
        self.onInit()
        #if status is None:
        #    status = _("Working")
        #self.status(status)

    def setMaxValue(self,n):
        self.maxval = n

    def update(self,msg,n=1):
        # shortcut to call both status() and inc()
        self.status(msg)
        self.inc(n)
        
    def inc(self,n=1):
        self.curval += n
        if self._done:
            return
        if self.maxval != 0:
            pc = int(100*self.curval/self.maxval)
            if pc == self.pc:
                return
            self.pc = pc
        self.onInc()
        
    def done(self,msg=None):
        if not self._done:
            self._done = True
            self.pc = 100
            self.onInc()
            if msg is not None and self._label is not None:
                msg = self._label+": "+msg
            self.onDone(msg)

    def aborted(self,msg=None):
        if not self._done:
            self._done = True
            #self.pc = 100
            #self.onInc()
            #self.onDone(msg)

            
    def onInc(self):
        pass
    
    def onInit(self):
        if self._label is not None:
            self.ui.info(self._label)
        
    def onDone(self,msg):
        if msg is None:
            self.ui.status("")
        else:
            self.ui.status(msg)
        


    def warning(self,msg):
        self.ui.warning(msg)
        
    def message(self,msg):
        self.ui.message(msg)
        
    def info(self,msg):
        self.ui.info(msg)
        
    def verbose(self,msg):
        self.ui.verbose(msg)
        
    def error(self,*args,**kw):
        self.ui.error(*args,**kw)
        
    def debug(self,msg):
        self.ui.debug(msg)
        
    def status(self,msg):
        self.ui.status(msg)
    
        

class PurzelConsoleJob(Job):
    # for StatusConsole

    purzelMann = "|/-\\"

    def __init__(self,*args,**kw):
        self._status = ""
        Job.__init__(self,*args,**kw)
        

##     def update(self,msg,n=1):
##         # optimized (?) for better performance
##         self.ui._status=msg
##         self.inc(n)
    
    
    def status(self,msg,*args,**kw):
        msg = self.ui._buildMessage(msg,*args,**kw)
        self._status = msg
        self._display()
        
    def onInc(self):
        self._display()
        
    def _display(self):
        if self.maxval == 0:
            s = '[' + self.purzelMann[self.curval % 4] + "] "
        else:
            if self.pc is None:
                s = "[    ] " 
            else:
                s = "[%3d%%] " % self.pc
        self.ui.status(s+self._status)




## class ProgressBar:

##     def __init__(self,label=None):
        
##         self._label = label
##         self._jobs = []
##         self.onInit()
##         #self.status(status)

##     def addJob(self,ui,*args,**kw):
##         job = Job(self,ui,*args,**kw)
##         self._jobs.append(job)
##         self.onJob(job)
##         return job
        
##     def onInit(self):
##         pass
    
##     def onJob(self,job):
##         self.onStatus(job,job._status)
    
##     def onStatus(self,job,status):
##         pass
    
##     def onInc(self,job):
##         pass

##     def onDone(self,job):
##         assert self._jobs[-1] == job, "%s != %s" % (
##             str(job), str(self._jobs[-1]))
##         del self._jobs[-1]
    

            



class Task:
    def __init__(self):
        self.job = None
        self._todo = []
        self.count_errors = 0
        self.count_warnings = 0

##     def schedule(self,m,*args,**kw):
##         self._todo.append( (m,args,kw) )

    def getLabel(self):
        return _("Working")
    
    def run(self,ui):
        self.job = ui.job(self.getLabel())
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
        
    def error(self,*args,**kw):
        self.count_errors += 1
        self.job.error(*args,**kw)

    def warning(self,msg):
        self.count_warnings += 1
        self.job.warning(msg)
        

    def start(self):
        raise NotImplementedError



