from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import Nations
from lino.adamo.filters import NotEmpty

sess = demo.beginSession(big=True)
        
qry=sess.query(Nations,"id name")
qry.addColumn("cities").addFilter(NotEmpty)
rpt=sess.createDataReport(qry,columnWidths="2 15 20")
sess.report(rpt)

print
print qry.getSqlSelect()
