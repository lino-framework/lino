from lino.apps.pinboard.pinboard import Pinboard
from lino.apps.pinboard.loaders import LOADERS

from lino.adamo.store import Populator
from lino.forms import gui

loadfrom=r".\WEB\LINO"

class MyPopulator(Populator):
    def populateNewsgroups(self,q):
        q.appendRow(id="srf",name="Surf notes")
        q.appendRow(id="api",name="API change")
        q.appendRow(id="rel",name="Release note")


app=Pinboard()
sess=app.quickStartup()
sess.populate(MyPopulator())
for lc in LOADERS:
    sess.runTask(lc(loadfrom))
gui.run(sess)


