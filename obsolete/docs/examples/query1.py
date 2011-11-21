# list of all cities and number of inhabitants
from lino.apps.contacts.contacts_demo import startup
from lino.apps.contacts.contacts_tables import City
from lino.adamo.filters import NotEmpty

sess=startup()
qry=sess.query(City,"nation name inhabitants", orderBy="inhabitants")
qry.getColumnByName("inhabitants").addFilter(NotEmpty)
qry.show(width=50)

print
print qry.getSqlSelect()

sess.shutdown()
