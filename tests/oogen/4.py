#coding: latin1
import os
from lino.misc import console, tsttools
from lino.oogen import Document,OoText, elements

class Case(tsttools.TestCase):
	
	def test01(self):
		"First styles"
		doc = Document("rechnung")
		
		doc.styles.append(elements.Style(
			elements.Properties(textAlign="end",justifySingleWord=False),
			name="Rechts",family="paragraph",parentStyleName="Standard",className="text"))
		
		doc.h(1,"Rechnung Nr. 040235")
		doc.p("Datum: 10. Dezember 2004",styleName="Rechts")
		
		t = doc.table()
		t.addColumn()
		t.addColumn()
		t.addColumn()
		t.addColumn()
		t.addRow("Bezeichnung", "Menge", "Stückpreis", "Preis")
		t.addRow("Tisch","1","15","15")
		t.addRow("Stuhl","4","10","40")
		
		doc.p("Alle Preise in €.")
		doc.p("Zahlungsbedingungen: ...")
	
		oo = OoText(doc)
		oo.save()
		
		self.checkGeneratedFiles(oo.outputFilename)

if __name__ == "__main__":
	tsttools.main()
