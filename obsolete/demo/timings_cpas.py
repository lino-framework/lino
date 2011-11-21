from lino.apps.timings.timings import Timings
from lino.apps.timings.loaders import LOADERS

from lino.adamo.store import Populator
from lino.forms import gui

loadfrom=r".\CPAS"

class CpasPopulator(Populator):
    def populateUsageTypes(self,q):
        q.appendRow(id="A",name="Arbeit")
        q.appendRow(id="U",name="Urlaub")
        q.appendRow(id="M",name="Mission")


app=Timings()
sess=app.quickStartup()
sess.populate(CpasPopulator())
for lc in LOADERS:
    sess.runTask(lc(loadfrom))
gui.run(sess)


