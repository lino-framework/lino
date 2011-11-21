## Copyright 2003-2007 Luc Saffre

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

import os
import codecs

from lino.misc.tsttools import TestCase, main

from lino import config

examplesDir=os.path.join(config.paths.get("docs_path"),"examples")

#examplesDir=os.path.join(os.path.dirname(__file__),
#                         "..", "docs","examples")

class Case(TestCase):

    def test01(self):
        examples=[]
        #count=0
        for dirpath, dirnames, filenames in os.walk(examplesDir):
            for filename in filenames:
                base,ext = os.path.splitext(filename)
                if ext == '.py':
                    examples.append((dirpath,base))
                    
        #self.assertEqual(len(examples),13)
        
        for dirpath,base in examples:
            #filename = os.path.join(dirpath,base)+".py"
            cmd="python %s.py --batch" % base

            outfile=os.path.join(examplesDir,dirpath,base)+".out"
            #outfile=base+".out"
            #expected=open(outfile).read()
            expected=codecs.open(outfile,encoding="iso-8859-1").read().strip()
            
            
            if expected.startswith("TODO:"):
                print cmd, expected.splitlines()[0]
            else:
                #print cmd
                #print expected
                self.trycmd(cmd,expected,
                            startdir=os.path.join(examplesDir,dirpath))
            
            
##             fd=os.popen(cmd,"r")
##             observed=fd.read()
##             cr=fd.close()
            
##             msg="Example %s failed" % filename
##             self.assertEqual(
##                 cr,None,msg+" (close() returned %r)"%cr)
##             else:
##                 self.assertEquivalent(observed,expected,msg)
                    
                                          
        
        
if __name__ == '__main__':
    main()

