# coding: latin1
"""
"""


import os
from lino.adamo import quickdb
from sprl import Schema



def populate(sess,big=False):
	from lino.schemas.sprl.data import std,demo1
	std.populate(sess,big)
	demo1.populate(sess,big)


		
def beginSession(populator=populate,
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
	sess = db.beginSession()
	if populator:
		populator(sess)
	return sess

# old name:
getDemoDB = beginSession

if __name__ == '__main__':
	sess = beginSession()
	#db.installto(globals())
	for partner in sess.context.tables.PARTNERS.query(orderBy="name"):
		print partner
	sess.shutdown()
