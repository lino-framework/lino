# list of Belgian cities and number of inhabitants
from lino.apps.addrbook import demo, tables

sess=demo.startup()
be=sess.query(tables.Nation).peek("be")
qry=be.cities("name inhabitants",orderBy="inhabitants")

sess.showQuery(qry,width=50)

print
print qry.getSqlSelect()
