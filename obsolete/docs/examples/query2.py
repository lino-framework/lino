# list of Belgian cities and number of inhabitants
from lino.apps.contacts.contacts_demo import startup
from lino.apps.contacts.contacts_tables import Nation

sess=startup()
be=sess.query(Nation).peek("be")
qry=be.cities("name inhabitants",orderBy="inhabitants")

qry.show(width=50)

print
print qry.getSqlSelect()

sess.shutdown()
