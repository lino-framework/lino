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
generate gendoc examples to webhome
"""
## import sys
import os
import glob

from lino.misc import tsttools
from lino import config

EXAMPLES=os.path.join(config.paths.get('docs_path'),
                    'examples','gendoc','*.py')
OUTDIR=os.path.join(config.paths.get('webhome'),
                    'examples','gendoc')


class Case(tsttools.TestCase):


    
    
##     ""
##     prnfiles=('1','2','3','4','5', '20060829')
    
    def test01(self):
        l=[]
        for filename in glob.glob(EXAMPLES):
            base,ext = os.path.splitext(os.path.basename(filename))
            l.append(base)
            for ext in (".pdf",".html"):
                outfile=os.path.join(OUTDIR,base)+ext
                cmd="python %s --batch %s" % (filename,outfile)
                self.trycmd(cmd)

        self.assertEqual(len(l),8)
                
            
    


        
##         for i in self.prnfiles:
##             spoolFile = self.addTempFile(i+".ps",showOutput=True)
##             inputFile = os.path.join(dataPath,i)+".prn"

##             cmd='lino prnprint -b -e cp850 -p "%s" -o "%s" "%s"' % (
##                 config.win32.get('postscript_printer'),
##                 spoolFile,inputFile)
##             expected="""
## Printing on printer '%s'
## %s : 1 page has been printed
## """ % (config.win32.get('postscript_printer'),inputFile)
##             expected=None
##             """
            
##             Not all files print only 1 page, so it is difficult to
##             test for the exact output.  But if something fails, then I
##             can set expected='' to see the output of the failing
##             command.
            
##             """
##             self.trycmd(cmd,expected)
            
##     def test02(self):
##         for i in self.prnfiles:
##             spoolFile = self.addTempFile(i+".pdf",showOutput=True)
##             inputFile = os.path.join(dataPath,i)+".prn"

##             cmd='lino prn2pdf -b -e cp850 -o "%s" "%s"' % (spoolFile,inputFile)

##             self.trycmd(cmd,expectfile=spoolFile)
            
            

## if __name__ == '__main__':
##     tsttools.main()

