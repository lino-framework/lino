from lino.forms import gui
from lino.apps.addrbook.addrbook import MyMainForm
from lino.apps.addrbook import demo

dbc=demo.startup() # filename="addrbook.db",big=False)
frm=MyMainForm(dbc)
gui.show(frm)



