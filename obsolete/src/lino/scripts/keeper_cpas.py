from lino.apps.keeper.keeper_tables import KeeperSchema
from lino.apps.keeper.keeper_forms import Keeper
from lino.adamo.ddl import Populator

class MyPopulator(Populator):
    def populateVolumes(self,q):
        vol=q.appendRow(name="test",path="test")
        vol.load()
        vol=q.appendRow(name="f",path="f")
        vol.load()
        
app=Keeper()
dbc=app.createContext(filename="keeper.db")
dbc.populate(MyPopulator())
app.main()
