#coding: latin1

## Copyright 2003-2007 Luc Saffre 

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
import codecs
#import types

from cStringIO import StringIO

try:
    import msvcrt
except ImportError:
    msvcrt = False

try:
    import sound
except ImportError,e:
    sound = False

from PyQt4 import QtCore

# rewriter() inspired by a snippet in Marc-Andre Lemburg's Python
# Unicode Tutorial
# (http://www.reportlab.com/i18n/python_unicode_tutorial.html)

## def rewriter(from_encoding,to_stream,encoding):
##     if encoding is None and hasattr(to_stream,'encoding'):
##         encoding=to_stream.encoding
##     #print 'rewriter(%r,%r)' % (from_encoding, encoding)
##     if encoding is None: return to_stream
##     if encoding == from_encoding: return to_stream

##     (e,d,sr,sw) = codecs.lookup(encoding)
##     #unicode_to_fs = sw(to_stream)
##     unicode_to_fs = sw(to_stream,errors='replace')

##     (e,d,sr,sw) = codecs.lookup(from_encoding)
    
##     class StreamRewriter(codecs.StreamWriter):

##         encode = e
##         decode = d

##         def write(self,object):
##             data,consumed = self.decode(object,self.errors)
##             self.stream.write(data)
##             return len(data)

##     return StreamRewriter(unicode_to_fs,errors='replace')


class BaseToolkit:

    def on_breathe(self,task):
        if hasattr(self,"qtapp"):
            self.qtapp.processEvents()
        #else:
        #    print "no qtapp"
        if self.abortRequested():
            task.requestAbort()
##         else:
##             self.showStatus(task.getStatus())
    
    def abortRequested(self):
        return False

##     def showStatus(self,msg):
##         pass
    
class Console(BaseToolkit):
    errors="replace"
    def __init__(self, stdout, stderr, encoding=None,**kw):
        self._verbosity = 0
        self._batch = False
        self._logfile = None
        self._logfile_stack = []
        self.redirect(stdout,stderr,encoding)
        self.configure(**kw)

    def redirect(self,stdout,stderr,encoding=None):
        assert hasattr(stdout,'write')
        assert hasattr(stderr,'write')
        #if encoding is None:
        #    encoding=sys.getdefaultencoding()
        if encoding is None and hasattr(stdout,'encoding'):
            encoding=stdout.encoding
        if encoding is None:
            encoding=sys.getfilesystemencoding()
            #encoding="utf8"
            #encoding=sys.stdout.encoding
        self.encoding=encoding
        self.stdout=stdout
        self.stderr=stderr
        #self.stdout=rewriter(sys.getdefaultencoding(),stdout,encoding)
        #self.stderr=rewriter(sys.getdefaultencoding(),stderr,encoding)


    def configure(self,
                  verbosity=None, batch=None, logfile=None,
                  addverbosity=None):
        if batch is not None:
            self._batch = batch
        if verbosity is not None:
            self._verbosity=verbosity
            #print "%s.verbositiy %d" % (self,self._verbosity)
        if addverbosity is not None:
            self._verbosity += addverbosity
        if logfile is not None:
            if self._logfile is not None:
                self._logfile.close()
            self._logfile = open(logfile,"a")



    def setupOptionParser(self,p):
        def tk_config(option, opt_str, value, parser,**kw):
            self.configure(**kw)

        p.add_option("-l", "--logfile",
                     help="log a report to FILE",
                     type="string",
                     dest="logfile",
                     #action="callback",
                     #callback=call_set,
                     #callback_kwargs=dict(logfile=...)
                     )
        p.add_option("-v",
                     "--verbose",
                     help="increase verbosity",
                     action="callback",
                     callback=tk_config,
                     callback_kwargs=dict(addverbosity=1)
                     )

        p.add_option("-q",
                     "--quiet",
                     help="decrease verbosity",
                     action="callback",
                     callback=tk_config,
                     callback_kwargs=dict(addverbosity=-1)
                     )

        p.add_option("-b",
                     "--batch",
                     help="not interactive (don't ask anything)",
                     default=self.isBatch(),
                     action="callback",
                     callback=tk_config,
                     callback_kwargs=dict(batch=True)
                     )
        
        #AbstractToolkit.setupOptionParser(self,p)
        
    
            

    def beginLog(self,filename):
        self._logfile_stack.append(self._logfile)
        self._logfile = open(filename,"a")

    def endLog(self):
        assert len(self._logfile_stack) > 0
        if self._logfile is not None:
            self._logfile.close()
        self._logfile = self._logfile_stack.pop()
            
    #def writelog(self,msg):
    def logmessage(self,msg):
        if self._logfile:
            #t = strftime("%a %Y-%m-%d %H:%M:%S")
            t = time.strftime("%Y-%m-%d %H:%M:%S")
            self._logfile.write(t+" "+msg+"\n")
            self._logfile.flush()
            
    def readkey(self,msg,default=""):
        if self._batch:
            self.logmessage(msg)
            return default
        if msg is not None:
            self.write(msg)
        return raw_input()
            
        
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
        if self.encoding is not None:
            msg=msg.encode(self.encoding,self.errors)
        self.stdout.write(msg)
        
    def writeln(self,msg):
        self.write(msg+"\n")

    def start_running(self,app):
        #print "start_running()"
        self.qtapp=QtCore.QCoreApplication([])
        #if self.qtapp.hasPendingEvents():
        #    print "there are pending events"
        #self.qtapp.processEvents() # install DB drivers
        #self.qtapp.exec_()
        if app.name and self.isInteractive():
            app.notice(app.aboutString())
            
    def stop_running(self):
        self.qtapp.processEvents() # install DB drivers
        
##     def show_status(self,sess,msg=None,*args,**kw):
##         #if msg is not None:
##         self.show_verbose(sess,msg,*args,**kw)
        
        
    def show_message(self,sess,msg,*args,**kw):
        msg = sess.buildMessage(msg,*args,**kw)
        #if sound:
        #    sound.asterisk()
        self.writeln(msg)
        #self.alert(msg)
        if not self._batch:
            self.readkey("Press ENTER to continue...")

            
    def show_confirm(self,sess,prompt,default=True):
        """Ask user a yes/no question and return only when she has
        given her answer. returns True or False.
        
        """
        assert type(default) is type(False)
        #print self.stdout
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
            s = self.readkey(prompt)
            if s == "":
                return default
            s = s.lower()
            if s == "y":
                return True
            if s == "n":
                return False
            self.show_notice(sess,
                             "wrong answer, must be 'y' or 'n': "+s)
            

    def show_decide(self,sess,prompt,answers,
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
            s = self.readkey(
                prompt+(" [%s]" % ",".join(answers)))
            if s == "":
                s = dfault
            if ignoreCase:
                s = s.lower()
            if s in answers:
                return s
            self.warning("wrong answer: "+s)


            
    def show_error(self,sess,msg,*args,**kw):
        msg = sess.buildMessage(msg,*args,**kw)
        self.stderr.write(msg + "\n")
        self.logmessage(msg)

    def critical(self,msg,*args,**kw):
        raise "Something terrible has happened..."
        #self.writelog(msg)
        #if sound:
        #    sound.asterisk()
        self.error("critical: " + msg,*args,**kw)

##     def handleException(self,e):
##         self.error(str(e))
    
    def showException(self,e,details=None):
        if details is not None:
            print details
        raise

    def show_warning(self,sess,msg,*args):
        "Display message if verbosity is normal. Logged."
        msg = sess.buildMessage(msg,*args)
        self.logmessage(msg)
        #self.writelog(msg)
        if self._verbosity >= 0:
            self.writeln(msg)
            self.last_updated=0.0 # redisplay status
            self.on_breathe(sess)

    def show_notice(self,sess,msg,*args):
        "Display message if verbosity is normal. Logged."
        if self._verbosity >= 0:
            msg = sess.buildMessage(msg,*args)
            self.logmessage(msg)
            self.writeln(msg)
            self.last_updated=0.0 # redisplay status
            self.on_breathe(sess)

    def show_verbose(self,sess,msg,*args):
        "Display message if verbosity is high. Not logged."
        if self._verbosity > 0:
            msg = sess.buildMessage(msg,*args)
            self.writeln(msg)
            self.last_updated=0.0 # redisplay status
            self.on_breathe(sess)
        
    def show_debug(self,sess,msg,*args):
        "Display message if verbosity is very high. Not logged."
        if self._verbosity > 1:
            msg = sess.buildMessage(msg,*args)
            self.writeln(msg)
            #self.out.write(msg + "\n")
            self.last_updated=0.0 # redisplay status
            self.on_breathe(sess)
##         else:
##             print "%s.verbositiy %d" % (self,self._verbosity)

            
    def shutdown(self):
        assert len(self._logfile_stack) == 0
        if self._logfile:
            self._logfile.close()

    def runtask(self,task,*args,**kw):
        # used by test 33
        return task.runfrom(self,*args,**kw)

    def onTaskBegin(self,task):
        if task.name is not None:
            task.notice(task.name)

    def onTaskDone(self,task):
        pass
        ##self.onTaskStatus(task)
        ##task.status()
        #task.summary()
        #if msg is not None:
        #    task.session.notice(task.getLabel() + ": " + msg)
    
    def onTaskAbort(self,task):
        pass
        ##self.onTaskStatus(task)
        ##task.status()
        #task.summary()
        #if task.getLabel() is not None:
        #    msg = task.getLabel() + ": " + msg
        #task.session.error(msg)

##     def onTaskIncrement(self,task):
##         self.on_breathe(task)
##         #self.onTaskStatus(task)
        
##     def onTaskBreathe(self,task):
##         if self.abortRequested():
##             task.requestAbort()
    
    def onTaskResume(self,task):
        pass
    
##     def onTaskStatus(self,task):
##         pass
##         #self.showStatus(task.session.statusMessage)
    
        
            
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
        while msvcrt.kbhit():
            ch = msvcrt.getch()
            #print ch
            if ord(ch) == 0: #'\000':
                ch = msvcrt.getch()
                if ord(ch) == 27:
                    #print "abortRequested"
                    return True
            elif ord(ch) == 27:
                #print "abortRequested"
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
            



##     def job(self,*args,**kw):
##         job = Job()
##         job.init(self,*args,**kw)
##         return job
    
    def textprinter(self,**kw):
        from lino.textprinter.plain import PlainTextPrinter
        return PlainTextPrinter(self.stdout,**kw)
        
##     def report(self,**kw):
##         from lino.reports.plain import Report
##         return Report(writer=self.stdout,**kw)


    def show_report(self,rpt,*args,**kw):
        from lino.gendoc.plain import PlainDocument
        doc = PlainDocument(self)
        doc.beginDocument()
        doc.report(rpt)
        doc.endDocument()
    

    def executeShow(self,frm):
        from lino.gendoc.plain import PlainDocument
        #gd = PlainDocument()
        gd = PlainDocument(self.stdout)
        gd.beginDocument()
        gd.renderForm(frm)
        gd.endDocument()

    def refreshForm(self,frm):
        self.showForm(frm)






class CaptureConsole(Console):
    
##     def __init__(self,batch=True,encoding="utf8",**kw):
##         self.buffer = StringIO()
##         #self.encoding=encoding
##         Console.__init__(self,
##                          self.buffer,
##                          self.buffer,
##                          batch=batch,
##                          encoding=encoding,
##                          **kw)

    def __init__(self,batch=True,**kw):
        self.buffer = StringIO()
        Console.__init__(self,
                         self.buffer,
                         self.buffer,
                         batch=batch,
                         **kw)

    def getConsoleOutput(self):
        s = self.buffer.getvalue()
        self.buffer.close()
        self.buffer = StringIO()
        self.redirect(self.buffer,self.buffer,self.encoding)
        if self.encoding is not None:
            s=s.decode(self.encoding)
        return s









class TtyConsole(Console):

    purzelPos=0
    purzelMann = r"/-\|"
    width = 78  #
    update_interval=0.1

    def __init__(self,*args,**kw):
        self.statusMessage=None
        self.last_updated=0.0
        self._empty_line="".ljust(self.width)
        Console.__init__(self,*args,**kw)

    def writeln(self,msg):
        self.stdout.write(self._empty_line+"\r")
        #self.stdout.write("".ljust(self.width)+"\r")
        if self.encoding is not None:
            if msg.upper() != "foo":
                try:
                    msg=msg.encode(self.encoding,self.errors)
                except UnicodeDecodeError,e:
                    print self.encoding, self.errors, repr(msg)
                    raise
        self.stdout.write(msg+"\n")
        #self.stdout.write(msg.ljust(self.width)+"\n")
        #self._refresh()
        
    def onTaskDone(self,task):
        # clear the status line
        self.stdout.write(self._empty_line) 
        
    def readkey(self,msg,default=""):
        if self._batch:
            self.logmessage(msg)
            return default
        self.stdout.write(self._empty_line+"\r")
        if msg is not None:
            self.write(msg)
        return raw_input()

    def on_breathe(self,task):
        Console.on_breathe(self,task)
        if time.clock() - self.last_updated < self.update_interval:
            return
        self.last_updated=time.clock()
        
        if task.maxval == 0:
            s = '[' + self.purzelMann[self.purzelPos] + "] "
            self.purzelPos+=1
            if self.purzelPos == len(self.purzelMann):
                self.purzelPos=0
        else:
            s = "[%d%%] " % int(100*task.curval/task.maxval)
            
        msg=task.getStatus()
        if msg is not None:
            s += msg
            s = s[:self.width]
        if self.encoding is not None:
            s=s.encode(self.encoding,self.errors)
        self.stdout.write(s.ljust(self.width)+"\r")
        
    



