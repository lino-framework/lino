from lino.schemas.sprl import demo
from lino.reports import Report
from lino.adamo.rowattrs import Field, Detail

sess = demo.startup(populate=False)

rpt=Report(sess.schema.getTableList())

rpt.addColumn(
    meth=lambda row: row.item.getTableName(),
    label="TableName",
    width=15)
rpt.addColumn(
    meth=lambda row:\
    ", ".join([fld.name for fld in row.item.getFields()
               if isinstance(fld,Field)]),
    label="Fields",
    width=30)
rpt.addColumn(
    meth=lambda row:\
    ", ".join([fld.name for fld in row.item.getFields()
               if isinstance(fld,Detail)]),
    label="Details",
    width=35)

rpt.show()

