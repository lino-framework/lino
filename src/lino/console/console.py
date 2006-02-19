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

import os
import sys
import time

#from optparse import OptionParser
from cStringIO import StringIO
#from lino.forms.base import AbstractToolkit
#from lino.misc.jobs import Job

from lino.forms.base import AbstractToolkit

try:
    import msvcrt
except ImportError:
    msvcrt = False

try:
    import sound
except ImportError,e:
    sound = False


class UserAborted(Exception):
    pass

class OperationFailed(Exception):
    pass

#class TaskAborted(Exception):
#    def __init__(self, task):
#        self.task = task

#from lino.misc.jobs import JobAborted, Job #, PurzelConsoleJob
#from lino.forms.progresser import Progresser

## class UI:
##     pass
    
## class CLI:
##     usage = None
##     description = None
    
##     def parse_args(self,argv=None): #,**kw):
##         p = OptionParser(
##             usage=self.usage,
##             description=self.description)
            
##         self.setupOptionParser(p)
        
##         if argv is None:
##             argv = sys.argv[1:]
        
##         options,args = p.parse_args(argv)
##         self.applyOptions(options,args)
        

##     def applyOptions(self,options,args):
##         pass
    
##     def setupOptionParser(self,parser):
##         pass




            
#class Console(UI,CLI):
class Console(AbstractToolkit):

    #jobFactory = Job #progresserFactory = Progresser

    def __init__(self, stdout, stderr, **kw):
        AbstractToolkit.__init__(self)
        assert hasattr(stdout,'write')
        assert hasattr(stderr,'write')
        self._stdout = stdout
        self._stderr = stderr
        self._verbosity = 0
        self._batch = False
        #self._status = None
        #self._started = time.time()
        #self._dumping = None
        # UI.__init__(self)
        self.configure(**kw)

##     def closeSession(self,sess):
##         pass
    
    def redirect(self,stdout,stderr):
        assert hasattr(stdout,'write')
        assert hasattr(stderr,'write')
        old = (self._stdout, self._stderr)
        self._stdout = stdout
        self._stderr = stderr
        return old

    def configure(self, verbosity=None, batch=None, **kw):
        if batch is not None:
            self._batch = batch
        if verbosity is not None:
            self._verbosity += verbosity
            #print "verbositiy %d" % self._verbosity
        #AbstractToolkit.configure(self,**kw)
##         if ui is not None:
##             self._ui = ui
        #if debug is not None:
        #    self._debug = debug

        
    def isBatch(self):
        return self._batch
    def isInteractive(self):
        return not self._batch
    

##     def isBatch(self):
##         return True
##     def isInteractive(self):
##         return False
    
    def isVerbose(self):
        return (self._verbosity > 0)
    
    def isQuiet(self):
        return (self._verbosity < 0)
    
    def isVeryQuiet(self):
        return (self._verbosity < -1)
    

    def write(self,msg):
        self._stdout.write(msg)
        
    def writeout(self,msg):
        self._stdout.write(msg+"\n")

            
    def showStatus(self,sess,msg):
        if msg is not None:
            sess.verbose(msg)

    def error(self,sess,msg,*args,**kw):
        msg = sess.buildMessage(msg,*args,**kw)
        self._stderr(msg + "\n")
        sess.logmessage(msg)

    def critical(self,sess,msg,*args,**kw):
        "Something terrible has happened..."
        #self.writelog(msg)
        #if sound:
        #    sound.asterisk()
        self.error(sess,"critical: " + msg,*args,**kw)

##     def handleException(self,e):
##         self.error(str(e))
    
    def showException(self,sess,e,details=None):
        if details is not None:
            print details
        raise

    def warning(self,sess,msg,*args,**kw):
        "Display message if verbosity is normal. Logged."
        msg = sess.buildMessage(msg,*args,**kw)
        sess.logmessage(msg)
        #self.writelog(msg)
        if self._verbosity >= 0:
            self.writeout(msg)

    def notice(self,sess,msg,*args,**kw):
        "Display message if verbosity is normal. Logged."
        if self._verbosity >= 0:
            msg = sess.buildMessage(msg,*args,**kw)
            sess.logmessage(msg)
            self.writeout(msg)

    def verbose(self,sess,msg,*args,**kw):
        "Display message if verbosity is high. Not logged."
        if self._verbosity > 0:
            msg = sess.buildMessage(msg,*args,**kw)
            self.writeout(msg)
        
    def debug(self,sess,msg,*args,**kw):
        "Display message if verbosity is very high. Not logged."
        if self._verbosity > 1:
            msg = sess.buildMessage(msg,*args,**kw)
            self.writeout(msg)
            #self.out.write(msg + "\n")

            


    def onTaskBegin(self,task):
        if task.getLabel() is not None:
            task.session.notice(task.getLabel())

    def onTaskDone(self,task):
        self.onTaskStatus(task)
        task.session.status()
        #task.summary()
        #if msg is not None:
        #    task.session.notice(task.getLabel() + ": " + msg)
    
    def onTaskAbort(self,task):
        self.onTaskStatus(task)
        task.session.status()
        #task.summary()
        #if task.getLabel() is not None:
        #    msg = task.getLabel() + ": " + msg
        #task.session.error(msg)

    def onTaskIncrement(self,task):
        self.onTaskStatus(task)
        
    def onTaskBreathe(self,task):
        if self.abortRequested():
            task.requestAbort()
    
    def onTaskResume(self,task):
        pass
    
    def onTaskStatus(self,task):
        self.showStatus(task.session,
                        task.session.statusMessage)
    
        
            
##     def onJobRefresh(self,job):
##         pass
    
##     def onJobInit(self,job):
##         if job.getLabel() is not None:
##             self.notice(job.session,job.getLabel())

##     def onJobDone(self,job,msg):
##         self._display_job(job)
##         self.status(job.session,None)
##         job.summary()
##         if msg is not None:
##             self.notice(job.session,job.getLabel() + ": " + msg)
    
##     def onJobAbort(self,job,msg):
##         self.status(job.session,None)
##         job.summary()
##         self.error(job.session,job.getLabel() + ": " + msg)



##     def onJobRefresh(self,job):
##         self._display_job(job)
##         if self.abortRequested():
##             if job.confirmAbort():
##                 #job.abort()
##                 raise JobAborted(job)
                
##     def _display_job(self,job):
##         if job.maxval == 0:
##             s = '[' + self.purzelMann[job.curval % 4] + "] "
##         else:
##             if job.pc is None:
##                 s = "[    ] " 
##             else:
##                 s = "[%3d%%] " % job.pc
##         self.status(job.session,s+job.getStatus())
    

        
##     def abortRequested(self):
##         return False
        
    def abortRequested(self):
        if not msvcrt: return False
        # print "abortRequested"
        while msvcrt.kbhit():
            ch = msvcrt.getch()
            #print ch
            if ord(ch) == 0: #'\000':
                ch = msvcrt.getch()
                if ord(ch) == 27:
                    return True
            elif ord(ch) == 27:
                return True
        return False


            
        
##      def notify(self,msg):

##          """Notify the user about something just for information.

##          Without acknowledgment request.

##          examples: why a requested action was not executed
##          """
##          if sound:
##              sound.asterisk()
##          #notifier(msg)
##          self.out.write(msg + "\n")
##          #self.out.write('[note] ' + msg + "\n")

##      def progress(self,msg):
##          """as notify, but only if verbose """
##          if self.verbose:
##              self.notify(msg)
            

    def setupOptionParser(self,p):
        def call_set(option, opt_str, value, parser,**kw):
            self.configure(**kw)

        p.add_option("-v",
                     "--verbose",
                     help="increase verbosity",
                     action="callback",
                     callback=call_set,
                     callback_kwargs=dict(verbosity=1)
                     )

        p.add_option("-q",
                     "--quiet",
                     help="decrease verbosity",
                     action="callback",
                     callback=call_set,
                     callback_kwargs=dict(verbosity=-1)
                     )

        p.add_option("-b",
                     "--batch",
                     help="not interactive (don't ask anything)",
                     default=self.isBatch(),
                     action="callback",
                     callback=call_set,
                     callback_kwargs=dict(batch=True)
                     )
        
        AbstractToolkit.setupOptionParser(self,p)
        

    def message(self,sess,msg,**kw):
        #msg=sess.buildMessage(msg,**kw)
##         if self.app is not None:
##             return self.app.warning(msg)
        
        #if sound:
        #    sound.asterisk()
        self.writeout(msg)
        #self.alert(msg)
        if not self._batch:
            self.readkey(sess,"Press ENTER to continue...")


    def readkey(self,sess,msg):
        if self._batch:
            sess.notice(msg)
            return ""
        return raw_input(msg)
            
            
    def confirm(self,sess,prompt,default=True):
        """Ask user a yes/no question and return only when she has
        given her answer. returns True or False.
        
        """
        assert type(default) is type(False)
        #print self._stdout
##         if self.app is not None:
##             return self.app.confirm(prompt,default)
        if sound:
            sound.asterisk()
        if default:
            prompt += " [Y,n]"
        else:
            #assert default == "n"
            prompt += " [y,N]"
        while True:
            s = self.readkey(sess,prompt)
            if s == "":
                return default
            s = s.lower()
            if s == "y":
                return True
            if s == "n":
                return False
            self.error("wrong answer, must be 'y' or 'n': "+s)
            

    def decide(self,sess,prompt,answers,
               dfault=None,
               ignoreCase=True):
        
        """Ask user a question and return only when she has given her
        answer. Returns the index of chosen answer or -1 if user
        refused to answer.
        
        """
        if dfault is None:
            dfault = answers[0]

        if self._batch:
            return dfault

        if sound:
            sound.asterisk()
        while True:
            s = self.readkey(sess,prompt+(" [%s]" % ",".join(answers)))
            if s == "":
                s = dfault
            if ignoreCase:
                s = s.lower()
            if s in answers:
                return s
            self.warning("wrong answer: "+s)


##     def job(self,*args,**kw):
##         job = Job()
##         job.init(self,*args,**kw)
##         return job
    
    def textprinter(self,sess,**kw):
        from lino.textprinter.plain import PlainTextPrinter
        return PlainTextPrinter(self._stdout,**kw)
        
##     def report(self,**kw):
##         from lino.reports.plain import Report
##         return Report(writer=self._stdout,**kw)


    def showReport(self,sess,rpt,*args,**kw):
        from lino.gendoc.plain import PlainDocument
        gd = PlainDocument(self._stdout)
        gd.beginDocument()
        gd.report(rpt)
        gd.endDocument()
    

    def showForm(self,frm):
        from lino.gendoc.plain import PlainDocument
        #gd = PlainDocument()
        gd = PlainDocument(self._stdout)
        gd.beginDocument()
        gd.renderForm(frm)
        gd.endDocument()

    def refreshForm(self,frm):
        self.showForm(frm)


class TtyConsole(Console):

    purzelMann = "|/-\\"
    width = 78  # 

##     def __init__(self,*args,**kw):
##         self._batch = False
##         Console.__init__(self,*args,**kw)
        
##     def configure(self, batch=None, **kw):
##         if batch is not None:
##             self._batch = batch
##         Console.configure(self,**kw)


    def warning(self,sess,msg,*args,**kw):
        msg = sess.buildMessage(msg,*args,**kw)
        Console.warning(self,sess,msg.ljust(self.width))
        self._refresh(sess)
        
    def message(self,sess,msg,*args,**kw):
        msg = sess.buildMessage(msg,*args,**kw)
        Console.message(self,sess,msg.ljust(self.width))
        self._refresh(sess)
        
    def notice(self,sess,msg,*args,**kw):
        msg = sess.buildMessage(msg,*args,**kw)
        Console.notice(self,sess,msg.ljust(self.width))
        self._refresh(sess)
        
    def verbose(self,sess,msg,*args,**kw):
        msg = sess.buildMessage(msg,*args,**kw)
        Console.verbose(self,sess,msg.ljust(self.width))
        self._refresh(sess)
        
    def error(self,sess,msg,*args,**kw):
        msg = sess.buildMessage(msg,*args,**kw)
        Console.error(self,sess,msg.ljust(self.width))
        self._refresh(sess)
        
    def critical(self,sess,msg,*args,**kw):
        msg = sess.buildMessage(msg,*args,**kw)
        Console.critical(self,sess,msg.ljust(self.width))
        self._refresh(sess)
        
        
    def onTaskStatus(self,task):
        if task.maxval == 0:
            s = '[' + self.purzelMann[task.curval % 4] + "] "
        else:
            if task.percentCompleted is None:
                s = "[    ] " 
            else:
                s = "[%3d%%] " % task.percentCompleted
        if task.session.statusMessage is None:
            self.showStatus(task.session,s)
        else:
            self.showStatus(task.session,
                            s+task.session.statusMessage)
        
    def showStatus(self,sess,msg):
        if msg is None:
            msg=''
        else:
            msg = msg[:self.width]
        self._stdout.write(msg.ljust(self.width)+"\r")

    def _refresh(self,sess):
        self.showStatus(sess,sess.statusMessage)
        #if sess._status is not None:
        #    self._stdout(sess._status+"\r")

    def readkey(self,sess,msg):
        if self._batch:
            sess.notice(msg)
            return ""
        if sess.statusMessage is not None:
            self._stdout.write(
                sess.statusMessage.ljust(self.width)+"\n")
        return raw_input(msg)


class CaptureConsole(Console):
    
    def __init__(self,batch=True,**kw):
        self.buffer = StringIO()
        Console.__init__(self,
                         self.buffer,
                         self.buffer,
                         batch=batch,**kw)

    def getConsoleOutput(self):
        s = self.buffer.getvalue()
        self.buffer.close()
        self.buffer = StringIO()
        self.redirect(self.buffer,self.buffer)
        return s
    
