from lino.apps.keeper.keeper import Keeper
from lino.misc.tsttools import TESTDATA
from lino.adamo.store import Populator
from lino.forms import gui

class TestPopulator(Populator):
    def populateVolumes(self,q):
        tv=q.appendRow(name="test",path=TESTDATA)
        tv.load(q.getSession())
        
app=Keeper()
sess=app.quickStartup(filename="keeper.db")
sess.populate(TestPopulator())
gui.run(sess)


