# coding: latin1

from lino.misc.compat import *
from lino.misc import tsttools

from lino.sdoc.macros import fileref

import doctest
import unittest
import os, sys

def doctest_dir(dirname,verbose):
	for fn in os.listdir(dirname):
		pfn = os.path.join(dirname,fn)
		if fn.endswith('.txt'):
			tester = doctest.Tester(globs={},\
											verbose=verbose)
			s = file(pfn).read()
			tester.runstring(s,pfn)
			doctest.master.merge(tester)
		elif os.path.isdir(pfn):
			doctest_dir(pfn,verbose)

def main(targets):

	verbose = False

	if "-v" in targets:
		targets.remove("-v")
		verbose = True
		print "Gonna be verbose...!"
		
	if len(targets) == 0:
		targets = ['html','tests']
		# targets = ['html','doctest']

	if 'tests' in targets:
		targets.remove('tests')
		targets += ('unittest', 'doctest')
		
	if 'clean' in targets:
		targets.remove('clean')
		for root, dirs, files in os.walk('.'):
			for fn in files:
				(name,ext) = os.path.splitext(fn)
				if ext in (".html",'.pdf'):
					fn = os.path.join(root,fn)
					if verbose:
						print fn
					os.remove(fn)
		
	if 'upload' in targets:
		targets.remove('upload')
		os.chdir("docs")
		os.system('rsync --rsh=ssh -v -r . lsaffre@shell.sourceforge.net:/home/groups/l/li/lino/htdocs')
		os.chdir("..")
		
	if 'html' in targets:
		targets.remove('html')
		print "Generating docs..."
		from lino.webman.static import wmm2html
		wmm2html(srcdir='docs') #,force=True) 
		
## 		from lino.timtools.txt2html import txt2html
## 		txt2html(sourceRoot='docs')
##       localBase = os.path.join(os.getcwd(),'docs'))


	if 'unittest' in targets:
		targets.remove('unittest')
		print "Running unittest on test/ ..."
		#cwd = os.getcwd()
		#from os.path import join, getsize
		suites = []
		for root, dirs, files in os.walk('tests'):
			tests = [name[:-3] for name in files if name.endswith('.py')]
			if len(tests):
				print "	collecting cases in " + root
				sys.path.append(os.path.abspath(root))
				# os.chdir(root)
				for modname in tests:
					# print modname
					s = tsttools.makesuite(modname)
					suites.append(s)
					# print os.path.join(root,modname+".py")
					# unittest.main(modname)
			# don't visit CVS and _attic directories
			for dontGo in ('CVS','_attic'):
				try:
					dirs.remove(dontGo)
				except ValueError:
					pass
				
		# os.chdir(cwd)
		runner = unittest.TextTestRunner()
		runner.run(unittest.TestSuite(suites))

		

	if 'doctest' in targets:
		targets.remove('doctest')

		from lino import adamo, sdoc
		modules = (adamo,sdoc)

		print "Running doctest on %s ..." % [M.__name__ for M in modules]
		for M in modules: 
			doctest.testmod(M, verbose=False, report=0)


		print "Running doctest on docs/ ..."
		doctest_dir('docs',verbose=False)


		doctest.master.summarize(verbose=verbose)

	if len(targets):
		print "Unknown targets : %s" % str(targets)

if __name__ == "__main__":
	cd = os.path.dirname( __file__)
	if len(cd) :
		os.chdir(cd)
	main(sys.argv[1:])
