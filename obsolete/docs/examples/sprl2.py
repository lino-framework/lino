from lino.apps.ledger.ledger_tables import LedgerSchema
from lino.reports import Report
from lino.adamo.rowattrs import Field, Pointer, Detail

class SchemaOverview(Report):
    def __init__(self,schema):
        self.schema=schema
        Report.__init__(self)
        
    def getIterator(self):
        return self.schema.getTableList()
        
    def setupReport(self):

        self.addVurtColumn(
            label="TableName",
            meth=lambda row: row.item.getTableName(),
            width=15)
        self.addVurtColumn(
            label="Fields",
            meth=lambda row:\
            ", ".join([fld.name for fld in row.item.getFields()
                       if isinstance(fld,Field) \
                       and not isinstance(fld,Pointer)]),
            width=20)
        self.addVurtColumn(
            label="Pointers",
            meth=lambda row:\
            ", ".join([fld.name for fld in row.item.getFields()
                       if isinstance(fld,Pointer)]),
            width=15)
        self.addVurtColumn(
            label="Details",
            meth=lambda row:\
            ", ".join([fld.name for fld in row.item.getFields()
                       if isinstance(fld,Detail)]),
            width=25)


sch=LedgerSchema()
rpt=SchemaOverview(sch)
rpt.show()
