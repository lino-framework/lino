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
import atexit
from time import strftime

from optparse import OptionParser
from cStringIO import StringIO

from lino import __version__, __author__

"""

A Console instance represents the console and encapsulates some
often-used things that have to do with the console.

"""

try:
    import sound
except ImportError,e:
    sound = False


            
class UI:
    def __init__(self):
        self._progressBar = None

    def job(self,msg,maxval=0):
        if self._progressBar is None:
            self._progressBar = self.make_progressbar()
        return self._progressBar.addJob(msg,maxval)
        


class Console(UI):

    def __init__(self, out=None,**kw):
        if out is None:
            out = sys.stdout
        self.out = out
        self._log = None
        #self.app = None
        self._verbosity = 0
        self._batch = False
        self._dumping = None
        UI.__init__(self)
        #self._ui = self
        self.set(**kw)

    def set(self,
            verbosity=None,
            debug=None,
            batch=None,
            logfile=None):
        if verbosity is not None:
            self._verbosity += verbosity
            #print "verbositiy %d" % self._verbosity
        if batch is not None:
            self._batch = batch
        if logfile is not None:
            if self._log is not None:
                self._log.close()
            self._log = open(logfile,"a")
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
        
    def writeout(self,msg):
        self.out.write(msg+"\n")

    def writelog(self,msg):
        if self._log:
            t = strftime("%a %Y-%m-%d %H:%M:%S")
            self._log.write(t+" "+msg+"\n")
            
##     def log_message(self,msg):
##         "Log a message to stdout."
##         self.write(msg+"\n")

    def status(self,msg):
        self.verbose(msg)

    def error(self,msg):
        "Log a message to stderr"
        sys.stderr.write(msg + "\n")
        self.writelog(msg)

    def critical(self,msg):
        "Something terrible has happened..."
        self.writelog(msg)
        if sound:
            sound.asterisk()
        raise "critical error: " + msg
    
        

    def warning(self,msg):
        "Display message if verbosity is normal. Logged."
        self.writelog(msg)
        if self._verbosity >= 0:
            self.writeout(msg)

    def info(self,msg):
        "Display message if verbosity is normal. Not logged."
        if self._verbosity >= 0:
            self.writeout(msg)

    def verbose(self,msg):
        "Display message if verbosity is high. Not logged."
        if self._verbosity > 0:
            self.writeout(msg)
        
    def debug(self,msg):
        "Display message if verbosity is very high. Not logged."
        if self._verbosity > 1:
            self.writeout(msg)
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

        def set_logfile(option, opt_str, value, parser,**kw):
            self.set(logfile=value)

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
        p.add_option("-l", "--logfile",
                     help="log a report to FILE",
                     type="string",
                     dest="logFile",
                     action="callback",
                     callback=set_logfile)
        return p

    def message(self,msg):
##         if self.app is not None:
##             return self.app.warning(msg)
        
        if sound:
            sound.asterisk()
        self.writeout(msg)
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

    def shutdown(self):
        if self._log:
            self._log.close()

    def form(self,*args,**kw):
        raise NotImplementedError

    def make_progressbar(self,*args,**kw):
        from lino.misc.jobs import ProgressBar, \
             DecentConsoleProgressBar, \
             PurzelConsoleProgressBar
        if self.isVeryQuiet():
            return ProgressBar(self,*args,**kw)
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
atexit.register(_syscon.shutdown)

def getSystemConsole():
    return _syscon


for m in ('debug','message','info','status',
          'job', 'verbose', 'error','critical',
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
