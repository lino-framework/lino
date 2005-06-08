from lino.schemas.sprl import demo
from lino.reports import Report, RIGHT

sess = demo.startup()

rpt=Report(sess.db.app.getTableList())

def onEach(row):
    row.count=len(sess.query(row.item.__class__))
rpt.onEach(onEach)

rpt.addVurtColumn(
    label="TableName",
    meth=lambda row: row.item.getTableName(),
    width=20)
rpt.addVurtColumn(
    label="Count",
    meth=lambda row: row.count,
    width=5, halign=RIGHT
    )
rpt.addVurtColumn(
    label="First",
    meth=lambda row: sess.query(row.item.__class__)[0],
    when=lambda row: row.count>0,
    width=20)
rpt.addVurtColumn(
    label="Last",
    meth=lambda row: sess.query(row.item.__class__)[-1],
    when=lambda row: row.count>0,
    width=20)

rpt.show()

