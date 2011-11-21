from lino.adamo.dbreports import DatabaseOverview, SchemaOverview
from lino.apps.contacts.contacts_tables import Contacts
from lino.apps.keeper.keeper_tables import Keeper
from lino.apps.ledger.ledger_tables import Ledger


for appclass in Contacts, Keeper, Ledger:
    app=appclass()
    db=app.createContext()
    print
    print app
    SchemaOverview(db.getSchema()).show()
    app.shutdown()
    
