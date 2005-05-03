"""
scan a directory tree for .py files containing test cases and run them
"""
import os
import sys
import types
import unittest

#from lino.misc import tsttools
from lino.misc.my_import import my_import
from lino.ui.console import ConsoleApplication


class StoppingTestResult(unittest._TextTestResult):

    def stopTest(self, test):
        "Called when the given test has been run"
        if len(self.errors) or len(self.failures):
            self.stop()


class StoppingTestRunner(unittest.TextTestRunner):
    
    def _makeResult(self):
        return StoppingTestResult(self.stream,
                                  self.descriptions,
                                  self.verbosity)

def makesuite(modname):
    mod = my_import(modname)
    if hasattr(mod,"suite"):
        return mod.suite()
        # print modname + ".suite()"
    suites = []
    for (k,v) in mod.__dict__.items():
        # Python 2.2 if type(v) == types.ClassType:
        if type(v) == types.TypeType: # since 2.3
            if issubclass(v,unittest.TestCase):
                # print k
                #if v != TestCase:
                suites.append(unittest.makeSuite(v))
                    # print modname + "." + k
        #else:
        #    print "type(%s) is %s" % (k,str(type(v)))
    return unittest.TestSuite(suites)

    


class Runtests(ConsoleApplication):

    name="Lino/runtests"
    years='2004-2005'
    author='Luc Saffre'
    
    usage="usage: %prog [options] [TESTS]"
    
    description="""\
where TESTS specifies the tests to run. Default is all. Other possible values e.g. `1` or `1-7` 
"""
    def setupOptionParser(self,parser):
        ConsoleApplication.setupOptionParser(self,parser)
    
        parser.add_option("-i", "--ignore-failures",
                          help="""\
continue testing even if failures or errors occur""",
                          action="store_true",
                          dest="ignore",
                          default=False)
    
    def collectTestCases(self,ui,argv,root='.'):

        job = ui.job("Collecting test cases")
        tests = []
        for dirpath, dirnames, filenames in os.walk(root):
            job.status(dirpath)
            sys.path.append(dirpath)
            for filename in filenames:
                modname,ext = os.path.splitext(filename)
                if ext == '.py':
                    doit = (len(argv) == 0)
                    for arg in argv:
                        a = arg.split('-')
                        if len(a) == 2:
                            if a[0].isdigit() and a[1].isdigit():
                                if modname.isdigit():
                                    if int(modname) >= int(a[0]) \
                                          and int(modname) <= int(a[1]):
                                        doit = True
                            else:
                                if modname >= a[0] and modname <= a[1]:
                                    doit = True
                        elif len(a) == 1:
                            if modname == a[0]:
                                doit = True
                        else:
                            job.warning("unrecognized argument %s",
                                        arg)
                    if doit:
                        job.status("Extracting tests from %s...", 
                                   modname)
                        tests.append(makesuite(modname))
            sys.path.remove(dirpath)

        job.done("Found %d tests.",len(tests))
        return tests
     
    
    
    def run(self,ui):
        #suite = tsttools.alltests(self.args)
        tests = self.collectTestCases(ui,self.args)
        suite = unittest.TestSuite(tests)
        #runner = unittest.TextTestRunner()
        if self.options.ignore:
            runner = unittest.TextTestRunner()
        else:
            runner = StoppingTestRunner()
        runner.run(suite)
        
##     def run(self,ui):
##         tests = tsttools.collectTestCases(ui,self.args)
##         runner = unittest.TextTestRunner(verbosity=1)
##         for t in tests:
##             result=runner.run(t)
##             if not result.wasSuccessful():
##                 return -1


# lino.runscript expects a name consoleApplicationClass
consoleApplicationClass = Runtests

if __name__ == '__main__':
    consoleApplicationClass().main() # console,sys.argv[1:])
    



