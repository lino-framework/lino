## Copyright Luc Saffre 2004.

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


import doctest
import unittest
import os, sys

from lino.misc.compat import *
from lino.misc import tsttools
from lino.ui import console


class FailuresFound(Exception):
    pass

def doctest_dir(dirname,verbose,severe=False):
    for fn in os.listdir(dirname):
        pfn = os.path.join(dirname,fn)
        if fn.endswith('.txt'):
            tester = doctest.Tester(globs={},\
                                            verbose=False)
            s = file(pfn).read()
            (f,t) = tester.runstring(s,pfn)
            if f != 0 and severe:
                raise FailuresFound,\
                        "Stopped after %d failures in %s" % (f,pfn)
            doctest.master.merge(tester)
        elif os.path.isdir(pfn):
            doctest_dir(pfn,verbose,severe)

def main(targets):

    verbose = False
    severe = False

    if "-v" in targets:
        targets.remove("-v")
        verbose = True
        print "Gonna be verbose...!"
    else:
        console.set(verbosity=-1)
        
    if "-s" in targets:
        targets.remove("-s")
        severe = True
        if verbose:
            print "Gonna be severe...!"
        
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
                        print "removed:", fn
                    os.remove(fn)
        
    if 'upload_sf' in targets:
        targets.remove('upload_sf')
        os.chdir("docs")
        os.system('rsync --rsh=ssh -v -r . lsaffre@shell.sourceforge.net:/home/groups/l/li/lino/htdocs')
        os.chdir("..")
        
    if 'html' in targets:
        targets.remove('html')
        print "Generating docs..."
        from lino.webman.static import wmm2html
        wmm2html(srcdir='docs',showOutput=False) #,force=True) 
        

    if 'unittest' in targets:
        targets.remove('unittest')
        print "Running unittest on test/ ..."
        #cwd = os.getcwd()
        #from os.path import join, getsize
        suites = []
        for root, dirs, files in os.walk('tests'):
            tests = [name[:-3] for name in files if name.endswith('.py')]
            if len(tests):
                print " collecting cases in " + root
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
        failures = 0
        tested = 0
        for M in modules: 
            (f,t) = doctest.testmod(M, verbose=False, report=0)
            if f != 0 and severe:
                raise FailuresFound,\
                        "Stopped after %d failures in %s" % (f,pfn)
            failures += f
            tested += t


        print "Running doctest on docs/ ..."
        doctest_dir('docs',verbose,severe)


        doctest.master.summarize(verbose=verbose)

    if len(targets):
        print "Unknown targets : %s" % str(targets)

if __name__ == "__main__":
    cd = os.path.dirname( __file__)
    if len(cd) :
        os.chdir(cd)
    main(sys.argv[1:])
