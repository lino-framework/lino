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

"""
"""
#import re
import unittest
import tempfile
import sys
import os
import types

from cStringIO import StringIO

from lino.misc.my_import import my_import
from lino.ui import console 


#~ def run(modname):
   #~ suite = makesuite(modname)
   #~ runner = unittest.TextTestRunner()
   #~ runner.run(suite)


def oneof(l,*args,**kw):
    for f in l:
        if f(*args,**kw): return True
    return False
    
   
   
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
                if v != TestCase:
                    suites.append(unittest.makeSuite(v))
                    # print modname + "." + k
        #else:
        #    print "type(%s) is %s" % (k,str(type(v)))
    return unittest.TestSuite(suites)


def alltests(argv,root='.'):
    
    """inspect all python modules in the current directory for test
    cases and suites. make one big suite from all this. """

##     namefilters = []
##     for arg in argv:
##         a = arg.split('-')
##         if len(a) == 2:
##             if a[0].isdigit() and a[1].isdigit():
##                 def f(modname):
##                     if not modname.isdigit():
##                         return False
##                     if int(modname) >= int(a[0]) \
##                           and int(modname) <= int(a[1]):
##                         return True
##             else:
##                 def f(modname):
##                     if modname >= a[0] and modname <= a[1]:
##                         return True
##         elif len(a) == 1:
##             def f(modname):
##                 if modname == a[0]:
##                     return True
##         else:
##             raise "unrecognized argument "+arg
        
##         namefilters.append(f)

    suites = []
    #for dirpath, dirname, filename in os.listdir(dirname):
    for dirpath, dirnames, filenames in os.walk(root):
        sys.path.append(dirpath)
        for filename in filenames:
            modname,ext = os.path.splitext(filename)
            #dirpath = dirpath.replace("."+os.path.sep,"")
            #modname = dirpath.replace(os.path.sep,".")+"."+modname
            #print dirpath, filename
            #print modname
            if ext == '.py':
##                 if len(namefilters) == 0 or oneof(namefilters,modname):
##                     print modname
##                     suites.append(makesuite(modname))
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
                        print "unrecognized argument "+arg
                if doit:
                    console.info("Extracting tests from %s..." % \
                                modname)
                    suites.append(makesuite(modname))
        sys.path.remove(dirpath)

    return unittest.TestSuite(suites)
     




#def compressWhiteSpace(s):
#    return re.sub(r'\s+',' ',s)
    
class TestCase(unittest.TestCase):

    win32_printerName_PS = "Lexmark Optra PS"
    
    def setUp(self):
        self._tempFiles = []
        self._showFiles = []
        self.keepTemporaryFiles = False

    def tearDown(self):
        for fn in self._showFiles:
            self.failUnless(os.path.exists(fn))
            if console.confirm("Okay to start %s ?" % fn,\
                              default="n"):
                os.system('start ' + fn)
        if len(self._tempFiles) > 0:
            if console.confirm("Okay to delete %d temporary files ?" \
                              % len(self._tempFiles)):
                for fn in self._tempFiles:
                    os.remove(fn)
        
    def assertEquivalent(self,txt1,txt2):
        
        """like assertEqual(), but any whitespace is converted to a
        single space, and if they differ, they are printed with a
        newline before each (so that it is more easy to see the
        difference)

        """

        l1 = txt1.strip().split()
        l2 = txt2.strip().split()

        if l1 == l2: return

##          txt1 = compressWhiteSpace(txt1.strip())
##          txt2 = compressWhiteSpace(txt2.strip())
##          if txt1 == txt2: return
        a = StringIO()
        a.write("\n--- observed --- :\n")
        a.write(" ".join(l1)) # txt1)
        a.write("\n--- expected --- :\n")
        a.write(" ".join(l2)) # txt1)
        # b.write(txt2)
        a.write("\n")

        if False:
            from difflib import ndiff
            diff = ndiff(l1,l2)
            print '\n'.join(diff)
        
        self.fail(a.getvalue()) # "texts differ. See stdout")

    def addTempFile(self,filename,showOutput=None):
        "unlike tempfile, these files are not OPENED"
        fn = os.path.join(tempfile.gettempdir(),filename)
        self._tempFiles.append(fn)
        if showOutput:
            self._showFiles.append(fn)
        return fn
    
    def checkGeneratedFiles(self,*filenames):
        raise DeprecationWarning("use addTempFile(showOutput=True)")
##         for fn in filenames:
##             if console.isInteractive(): 
##                 os.system("start "+fn)
##             else:
##                 self.failUnless(os.path.exists(fn))
##                 os.remove(fn)


#a = sys.stdout # open("a.txt","w")
#b = sys.stdout # open("b.txt","w")

main = unittest.main

