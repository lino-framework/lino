#----------------------------------------------------------------------
# ID:        $Id: console.py$
# Copyright: (c) 2003-2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------
import sys
try:
	import sound
except ImportError,e:
	sound = False

class Console:

	def __init__(self,out=None,verbose=False):
		if out is None:
			out = sys.stdout
		self.out = out
		self.verbose = verbose
		

	def confirm(self,prompt,answer="y",allowed="yn"):
		
		""" ask the user a question and return only whe she has given
		her answer.
		
		"""
		if sound:
			sound.asterisk()
		while True:
			s = raw_input(prompt+" [y,n]")
			if s == "":
				s = answer
			s = s.lower()
			if s == "y":
				return True
			if s == "n":
				return False


	def warning(self,msg):
		
		"""Notify the user about something, and make sure that she has seen this message before returning.

		(currently not used)
		
		"""
		if sound:
			sound.asterisk()
		#notifier(msg)
		self.out.write('[note] ' + msg + "\n")
		raw_input("Press ENTER to continue...")
		
	def notify(self,msg):

		"""Notify the user about something just for information.

		Without acknowledgment request.

		examples: why a requested action was not executed
		"""
		if sound:
			sound.asterisk()
		#notifier(msg)
		self.out.write(msg + "\n")
		#self.out.write('[note] ' + msg + "\n")

	def progress(self,msg):
		"""as notify, but only if verbose """
		if self.verbose:
			self.notify(msg)
			

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
## 	print '[note] ' + msg
	
## notifier = console_notify

