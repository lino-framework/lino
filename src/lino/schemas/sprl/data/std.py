# coding: latin1
"""
"""


import os
from lino.misc.normalDate import ND


def populate(db,big=False):

	db.installto(globals())

	# ISO 639 : Code for the representation of names of languages
	if big:
		import languages
		languages.populate(db)
		
	if len(LANGS) == 0:
		q = LANGS.query('id name')
		setBabelLangs('en de fr')
		q.appendRow('en',('English','Englisch','Anglais')	  )
		q.appendRow('de',('German','Deutsch', 'Allemand')	  )
		q.appendRow('et',('Estonian','Estnisch','Estonien')  )
		q.appendRow('fr',('French','Französisch','Français')	  )
		q.appendRow('nl',('Dutch','Niederländisch','Neerlandais')	  )
		
		# ISO 3166 : alpha-2 country codes

		
	q = PARTYPES.query('id name')
	setBabelLangs('en de fr')
	q.appendRow('c',('Customer', 'Kunde', 'Client'))
	q.appendRow('s',('Supplier', 'Lieferant', 'Fournisseur'))
	q.appendRow('m',('Member', 'Mitglied', "Membre"))
	q.appendRow('e',('Employee', 'Angestellter', "Employé"))
	q.appendRow('d',('Sponsor', 'Sponsor', "Sponsor"))
	
	q = PRJSTAT.query('id name')
	setBabelLangs('en de')
	q.appendRow('T',('to do','zu erledigen'))
	q.appendRow('D',('done','erledigt'))
	q.appendRow('W',('waiting','wartet'))
	q.appendRow('A',('abandoned','storniert'))
	q.appendRow('S',('sleeping','schläft'))

	q = PUBTYPES.query('id name typeRefPrefix pubRefLabel')
	setBabelLangs('en de')
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

	q = PEVTYPES.query('id name')
	setBabelLangs('en de')
	q.appendRow(1,('born','geboren'))
	q.appendRow(2,('died','gestorben'))
	q.appendRow(3,('married','Heirat'))
	q.appendRow(4,('school','Schulabschluss'))
	q.appendRow(5,('other','Sonstige'))	

	if big:
		import nations
		nations.populate(db)

	if len(NATIONS) == 0:
		q = NATIONS.query('id name' )
		setBabelLangs('en')
		q.appendRow("ee","Estonia")
		q.appendRow("be","Belgium")
		q.appendRow("de","Germany")
		q.appendRow("fr","France")
		q.appendRow("us","United States of America")
		
	#print belgique
	
	if big:
		import cities_be
		cities_be.populate(db)
		
	setBabelLangs('en')
	EUR = Currencies.appendRow(id="EUR",name="Euro")
	Currencies.appendRow(id="USD",name="US Dollar")
	BEF = Currencies.appendRow(id="BEF",name="Belgian Franc")


