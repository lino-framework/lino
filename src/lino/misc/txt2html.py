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

import htmlentitydefs

from twisted.web.html import escape

def html_encode(txt):
	txt2 = ''
	for c in txt:
		o = ord(c)
		if o < 128:
			txt2 += c
		else:
			try:
				txt2 += "&%s;" % htmlentitydefs.codepoint2name[o]
			except KeyError:
				txt2 += "&#%d;" % o
	return txt2
		

def txt2html(txt):
    return html_encode(txt)


