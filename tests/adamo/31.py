#coding: latin1

## Copyright Luc Saffre 2003-2004.

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
discovering and extending Lars M. Garshol's dbfreader.py
"""
import os
from lino.ui import console
from lino.misc import tsttools

from lino.adamo import *
from lino.adamo import beginQuickSession
from lino.tools.dbfreader import DBFFile

from lino.schemas.sprl.addrbook import Partners,\
     Cities, Nations, Currencies, PartnerTypes, Persons
from lino.schemas.sprl.races import Races, Participants
from lino.schemas.sprl.babel import Languages


class BasePlugin(SchemaPlugin):
    def defineTables(self,schema):
        #schema.addTable(PartnerTypes("PRT"))
        #schema.addTable(Currencies("DEV"))
        #schema.addTable(Languages("LNG"))
        #schema.addTable(Cities("PLZ"))
        #schema.addTable(Nations("NAT"))
        #schema.addTable(Partners("PAR"))
        schema.addTable(Persons("PAR"))
        schema.addTable(Races("RAL"))
        schema.addTable(Participants("POS"))
        
        
        
def populate(sess):
    """
    Create some data and play with it
    """
    sess.installto(globals())

    dbf = DBFFile(r'c:\temp\par.dbf')
    dbf.open()
    for p in dbf:
        PAR.appendRow(name=p['FIRME'],
                      firstName=p['VORNAME'])
        if p.recno() > 30:
            break
    dbf.close()
    
    sess.commit()


def query(sess):
    """
    Create some data and play with it
    """
    sess.installto(globals())

    rpt = PAR.report(orderBy="name firstName",
                     pageLen=10)
    sess.showReport(rpt)


class Case(tsttools.TestCase):
    
    def test01(self):
        schema = Schema(label="ERTK report generator")
        schema.addPlugin(BasePlugin())

        sess = beginQuickSession(
            schema,
            populator=populate,
            isTemporary=True)

        query(sess)

        sess.shutdown()



        
        
if __name__ == "__main__":
    tsttools.main()
