# -*- coding: UTF-8 -*-
# Copyright 2012-2016 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

r""" OdsReader uses odfpy to extract data from an .ods document
(OpenOffice.org spreadsheet).

Thanks to Marco Conti and gtr for their blog post `Read an ODS file
with Python and Odfpy
<http://www.marco83.com/work/173/read-an-ods-file-with-python-and-odfpy/>`_
which was a valuable source of inspiration to me.  Unlike Marco's
reader this one doesn't store any data in memory, it just loops over
the rows.

OdsReader is used to import data from .ods files into a Django
database using a :ref:`dpy` fixture, but not limited to this usage.

State : works for me, but very young and probably full of bugs.

Usage example:

The following code reads a file :srcref:`odsreader_sample.ods` 
and prints a line of text for each row of data.

>>> class Sample(OdsReader):
...     filename = srcpath('odsreader_sample.ods')
...     headers = ["N°", "Prénom", "Last name", "Country", "City", "Language"]
...     column_names = 'no first_name last_name country city language'.split()
...    
>>> for row in Sample().rows():
...     print( "%(first_name)s %(last_name)s from %(city)s" % row)
Rudi Rutté from Eupen
Romain Raffault from Liège
Rando Roosi from Tallinn
Rik Rozenbos from Antwerpen
Robin Rood from London

(Note: these are fictive person names from :mod:`lino.modlib.users.fixtures.demo`).


"""
from __future__ import print_function, unicode_literals
from builtins import str
from builtins import range
from builtins import object
import logging
# ~ logging.basicConfig(level='DEBUG') # uncomment this when debugging
logger = logging.getLogger(__name__)

import os


def srcpath(filename):
    return os.path.join(os.path.dirname(__file__), filename)

from odf import opendocument
from odf.table import Table, TableRow, TableCell
from odf.text import P

from lino.utils import AttrDict


class SimpleOdsReader(object):
    """Abstract base class. For each .ods file you are probably creating a
    subclass of this.

    """
    filename = None
    """The full path name of the .ods file to be read.

    """

    headers = None
    """A list of unicode strings, one for each column in the file.  The
    headers specified here must match exactly those found in the .ods
    file.

    """

    def __init__(self, **kw):
        for k, v in list(kw.items()):
            setattr(self, k, v)

    def cells2row(self, cells):
        """This will be called for each recognized data row and may perform a
        conversion before yielding it.  Subclasses may override this.

        """
        return cells

    def rows(self):
        """
        Yields the data rows found in this .ods file.
        """
        doc = opendocument.load(self.filename)
        logger.debug("Reading %s", self.filename)
        if self.column_names is None:
            self.column_names = self.headers
        assert len(self.column_names) == len(self.headers)
        for sheet in doc.spreadsheet.getElementsByType(Table):
            sheet_name = sheet.getAttribute("name")
            headers_found = False
            for row in sheet.getElementsByType(TableRow):
                cells = []
                for i, cell in enumerate(row.getElementsByType(TableCell)):

                    content = ''
                    for p in cell.getElementsByType(P):
                        for n in p.childNodes:
                            content += str(n.data)
                    content = content.strip()
                    repeat = cell.getAttribute("numbercolumnsrepeated")
                    if repeat:
                        repeat = int(repeat)
                    else:
                        repeat = 1
                    for r in range(repeat):
                        cells.append(content)

                #~ if len(cells):
                if ''.join(cells).strip():
                    if headers_found:
                        yield self.cells2row(cells)
                    elif cells == self.headers:
                        headers_found = True
                    else:
                        logger.debug("Unrecognized row %s", cells)
            if not headers_found:
                logger.debug("No data in %s.%s", self.filename, sheet_name)
        logger.debug("Done reading %s", self.filename)


class OdsReader(SimpleOdsReader):

    """
    Like :class:`SimpleOdsReader`, but each row is converted to 
    an :class:`lino.utils.AttrDict`. This requires you to specifiy, 
    besides the :attr:`SimpleOdsReader.headers` attrribute, 
    another list of pure ASCII strings which must be valid Python 
    attribute names.
    
    """
    column_names = None

    def cells2row(self, cells):
        d = {}
        for i, cell in enumerate(cells):
            name = self.column_names[i]
            if name:
                d[name] = cell
        i += 1
        while i < len(self.headers):
            name = self.column_names[i]
            if name:
                d[name] = None
            i += 1
        #~ logger.info("20121122 cells2row %s -> %s",cells,d)
        return AttrDict(d)


def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
