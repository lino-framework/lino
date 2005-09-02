from lino.apps.ledger import demo
from lino.reports import Report
from lino.adamo.rowattrs import Field, Detail

sess=demo.startup(populate=False)

rpt=Report(sess.db.app.getTableList())

rpt.addVurtColumn(
    label="TableName",
    meth=lambda row: row.item.getTableName(),
    width=15)
rpt.addVurtColumn(
    label="Fields",
    meth=lambda row:\
    ", ".join([fld.name for fld in row.item.getFields()
               if isinstance(fld,Field)]),
    width=30)
rpt.addVurtColumn(
    label="Details",
    meth=lambda row:\
    ", ".join([fld.name for fld in row.item.getFields()
               if isinstance(fld,Detail)]),
    width=35)

rpt.show()

