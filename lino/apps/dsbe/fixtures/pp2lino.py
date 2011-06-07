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

"""

import csv
import subprocess

MDB_FILE = 'PPv5MasterCopie.mdb'
MDBTOOLS_EXPORT = 'mdb-export'

def objects():
    args = [MDBTOOLS_EXPORT, MDB_FILE, 'TBClient']
    s = subprocess.check_output(args,executable=MDBTOOLS_EXPORT)
    print s
    #~ reader = csv.reader(open(,'rb'))