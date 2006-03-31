from lino.adamo.dbreports import DatabaseOverview, SchemaOverview
from lino.apps.contacts.contacts_forms import Contacts
from lino.apps.keeper.keeper_forms import Keeper
from lino.apps.ledger.ledger_forms import Ledger


for appclass in Contacts, Keeper, Ledger:
    app=appclass()
    app.createContext()
    print
    print app
    SchemaOverview(app.dbsess.db.schema).show()
    
