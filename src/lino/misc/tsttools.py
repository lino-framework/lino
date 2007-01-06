## Copyright 2003-2006 Luc Saffre

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

"""
"""
#import re
import unittest
import sys
import os
import types

from cStringIO import StringIO

#from lino.ui import console
from lino.console import syscon
from lino.console.console import CaptureConsole
from lino.forms.testkit import Toolkit
from lino import config

class UniStringIO:
    def __init__(self,s=u''):
        self.buffer=s
    def write(self,s):
        #self.s += s.encode('utf-8')
        self.buffer+=unicode(s)
    def getvalue(self):
        return self.buffer
    def __str__(self):
        return repr(self.buffer)


def trycmd(cmd,startdir=None):
    
    """Run the system command 'cmd' in a child process.

    Returns the observed output (as a string) and the exit status (an integer) as a tuple.
    Saves and restores the current working directory.
    """
    cwd=os.getcwd()
    if startdir is not None:
        os.chdir(startdir)
    pin,pout=os.popen4(cmd,"t")
    observed=pout.read()
    exitstatus=pout.close()
    pin.close()
    os.chdir(cwd)
    return observed,exitstatus


TESTDATA = os.path.join(config.paths.get('tests_path'),'testdata')
DOCROOT = config.paths.get('docs_path')

## TESTDATA = os.path.normpath( os.path.join(
##     os.path.dirname(__file__),
##     '..','..','..','tests','testdata'))

## DOCROOT = os.path.normpath( os.path.join(
##     os.path.dirname(__file__),
##     '..','..','..','docs'))



## class TestConsole(console.CaptureConsole):
##     pass


#~ def run(modname):
   #~ suite = makesuite(modname)
   #~ runner = unittest.TextTestRunner()
   #~ runner.run(suite)


## def catch_output(f,*args,**kw):
##     out = sys.stdout
##     sys.stdout = StringIO()
##     try:
##         f(*args,**kw)
##     #except Exception,e:
##     #    raise e
##     finally:
##         r = sys.stdout.getvalue()
##         sys.stdout = out
##         return r


   


## def oneof(l,*args,**kw):
##     for f in l:
##         if f(*args,**kw): return True
##     return False
    
   
   

## def alltests(argv,root='.'):
    
##     """inspect all python modules in the current directory for test
##     cases and suites. make one big suite from all this. """

## ##     namefilters = []
## ##     for arg in argv:
## ##         a = arg.split('-')
## ##         if len(a) == 2:
## ##             if a[0].isdigit() and a[1].isdigit():
## ##                 def f(modname):
## ##                     if not modname.isdigit():
## ##                         return False
## ##                     if int(modname) >= int(a[0]) \
## ##                           and int(modname) <= int(a[1]):
## ##                         return True
## ##             else:
## ##                 def f(modname):
## ##                     if modname >= a[0] and modname <= a[1]:
## ##                         return True
## ##         elif len(a) == 1:
## ##             def f(modname):
## ##                 if modname == a[0]:
## ##                     return True
## ##         else:
## ##             raise "unrecognized argument "+arg
        
## ##         namefilters.append(f)

##     job = console.job("Collecting test cases")
##     suites = []
##     #for dirpath, dirname, filename in os.listdir(dirname):
##     for dirpath, dirnames, filenames in os.walk(root):
##         job.status(dirpath)
##         sys.path.append(dirpath)
##         for filename in filenames:
##             modname,ext = os.path.splitext(filename)
##             #dirpath = dirpath.replace("."+os.path.sep,"")
##             #modname = dirpath.replace(os.path.sep,".")+"."+modname
##             #print dirpath, filename
##             #print modname
##             if ext == '.py':
## ##                 if len(namefilters) == 0 or oneof(namefilters,modname):
## ##                     print modname
## ##                     suites.append(makesuite(modname))
##                 doit = (len(argv) == 0)
##                 for arg in argv:
##                     a = arg.split('-')
##                     if len(a) == 2:
##                         if a[0].isdigit() and a[1].isdigit():
##                             if modname.isdigit():
##                                 if int(modname) >= int(a[0]) \
##                                       and int(modname) <= int(a[1]):
##                                     doit = True
##                         else:
##                             if modname >= a[0] and modname <= a[1]:
##                                 doit = True
##                     elif len(a) == 1:
##                         if modname == a[0]:
##                             doit = True
##                     else:
##                         job.warning("unrecognized argument %s",
##                                     arg)
##                 if doit:
##                     job.status("Extracting tests from %s...", 
##                                modname)
##                     suites.append(makesuite(modname))
##         sys.path.remove(dirpath)
        
##     suite = unittest.TestSuite(suites)
##     job.done("Found %d tests.",suite.countTestCases())
##     return suite
     


#def compressWhiteSpace(s):
#    return re.sub(r'\s+',' ',s)

    
class TestCase(unittest.TestCase):
    waiting=False
    #win32_printerName_PS = "Lexmark Optra PS"
    #tempDir = r"c:\temp"
    verbosity=-2
    batch=True

##     def __init__(self):
##         unittest.TestCase.__init__(self)
##         self.shouldStop = 1
    
##     def defaultTestResult(self):
##         return TestResult()
    
    def setUp(self):
        self._tempFiles = []
        self._showFiles = []
        self.keepTemporaryFiles = False
        #self.ui = console.CaptureConsole(verbosity=-2,batch=True)
        self._oldToolkit=syscon.getSystemConsole()
        self.toolkit=CaptureConsole(
            encoding="latin1",
            verbosity=self.verbosity,
            batch=self.batch)
        syscon.setSystemConsole(self.toolkit)

    def tearDown(self):
        if self._oldToolkit.isVerbose(): # called with -v or -vv
            print self.getConsoleOutput()
        syscon.setSystemConsole(self._oldToolkit)
        #print s
        #raise "blabla"
        if len(self._tempFiles) > 0:
            for fn in self._tempFiles:
                if not os.path.exists(fn):
                    self.fail(
                        "Temporary file %s has not been created" % fn)

    def afterRun(self,sess):
        # called by runtests.py
        if not hasattr(self,"_showFiles"):
            return # happens if test was never run because a
                   # previous test failed
        for fn in self._showFiles:
            #self.failUnless(os.path.exists(fn))
            if sess.confirm(
                "Okay to start %s ?" % fn, default=False):
                os.system('start ' + fn)
        if len(self._tempFiles) > 0:
            if sess.confirm("Okay to delete %d temporary files ?" \
                            % len(self._tempFiles)):
                for fn in self._tempFiles:
                    os.remove(fn)

    def getConsoleOutput(self):
        return self.toolkit.getConsoleOutput()
        #return self.ui.getConsoleOutput()
        
    def assertEquivalent(self,observed,expected,msg=None):
        
        """like assertEqual(), but any whitespace is converted to a
        single space, and if they differ, they are printed with a
        newline before each (so that it is more easy to see the
        difference)

        """
        l1 = observed.split()
        l2 = expected.split()

        #print l1
        #print "---"
        #print l2
        
        if l1 == l2: return

        u=UniStringIO()
        #u=StringIO()

        if msg is not None:
            u.write(msg+":")
        u.write("\n--- observed --- :\n")
        u.write(observed)
        #uwrite(repr(" ".join(l1))) # txt1)
        u.write("\n--- expected --- :\n")
        u.write(expected)
        #uwrite(repr(" ".join(l2))) # txt1)
        u.write("\n---\n")

        if False:
            from difflib import ndiff
            diff = ndiff(l1,l2)
            print '\n'.join(diff)

        if False:
            file("observed.txt","wt").write(observed)
            file("expected.txt","wt").write(expected)
        
        #self.fail(a.getvalue()) 
        self.fail(u.getvalue())

    def addTempFile(self,filename,showOutput=None):
        """unlike tempfile, these files are not OPENED
        """
        fn = os.path.join(config.paths.get('tempdir'),filename)
        if os.path.exists(fn):
            os.remove(fn)
        self._tempFiles.append(fn)
        if showOutput:
            self._showFiles.append(fn)
        return fn
    
##     def trycmd(self,cmd,expected=None,msg=None):
##         fd=os.popen(cmd,"r")
##         observed=fd.read()
##         exitstatus=fd.close()
        
##         #print "observed", observed
            
##         #msg=repr(cmd)+" failed"
##         if exitstatus is not None:
##             self.fail(
##                 "%r failed: close() returned %r, stdout is %r." \
##                 % (cmd,exitstatus,observed))
                
##         if expected is not None:
##             self.assertEquivalent(observed,expected,msg)

    def trycmd(self,cmd,
               expected=None,
               msg=None,
               startdir=None,
               expectfile=None):
            
        observed,exitstatus=trycmd(cmd,startdir=startdir)
        
        #print "observed", observed
            
        #msg=repr(cmd)+" failed"
        if exitstatus is not None:
            self.fail(
                "%r failed: close() returned %r, stdout is %r." \
                % (cmd,exitstatus,observed))
                
        if expected is not None:
            if msg is None:
                msg="unexpected output of `%s`" % cmd
            self.assertEquivalent(observed,expected,msg)

        if expectfile is not None:
            self._tempFiles.remove(expectfile)
            if not os.path.exists(expectfile):
                self.fail(
                    '`%s` did not generate file %s. Output is:\n%s'\
                    % (cmd,expectfile,observed))
        

#a = sys.stdout # open("a.txt","w")
#b = sys.stdout # open("b.txt","w")

main = unittest.main

## def main(*args,**kw):
##     runner = TextTestRunner(stream=?)
##     TestProgram(testRunner)

