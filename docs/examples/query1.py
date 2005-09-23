# list of all cities and number of inhabitants
from lino.apps.addrbook import demo, City
from lino.adamo.filters import NotEmpty
sess=demo.startup()
qry=sess.query(City,"nation name inhabitants", orderBy="inhabitants")
qry.getColumnByName("inhabitants").addFilter(NotEmpty)
sess.showQuery(qry,width=50)

print
print qry.getSqlSelect()
