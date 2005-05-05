from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import Nations
from lino.adamo.filters import NotEmpty

sess = demo.beginSession(big=True)
        
qry=sess.query(Nations,"id name cities")
cities=qry.getColumnByName("cities")
qry.addFilter(NotEmpty(cities))
qry.report(pageLen=5,pageNum=1,columnWidths="2 15 20")

print
print qry.getSqlSelect()
