#coding: latin1
import os, sys, traceback

from lino.sdoc.environment import ParseError

#from lino.sdoc import styles, tables
from lino.sdoc import commands

def main(ifname,renderer,ofname=None,
			showOutput=True,
			verbose=True,
			force=True):

	(root,ext) = os.path.splitext(ifname)
	if ext == '':
		ifname += ".pds"

	if ofname is None:
		ofname = root 
		
	(head,tail) = os.path.split(ifname)
	initfile = os.path.join(head,'__init__.pds')

	try:
		commands.beginDocument(ofname,renderer,ifname)
		if verbose:
			print "%s --> %s..." % (commands.getSourceFileName(),
											commands.getOutputFileName())
		namespace = {}
		namespace.update(globals())
		namespace['pds'] = commands
		try:
			if os.path.exists(initfile):
				execfile(initfile,namespace,namespace) 
			execfile(ifname,namespace,namespace)
			commands.endDocument(showOutput)
			if verbose:
				print "%d pages." % commands.getPageNumber()
		except ParseError,e:
			raise
			#traceback.print_exc(2)
			# print document
			# print e
			# showOutput = False


	except IOError,e:
		print e
		sys.exit(1)

	

	 

