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

import os
import sys
import time

from optparse import OptionParser
from cStringIO import StringIO
#from lino.forms.base import AbstractToolkit
#from lino.misc.jobs import Job


try:
    import msvcrt
except ImportError:
    msvcrt = False

try:
    import sound
except ImportError,e:
    sound = False


from lino.console.task import TaskAborted    

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



class AbstractToolkit:
    
    #jobFactory=Job
    #progresserFactory=Progresser
    
    def __init__(self):
        self._logfile = None
        self._sessions = []
        self._currentProgresser=None
        
    def configure(self, logfile=None):
        if logfile is not None:
            if self._logfile is not None:
                self._logfile.close()
            self._logfile = open(logfile,"a")
        
    def writelog(self,msg):
        if self._logfile:
            #t = strftime("%a %Y-%m-%d %H:%M:%S")
            t = time.strftime("%H:%M:%S")
            self._logfile.write(t+" "+msg+"\n")
            self._logfile.flush()

            
    def setupOptionParser(self,p):
        def set_logfile(option, opt_str, value, parser,**kw):
            self.configure(logfile=value)
        p.add_option("-l", "--logfile",
                     help="log a report to FILE",
                     type="string",
                     dest="logFile",
                     action="callback",
                     callback=set_logfile)

        
    def shutdown(self):
        #self.verbose("Done after %f seconds.",
        #             time.time() - self._started)
##         if sys.platform == "win32":
##             utime, stime, cutime, cstime, elapsed_time = os.times()
##             syscon.verbose("%.2f+%.2f=%.2f seconds used",
##                            utime,stime,utime+stime)
##         else:
##             syscon.verbose( "+".join([str(x) for x in os.times()])
##                           + " seconds used")
        if self._logfile:
            self._logfile.close()


        
    def critical(self,sess,msg,*args,**kw):
        if msg is not None:
            self.error(sess,msg,*args,**kw)
        sess.close()
        self.stopRunning()

    def createForm(self,sess,parent,*args,**kw):
        return self.formFactory(sess,parent,*args,**kw)


    def beginProgresser(self,sess,*args,**kw):
        self._currentProgresser=Progresser(self._currentProgresser)
        
    
##     def createJob(self,sess,*args,**kw):
##         job=self.jobFactory()
##         job.init(sess,*args,**kw)
##         return job
    
##     def createProgresser(self,sess,*args,**kw):
##         return self.progresserFactory(sess,*args,**kw)
    
    def openSession(self,sess):
        #app.setToolkit(self)
        #sess.toolkit = self
        assert sess.toolkit is self
        self._sessions.append(sess)
        
    def closeSession(self,sess):
        self._sessions.remove(sess)
        if len(self._sessions) == 0:
            self.stopRunning()
            #if self.consoleForm is not None:
            #    self.consoleForm.close()
        

    def running(self):
        raise NotImplementedError
        
    def run_forever(self):
        raise NotImplementedError
    
    def run_awhile(self):
        raise NotImplementedError

    def stopRunning(self):
        pass
        

##     def main(self,app,argv=None):
##         app.parse_args(argv)
##         self.addSession(sess)
##         self.run_forever()
        


            
#class Console(UI,CLI):
class Console(AbstractToolkit):

    purzelMann = "|/-\\"
    #jobFactory = Job #progresserFactory = Progresser

    def __init__(self, stdout, stderr,**kw):
        AbstractToolkit.__init__(self)
        self._stdout = stdout
        self._stderr = stderr
        self._verbosity = 0
        self._batch = False
        #self._started = time.time()
        #self._dumping = None
        # UI.__init__(self)
        self.set(**kw)

##     def closeSession(self,sess):
##         pass
    
    def redirect(self,stdout,stderr):
        old = (self._stdout, self._stderr)
        self._stdout = stdout
        self._stderr = stderr
        return old

    def set(self, verbosity=None, batch=None, **kw):
        if verbosity is not None:
            self._verbosity += verbosity
            #print "verbositiy %d" % self._verbosity
        if batch is not None:
            self._batch = batch
        AbstractToolkit.configure(self,**kw)
##         if ui is not None:
##             self._ui = ui
        #if debug is not None:
        #    self._debug = debug

        
    def isBatch(self):
        return self._batch
    def isInteractive(self):
        return not self._batch
    
    def isVerbose(self):
        return (self._verbosity > 0)
    
    def isQuiet(self):
        return (self._verbosity < 0)
    
    def isVeryQuiet(self):
        return (self._verbosity < -1)
    

    def write(self,msg):
        self._stdout(msg)
        
    def writeout(self,msg):
        self._stdout(msg+"\n")

            
    def status(self,sess,msg=None, *args,**kw):
        if msg is not None:
            assert type(msg) == type('')
            self.verbose(sess,msg,*args,**kw)

    def error(self,sess,msg,*args,**kw):
        msg = sess.buildMessage(msg,*args,**kw)
        self._stderr(msg + "\n")
        self.writelog(msg)

    def critical(self,sess,msg,*args,**kw):
        "Something terrible has happened..."
        #self.writelog(msg)
        #if sound:
        #    sound.asterisk()
        self.error(sess,"critical: " + msg,*args,**kw)

##     def handleException(self,e):
##         self.error(str(e))
    
    def showException(self,sess,e,details=None):
        raise

    def warning(self,sess,msg,*args,**kw):
        "Display message if verbosity is normal. Logged."
        msg = sess.buildMessage(msg,*args,**kw)
        self.writelog(msg)
        if self._verbosity >= 0:
            self.writeout(msg)

    def notice(self,sess,msg,*args,**kw):
        "Display message if verbosity is normal. Not logged."
        if self._verbosity >= 0:
            msg = sess.buildMessage(msg,*args,**kw)
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

    def onTaskDone(self,task,msg):
        self._display_task(task)
        task.session.status(None)
        task.summary()
        if msg is not None:
            task.session.notice(task.getLabel() + ": " + msg)
    
    def onTaskAbort(self,task,msg):
        task.session.status(None)
        task.summary()
        task.session.error(task.getLabel() + ": " + msg)

    def onTaskIncrement(self,task):
        self._display_task(task)
        
    def onTaskBreathe(self,task):
        pass
    
    def _display_task(self,task):
        if task.maxval == 0:
            s = '[' + self.purzelMann[task.curval % 4] + "] "
        else:
            if task.percentCompleted is None:
                s = "[    ] " 
            else:
                s = "[%3d%%] " % task.percentCompleted
        task.session.status(s+task.getStatus())
        
    
        

            
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
            self.set(**kw)

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
            self.readkey("Press ENTER to continue...")


    def readkey(self,msg):
        return raw_input(msg)
            
            
    def confirm(self,sess,prompt,default="y"):
        """Ask user a yes/no question and return only when she has
        given her answer. returns True or False.
        
        """
        #print self._stdout
##         if self.app is not None:
##             return self.app.confirm(prompt,default)
        if self._batch:
            return (default=='y')
        
        if sound:
            sound.asterisk()
        if default == "y":
            prompt += " [Y,n]"
        else:
            assert default == "n"
            prompt += " [y,N]"
        while True:
            s = self.readkey(prompt)
            if s == "":
                s = default
            s = s.lower()
            if s == "y":
                return True
            if s == "n":
                return False
            self.error("wrong answer, must be 'y' or 'n': "+s)
            

    def decide(self,sess,prompt,answers,
               default=None,
               ignoreCase=True):
        
        """Ask user a question and return only when she has given her
        answer. Returns the index of chosen answer or -1 if user
        refused to answer.
        
        """
        if default is None:
            default = answers[0]
            
        if self._batch:
            return default
        
        if sound:
            sound.asterisk()
        while True:
            s = self.readkey(prompt+(" [%s]" % ",".join(answers)))
            if s == "":
                s = default
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
        gd = PlainDocument(writer=self._stdout)
        gd.beginDocument()
        gd.report(rpt)
        gd.endDocument()
    



class TtyConsole(Console):

    width = 78  # 


    def __init__(self,*args,**kw):
        self._status = None
        Console.__init__(self,*args,**kw)


    def warning(self,sess,msg,*args,**kw):
        msg = sess.buildMessage(msg,*args,**kw)
        Console.warning(self,sess,msg.ljust(self.width))
        self._refresh()
        
    def message(self,sess,msg,*args,**kw):
        msg = sess.buildMessage(msg,*args,**kw)
        Console.message(self,sess,msg.ljust(self.width))
        self._refresh()
        
    def notice(self,sess,msg,*args,**kw):
        msg = sess.buildMessage(msg,*args,**kw)
        Console.notice(self,sess,msg.ljust(self.width))
        self._refresh()
        
    def verbose(self,sess,msg,*args,**kw):
        msg = sess.buildMessage(msg,*args,**kw)
        Console.verbose(self,sess,msg.ljust(self.width))
        self._refresh()
        
    def error(self,sess,msg,*args,**kw):
        msg = sess.buildMessage(msg,*args,**kw)
        Console.error(self,sess,msg.ljust(self.width))
        self._refresh()
        
    def critical(self,sess,msg,*args,**kw):
        msg = sess.buildMessage(msg,*args,**kw)
        Console.critical(self,sess,msg.ljust(self.width))
        self._refresh()
        
        
    def status(self,sess,msg=None,*args,**kw):
        if msg is None:
            self._status = None
        else:
            msg = sess.buildMessage(msg,*args,**kw)
            self._status = msg[:self.width]
            self._stdout(self._status.ljust(self.width)+"\r")

    def _refresh(self):
        if self._status is not None:
            self._stdout(self._status+"\r")

    def readkey(self,msg):
        if self._status is not None:
            self._stdout(self._status+"\n")
        return raw_input(msg)


class CaptureConsole(Console):
    
    def __init__(self,**kw):
        self.buffer = StringIO()
        Console.__init__(self,
                         self.buffer.write,
                         self.buffer.write,**kw)

    def getConsoleOutput(self):
        s = self.buffer.getvalue()
        self.buffer.close()
        self.buffer = StringIO()
        self.redirect(self.buffer.write,self.buffer.write)
        return s
    
