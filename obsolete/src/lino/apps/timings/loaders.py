## Copyright 2004-2005 Luc Saffre 

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
import sys


from lino import adamo

from lino.apps.timings.tables import *

from lino.adamo.table import DbfMirrorLoader


class ResourcesMirrorLoader(DbfMirrorLoader):
    tableClass = Resource
    tableName = "RES"
    def appendFromDBF(self,q,row):
        q.appendRow(
            id=row['IDRES'],
            name=self.dbfstring(row['NOM1'])
            )


class UsagesMirrorLoader(DbfMirrorLoader):
    tableClass = Usage
    tableName = "PTL"
    def appendFromDBF(self,q,row):
        sess = q.getSession()
        usageType = sess.peek(UsageTypes,row['TYPE'])
        resource = sess.peek(Resources,row['IDRES'])
        if resource is None:
            sess.warning("ignored PTL with empty IDRES: %r",row)
            return
        day=sess.query(Days).peek(self.dbfdate(row['DATE']))
        if day is None:
            day=sess.query(Days).appendRow(
                date=self.dbfdate(row['DATE']))
        q.appendRow(
            date=day,
            start=self.dbftime(row['QTE1']),
            stop=self.dbftime(row['QTE2']),
            resource=resource,
            type=usageType,
            remark=self.dbfstring(row['REMARQ'])
            )

LOADERS = (
    ResourcesMirrorLoader,
    UsagesMirrorLoader,
    )






