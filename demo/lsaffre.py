#coding: latin1

"""\
Usage : lsaffre.py [options] 

This starts the web server who serves the content at
http://lsaffre.dyndns.org

Options:
  
  -p PORT, --port PORT     alternate PORT where to listen
                           (default is 8080)
  -b, --batch              don't start a browser 
  -n, --skip-test          skip integrity check of foreign databases
  -h, --help               display this text
"""


import sys, getopt, os

from lino.adamo.dbds.sqlite_dbd import Connection
#from lino.adamo.ui import UI
from lino.adamo.ui import UI

#from lino.adamo.twisted_ui import WebServer
from lino.schemas.sprl.sprl import Schema
from tls import sprlwidgets
from tls.widgets import WidgetFactory

from lino.adamo.database import Database
from lino.misc.my_import import my_import

from tls.server import WebServer

if os.name == 'nt':
	wwwRoot = r'u:\htdocs\lsaffre'
	dbRoot = r'u:\tim2lino'
else:
	#wwwRoot = '/mnt/wwwroot'
	#dbRoot = '/mnt/dbroot'
	wwwRoot = '/var/lino/wwwroot'
	dbRoot = '/var/lino/dbroot'
	
class DBinfo:
	def __init__(self,name,label,langs,dbfile,staticDirs):
		self.name = name
		self.langs = langs
		self.label = label
		self.dbfile = dbfile
		self.staticDirs = staticDirs


def TIMtree(root):
	return {
		'files': root ,
		'images': os.path.join(root,'images') ,
		#'thumbnails': os.path.join(root,'thumbnails') ,
		}


dbinfos = []

dbinfos.append(DBinfo(
	'luc',
	label="Lucs Heimatseite",
	langs='de en fr et',
	dbfile = os.path.join(dbRoot,'luc.db'),
	staticDirs = TIMtree(wwwRoot)))

dbinfos.append(DBinfo(
	'tim',
	label="Die TIM-Webseite",
	langs='de en',
	dbfile = os.path.join(dbRoot,'tim.db'),
	staticDirs = TIMtree(os.path.join(wwwRoot,'tim'))))

dbinfos.append(DBinfo(
	'lino',
	label="The Lino Project",	
	langs='en',
	dbfile = os.path.join(dbRoot,'comp.db'),
	staticDirs = TIMtree(os.path.join(wwwRoot,'comp'))))



if __name__ == '__main__':

	port = 8080
	showOutput = False
	verbose = True
	skipTest = False
	demoDir = os.path.dirname(__file__)

	try:
		opts, args = getopt.getopt(sys.argv[1:],
											"?hp:bnq",
											["help", "port=","batch",
											 "skip-test", "quiet"])

	except getopt.GetoptError,e:
		print __doc__
		print e
		sys.exit(-1)

## 	if len(args) < 1:
## 		print __doc__
## 		sys.exit(-1)

	
	for o, a in opts:
		if o in ("-?", "-h", "--help"):
			print __doc__
			sys.exit()
		elif o in ("-p", "--port"):
			port = int(a)
		elif o in ("-n", "--skip-test"):
			skipTest = True
		elif o in ("-q", "--quiet"):
			verbose = False
		elif o in ("-b", "--batch"):
			showOutput = False

	
	ui = UI(verbose=verbose)
	schema = Schema() #langs=('en','de','fr'))
	schema.startup(ui)
	
	wf = WidgetFactory(sprlwidgets)
	
	server = WebServer(demoDir,ui, wf, port=port)

	if True:

		ui.progress("Starting std.db...")
		conn = Connection(filename="std.db",
								isTemporary=True,
								schema=schema)
		stddb = Database(ui=ui,
							  langs="en de fr et",
							  schema=schema,
							  name="std",
							  label="shared standard data")

		sharedTables = ('LANGS','NATIONS', #'CITIES',
							 'PARTYPES','Currencies',
							 'PEVTYPES',
							 'PUBTYPES',
							 'PRJSTAT')

		stddb.startup(conn,
						  lambda t: t.getTableName() in sharedTables)
		
		stddb.createTables()

		from lino.schemas.sprl.data import std
		std.populate(stddb,big=False)

		
	
	for dbi in dbinfos:
		if len(args) == 0 or dbi.name in args:
			ui.progress("Opening %s..." % dbi.name)

			db = Database(ui=ui,
							  langs=dbi.langs,
							  schema=schema,
							  name=dbi.name,
							  label=dbi.label)
			
			conn = Connection(filename=dbi.dbfile,
									schema=schema)

			db.startup(conn)

			db.update(stddb)
			
			if not skipTest:
				print "checkIntegrity: " + db.getName()
				msgs = db.checkIntegrity()
				if len(msgs):
					msg = "%s : %d database integrity problems" % (
						db.getName(), len(msgs))
					print msg + ":"
					print "\n".join(msgs)
					#from lino.adamo.datatypes import DataVeto
					#raise DataVeto, msg

			server.addDatabase(db,
									 stylesheet="files/www.css",
									 staticDirs=dbi.staticDirs)


	if True:

		sys.path.insert(0,demoDir)

		#for modName in ('vor', 'etc'):
		for modName in ('etc',):

			ui.progress("Opening %s..." % modName)

			mod = __import__(modName) # my_import(modName)

			#print "%s (%s)" % (modName,mod.label)

			conn = Connection(filename=modName+'.db',
									isTemporary=True,
									schema=schema)
			db = Database(ui=ui,
							  langs='en de',
							  schema=schema,
							  name=modName,
							  label=mod.label)

			db.startup(conn)
			db.createTables()

			mod.populate(db)

			server.addDatabase(db, staticDirs = {
				'files': os.path.join(demoDir,modName,'files'),
				'images': os.path.join(demoDir,modName,'images'),
				#'thumbnails': os.path.join(demoDir,modName,'thumbnails')
				})

			#db.flush()

		del sys.path[0]


	server.run(showOutput=showOutput)



	
