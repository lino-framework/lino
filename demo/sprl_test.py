from lino.schemas.sprl import demo
from lino.forms import gui

sess=demo.startup(filename="sprl.db",big=True)
gui.run(sess)


