#coding: latin1
# Luc Saffre 20041208

import os
import unittest
from lino.misc import console
from lino.oogen import Document,OoText,OoSpreadsheet





class Case(unittest.TestCase):
	
	generated_files = ("1.sxw", "1.sxc")
	
	def test01(self):

		doc = Document("1")
		doc.h(1,"Generating OpenOffice documents")
		doc.p("Here is a table:")
		t = doc.table()
		t.addColumn()
		t.addColumn()
		t.addRow("Kunde","Datum")
		t.addRow("Hinz","2004-11-16")
		t.addRow("Kunz","2004-11-17")
	
		doc.p("Here is another paragraph.")
	
		oo = OoText(doc)
		oo.save()
	
		oo = OoSpreadsheet(doc)
		oo.save()

		for fn in self.generated_files:
			if console.isInteractive(): # showOutput:
				os.system("start "+fn)
			else:
				self.failUnless(os.path.exists(fn))
				os.remove(fn)

if __name__ == "__main__":
	unittest.main()
