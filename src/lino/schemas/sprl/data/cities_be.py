"""
"""

import csv
import os
from lino.adamo.datatypes import DataVeto


dataDir = os.path.dirname(__file__)

def populate(db):
	db.installto(globals())
	be = NATIONS.peek('be')
	#print be
	f = file(os.path.join(dataDir,'belgzip.csv'),'rb')
	r = csv.reader(f)
	r.next()
	cities = be.cities
	#print cities
	for (name,zip) in r:
		cities.appendRow(name=name,zipCode=zip)

	
if __name__ == '__main__':
	from lino.schemas.sprl.sprl import Schema
	from lino.adamo import quickdb
	db = quickdb(Schema())
	db.createTables()
	populate(db)
	be = NATIONS.peek('be')
	print "%d cities in Belgium" % len(be.cities)
	
