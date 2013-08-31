# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

try:
    #~ needs pyPdf, see http://pybrary.net/pyPdf
    import pyPdf
    #~ from pyPdf import PdfFileWriter, PdfFileReader
except ImportError:
    pass

def merge_pdfs(pdfs,output_name):
    output = pyPdf.PdfFileWriter()
    
    for input_name in pdfs:
        input = pyPdf.PdfFileReader(file(input_name, "rb"))
        #~ print "%s has %s pages." % (input_name, input.getNumPages())
        for page in input.pages:
            output.addPage(page)
            
    outputStream = file(output_name, "wb")
    output.write(outputStream)
    outputStream.close()
