from lino.apps.addrbook import demo
from lino.forms import gui

sess=demo.startup() # filename="addrbook.db",big=False)
gui.run(sess.app,sess)


