#----------------------------------------------------------------------
# ID:			 $Id: console.py$
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------
import sys
try:
	import sound
except ImportError,e:
	sound = False

_syscon = None	  

class Console:

	forwardables = ('notify','confirm','warning','debug','info','error','critical')
	"""
	notify, confirm and warning are always user messages
	"""

	def __init__(self,out=None,verbose=False,debug=False,batch=False):
		if out is None:
			out = sys.stdout
		self.out = out
		self._verbose = verbose
		self._debug = debug
		self._batch = batch

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
		
		""" ask the user a question and return only when she has given
		her answer.
		
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


	def notify(self,msg):
		if sound:
			sound.asterisk()
		self.out.write(msg + "\n")

	def warning(self,msg):
		
		""" Log a warning message.	 If self._batch is False, make sure
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
		
##		def notify(self,msg):

##			"""Notify the user about something just for information.

##			Without acknowledgment request.

##			examples: why a requested action was not executed
##			"""
##			if sound:
##				sound.asterisk()
##			#notifier(msg)
##			self.out.write(msg + "\n")
##			#self.out.write('[note] ' + msg + "\n")

##		def progress(self,msg):
##			"""as notify, but only if verbose """
##			if self.verbose:
##				self.notify(msg)
			

def getSystemConsole(**kw):
	global _syscon
	if _syscon is None:
		_syscon = Console(**kw)
	return _syscon

def confirm(*args,**kw):
	return getSystemConsole().confirm(*args,**kw)

def notify(*args,**kw):
	return getSystemConsole().confirm(*args,**kw)


## def console_notify(msg):
##		print '[note] ' + msg
	
## notifier = console_notify

