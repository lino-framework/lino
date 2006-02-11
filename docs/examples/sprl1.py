from lino.apps.ledger import demo
from lino.reports import Report, RIGHT
from lino.adamo.datatypes import INT

sess = demo.startup()

rpt=Report(sess.db.app.getTableList())

def onEach(row):
    row.qry=sess.query(row.item._instanceClass)
    
rpt.onEach(onEach)

rpt.addVurtColumn(
    label="TableName",
    meth=lambda row: row.item.getTableName(),
    width=20)
rpt.addVurtColumn(
    label="Count",
    meth=lambda row: len(row.qry),
    datatype=INT,
    width=5, halign=RIGHT
    )
rpt.addVurtColumn(
    label="First",
    meth=lambda row: str(row.qry[0]),
    when=lambda row: len(row.qry)>0,
    width=20)
rpt.addVurtColumn(
    label="Last",
    meth=lambda row: str(row.qry[-1]),
    when=lambda row: len(row.qry)>0,
    width=20)

rpt.show()

