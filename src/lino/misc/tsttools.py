"""
"""
#import re
import unittest
import sys
import os
import types

from cStringIO import StringIO

from lino.misc.my_import import my_import
from lino.misc import console 

#~ def run(modname):
   #~ suite = makesuite(modname)
   #~ runner = unittest.TextTestRunner()
   #~ runner.run(suite)
   
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


def alltests(argv,dirname='.'):
    
    """inspect all python modules in the current directory for test
    cases and suites. make one big suite from all this. """
    
    suites = []
    sys.path.append(dirname)
    for fn in os.listdir(dirname):
        modname,ext = os.path.splitext(fn)
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
                    raise "unrecognized argument "+arg
            if doit:
                suites.append(makesuite(modname))
    sys.path.remove(dirname)

    return unittest.TestSuite(suites)
     




#def compressWhiteSpace(s):
#    return re.sub(r'\s+',' ',s)
    
class TestCase(unittest.TestCase):
        
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
    
    def checkGeneratedFiles(self,*filenames):
        for fn in filenames:
            if console.isInteractive(): 
                os.system("start "+fn)
            else:
                self.failUnless(os.path.exists(fn))
                os.remove(fn)


#a = sys.stdout # open("a.txt","w")
#b = sys.stdout # open("b.txt","w")

main = unittest.main
