from lino.apps.contacts.contacts_demo import startup
from lino.apps.contacts.contacts_tables import Nation
from lino.adamo.filters import NotEmpty

dbc = startup() # big=True)
        
qry=dbc.query(Nation,"id name cities")
qry.addColFilter('cities',NotEmpty)
qry.show(columnWidths="2 15 20")

print
print qry.getSqlSelect()

del dbc, qry
