#import os
import os.path
#import sys
import unittest
import shutil

import lino

from lino.dbd import pickle_dbd

from lino.lib.tsttools import TestCase


from lino.plugins.addrbook import PERSONS

class Case(TestCase):
   
   def test_4a(self):
      "Creating rows from scratch"
      
      """ these are the components in PERSONS: """
      
      a = []
      for comp in PERSONS.comps:
         a.append(comp.name)
      self.assertEqualText(" ".join(a),"""\
id name fname title email phone born died partners children parents
orgs projects news changes quotes publications
""")

      "create an empty database"

      lino.initdb()
      
      "yes, also PERSONS is empty:"
      
      cursor = PERSONS.getCursor()
      
      """len() of a cursor returns the number of rows. if you call
      len() of a cursor, there will be an automatic lookup"""
      
      self.assertEqual(len(cursor),0)
      
      """but otherwise a new cursor must first be executed before you
      can see the data. You can test this using mustExecute()"""
      
      self.assertEqual(cursor.mustExecute(),True)
      cursor.executeSelect()
      self.assertEqual(cursor.mustExecute(),False)
      
      "rowcount is 0:"
      self.assertEqual(cursor.rowcount,0)
      
      "the current row is None:"
      self.assertEqual(cursor.row,None)
      # 
      
      cursor.appendRow(id=1,name="Saffre",fname="Luc",
                       born="1968-06-01")
      self.failUnless(cursor.row.IsNew())
      self.failUnless(cursor.row.IsDirty())
      self.assertEqual(cursor.row.id,1)
      
      cursor.appendRow(id=2,name="Rumma",fname="Ly",
                       born="1968-04-27")
      
      cursor.appendRow(id=3,name="Saffre",fname="Mari",
                       born="2002-04-05")
      
      cursor.close()

      #cursor = PERSONS.getCursor("id name fname parents")
      #cursor.SetCellByExpr("parents","1 2")
      #self.assertEqual(len(cursor.row.parents),2)
      #cursor.close()

      # restart is not clear code. here it is just a hack:
      lino.disconnect()
      lino.connect(pickle_dbd.Connection(self.tmpDir))

      cursor = PERSONS.getCursor()
      s = ""
      i = 0
      cursor.executeSelect()
      for row in cursor:
         i += 1
         s += row.fname + " " + row.name + "\n"
##       row = cursor.fetchone()
##       while row != None:
##          i += 1
##          s += row.fname + " " + row.name + "\n"
##          row = cursor.fetchone()
      self.assertEqualText(s,"Luc Saffre Ly Rumma Mari Saffre")
      self.assertEqual(i,3)
      self.assertEqual(len(cursor),3)
      
      #cursor = PERS2PERS.getCursor()
      ##cursor.executeSelect()
      #self.assertEqual(len(cursor),2)

      row = PERSONS.peek(1)
      self.assertEqual(row.id,1)
      self.assertEqual(row.name,"Saffre")
      self.assertEqual(row.fname,"Luc")

      # PERSONS.children is a Detail component.
      # That's why the corresponding value is a Cursor object
      
      #row.children.executeCount()

      #self.assertEqual(row.children.rowcount,1)
      
      
   def test_4b(self):
      "a first look at the demo database"

      lino.initdb()
      lino.populateDemo()

      "there are 16 persons in the demo database"
      cursor = PERSONS.getCursor()
      cursor.executeSelect()
      self.assertEqual(cursor.rowcount,16)

##       from lino.renderer import HtmlRenderer
##       writer = BufferWriter()
##       r = HtmlRenderer(writer)
##       r.ShowQuery(cursor)
##       self.assertEqualText(writer.unwrite(),"""
##       <HTML>
##       <BODY>
##       (TODO)
##       </BODY>
##       </HTML>
##       """)
      

   def setUp(self):
      self.tmpDir = os.path.join("tmp","2")
      if not os.path.exists(self.tmpDir):
         os.makedirs(self.tmpDir)
      lino.connect(pickle_dbd.Connection(self.tmpDir))
      
   def tearDown(self):
      lino.disconnect()
      shutil.rmtree(self.tmpDir)
      
      
