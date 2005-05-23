from lino.schemas.sprl import demo
from lino.reports import Report, RIGHT

sess = demo.startup()

rpt=Report(sess.db.app.getTableList())

def onEach(row):
    row.count=len(sess.query(row.item.__class__))
rpt.onEach(onEach)

rpt.addColumn(
    meth=lambda row: row.item.getTableName(),
    label="TableName",
    width=20)
rpt.addColumn(
    meth=lambda row: row.count,
    width=5, halign=RIGHT,
    label="Count")
rpt.addColumn(
    meth=lambda row: sess.query(row.item.__class__)[0],
    when=lambda row: row.count>0,
    label="First",
    width=20)
rpt.addColumn(
    meth=lambda row: sess.query(row.item.__class__)[-1],
    when=lambda row: row.count>0,
    label="Last",
    width=20)

rpt.show()

