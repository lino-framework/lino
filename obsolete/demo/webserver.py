"""\
Usage : webserver [options] FILE

webserver starts a Twisted web server on an Adamo database in FILE

Options:
  
  -p PORT, --port PORT     alternate PORT where to listen
                           (default is 8080)
  -b, --batch              don't start a browser 
  -h, --help               display this text
"""

import sys, getopt, os

# from lino.misc import gpl
#from lino import __version__

from lino.adamo.dbds.sqlite_dbd import Connection
from lino.adamo.ui import UI
from lino.adamo.twisted_ui import webserver
from lino.adamo import twisted_ui 
from lino.schemas.sprl.sprl import Schema
#from lino.schemas.sprl import demo




if __name__ == '__main__':
	port = 8080
	showOutput = True

	try:
		opts, args = getopt.getopt(sys.argv[1:],
											"?hp:b",
											["help", "port=","batch"])

	except getopt.GetoptError,e:
		print __doc__
		print e
		sys.exit(-1)

	if len(args) != 1:
		print __doc__
		sys.exit(-1)

	
	for o, a in opts:
		if o in ("-?", "-h", "--help"):
			print __doc__
			sys.exit()
		elif o in ("-p", "--port"):
			port = int(a)
		elif o in ("-b", "--batch"):
			showOutput = False

	dbfile = args[0]

	ui = UI(verbose=True)
	schema = Schema()
	schema.startup(ui)
	
	conn = Connection(dbfile) #, isTemporary=True)
	
	db = ui.addDatabase(None, conn, schema,
							  label="Lino Demo Database")
	
	#ui = UI(verbose=True)
	#db = demo.startup(verbose=True)

	twisted_ui.webserver(db,port,showOutput, staticDirs = {
		'files': os.path.join(os.path.dirname(dbfile),'files'),
		'images': r'h:\htdocs\lsaffre\images' ,
		'thumbnails': r'h:\htdocs\lsaffre\thumbnails' ,
		})


