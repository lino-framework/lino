## Copyright 2004-2006 Luc Saffre

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
testing prnprinter
"""
import sys
import os

from lino.misc import tsttools

#from lino.scripts.prnprint import PrnPrint

#dataPath = os.path.join(os.path.dirname(__file__),
#                        'testdata','textprinter')

dataPath = os.path.join(tsttools.TESTDATA,'textprinter')
#dataPath = os.path.abspath(dataPath)


class Case(tsttools.TestCase):
    ""
    prnfiles=('1','2','4','5')
    def test01(self):
        for i in self.prnfiles:
            spoolFile = self.addTempFile(i+".ps",showOutput=True)
            inputFile = os.path.join(dataPath,i)+".prn"

            cmd='lino prnprint -p "%s" -o "%s" "%s"' % (
                self.win32_printerName_PS,spoolFile,inputFile)
            
            fd=os.popen(cmd,"r")
            observed=fd.read()
            cr=fd.close()
            
            #print "observed", observed
            
            msg=repr(cmd)+" failed"
            self.assertEqual(
                cr,None,msg+" (close() returned %r)"%cr)
            
    def test02(self):
        for i in self.prnfiles:
            spoolFile = self.addTempFile(i+".pdf",showOutput=True)
            inputFile = os.path.join(dataPath,i)+".prn"

            cmd='lino prn2pdf -b -o "%s" "%s"' % (spoolFile,inputFile)
            
            fd=os.popen(cmd,"r")
            observed=fd.read()
            cr=fd.close()
            
            #print "observed", observed
            
            msg=repr(cmd)+" failed"
            self.assertEqual(
                cr,None,msg+" (close() returned %r)"%cr)
            

if __name__ == '__main__':
    tsttools.main()

