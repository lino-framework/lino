from lino.apps.contacts.contacts_demo import startup
from lino.apps.contacts.contacts_tables import Nation
from lino.adamo.filters import NotEmpty

dbc = startup(big=True)
        
qry=dbc.query(Nation,"id name")
qry.addColumn("cities",search="dre",orderBy="name",depth=1)
qry.addColFilter('cities',NotEmpty)
qry.show(
    columnWidths="2 15 *",
    title="Nations and their Cities containing search string 'dre'")

print
print qry.getSqlSelect()

del dbc, qry
