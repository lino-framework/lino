#coding: latin1
import os
from lino.misc import console, tsttools
from lino.oogen import Document,OoText, elements

class Case(tsttools.TestCase):
	
	def test01(self):
		"First styles"
		doc = Document("2")
		
		s = elements.Style(name="Rechts",family="paragraph",parentStyleName="Standard",className="text")
		s.append(elements.Properties(textAlign="end",justifySingleWord=False))
		doc.styles.append(s)
		
		doc.h(1,"This is a header")
		doc.p("This is a right-aligned paragraph.",styleName="Rechts")
		doc.p("Here is a standard paragraph.")
	
		oo = OoText(doc)
		oo.save()

		for fn in [ oo.outputFilename ]:
			if console.isInteractive(): # showOutput:
				os.system("start "+fn)
			else:
				self.failUnless(os.path.exists(fn))
				os.remove(fn)

if __name__ == "__main__":
	tsttools.main()
