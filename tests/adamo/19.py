# coding: latin1
## Copyright Luc Saffre 2003-2005

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
20040513



"""

from lino.misc.tsttools import TestCase, main
from lino.adamo import *
from lino import adamo

## from lino.adamo.rowattrs import Field, BabelField, Pointer, \
##    RowAttribute

# from lino.adamo.table import Table


class Nations(Table):
    def init(self):
        self.addField('id',STRING(width=2))
        self.addBabelField('name',STRING)
        self.addField('area',INT)
        self.addField('population',INT)
        self.addField('curr',STRING)
        self.addField('isocode',STRING)

##  def validateRow(self,row):
##      if len(row.id) != 2:
##          return "id must be 2 chars"
##          #raise DataVeto("Nation.id must be 2 chars")
        
##  def getRowLabel(self,row):
##      return row.name_en
        
class Cities(Table):
    
    def init(self):
        self.addField('id',ROWID)
        self.addPointer('nation',Nations).setDetail('cities',
                                                    orderBy='name')
        self.addField('name',STRING)
        self.addField('zipCode',STRING)
        self.addField('inhabitants',INT)
        self.setPrimaryKey("nation id")
        
    class Instance(Table.Instance):
        def getLabel(self):     
            if self.nation is None:
                return self.name
            return self.name + " (%s)" % self.nation.id
        

class Contacts:
    def init(self):
        self.addField('email',EMAIL)
        self.addField('phone',STRING)

class Addresses:
    def init(self):
        self.addPointer('nation',Nations)
        self.addPointer('city',Cities)
        self.addField('street',STRING)

    def after_city(self,row):
        if row.city is not None:
            row.nation = row.city.nation

class Organisations(Table,Contacts,Addresses):
    "An Organisation is any named group of people."
    def init(self):
        self.addField('id',ROWID, doc="the internal id number")
        self.addField('name',STRING)
        Contacts.init(self)
        Addresses.init(self)


class MyPlugin(SchemaPlugin):
    
    def defineTables(self,schema):
        schema.addTable(Nations)
        schema.addTable(Cities)
        schema.addTable(Organisations)
        


class Case(TestCase):
    
    def test01(self):

        schema = Schema()
        schema.addPlugin(MyPlugin())

        sess = schema.quickStartup(langs='en de fr')

        #sess.setBabelLangs('en')
        
        ds = sess.query(Nations)

        be = ds.appendRow(id="be", name="Belgium")
        de = ds.appendRow(id="de", name="Germany")

        be.lock()
        de.lock()

        
        sess.setBabelLangs('de')
        self.assertEqual(be.name,None)
        be.name = "Belgien"
        de.name = "Deutschland"
        
        sess.setBabelLangs('fr')
        be.name = "Belgique"
        de.name = "Allemagne"

        be.unlock()
        de.unlock()
        
        
        be = sess.query(Nations).peek('be')
        #print ctx._db._connection.stopDump()
        #print be._values['name']
        
        sess.query(Cities).appendRow(nation=be,name="Eupen")
        
        sess.setBabelLangs('de')
        self.assertEqual(be.name,'Belgien')
        
        sess.setBabelLangs('fr')
        self.assertEqual(be.name,'Belgique')
        
        sess.setBabelLangs('en')
        self.assertEqual(be.name,'Belgium')
        
        sess.setBabelLangs('en de')
        self.assertEqual(be.name,['Belgium','Belgien'])
        
        sess.shutdown()

        

        
if __name__ == '__main__':
    main()

