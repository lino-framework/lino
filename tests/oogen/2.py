#coding: latin1
import os
from lino.oogen import Document,OoText

showOutput = True

if __name__ == "__main__":
	doc = Document("test")
	doc.addStyle(name="Rechts",textAlign="end",parentStyle="Text body"
	doc.h(1,"Rechnung Nr. 040235")
	doc.p("Datum: 10. Dezember 2004",textAlign="end")
	t = doc.table()
	t.addColumn()
	t.addColumn()
	t.addRow("Kunde","Datum")
	t.addRow("Hinz","2004-11-16")
	t.addRow("Kunz","2004-11-17")
	
	doc.p("Here is another paragraph.")
	
	oo = OoText(doc)
	oo.save()

	if showOutput:
		os.system("start test.sxw")
