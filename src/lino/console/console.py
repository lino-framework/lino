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
import codecs
import textwrap
import types

from cStringIO import StringIO

import lino

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

# rewriter() inspired by a snippet in Marc-Andre Lemburg's Python
# Unicode Tutorial
# (http://www.reportlab.com/i18n/python_unicode_tutorial.html)

def rewriter(from_encoding,to_stream,encoding):
    if encoding is None:
        encoding=to_stream.encoding
    if encoding is None: return to_stream
    if encoding == from_encoding: return to_stream

    (e,d,sr,sw) = codecs.lookup(encoding)
    unicode_to_fs = sw(to_stream)

    (e,d,sr,sw) = codecs.lookup(from_encoding)
    
    class StreamRewriter(codecs.StreamWriter):

        encode = e
        decode = d
        #errors='replace'

        def write(self,object):
            data,consumed = self.decode(object,self.errors)
            self.stream.write(data)
            return len(data)

    return StreamRewriter(unicode_to_fs)




            
#class Console(UI,CLI):
class Console: # (AbstractToolkit):

    def __init__(self, stdout, stderr, encoding=None,**kw):
        self._verbosity = 0
        self._batch = False
        self._logfile = None
        self._logfile_stack = []
        self.redirect(stdout,stderr,encoding)
        self.configure(**kw)

    def buildMessage(self,msg,*args,**kw):
        assert len(kw) == 0, "kwargs not yet implemented"
        if len(args) == 0:
            return msg
        return msg % args
    
    def redirect(self,stdout,stderr,encoding=None):
        assert hasattr(stdout,'write')
        assert hasattr(stderr,'write')
        self.stdout=rewriter(sys.getdefaultencoding(),stdout,encoding)
        self.stderr=rewriter(sys.getdefaultencoding(),stderr,encoding)


    def configure(self, verbosity=None, batch=None, logfile=None):
        if batch is not None:
            self._batch = batch
        if verbosity is not None:
            self._verbosity += verbosity
            #print "verbositiy %d" % self._verbosity
        if logfile is not None:
            if self._logfile is not None:
                self._logfile.close()
            self._logfile = open(logfile,"a")

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
        return raw_input(msg)
            
        
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
        self.stdout.write(msg)
        
    def writeln(self,msg):
        self.stdout.write(msg+"\n")

            
    def showStatus(self,msg):
        if msg is not None:
            self.verbose(msg)

    def message(self,msg):
        #if sound:
        #    sound.asterisk()
        self.writeln(msg)
        #self.alert(msg)
        if not self._batch:
            self.readkey("Press ENTER to continue...")

            
    def confirm(self,prompt,default=True):
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
            self.notice("wrong answer, must be 'y' or 'n': "+s)
            

    def decide(self,prompt,answers,
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


            
    def error(self,msg,*args,**kw):
        msg = self.buildMessage(msg,*args,**kw)
        self.stderr.write(msg + "\n")
        self.logmessage(msg)

    def critical(self,msg,*args,**kw):
        "Something terrible has happened..."
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

    def warning(self,msg,*args,**kw):
        "Display message if verbosity is normal. Logged."
        msg = self.buildMessage(msg,*args,**kw)
        self.logmessage(msg)
        #self.writelog(msg)
        if self._verbosity >= 0:
            self.writeln(msg)

    def notice(self,msg):
        "Display message if verbosity is normal. Logged."
        if self._verbosity >= 0:
            #msg = sess.buildMessage(msg,*args,**kw)
            self.logmessage(msg)
            self.writeln(msg)

    def verbose(self,msg,*args,**kw):
        "Display message if verbosity is high. Not logged."
        if self._verbosity > 0:
            msg = self.buildMessage(msg,*args,**kw)
            self.writeln(msg)
        
    def debug(self,msg,*args,**kw):
        "Display message if verbosity is very high. Not logged."
        if self._verbosity > 1:
            msg = self.buildMessage(msg,*args,**kw)
            self.writeln(msg)
            #self.out.write(msg + "\n")

            
    def shutdown(self):
        assert len(self._logfile_stack) == 0
        if self._logfile:
            self._logfile.close()


    def onTaskBegin(self,task):
        if task.getLabel() is not None:
            self.notice(task.getLabel())

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
        pass
        #self.showStatus(task.session.statusMessage)
    
        
            
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

        p.add_option("-l", "--logfile",
                     help="log a report to FILE",
                     type="string",
                     dest="logFile",
                     action="callback",
                     callback=call_set,
                     callback_kwargs=dict(logfile=1)
                     )
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
        
        #AbstractToolkit.setupOptionParser(self,p)
        


##     def job(self,*args,**kw):
##         job = Job()
##         job.init(self,*args,**kw)
##         return job
    
    def textprinter(self,sess,**kw):
        from lino.textprinter.plain import PlainTextPrinter
        return PlainTextPrinter(self.stdout,**kw)
        
##     def report(self,**kw):
##         from lino.reports.plain import Report
##         return Report(writer=self.stdout,**kw)


    def showReport(self,rpt,*args,**kw):
        from lino.gendoc.plain import PlainDocument
        gd = PlainDocument(self.stdout)
        gd.beginDocument()
        gd.report(rpt)
        gd.endDocument()
    

    def showForm(self,frm):
        from lino.gendoc.plain import PlainDocument
        #gd = PlainDocument()
        gd = PlainDocument(self.stdout)
        gd.beginDocument()
        gd.renderForm(frm)
        gd.endDocument()

    def refreshForm(self,frm):
        self.showForm(frm)




class TtyConsole(Console):

    purzelMann = "|/-\\"
    width = 78  # 


    def __init__(self,*args,**kw):
        self.statusMessage=None
        Console.__init__(self,*args,**kw)

##     def __init__(self, stdout, stderr, **kw):
##         stdout=rewriter(stdout)
## ##         try:
## ##             if stdout.encoding != sys.getdefaultencoding():
## ##                 stdout=rewriter(stdout)
## ##             else:
## ##                 print "foo"
## ##         except AttributError,e:
## ##             print "oops: ", e
        
##         Console.__init__(self,stdout,stderr,**kw)

##     def __init__(self,*args,**kw):
##         self._batch = False
##         Console.__init__(self,*args,**kw)
        
##     def configure(self, batch=None, **kw):
##         if batch is not None:
##             self._batch = batch
##         Console.configure(self,**kw)


    def warning(self,msg,*args,**kw):
        msg = self.buildMessage(msg,*args,**kw)
        Console.warning(self,msg.ljust(self.width))
        self._refresh()
        
    def message(self,msg,*args,**kw):
        msg = self.buildMessage(msg,*args,**kw)
        Console.message(self,msg.ljust(self.width))
        self._refresh()
        
    def verbose(self,msg,*args,**kw):
        msg = self.buildMessage(msg,*args,**kw)
        Console.verbose(self,msg.ljust(self.width))
        self._refresh()
        
    def error(self,msg,*args,**kw):
        msg = self.buildMessage(msg,*args,**kw)
        Console.error(self,msg.ljust(self.width))
        self._refresh()
        
    def critical(self,msg,*args,**kw):
        msg = self.buildMessage(msg,*args,**kw)
        Console.critical(self,msg.ljust(self.width))
        self._refresh()
        
        
    def notice(self,msg):
        Console.notice(self,msg.ljust(self.width))
        self._refresh()
        
    def onTaskStatus(self,task):
        if task.maxval == 0:
            s = '[' + self.purzelMann[task.curval % 4] + "] "
        else:
            if task.percentCompleted is None:
                s = "[    ] " 
            else:
                s = "[%3d%%] " % task.percentCompleted
        if self.statusMessage is None:
            self.showStatus(s)
        else:
            self.showStatus(s+self.statusMessage)
        
    def showStatus(self,msg):
        if msg is None:
            msg=''
        else:
            msg = msg[:self.width]
        self.stdout.write(msg.ljust(self.width)+"\r")

    def _refresh(self):
        self.showStatus(self.statusMessage)
        #if sess._status is not None:
        #    self.stdout(sess._status+"\r")

##     def readkey(self,sess,msg,default=""):
##         if self._batch:
##             self.logfile(msg)
##             return default
##         if sess.statusMessage is not None:
##             self.stdout.write(
##                 sess.statusMessage.ljust(self.width)+"\n")
##         return raw_input(msg)


class CaptureConsole(Console):
    
    def __init__(self,batch=True,encoding="utf8",**kw):
        self.buffer = StringIO()
        self.encoding=encoding
        Console.__init__(self,
                         self.buffer,
                         self.buffer,
                         batch=batch,
                         encoding=self.encoding,
                         **kw)

    def getConsoleOutput(self):
        s = self.buffer.getvalue()
        self.buffer.close()
        self.buffer = StringIO()
        self.redirect(self.buffer,self.buffer,self.encoding)
        if self.encoding is not None:
            s=s.decode(self.encoding)
        return s
    



class Application:
    
    name = None
    version=lino.__version__
    copyright=None
    url=None
    #years = None
    author=None
    usage = None
    description = None

    #toolkits="console"
    
    #_sessionFactory=Session
    
    """
    
    vocabulary:
    
    main() processes command-line arguments ("get the
    instructions") runs the application and returns a system error
    code (usually forwarded to sys.exit())

    run() expects that all instructions are known and performs the
    actual task.
    
    
    """
    def __init__(self):
        #if session is None:
        #    session=syscon.getSystemConsole()
        if self.name is None:
            self.name=self.__class__.__name__
        #self._sessions = []
        #self.session=session
            
        self._ignoreExceptions = []
        self.toolkit=None
        #self.setToolkit(toolkit)
        

        
##     def parse_args(self,argv=None): #,**kw):
##         if self.author is not None:
##             self.copyleft(name=self.name,
##                           years=self.years,
##                           author=self.author)
##         p = OptionParser(
##             usage=self.usage,
##             description=self.description)
            
##         self.setupOptionParser(p)
        
##         if argv is None:
##             argv = sys.argv[1:]
        
##         options,args = p.parse_args(argv)
##         self.applyOptions(options,args)
##         return p
        
    def close(self):
        pass
    
    def setupOptionParser(self,parser):
        pass

    def applyOptions(self,options,args):
        self.options=options
        self.args=args


    def aboutString(self):
        if self.name is None:
            s = self.__class__.__name__
        else:
            s = self.name
            
        if self.version is not None:
            s += " version " + self.version
        if self.author is not None:
            s += "\nAuthor: " +  self.author
        if self.copyright is not None:
            s += "\n"+self.copyright
            # "\nCopyright (c) %s %s." % (self.years, self.author)
            
        #from lino import __copyright__,  __url__
        #s += "\n\n" + __copyright__
        if self.url is not None:
            s += "\nHomepage: " + self.url
            
        using = []
        using.append('Lino ' + lino.__version__)
        using.append("Python %d.%d.%d %s" % sys.version_info[0:4])

        if sys.modules.has_key('wx'):
            wx = sys.modules['wx']
            using.append("wxPython " + wx.__version__)
    
        if sys.modules.has_key('pysqlite2'):
            from pysqlite2.dbapi2 import version
            #sqlite = sys.modules['pysqlite2']
            using.append("PySQLLite " + version)
    
        if sys.modules.has_key('reportlab'):
            reportlab = sys.modules['reportlab']
            using.append("Reportlab PDF library "+reportlab.Version)

        if sys.modules.has_key('win32print'):
            win32print = sys.modules['win32print']
            using.append("Python Windows Extensions")
        
        if sys.modules.has_key('cherrypy'):
            cherrypy = sys.modules['cherrypy']
            using.append("CherryPy " + cherrypy.__version__)

        if sys.modules.has_key('PIL'):
            using.append("PIL")

        s += "\nUsing " + "\n".join(
            textwrap.wrap(", ".join(using),76))
        
        if False:
            s += "\n".join(
                textwrap.wrap(
                " ".join([ k for k in sys.modules.keys()
                           if not k.startswith("lino.")]),76))
            
        return s
    
        
        
    
            
    def confirm(self,*args,**kw):
        self.toolkit.confirm(*args,**kw)
    def decide(self,*args,**kw):
        self.toolkit.decide(*args,**kw)
    def message(self,*args,**kw):
        self.toolkit.message(*args,**kw)
    def notice(self,*args,**kw):
        return self.toolkit.notice(*args,**kw)


    def debug(self,*args,**kw):
        return self.toolkit.debug(self,*args,**kw)
        
    def warning(self,*args,**kw):
        return self.toolkit.warning(self,*args,**kw)

    def verbose(self,*args,**kw):
        return self.toolkit.verbose(self,*args,**kw)

    def error(self,*args,**kw):
        return self.toolkit.error(self,*args,**kw)
    
    def critical(self,*args,**kw):
        return self.toolkit.critical(self,*args,**kw)
    
    def logmessage(self,*args,**kw):
        return self.toolkit.logmessage(self,*args,**kw)

    def showReport(self,*args,**kw):
        #print self.toolkit
        return self.toolkit.showReport(*args,**kw)

    def showAbout(self):
        self.message(self.app.aboutString(),title="About")
        
    def textprinter(self,*args,**kw):
        return self.toolkit.textprinter(self,*args,**kw)

    def readkey(self,*args,**kw):
        return self.toolkit.readkey(self,*args,**kw)
    
    def loop(self,func,label,maxval=0,*args,**kw):
        task=Task(self,label,maxval)
        task.loop(func,*args,**kw)
        return task
    
    def setToolkit(self,toolkit):
        #assert isinstance(toolkit,AbstractToolkit),\
        #       repr(toolkit)+" is not a toolkit"
        self.toolkit = toolkit

    def exception(self,e,details=None):
        if e.__class__ in self._ignoreExceptions:
            return
        self.toolkit.showException(self,e,details)

    def status(self,msg=None,*args,**kw):
        if msg is not None:
            #ssert type(msg) == type('')
            assert msg.__class__ in (types.StringType,
                                     types.UnicodeType)
            msg=self.buildMessage(msg,*args,**kw)
        self.statusMessage=msg
        return self.toolkit.showStatus(self,msg)

    def setStatusMessage(self,msg):
        self.statusMessage=msg
    
