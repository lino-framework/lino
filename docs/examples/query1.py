# list of all cities and number of inhabitants
from lino.apps.addrbook import demo, City
sess=demo.startup()
qry=sess.query(City,"nation name inhabitants", orderBy="inhabitants")
sess.showQuery(qry,width=50)

print
print qry.getSqlSelect()
