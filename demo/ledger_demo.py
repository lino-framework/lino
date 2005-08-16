from lino.apps.ledger import demo
from lino.forms import gui

sess=demo.startup() # filename="ledger.db")
gui.run(sess)


