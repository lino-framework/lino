#coding: latin1
import os
from lino.oogen import Document,OoText,OoSpreadsheet

showOutput = True

if __name__ == "__main__":
	doc = Document("test")
	doc.h(1,"Generating OpenOffice documents")
	doc.p("Here is a table:")
	t = doc.table()
	t.addColumn()
	t.addColumn()
	t.addRow(cells=("Kunde","Datum"))
	t.addRow(cells=("Hinz","2004-11-16"))
	t.addRow(cells=("Kunz","2004-11-17"))
	
	doc.p("Here is another paragraph:")
	
	oo = OoText(doc)
	oo.save()
	
	oo = OoSpreadsheet(doc)
	oo.save()

	if showOutput:
		os.system("start test.sxw")
		os.system("start test.sxc")
