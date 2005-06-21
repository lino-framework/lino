from lino.schemas.sprl import demo
from lino.schemas.sprl.tables import Nations
from lino.adamo.filters import NotEmpty

sess = demo.beginSession(big=True)
        
qry=sess.query(
    Nations,"id name",
    label="Nations and their Cities containing search string 'dre'")
qry.addColumn("cities",search="dre",depth=1).addFilter(NotEmpty)
sess.showQuery(qry,columnWidths="2 15 *")

print
print qry.getSqlSelect()
