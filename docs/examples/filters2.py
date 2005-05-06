from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import Nations
from lino.adamo.filters import NotEmpty

sess = demo.beginSession(big=True)
        
q=sess.query(Nations,"id name")
q.addColumn("cities",search="dre",depth=1).addFilter(NotEmpty)
q.report(columnWidths="2 15 *")

print
print q.getSqlSelect()
