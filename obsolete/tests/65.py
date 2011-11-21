# coding: latin1

## Copyright 2004-2005 Luc Saffre

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



import unittest
from cStringIO import StringIO

from lino.oogen.elements import H,P

class Case(unittest.TestCase):
	
	def test01(self):
		"low-level tests about xml generation"
		
		e = P("This is a paragraph")
		s = StringIO()
		e.__xml__(s.write)
		self.assertEqual(s.getvalue(),"""\
<text:p>This is a paragraph</text:p>""")
		
		e = P("This is a paragraph",styleName="Standard")
		s = StringIO()
		e.__xml__(s.write)
		self.assertEqual(s.getvalue(),"""\
<text:p text:style-name="Standard">This is a paragraph</text:p>""")

		e = H(1,"This is a header")
		s = StringIO()
		e.__xml__(s.write)
		self.assertEqual(s.getvalue(),"""\
<text:h text:style-name="Heading 1" text:level="1">This is a header</text:h>""")

if __name__ == '__main__':
	unittest.main()

