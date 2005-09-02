from lino.apps.addrbook import demo, tables
from lino.adamo.filters import NotEmpty

sess = demo.startup(big=True)
        
qry=sess.query(
    tables.Nation,"id name",
    label="Nations and their Cities containing search string 'dre'")
cities=qry.addColumn("cities",search="dre",depth=1)
qry.addFilter(NotEmpty(cities))
sess.showQuery(qry,columnWidths="2 15 *")

print
print qry.getSqlSelect()
