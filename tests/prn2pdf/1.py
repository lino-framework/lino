# coding: latin1
#----------------------------------------------------------------------
# Copyright: (c) 2003-2004 Luc Saffre
# License:   GPL
#----------------------------------------------------------------------

"""
testing prnprinter
"""
import sys
import os

from lino.misc import tsttools

#scriptsPath = os.path.join("..","..","scripts")
#sys.path.append(scriptsPath)
from lino.scripts.prn2printer import main

dataPath = os.path.join(os.path.dirname(__file__),'testdata')
dataPath = os.path.abspath(dataPath)


class Case(tsttools.TestCase):
    ""

    def test01(self):
        for i in ('1','2'):
            spoolFile = self.addTempFile(i+".ps",showOutput=True)
            inputFile = os.path.join(dataPath,i)+".prn"
            main([ "-p", self.win32_printerName_PS,
                   "-o", spoolFile,
                   inputFile] )
        
            

if __name__ == '__main__':
    tsttools.main()

