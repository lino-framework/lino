#coding: latin1

label = 'A Collection of Lino Demo Data'

from lino.schemas.sprl import demo 
#from lino.schemas.sprl.data import langs

def populate(sess):
	
	#import etc1
	#etc1.populate(db)

	#langs.populate(db)
	demo.populate(sess,big=True)
	
	sess.installto(globals())
	
	from lino.schemas.sprl.data import nations_de
	nations_de.populate(sess)
	

	de = LANGS.peek('de')
	en = LANGS.peek('en')

	q = ORGS.query('name website email phone fax')
	q.appendRow(
		"VHS der Ostkantone",
		'http://www.vhs-ostkantone.org/')
	q.appendRow('Chudoscnik Sunergia','http://www.sunergia.be/')
	q.appendRow("Belgischer Rundfunk","http://www.brf.be/")
	q.appendRow("Grenz Echo","http://www.grenzecho.be/")
	q.appendRow("NetEcho","http://www.netecho.be/")
	q.appendRow("Die Raupe","http://www.raupe.be/")
	#q.appendRow("","")


	sess.commit()
