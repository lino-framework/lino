"""
starts a medusa web server with Quixote, serving an adamo database
"""
if __name__ == "__main__":
	
	import os
	from quixote import enable_ptl
	enable_ptl()

	from lino.quix import default 
	from lino.quix.serve import startServer

	from lino.schemas.sprl import demo

	#import webbrowser

	db = demo.startup(verbose=True)

	#webbrowser.open("http://localhost:8080",new=1)

	# serve.main(db)
	namespace = default.DatabaseNamespace(db)
	#default.setDatabase(db)
	configPath = os.path.dirname(default.__file__)
	startServer(namespace,db.getLabel(),configPath)
	#startServer(default,db.getLabel())
