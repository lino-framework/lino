# coding: latin1
"""
"""


import os
from lino.adamo import quickdb
from sprl import Schema



def populate(db,big=False):
	from lino.schemas.sprl.data import std,demo1
	std.populate(db,big)
	demo1.populate(db,big)


		
def getDemoDB(populator=populate,
				  langs=None,
				  isTemporary=True,
				  verbose=False,
				  **kw):
	schema = Schema(**kw)
	db = quickdb(schema,
					 langs=langs,
					 isTemporary=isTemporary,
					 verbose=verbose)
	db.createTables()
	if populator:
		populator(db)
	return db


if __name__ == '__main__':
	db = getDemoDB()
	db.installto(globals())
	for partner in PARTNERS.query(orderBy=name):
		print partner
	db.shutdown()
