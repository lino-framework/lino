from lino.apps.spz.spz import SPZ
from lino.apps.spz.loaders import LOADERS

from lino.adamo.store import Populator
from lino.forms import gui

loadfrom=r".\SPZ"

app=SPZ()
sess=app.quickStartup()
#sess.populate(CpasPopulator())
for lc in LOADERS:
    sess.runTask(lc(loadfrom))
gui.run(sess)


