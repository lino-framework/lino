#coding: latin1

"""
http://www.loc.gov/standards/iso639-2/

http://www.loc.gov/standards/iso639-2/ISO-639-2_values_8bits.txt

To read this file, please note that one line of text contains one
entry. An alpha-3 (bibliographic) code, an alpha-3 (terminologic) code
(when given), an alpha-2 code (when given), an English name, and a
French name of a language are all separated by pipe (|)
characters. The Line terminator is the LF character.
"""

import os
from lino.adamo.datatypes import DataVeto

dataDir = os.path.dirname(__file__)

def populate(db):
	#print db
	db.installto(globals())
	setBabelLangs('en fr')
	ds = LANGS.query()
	f = file(os.path.join(dataDir,'ISO-639-2_values_8bits.txt'))
	for line in f.readlines():
		a = line.split('|')
		if len(a) > 2:
			bibliographic = a[0]
			terminologic = a[1]
			alpha2 = a[2]
			name_en = a[3]

			#if len(a) > 4:
			name_fr = a[4]
			#print (name_en,name_fr)
			if len(alpha2):
				try:
					LANGS.appendRow(id=alpha2,
										 name=(name_en,name_fr))
				except DataVeto,e:
					print e
		elif len(line.strip()):
			print "ignored:", line

	f.close()
