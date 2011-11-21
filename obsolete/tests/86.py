## Copyright 2007 Luc Saffre

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
from lino.misc.tsttools import TestCase, main, removetree
from lino import config

sourceDir=os.path.join(config.paths.get("tests_path"),"testdata")
targetDir=os.path.join(config.paths.get("tempdir"),"synctest")

class Case(TestCase):

    def test01(self):

        removetree(targetDir)
        expected="""
        Target directory '%s' doesn't exist.
        """ % targetDir

        cmd = "lino sync -rvvb %s %s" % (sourceDir,targetDir)

        self.trycmd(cmd,expected)

        
    def test02(self):

        removetree(targetDir)
        expected="""
        Zielordner '%s' existiert nicht.
        """ % targetDir

        cmd = "lino sync -rvvb %s %s --lang=de" % (sourceDir,targetDir)

        self.trycmd(cmd,expected)

    def test03(self):

        removetree(targetDir)
        os.mkdir(targetDir)

        expected=r"""

Analyzing sync 'c:\drives\t\svnwork\lino\trunk\tests\testdata' 'c:\temp\synctest' -r ...
Must copy c:\temp\synctest\webman\2\.cvsignore
Must copy c:\temp\synctest\webman\2\1.txt
Must copy c:\temp\synctest\webman\2\index.txt
Must copy c:\temp\synctest\webman\2\init.wmi
Must copy c:\temp\synctest\webman\1.txt
Must copy c:\temp\synctest\webman\index.txt
Must copy c:\temp\synctest\webman\init.wmi
Must copy c:\temp\synctest\5.pds
Must copy c:\temp\synctest\5b.pds
Must copy c:\temp\synctest\5c.pds
Must copy c:\temp\synctest\5d.pds
Must copy c:\temp\synctest\cp1252a.txt
Must copy c:\temp\synctest\cp1252b.txt
Must copy c:\temp\synctest\cp437box.txt
Must copy c:\temp\synctest\cp850a.txt
Must copy c:\temp\synctest\cp850b.txt
Must copy c:\temp\synctest\cp850box.txt
Must copy c:\temp\synctest\ee_de.txt~
Must copy c:\temp\synctest\eupen.pdf
Must copy c:\temp\synctest\gnosis-readme
Must copy c:\temp\synctest\jona.txt
Must copy c:\temp\synctest\NAT.DBF
Must copy c:\temp\synctest\PAR.DBF
Must copy c:\temp\synctest\PAR.DBT
Must copy c:\temp\synctest\PLZ.DBF
Must copy c:\temp\synctest\README.TXT
26 files and 2 directories to copy
Synchronizing sync 'c:\drives\t\svnwork\lino\trunk\tests\testdata' 'c:\temp\synctest' -r ...
Creating directory c:\temp\synctest\webman
Creating directory c:\temp\synctest\webman\2
Copying c:\temp\synctest\webman\2\.cvsignore
Copying c:\temp\synctest\webman\2\1.txt
Copying c:\temp\synctest\webman\2\index.txt
Copying c:\temp\synctest\webman\2\init.wmi
Copying c:\temp\synctest\webman\1.txt
Copying c:\temp\synctest\webman\index.txt
Copying c:\temp\synctest\webman\init.wmi
Copying c:\temp\synctest\5.pds
Copying c:\temp\synctest\5b.pds
Copying c:\temp\synctest\5c.pds
Copying c:\temp\synctest\5d.pds
Copying c:\temp\synctest\cp1252a.txt
Copying c:\temp\synctest\cp1252b.txt
Copying c:\temp\synctest\cp437box.txt
Copying c:\temp\synctest\cp850a.txt
Copying c:\temp\synctest\cp850b.txt
Copying c:\temp\synctest\cp850box.txt
Copying c:\temp\synctest\ee_de.txt~
Copying c:\temp\synctest\eupen.pdf        
Copying c:\temp\synctest\gnosis-readme
Copying c:\temp\synctest\jona.txt
Copying c:\temp\synctest\NAT.DBF
Copying c:\temp\synctest\PAR.DBF
Copying c:\temp\synctest\PAR.DBT
Copying c:\temp\synctest\PLZ.DBF
Copying c:\temp\synctest\README.TXT
26 files and 2 directories were copied
        """

        expected=expected.replace(r"c:\temp\synctest",targetDir)
        expected=expected.replace(r"c:\drives\t\svnwork\lino\trunk\tests\testdata",sourceDir)

        cmd = "lino sync -rvvb --ignore=.svn %s %s" % (sourceDir,targetDir)

        self.trycmd(cmd,expected)

        removetree(targetDir)
        
        
        
if __name__ == '__main__':
    main()

