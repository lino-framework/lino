from lino.apps.contacts.contacts_demo import startup
from lino.apps.contacts.contacts_tables import Nation
from lino.adamo.filters import NotEmpty

sess = startup() # big=True)
        
qry=sess.query(Nation,"id name cities")
qry.addColFilter('cities',NotEmpty)
qry.show(columnWidths="2 15 20")

print
print qry.getSqlSelect()
