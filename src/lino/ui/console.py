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

import sys

from optparse import OptionParser
from cStringIO import StringIO

from lino import __version__, __author__
from lino.i18n import itr,_

itr("Working...",
   de="Arbeitsvorgang läuft...",
   fr="Travail en cours...")

"""

A Console instance represents the console and encapsulates some
often-used things that have to do with the console.

Message importance levels:

debug
progress
info
warning
error
critical


"""

try:
    import sound
except ImportError,e:
    sound = False


class Job:
    
    def __init__(self,pb,title=None,maxval=0):
        self.pb = pb
        self.curval = 0
        self.maxval = maxval
        self._done = False
        if title is None:
            title = _("Working...")
        self.pc = None
        self.title(title)

    def title(self,newstr=""):
        self._title = newstr
        self.pb.onTitle(self)
        
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
        self.console.write(self._label+'\n')
        
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
            self.console.write(self._label+'\n')
        
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

    
            
            
class UI:
    def __init__(self):
        self._progressBar = None

    def progress(self,msg,maxval=0):
        if self._progressBar is None:
            self._progressBar = self.make_progressbar()
        return self._progressBar.addJob(msg,maxval)
        


class Console(UI):

##     forwardables = ('warning', 'confirm','decide', 
##                     'debug','info', 'progress',
##                     'error','critical',
##                     'report','textprinter',
##                     'startDump','stopDump')
    """
    confirm and warning are always user messages
    """

    def __init__(self, out=None,**kw):
        if out is None:
            out = sys.stdout
        self.out = out
        #self.app = None
        self._verbosity = 0
        self._batch = False
        self._dumping = None
        UI.__init__(self)
        #self._ui = self
        self.set(**kw)

    def set(self,verbosity=None,debug=None,batch=None):
        if verbosity is not None:
            self._verbosity += verbosity
            #print "verbositiy %d" % self._verbosity
        if batch is not None:
            self._batch = batch
##         if ui is not None:
##             self._ui = ui
        #if debug is not None:
        #    self._debug = debug

    def startDump(self,**kw):
        assert self._dumping is None
        self._dumping = self.out
        self.out=StringIO()

    def stopDump(self):
        assert self._dumping is not None, "dumping was not started"
        s = self.out.getvalue()
        self.out = self._dumping
        self._dumping = None
        return s
        
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
        self.out.write(msg)

    def log_message(self,msg):
        "Log a message to stdout."
        self.write(msg+"\n")

    def error(self,msg):
        "Log a message to stderr"
        sys.stderr.write(msg + "\n")

    def critical(self,msg):
        "Something terrible has happened..."
        if sound:
            sound.asterisk()
        raise "critical error: " + msg
    
        

    def info(self,msg):
        "Display message if verbosity is normal (not quiet)."
        if self._verbosity >= 0:
            self.log_message(msg)

    def plauder(self,msg):
        "Display message if verbosity is high."
        if self._verbosity > 0:
            self.log_message(msg)
        
    def debug(self,msg):
        "Display message if verbosity is very high."
        if self._verbosity > 1:
            self.log_message(msg)
            #self.out.write(msg + "\n")

            
        
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
            
    def parse_args(self,args=None):
        p = self.getOptionParser()
        return p.parse_args(args)

    def getOptionParser(self,**kw):
        p = OptionParser(**kw)

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
        return p

    def warning(self,msg):
        """Log a warning message.  If interactive, make sure that she
        has seen this message before returning.

        """
##         if self.app is not None:
##             return self.app.warning(msg)
        
        if sound:
            sound.asterisk()
        self.log_message(msg)
        #self.alert(msg)
        if not self._batch:
            raw_input("Press ENTER to continue...")
            
            
    def confirm(self,prompt,default="y"):
        """Ask user a yes/no question and return only when she has
        given her answer. returns True or False.
        
        """
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
            s = raw_input(prompt)
            if s == "":
                s = default
            s = s.lower()
            if s == "y":
                return True
            if s == "n":
                return False
            self.warning("wrong answer, must be 'y' or 'n': "+s)
            

    def decide(self,prompt,answers,
               default=None,
               ignoreCase=True):
        
        """Ask user a question and return only when she has
        given her answer. Returns the letter answered by user.
        
        """
##         if self.app is not None:
##             return self.app.decide(prompt,answers,default,ignoreCase)
        if default is None:
            default = answers[0]
            
        if self._batch:
            return default
        
        if sound:
            sound.asterisk()
        while True:
            s = raw_input(prompt+(" [%s]" % ",".join(answers)))
            if s == "":
                s = default
            if ignoreCase:
                s = s.lower()
            if s in answers:
                return s
            self.warning("wrong answer: "+s)

    def form(self,*args,**kw):
        raise NotImplementedError

    def make_progressbar(self,*args,**kw):
        if self.isVeryQuiet():
            return ProgressBar(*args,**kw)
        if self.isQuiet():
            return DecentConsoleProgressBar(self,*args,**kw)
        return PurzelConsoleProgressBar(self,*args,**kw)

    def textprinter(self):
        from lino.textprinter.plain import PlainDocument
        return PlainDocument(self.out)
        
    def report(self,**kw):
        from lino.reports.plain import Report
        return Report(writer=self.out,**kw)


_syscon = Console()

def getSystemConsole():
    return _syscon


for m in ('debug','info',
          'progress',
          'error','critical',
          'confirm','warning',
          'report','textprinter',
          'startDump','stopDump',
          'isInteractive','isVerbose', 'set',
          'getOptionParser','parse_args',
          ):
    globals()[m] = getattr(_syscon,m)


def copyleft(name="Lino",
             version=__version__,
             years="2002-2005",
             author=__author__):
    info("""\
%s version %s.
Copyright (c) %s %s.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information.""" % (
        name, version, years, author))
