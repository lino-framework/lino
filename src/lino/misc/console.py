#----------------------------------------------------------------------
# ID:			 $Id: console.py$
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------
import sys
from optparse import OptionParser

try:
    import sound
except ImportError,e:
    sound = False

class Console:

    forwardables = ('notify','confirm','warning',
                    'debug','info','error','critical')
    """
    notify, confirm and warning are always user messages
    """

    def __init__(self, out=None,**kw):
        if out is None:
            out = sys.stdout
        self.out = out
        self._verbose = False
        self._debug = False
        self._batch = False
        self.set(**kw)

    def set(self,verbose=None,debug=None,batch=None):
        if verbose is not None:
            self._verbose = verbose
        if batch is not None:
            self._batch = batch
        if debug is not None:
            self._debug = debug

    def isBatch(self):
        return self._batch

    def isVerbose(self):
        return self._verbose


    def confirm(self,prompt,default="y",allowed="yn",ignoreCase=True):
        
        """Ask user a question and return only when she has given her
        answer.
        
        """
        if self._batch:
            return (answer=='y')
        
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


    def progress(self,msg):
        self.out.write(msg + "\n")
        
    def notify(self,msg):
        if sound:
            sound.asterisk()
        self.progress(msg)

    def warning(self,msg):
        
        """Log a warning message.  If self._batch is False, make sure
        that she has seen this message before returning.

        """
        self.notify(msg)
        if not self._batch:
            raw_input("Press ENTER to continue...")
            
    def debug(self,msg):
        "log a message if --debug is on"
        if self._debug:
            self.out.write(msg + "\n")
            
    def info(self,msg):
        "log a message if _verbose is True"
        if self._verbose:
            self.out.write(msg + "\n")

    def error(self,msg):
        "log a message to stderr"
        sys.stderr.write(msg + "\n")

    def critical(self,msg):
        if sound:
            sound.asterisk()
        raise "critical error: " + msg
        
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
            

## _syscon = None    

## def getSystemConsole():
##     global _syscon
##     if _syscon is None:
##         _syscon = Console()
##     return _syscon

_syscon = Console()

def getSystemConsole():
    return _syscon

def set(**kw):
    return getSystemConsole().set(**kw)

def confirm(*args,**kw):
    return getSystemConsole().confirm(*args,**kw)

def notify(*args,**kw):
    return getSystemConsole().notify(*args,**kw)

def info(*args,**kw):
    return getSystemConsole().info(*args,**kw)

def progress(*args,**kw):
    return getSystemConsole().progress(*args,**kw)

def isInteractive():
    return not getSystemConsole().isBatch()


## def console_notify(msg):
##      print '[note] ' + msg
    
## notifier = console_notify

def getOptionParser(**kw):
    con = getSystemConsole()
    p = OptionParser(**kw)
    
##     def setVerbose(option, opt_str, value, parser):
##         con.set(verbose=True)
    def con_set(option, opt_str, value, parser,**kw):
        con.set(**kw)
        
    p.add_option("-v",
                 "--verbose",
                 help="display many messages [default: %default]",
                 default=con.isVerbose(),
                 action="callback",
                 callback=con_set,
                 callback_kwargs=dict(verbose=True)
                 )
    
    p.add_option("-b",
                 "--batch",
                 help="don't ask anything [default: %default]",
                 default=con.isBatch(),
                 action="callback",
                 callback=con_set,
                 callback_kwargs=dict(batch=True)
                 )
    return p
        
