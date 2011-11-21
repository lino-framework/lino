from lino.apps.pinboard.pinboard import Pinboard
#from lino.apps.pinboard.loaders import LOADERS

from lino.adamo.store import Populator
#from lino.forms import gui

class MyPopulator(Populator):
    def populateNewsgroups(self,q):
        q.appendRow(id="srf",name="Surf notes")
        q.appendRow(id="api",name="API change")
        q.appendRow(id="rel",name="Release note")

class TimwebsPinboard(Pinboard):
    populators=(MyPopulator(),)
    loadMirrorsFrom=r"c:\temp\web\lino"
    filename=r"c:\temp\pinboard.db"


def main(): TimwebsPinboard().main()

if __name__ == '__main__': main()
    
## app=Pinboard()
## sess=app.quickStartup()
## sess.populate(MyPopulator())
## for lc in LOADERS:
##     loader=lc(loadfrom)
##     sess.run(loader.run)
## gui.choose("cherrypy")
## gui.run(sess)


