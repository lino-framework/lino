from lino.apps.addrbook import demo, tables
from lino.adamo.filters import NotEmpty

sess = demo.startup() # big=True)
        
qry=sess.query(tables.Nation,"id name cities")
qry.addColFilter('cities',NotEmpty)
qry.showReport(columnWidths="2 15 20")

print
print qry.getSqlSelect()
