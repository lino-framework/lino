from lino.apps.addrbook import demo
from lino.forms import gui

sess=demo.startup() # filename="addrbook.db",big=False)
gui.choose("cherrypy")
gui.run(sess)


