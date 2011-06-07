# -*- coding: UTF-8 -*-
## Copyright 2009-2011 Luc Saffre
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
This fixture is for one-time use in a real case, 
and maybe as starting example for future similar cases.

It uses `mdb-export` to extract data from the .mdb file to .csv, 
then reads these csv files. 
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

"""

import sys
import csv
import codecs

try:
  from subprocess import check_output
except ImportError:
    # check_output was added only in Python 2.7

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

from lino.tools import resolve_model

MDB_FILE = 'PPv5MasterCopie.mdb'
MDBTOOLS_EXPORT = 'mdb-export'

class Loader:
    table_name = None
    model = None
    
    def load(self):
        args = [MDBTOOLS_EXPORT, MDB_FILE, self.table_name]
        s = check_output(args,executable=MDBTOOLS_EXPORT)
        s = s.decode(sys.getdefaultencoding())
        fn = self.table_name+".csv"
        fd = codecs.open(fn,"w",encoding="utf8")
        fd.write(s)
        fd.close()
        print "Wrote file", fn
    
    
class PersonLoader(Loader):
    table_name = 'TBClient'
    model = resolve_model('contacts.Person')

def objects():
    PersonLoader().load()
    
    #~ reader = csv.reader(open(,'rb'))