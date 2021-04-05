# -*- coding: UTF-8 -*-
# Copyright 2013 Luc Saffre
# License: GNU Affero General Public License v3 (see file COPYING for details)

try:
    #~ needs pyPdf, see http://pybrary.net/pyPdf
    import pyPdf
    #~ from pyPdf import PdfFileWriter, PdfFileReader
except ImportError:
    pass


def merge_pdfs(pdfs, output_name):
    output = pyPdf.PdfFileWriter()

    for input_name in pdfs:
        input = pyPdf.PdfFileReader(file(input_name, "rb"))
        #~ print "%s has %s pages." % (input_name, input.getNumPages())
        for page in input.pages:
            output.addPage(page)

    outputStream = file(output_name, "wb")
    output.write(outputStream)
    outputStream.close()
