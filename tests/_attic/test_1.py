import unittest
import re

import lino

from lino.dbd.sql_dbd import ConsoleHost
from lino.dbd.mysql_dbd import Connection

from lino.query import Query
from lino.dbd.cursor import DetailColumn


from tsttools import TestCase

from lino import pin2sql

from lino.plugins.addrbook import PERSONS
from lino.plugins.news import NEWS
from lino.plugins.sdk import METHODS, CHANGES, DBITEMS, CLASSES

class TestHost(ConsoleHost):
   """

   Simulates a host. The requests are not sent to any host. The
   testing code must retrieve them using unwrite() before any further
   request.
   
   """
   def __init__(self):
      self.log = ''

   def write(self,msg):
      self.log += msg + ";\n"
      
   def unwrite(self):
      log = self.log
      self.log = ''
      return log

##    def flush(self):
##       if self.log != None:
##          sys.stdout.write(self.log)
##       self.log = None


class MyCase(TestCase):

   def setUp(self):
      lino.connect(Connection(TestHost()))

   def tearDown(self):
      lino.disconnect()
      

   def test01(self):
      """
      some tests on PERSONS table
      """
      
      # Table.expr2row() returns a row of this table
      # the row is not completely known
      # but contains at least the identifier
      
      # 20021223 : expr2value() and expr2row() are broken. I think I
      # will solve the parser problem differently...
      
##       row = PERSONS.expr2row("1")
##       self.assertEqual(row.id,1)
##       try:
##          # foo is not a valid id for PERSONS
##          row = PERSONS.expr2row("foo")
##       except ValueError:
##          pass
##       else:
##          fail("must raise ValueError.")

      # just test if the component exists...
      c = PERSONS.FindComponent("name")


      query = Query(PERSONS)
      try:
         rowlist = query.expr2rowlist("foo")
      except ValueError:
         pass
      else:
         fail("must raise ValueError.")

         
   def test02(self):
      "width of LANG.id"
      from lino.system import LANG
      c = LANG.FindComponent("id")
      self.assertEqual(c.type.width,3)
      
         

   def test03(self):
      "using SetCellByExpr() to set value of a detail cell"
      cursor = NEWS.getCursor()
      
      # this cursor has a column "groups" which is a DetailColumn:
      self.failUnless(isinstance(cursor.FindColumn("groups"),
                                 DetailColumn))

      # create a new empty NEWS item
      cursor.append()
      
      #
      cursor.row.id = 1
      # cursor.SetCellByExpr("id","1")
      self.assertEqual(cursor.row.id,1)

      try:
         cursor.row.foo = 1
         self.fail("should have raised NameError")
      except NameError:
         pass
      
##       cursor.SetCellByExpr("groups","ng1 ng2")
##       groupsColumn = cursor.FindColumn("groups")
##       self.assertEqual(groupsColumn.slaveCursor.query.slices["p"],
##                        cursor.row)
      
      # the value of a DetailColumn is a Cursor:
      # I want that this NEWS item is published in two newsgroups.
      # create two NEWS2NEWSGROUPS rows
      groupsCursor = cursor.row.groups
      groupsCursor.append(group_id="ng1")
      groupsCursor.append(group_id="ng2")
      
      # there are now two rows in my current row:
      self.assertEqual(len(groupsRows),2)
      firstRow = groupsRows[0]

      # firstRow is a NEWS2NEWSGROUPS row.
      # NEWS2NEWSGROUPS rows have two components "p" and "c".
      # "p" points back to this NEWS row:
      self.assertEqual(firstRow.p,
                       cursor.row)
      
      # "c" is the join in NEWS2NEWSGROUPS which points to
      # NEWSGROUPS

      newsgroupsRow = firstRow.c
      
      # child now represents the NEWSGROUPS Row ng1 :
      
      self.assertEqual(newsgroupsRow.id,
                       "ng1")
      

   def test04(self):
      """
      does a detail header field create correct SQL for the LinkTable?
      
      """
      # if i have a .pin file with the following input...
      input = """
handler: NEWS
id: 1
date: 2002-08-08
title: Test
groups: lino-test lino-devel

The abstract.

The body.
"""
      
      # ... then Lino should generate the following SQL to create the
      # rows in the database
      
      expectedOutput = """
      INSERT INTO NEWS (
        title,
        abstract,
        body,
        date,
        id,
        author_id,
        project_id,
        lang_id
      ) VALUES (
          "Test",
          "The abstract. ",
          "The body. <p>",
          "2002-08-08",
          1,
          NULL,
          NULL,
          NULL
       );
      INSERT INTO NEWS2NEWSGROUPS ( p_id, c_id )
         VALUES ( 1, "lino-test" );
      INSERT INTO NEWS2NEWSGROUPS ( p_id, c_id )
         VALUES ( 1, "lino-devel" );
      """
      pin2sql.parsestring(lino,input)

      output = lino.conn.host.unwrite()
      
      self.assertEqualText(output,expectedOutput)

   def test05a(self):
      """
      simple create table
      """
      
      expectedOutput = """CREATE TABLE METHODS (
        title VARCHAR(50),
        abstract TEXT,
        body TEXT,
        name VARCHAR(50) NOT NULL,
        class_id VARCHAR(50) NOT NULL,
        PRIMARY KEY (name, class_id)
      );"""
      METHODS.createTable()
      self.assertEqualText(lino.conn.host.unwrite(),
                           expectedOutput)


   def test05b(self):
      expectedOutput = """CREATE TABLE PERSONS (
        id BIGINT NOT NULL,
        name VARCHAR(50),
        fname VARCHAR(50),
        title VARCHAR(50),
        email VARCHAR(50),
        phone VARCHAR(50),
        born DATE,
        died DATE,
        PRIMARY KEY (id)
      );
      """
      PERSONS.createTable()
      self.assertEqualText(lino.conn.host.unwrite(),
                           expectedOutput)
      
   def test05c(self):
      expectedOutput = """CREATE TABLE NEWS (
        title VARCHAR(50),
        abstract TEXT,
        body TEXT,
        date DATE,
        id BIGINT NOT NULL,
        author_id BIGINT,
        project_id BIGINT,
        lang_id CHAR(3),
        PRIMARY KEY (id)
      );
      """
      NEWS.createTable()
      #lino.conn.create_table(lino.plugins.news.NEWS)
      self.assertEqualText(lino.getConnection().host.unwrite(),
                           expectedOutput)
      #self.assertEqual(output,expectedOutput)


   def test06(self):
      cursor = PERSONS.getCursor()
      cursor.append(id=1,name="Saffre",fname="Luc")
      output = lino.getConnection().host.unwrite()
      expectedOutput = """INSERT INTO PERSONS
      (id, name, fname)
      VALUES (1, "Saffre", "Luc");
      """
      
   def test07(self):
      "setting a join to a table with complex id (CHANGES.version)"
      input = """
handler: CHANGES
date: 2002-08-17
title: Test
version: 0.1.0

The abstract.

The body.
"""
      # string "0.1.0" has to be split into its 3 elements
      
      expectedOutput = """INSERT INTO CHANGES (
        title, abstract, body,
        date, id,
        version_major, version_minor, version_release,
        author_id
      ) VALUES (
        "Test", "The abstract. ", "The body.  <p>",
        "2002-08-17",
        NULL, 0, 1, 0, NULL );"""

      pin2sql.parsestring(lino,input)

      output = lino.getConnection().host.unwrite()
      
      self.assertEqualText(output,expectedOutput)

   def test08(self):
      "sticky fields"
      cursor = CHANGES.getCursor()
      # create a first row:
      cursor.append()
      cursor.row.id = 1
      cursor.row.title = "This is the title"
      cursor.row.date = "2002-08-21"
      cursor.row.version = (0,1,2)
      
      self.assertEqual(cursor.row.id,1)
      self.assertEqual(cursor.row.date,"2002-08-21")
      self.assertEqual(cursor.row.version.major,0)
      self.assertEqual(cursor.row.version.minor,1)
      self.assertEqual(cursor.row.version.release,2)
      
      # create a second row, specifying current row as template:
      cursor.appendAsCopy(cursor.row)
      
      # non-sticky fields are empty:
      self.assertEqual(cursor.row.id,None)
      self.assertEqual(cursor.row.title,None)
      
      # but sticky values has been copied:
      self.assertEqual(cursor.row.date,"2002-08-21")
      self.assertEqual(cursor.row.version.major,0)
      self.assertEqual(cursor.row.version.minor,1)
      self.assertEqual(cursor.row.version.release,2)
      
   def test09(self):
      "SuperMemoTable"
      cursor = DBITEMS.getCursor()
      
   def test10(self):
      "found 3 components instead of 1"
      cursor = CLASSES.getCursor() 
      cursor.append()
      cursor.row.file = "test.inc.php"

   def test11(self):
      pass
   



## def suite():
##     l = [
##         unittest.makeSuite(MyCase),
##     ]
##     return unittest.TestSuite(l)

## if __name__ == '__main__':
##     runner = unittest.TextTestRunner()
##     runner.run(suite())
 

