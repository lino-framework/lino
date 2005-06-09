## Copyright Luc Saffre 2004. This file is part of the Lino project.

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

#scriptsPath = os.path.join("..","..","scripts")
#sys.path.append(scriptsPath)
from lino.scripts.prnprint import PrnPrint

dataPath = os.path.join(os.path.dirname(__file__),
                        'testdata','textprinter')
dataPath = os.path.abspath(dataPath)


class Case(tsttools.TestCase):
    ""

    def test01(self):
        app=PrnPrint()
        for i in ('1','2'):
            spoolFile = self.addTempFile(i+".ps",showOutput=True)
            inputFile = os.path.join(dataPath,i)+".prn"
            app.main([ "-p", self.win32_printerName_PS,
                       "-o", spoolFile,
                       inputFile] )
        
            

if __name__ == '__main__':
    tsttools.main()

