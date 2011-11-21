"""

starts a Medusa server with Quixote, serving a WebMan module on Lino's
`docs` directory.

"""

if __name__ == "__main__":
	
	import os
	import webbrowser
	from lino.webman.webman import WebModule
	from lino.quix.serve import startServer

	from lino.quix import serve

	servername = "localhost"

	webbrowser.open("http://%s:8080" % servername,new=1)

	srcdir = os.path.join(os.path.dirname(__file__),"..","docs")

	m = WebModule(srcdir)

	startServer(m,servername,configPath=m.getSourcePath())



