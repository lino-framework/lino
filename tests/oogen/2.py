#coding: latin1
import os
import unittest
from lino.misc import console
from lino.oogen import Document,OoText, elements

class Case(unittest.TestCase):
	
	generated_files = ("2.sxw", )
	
	def test01(self):
		"First styles"
		doc = Document("2")
		
		s = elements.Style(name="Rechts",family="paragraph",parentStyleName="Default")
		s.append(elements.Properties(textAlign="end"))
		doc.styles.append(s)
		
		doc.h(1,"Rechnung Nr. 040235")
		doc.p("Datum: 10. Dezember 2004",styleName="Rechts")
		t = doc.table()
		t.addColumn()
		t.addColumn()
		t.addRow("Kunde","Datum")
		t.addRow("Hinz","2004-11-16")
		t.addRow("Kunz","2004-11-17")
		
		doc.p("Here is another paragraph.")
	
		oo = OoText(doc)
		oo.save()

		for fn in self.generated_files:
			if console.isInteractive(): # showOutput:
				os.system("start "+fn)
			else:
				self.failUnless(os.path.exists(fn))
				os.remove(fn)

if __name__ == "__main__":
	unittest.main()
