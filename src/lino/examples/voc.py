#coding: latin1

from lino.adamo.datatypes import STRING, PRICE, DATE, BOOL, INT, ROWID, MEMO

from lino.adamo.dbds.mem_dbd import MemoryConnection
from lino.adamo.table import LinkTable

languages = (
	( 'id' , 'name'),
	( 'de' , 'Deutsch'),
	( 'ee' , 'Eesti'  ),
	)

## wordTypes = (
## 	('id' ,  'name',                  'langs'),
## 	('n' ,   'Substantiv',            None),
## 	('nn',   'Substantiv (neutral)',  'de'),
## 	('nf',   'Substantiv (weiblich)', 'de'),
## 	('nm',   'Substantiv (männlich)', 'de'),
## 	('np',   'Substantiv (plural)',   None),
## 	('v',    'Verb',                  None),
## 	('adj',  'Adjektiv',              None),
## 	('adv',  'Adverb',                None),
## 	('prep', 'Präposition',           None),
## 	('post', 'Postposition',          'ee'),
## 	('pron', 'Pronomen',              None),
## 	('num',  'Zahlwort',              None),
## 	('etc',  'Sonstige',              None),
## 	)

#	('expr', 'Ausdruck', None),
#	('exam', 'Beispiel', None),
#	('co',   'Konzept', None),
	
## linkTypes = (
## 	( 'id' , 'name'),
## 	( 'syn' , 'synonym'),
## 	( 'eth' , 'ethymologic'  ),
## 	)

class Language:
	def init(self,table):
		table.addField("id",STRING)
		table.addField("name",STRING)
		
	def provideWord(self,s):
		return WORDS.provideRow(lang=self,word=s)

class German(Language):
	def provideWord(self,s):
		if s.startswith("der "):
			
		return WORDS.provideRow(lang=self,word=s)
	

class Word:
	def init(self,table):
		# table.addField("id",ROWID)
		table.addPointer("lang",Language)
		table.addField("word",STRING,width=2)
		#table.addPointer("type",WordType)
		#table.addField("info",STRING)
		table.setPrimaryKey("lang word")

	def __str__(self):
		txt = self.word
## 		if self.lang.id == "de":
## 			if self.type.id == "nm":
## 				txt = "der " + txt
## 			elif self.type.id == "nf":
## 				txt = "die " + txt
## 			elif self.type.id == "nn":
## 				txt = "das " + txt
		# txt = self.lang.id+":"+txt+ ":"
		return txt

class Concept:
	def init(self,table):
		table.addField("id",ROWID)
		table.addBabelField("description",MEMO)
	def __str__(self):
		txt = "[%d]" % self.id
 		q = W2C.query()
 		q.setSamples(concept=self)
 		for w2c in q.instances():
 			txt += " " + str(w2c.word)
			if w2c.meaning:
				txt += " (%s)" % str(w2c.meaning)
		return txt


class W2C:	
	def init(self,table):
		table.addPointer("concept",Concept)
		table.addPointer("word",Word)
		table.addField("meaning",STRING)
			

## class WordType:
## 	def init(self,table):
## 		table.addField("id",STRING,width=4)
## 		table.addField("name",STRING)
## 		table.addField("langs",STRING)

## class LinkType:
## 	"type of link between two words"
## 	def init(self,table):
## 		table.addField("id",STRING,width=3)
## 		table.addField("name",STRING)

## class Word2Word:
## 	def init(self,table):
## 		table.addPointer('type',LinkType)
		
## class EstonianWord(Word):
## 	def init(self,table):
## 		Word.init(self,table)
	 
## class GermanWord(Word):
## 	pass
	 
def makeDatabase(conn):
	"Instantiate Database and declare tables"
	from lino.adamo.database import Database
	db = Database(conn)
	db.addTable("LANGS",Language, MemoryConnection(languages))
	#db.addTable("WORDTYPES",WordType, MemoryConnection(wordTypes))
	#db.addTable("LINKTYPES",LinkType, MemoryConnection(linkTypes))
	
	db.addTable("CONCEPTS",Concept)
	db.addTable("WORDS",Word)
	db.addTable("W2C",W2C)
	#db.addLinkTable("W2W",Word,Word,Word2Word)
	db.startup()
	return db

def startDatabase():
	"""start the database, connect it and create empty tables
	returns a ready to use database handle with empty tables
	"""
	from lino.adamo.dbds.sqlite_dbd import Connection
	conn = Connection("tmp.db")
	
	db = makeDatabase(conn)

	# Create the empty tables
	db.createTables()
	return db

## def de2ee_append(w1,w2,type1,type2=None):
## 	type1 = WORDTYPES[type1]
## 	if type2 is None:
## 		type2 = type1
## 	else:
## 		type2 = WORDTYPES[type2]
		
## 	w1 = WORDS.provideRow(lang=LANGS['de'],
## 								 word=w1,
## 								 type=type1)
## 	w2 = WORDS.provideRow(lang=LANGS['ee'],
## 								 word=w2,
## 								 type=type2)
## 	print "%s = %s" % (w1,w2)
	
## 	W2W.appendRow(p=w1,c=w2,type=LINKTYPES['syn'])

## def showtr(word):
## 		q = W2W.query('type c')
## 		q.setSample(p=word)
## 		for w2w in q.instances():
## 			txt += "\n" + str(w2w.c) 
			
## 		q = W2W.query('type p')
## 		q.setSample(c=word)
## 		for w2w in q.instances():
## 			txt += "\n" + str(w2w.p) 
	
def de2ee_append(s1,s2,m1=None,m2=None):
	c = CONCEPTS.appendRow()
	w1 = DE.provideWord(s1)
	w2 = EE.provideWord(s2)
	#w1 = WORDS.provideRow(lang=DE,word=w1)
	#w2 = WORDS.provideRow(lang=EE,word=w2)
	W2C.appendRow(concept=c,word=w1,meaning=m1)
	W2C.appendRow(concept=c,word=w2,meaning=m2)

def play(db):
	globals().update(db.tables)
	globals()['DE'] = LANGS['de']
	globals()['EE'] = LANGS['ee']
## 	WORDTYPES.query(columnList="id name langs")\
## 											 .render(columnWidths="4 30 10")
## 	LINKTYPES.query(columnList="id name").render()


## 	de2ee_append("Chor","koor","nm","n")
## 	de2ee_append("Sahne","koor","nf","n")
## 	de2ee_append("Schale","koor","nf","n")
	
	de2ee_append("der Chor","koor,koori",None,"laulu~")
	de2ee_append("die Sahne","koor,koore,koort",None,"kohvi~")
	de2ee_append("die Schale","koor,koore,koort",None,"muna~")
	de2ee_append("die Rinde","koor,koore,koort",None,"muna~")

	db.commit()
	
	q = CONCEPTS.query()
	print "This database contains %d concepts!" % len(q)
	for c in q.instances():
		print c

	# koor = WORDS[lang='ee',word='koor']

def main():
	db = startDatabase()
	play(db)
	db.shutdown()
	
if __name__ == "__main__":
	main()
