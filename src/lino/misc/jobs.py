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
#from lino.ui import console

itr("Working",
   de="Arbeitsvorgang läuft",
   fr="Travail en cours")


class Task:
    def __init__(self):
        self._todo = []

    def schedule(self,m,*args,**kw):
        self._todo.append( (m,args,kw) )

    def getLabel(self):
        return _("Working")
    
    def run(self,ui):
        self.ui = ui
        self.job = self.ui.progress(self.getLabel())
        self.start()
        while len(self._todo) > 0:
            self.job.inc()
            m,args,kw = self._todo.pop(0)
            m(*args,**kw)
        self.job.done()

    def message(self,msg):
        self.ui.message(msg)

    def error(self,msg):
        self.ui.error(msg)





class Job:
    
    def __init__(self,pb,title=None,maxval=0):
        self.pb = pb
        self.curval = 0
        self.maxval = maxval
        self._done = False
        if title is None:
            title = _("Working")
        self.pc = None
        self.title(title)

    def title(self,newstr=""):
        self._title = newstr
        self.pb.onTitle(self)

    def ping(self,msg):
        self._title = msg
        self.inc()
        
    def inc(self,n=1):
        self.curval += n
        if self._done:
            return
        if self.maxval == 0:
            self.pb.onInc(self)
        else:
            pc = int(100*self.curval/self.maxval)
            if pc == self.pc:
                return
            self.pc = pc
            self.pb.onInc(self)
        
    def done(self):
        if not self._done:
            self._done = True
            self.pc = 100
            self.pb.onInc(self)
            self.pb.onDone(self)

    def __str__(self):
        return self._title
            




class ProgressBar:

    """
    
    no longer inspired by
    http://docs.python.org/mac/progressbar-objects.html
    and
    http://search.cpan.org/src/FLUFFY/Term-ProgressBar-2.06-r1/README

    
    """
    def __init__(self,label=None):
        
        """
        
        title is the text string displayed (default ``Working...''),
        maxval is the value at which progress is complete (default 0,
        indicating that an indeterminate amount of work remains to be
        done), and label is the text that is displayed above the
        progress bar itself.
        
        
        """
        self._label = label
        self._jobs = []
        self.onInit()
        #self.title(title)

    def addJob(self,*args,**kw):
        job = Job(self,*args,**kw)
        self._jobs.append(job)
        self.onJob(job)
        return job
        
    def onInit(self):
        pass
    
    def onJob(self,job):
        self.onTitle(job)
    
    def onTitle(self,job):
        pass
    
    def onInc(self,job):
        pass

    def onDone(self,job):
        assert self._jobs[-1] == job, "%s != %s" % (
            str(job), str(self._jobs[-1]))
        del self._jobs[-1]
    

class ConsoleProgressBar(ProgressBar):
    def __init__(self,console,*args,**kw):
        self.console = console
        ProgressBar.__init__(self,*args,**kw)
        
    def onInit(self):
        self.console.writeout(self._label)
        
    def onDone(self,job):
        self.console.write('\n')
        ProgressBar.onDone(self,job)
        
class DecentConsoleProgressBar(ConsoleProgressBar):
    def onTitle(self):
        self.console.write(self._title)
        
    def onInc(self):
        self.console.write('.')
        
class PurzelConsoleProgressBar(ConsoleProgressBar):

    purzelMann = r"|/-\*"
    
    def onInit(self):
        if self._label is not None:
            self.console.writeout(self._label)
        
    def onTitle(self,job):
        self.onInc(job)
        
    def onInc(self,job):
        if job.maxval is 0:
            s = '[' + self.purzelMann[job.curval % 5] + "] "
        else:
            if job.pc is None:
                s = "[    ] " 
            else:
                s = "[%3d%%] " % job.pc
        s += job._title
        self.console.write(s.ljust(80) + '\r')

    
            
