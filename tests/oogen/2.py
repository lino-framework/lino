#coding: latin1
## Copyright Luc Saffre 2003-2004.

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

import os
from lino.ui import console, tsttools
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
