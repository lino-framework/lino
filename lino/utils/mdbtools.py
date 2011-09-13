## Copyright 2011 Luc Saffre
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

"""
This is for writing fixtures that import data from an MS-Access 
database (:xfile:`.mdb`) into Lino.

Usage examples see 
:mod:`lino.apps.dsbe.fixtures.pp2lino`
and
:mod:`lino.apps.crl.fixtures.hs2lino`.

It uses `mdb-export` to extract data from the :xfile:`.mdb` 
file to :xfile:`.csv`, then reads these csv files. 
`mdb-export` was written by Brian Bruns and is part 
of the `mdbtools` Debian package. To install it::

  aptitude install mdbtools
  
Usage of `mdbtools` command line::

  Usage: mdb-export [options] <file> <table>
  where options are:
    -H             supress header row
    -Q             don't wrap text-like fields in quotes
    -d <delimiter> specify a column delimiter
    -R <delimiter> specify a row delimiter
    -I             INSERT statements (instead of CSV)
    -D <format>    set the date format (see strftime(3) for details)
    -S             Sanitize names (replace spaces etc. with underscore)
    -q <char>      Use <char> to wrap text-like fields. Default is ".
    -X <char>      Use <char> to escape quoted characters within a field. Default is doubling.
    
Thanks to http://farismadi.wordpress.com/2008/07/13/encoding-of-mdb-tool/ 
for explanations on the environment variables used by `mdb-export`.

The function :func:`check_output` in this module is a copy from Python 2.7 
which we include here to make it usable in Python 2.6 too.


"""

import logging
logger = logging.getLogger(__name__)


#~ ENCODING = 'latin1' # the encoding used by the mdb file
ENCODING = 'utf8' 
#~ MDB_FILE = 'PPv5MasterCopie.mdb'
MDBTOOLS_EXPORT = 'mdb-export'

import os
import sys
#~ ENCODING = sys.stdout.encoding
#~ import csv
import codecs
import datetime

from django.conf import settings

from lino.utils import ucsv
from lino.utils import dblogger


#~ ENCODING = 'latin1' # the encoding used by the mdb file
ENCODING = 'utf8' 
#~ MDB_FILE = 'PPv5MasterCopie.mdb'
MDBTOOLS_EXPORT = 'mdb-export'


try:
  from subprocess import check_output
except ImportError:
    import subprocess
    
    def check_output(*popenargs, **kwargs):
        r"""Run command with arguments and return its output as a byte string.

        If the exit code was non-zero it raises a CalledProcessError.  The
        CalledProcessError object will have the return code in the returncode
        attribute and output in the output attribute.

        The arguments are the same as for the Popen constructor.  Example:

        >>> check_output(["ls", "-l", "/dev/null"])
        'crw-rw-rw- 1 root root 1, 3 Oct 18  2007 /dev/null\n'

        The stdout argument is not allowed as it is used internally.
        To capture standard error in the result, use stderr=STDOUT.

        >>> check_output(["/bin/sh", "-c",
        ...               "ls -l non_existent_file ; exit 0"],
        ...              stderr=STDOUT)
        'ls: non_existent_file: No such file or directory\n'
        """
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd, output=output)
        return output

class Loader:
    mdb_file = None
    table_name = None
    model = None
    
    def __iter__(self):
        fn = self.table_name + ".csv"
        if os.path.exists(fn):
            logger.warning("Not re-extracting %s since it exists.",fn)
        else:
            args = [MDBTOOLS_EXPORT, '-D', "%Y-%m-%d %H:%M:%S", self.mdb_file, self.table_name]
            s = check_output(args,executable=MDBTOOLS_EXPORT,
              env=dict(
                MDB_ICONV='utf-8',
                MDB_JET_CHARSET='utf-8'))
            #~ print ENCODING
            
            fd = open(fn,'w')
            fd.write(s)
            fd.close()
            logger.info("Extracted file %s", fn)
        reader = ucsv.UnicodeReader(open(fn,'r'),encoding=ENCODING)
        headers = reader.next()
        if not headers == self.headers:
            raise Exception("%r != %r" % (headers,self.headers))
        n = 0
        for values in reader:
            row = {}
            for i,h in enumerate(self.headers):
                row[h] = values[i]
            n += 1
            if False:
                if int(row['IDClient']) == 967:
                    print row
                    raise Exception("20110609")
                  
            if False:
                if n < 10:
                    print n, ':', row
                else:
                    raise Exception("20110609")
            for obj in self.row2obj(row):
                yield obj

    def parsedate(self,s):
        if not s: return None
        dt = s.split()
        if len(dt) != 2:
            raise Exception("Unexpected datetime string %r" % s)
        d = dt[0]
        #~ t = dt[1]
        a = [int(i) for i in d.split('-')]
        return datetime.date(year=a[0],month=a[1],day=a[2])

    def parsetime(self,s):
        if not s: return None
        dt = s.split()
        if len(dt) != 2:
            raise Exception("Unexpected datetime string %r" % s)
        t = dt[1]
        return t[:5]
        #~ a = [int(i) for i in t.split(':')]
        #~ return datetime.time(hour=a[0],minute=a[1],second=a[2])

