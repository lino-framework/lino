#coding: utf-8

## Copyright Luc Saffre 2004-2005.

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
oogen : generate OpenOffice documents programmatically

Bibliography:
-   http://books.evc-cit.info
    Using OpenOffice.org's XML Data Format
-   http://www.oooforum.org/forum/viewtopic.php?t=13861
    Opening 2 csv text files into OOo Calc as separate sheets
-   http://udk.openoffice.org/python/python-bridge.html
    Python-UNO bridge

"""
import zipfile
import os.path
opj = os.path.join

from ifiles import IFILES



class OoGenerator:
    "base clase for OoText,OoSpreadsheet,..."
    extension = NotImplementedError
    mimetype = NotImplementedError
    
    def __init__(self,doc=None,filename=None):
        if doc is None:
            doc = Document()
        self.doc = doc
        
        self.tempDir = r'c:\temp'

        if filename is None:
            filename = self.doc.name
        if not filename.lower().endswith(self.extension):
            filename += self.extension
        self.outputFilename = filename
        
        self.ifiles = tuple([cl(self) for cl in IFILES])
        
    def save(self):
        for f in self.ifiles:
            f.writeFile()
        zf = zipfile.ZipFile(self.outputFilename,'w',
                             zipfile.ZIP_DEFLATED)
        for f in self.ifiles:
            zf.write(opj(self.tempDir,f.filename),f.filename)
        zf.close()
        


class OoText(OoGenerator):
    extension = ".sxw"
    officeClass = "text"
    mimetype = "application/vnd.sun.xml.writer"
    
    def writeBody(self,wr):
        for elem in self.doc.story:
            elem.__xml__(wr)

class OoSpreadsheet(OoGenerator):
    extension = ".sxc"
    officeClass = "spreadsheet"
    mimetype = "application/vnd.sun.xml.calc"
        
    def writeBody(self,wr):
        for elem in self.doc.tables:
            elem.__xml__(wr)
