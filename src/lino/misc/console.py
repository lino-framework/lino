#----------------------------------------------------------------------
# ID:			 $Id: console.py$
# This file is part of the Lino project
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------
import sys
from optparse import OptionParser

"""

A Console instance represents the console and encapsulates some
often-used things that have to do with the console.

Message importance levels:

debug
info
warning
error
critical


"""

try:
    import sound
except ImportError,e:
    sound = False

class Console:

    forwardables = ('confirm','decide',
                    'debug','info',
                    'warning',
                    'error','critical')
    """
    confirm and warning are always user messages
    """

    def __init__(self, out=None,**kw):
        if out is None:
            out = sys.stdout
        self.out = out
        self._verbosity = 0
        #self._debug = False
        self._batch = False
        self.set(**kw)

    def set(self,verbosity=None,debug=None,batch=None):
        if verbosity is not None:
            self._verbosity += verbosity
        if batch is not None:
            self._batch = batch
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
    


    def log_message(self,msg):
        "Log a message to stdout."
        self.out.write(msg+"\n")

    def error(self,msg):
        "Log a message to stderr"
        sys.stderr.write(msg + "\n")

    def critical(self,msg):
        "Something terrible has happened..."
        if sound:
            sound.asterisk()
        raise "critical error: " + msg
    
        

    def progress(self,msg):
        "Display message if verbosity is normal."
        if self._verbosity >= 0:
            self.log_message(msg)
        
    def info(self,msg):
        "Display message if verbosity is high."
        if self._verbosity >= 1:
            self.log_message(msg)
            #self.out.write(msg + "\n")

    def debug(self,msg):
        "Display message if verbosity is very high."
        if self._verbosity >= 2:
            self.log_message(msg)
            #self.out.write(msg + "\n")
            
    def warning(self,msg):
        
        """Log a warning message.  If self._batch is False, make sure
        that she has seen this message before returning.

        """
        if sound:
            sound.asterisk()
        self.log_message(msg)
        #self.alert(msg)
        if not self._batch:
            raw_input("Press ENTER to continue...")
            
            
    def confirm(self,prompt,default="y",allowed="yn",ignoreCase=True):
        
        """Ask user a yes/no question and return only when she has
        given her answer.
        
        """
        if self._batch:
            return (default=='y')
        
        if sound:
            sound.asterisk()
        while True:
            s = raw_input(prompt+(" [%s]" % ",".join(allowed)))
            if s == "":
                s = default
            if ignoreCase:
                s = s.lower()
            if s == "y":
                return True
            if s == "n":
                return False
            self.warning("wrong answer: "+s)
            

    def decide(self,prompt,answers,
               default=None,
               ignoreCase=True):
        
        """Ask user a question and return only when she has
        given her answer.
        
        """
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
                     help="don't ask anything [default: %default]",
                     default=self.isBatch(),
                     action="callback",
                     callback=call_set,
                     callback_kwargs=dict(batch=True)
                     )
        return p

## _syscon = None    

## def getSystemConsole():
##     global _syscon
##     if _syscon is None:
##         _syscon = Console()
##     return _syscon

_syscon = Console()

def getSystemConsole():
    return _syscon

#for m in _syscon.forwardables:
#    __dict__[m] = getattr(_syscon,m)

error = _syscon.error       # to stderr
#message = _syscon.message   # to stdout


debug = _syscon.debug       # message if verbosity very high
info = _syscon.info         # message if verbosity high
progress = _syscon.progress # message if verbosity is normal
warning = _syscon.warning
error = _syscon.error
critical = _syscon.critical

# aliases
alert = _syscon.warning

# higher level:
confirm = _syscon.confirm
decide = _syscon.decide

isInteractive = _syscon.isInteractive
set = _syscon.set
getOptionParser = _syscon.getOptionParser

