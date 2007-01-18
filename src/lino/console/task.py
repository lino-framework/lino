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

from lino.console.console import BaseToolkit 
from lino.console.session import Session

    
from lino.i18n import itr,_

## itr("Working",
##    de=u"Arbeitsvorgang läuft",
##    fr="Travail en cours")
## itr("%d warnings",
##     de="%d Warnungen",
##     fr="%d avertissements")
## itr("%d errors" ,
##     de="%d Fehler",
##     fr="%d erreurs")
## itr("Aborted",
##     de="Vorgang abgebrochen")

#def _(s):
#    return s    



class Task(Session):

    """A named Session with a status label.

    name expresses what the Task is supposed to do.
    label expresses what the Task is currently doing.

    """
    
    #title=None
    label=None
    #curval=0
    #percentCompleted=0
    
    maxval=0 # used by Console.on_breathe
    
    
    def __init__(self,label=None,**kw):
        if label is not None:
            self.label=label
        Session.__init__(self,**kw)

    def getTitle(self):
        return str(self)

    def __str__(self):
        if self.name is None:
            return self.__class__.__name__
        return self.name
    

    def getStatus(self):
        # may override 
        return self.label

    def status(self,msg,*args,**kw):
        msg=self.buildMessage(msg,*args,**kw)
        self.label=msg
        self.breathe()

    def runfrom(self,toolkit,*args,**kw):
        # overridden by Progresser
        assert isinstance(toolkit,BaseToolkit)
        self.toolkit=toolkit
        return self.run(*args,**kw)
    

class Progresser(Task):

    def __init__(self,label=None,maxval=None,**kw):
        Task.__init__(self,label,**kw)
        self.curval=0
        if maxval is not None:
            self.maxval=maxval


    def runfrom(self,toolkit,*args,**kw):
        assert isinstance(toolkit,BaseToolkit)
        self.toolkit=toolkit
        self.curval=0
        
        self.toolkit.onTaskBegin(self)
        #okay=True
        #retval=None
        #success=False
        try:
            retval=self.run(*args,**kw)
            #self._done = True
            #success=True
            #self.percentCompleted = 100
            self.toolkit.onTaskDone(self)
            return retval
            
        except Exception,e:
            # cleanup, then forward the exception 
            self.toolkit.onTaskAbort(self)
            raise 


    def sleep(self,n=1.0):
        sleepStep=0.1
        while n > 0:
            self.breathe()
            n-=sleepStep
            if n == 0: return
            sleep(sleepStep)

        
    def increment(self,n=1):
        self.curval += n
        self.breathe()

    def breathe(self):
        return self.toolkit.on_breathe(self)

    def setMaxVal(self,n):
        self.maxval=n
        

    

class BugDemo(Progresser):
    name="&Bug demo"
    maxval=10
    label="Let's see what happens if an exception occurs..."
    
    
##     def getLabel(self):
##         return "Let's see what happens if an exception occurs..."
    
    def getStatus(self):
        return "%d seconds left" % self.curval
    
    def run(self):
        for i in range(self.maxval,0,-1):
            self.increment()
            self.sleep(1)
            
        self.thisWontWork()
            

## def run_task(sess,meth,label,maxval,*args,**kw):
##     task=Task(sess,label,maxval)
##     return task.run_in_session(meth,*args,**kw)
##     #meth(self,*args,**kw)

