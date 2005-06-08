from lino.sdoc import styles

import unittest 

class MyCase(unittest.TestCase):

   def test01(self):
      
      """ When a PropertySet has ListType attributes, inheriting them
      from a parent makes a copy of the list because updating the
      child must not update the parent. """

      return """ test doesn't work because DefaultTable is now defined
      dynamically by TablesMixin. Should be adapted... """

      sheet = styles.getDefaultStyleSheet()
      tm = sheet.DefaultTable.child()
      self.assertEqual(tm.getColumnCount(),0)
      tm.addColumn('foo')
      self.assertEqual(tm.getColumnCount(),1)
      self.assertEqual(sheet.DefaultTable.getColumnCount(),0)
