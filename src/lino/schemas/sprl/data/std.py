# coding: latin1
"""
"""


import os
from forum.normalDate import ND


def populate(sess,big=False):

	#db.installto(globals())

	# ISO 639 : Code for the representation of names of languages
	if big:
		import languages
		languages.populate(sess)
		
	if len(sess.tables.LANGS) == 0:
		q = sess.tables.LANGS.query('id name')
		sess.setBabelLangs('en de fr')
		#q.startDump()
		q.appendRow('en',('English','Englisch','Anglais')	  )
		q.appendRow('de',('German','Deutsch', 'Allemand')	  )
		q.appendRow('et',('Estonian','Estnisch','Estonien')  )
		q.appendRow('fr',('French','Französisch','Français')	  )
		q.appendRow('nl',('Dutch','Niederländisch','Neerlandais')	  )
		#print len(q)
		#print len(sess.tables.LANGS)
		#print q.stopDump()
		# ISO 3166 : alpha-2 country codes

		
	q = sess.tables.PARTYPES.query('id name')
	sess.setBabelLangs('en de fr')
	q.appendRow('c',('Customer', 'Kunde', 'Client'))
	q.appendRow('s',('Supplier', 'Lieferant', 'Fournisseur'))
	q.appendRow('m',('Member', 'Mitglied', "Membre"))
	q.appendRow('e',('Employee', 'Angestellter', "Employé"))
	q.appendRow('d',('Sponsor', 'Sponsor', "Sponsor"))
	
	q = sess.tables.PRJSTAT.query('id name')
	sess.setBabelLangs('en de')
	q.appendRow('T',('to do','zu erledigen'))
	q.appendRow('D',('done','erledigt'))
	q.appendRow('W',('waiting','wartet'))
	q.appendRow('A',('abandoned','storniert'))
	q.appendRow('S',('sleeping','schläft'))

	q = sess.tables.PUBTYPES.query('id name typeRefPrefix pubRefLabel')
	sess.setBabelLangs('en de')
	q.appendRow("book",
					('Book','Buch')        ,
					'ISBN: ',
					('page','Seite')  )
	q.appendRow("url" , ('Web Page','Webseite')    ,
					'http:' , ( None, None)   )
	q.appendRow("cd"  , ('CompactDisc', 'CD') , 'cddb: ',
					('track','Stück') )
	q.appendRow("art" , ('Article','Artikel')     ,
					''      , ('page','Seite')  )
	q.appendRow("mag" , ('Magazine','Zeitschrift')    ,
					''      , ('page','Seite')  )
	q.appendRow("sw"  , ('Software','Software')    ,
					''      , (None,None)    )

	q = sess.tables.PEVTYPES.query('id name')
	sess.setBabelLangs('en de')
	q.appendRow(1,('born','geboren'))
	q.appendRow(2,('died','gestorben'))
	q.appendRow(3,('married','Heirat'))
	q.appendRow(4,('school','Schulabschluss'))
	q.appendRow(5,('other','Sonstige'))	

	q = sess.tables.USERS.query('id firstName name')
	q.appendRow("luc", "Luc", "Saffre")
	q.appendRow("james", "James", "Bond")
	
	if big:
		import nations
		nations.populate(sess)

	if len(sess.tables.NATIONS) == 0:
		q = sess.tables.NATIONS.query('id name' )
		sess.setBabelLangs('en')
		q.appendRow("ee","Estonia")
		q.appendRow("be","Belgium")
		q.appendRow("de","Germany")
		q.appendRow("fr","France")
		q.appendRow("us","United States of America")
		
	#print belgique
	
	if big:
		import cities_be
		cities_be.populate(sess)
		
	sess.setBabelLangs('en')
	CURR = sess.tables.Currencies
	EUR = CURR.appendRow(id="EUR",name="Euro")
	CURR.appendRow(id="USD",name="US Dollar")
	BEF = CURR.appendRow(id="BEF",name="Belgian Franc")


