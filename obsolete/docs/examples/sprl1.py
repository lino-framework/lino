from lino.apps.ledger.ledger_demo import startup
from lino.reports import Report, RIGHT
from lino.adamo.datatypes import INT

class DatabaseOverview(Report):
    def __init__(self,dbsess):
        self.dbsess=dbsess
        Report.__init__(self)
        
    def setupRow(self,row):
        row.qry=self.dbsess.query(row.item._instanceClass)
        
    def getIterator(self):
        return self.dbsess.db.schema.getTableList()
        
    def setupReport(self):
        self.addVurtColumn(
            label="TableName",
            meth=lambda row: row.item.getTableName(),
            width=20)
        self.addVurtColumn(
            label="Count",
            meth=lambda row: len(row.qry),
            datatype=INT,
            width=5, halign=RIGHT
            )
        self.addVurtColumn(
            label="First",
            meth=lambda row: unicode(row.qry[0]),
            when=lambda row: len(row.qry)>0,
            width=20)
        self.addVurtColumn(
            label="Last",
            meth=lambda row: unicode(row.qry[-1]),
            when=lambda row: len(row.qry)>0,
            width=20)

    
sess = startup()
rpt=DatabaseOverview(sess)
rpt.show()

sess.shutdown()
