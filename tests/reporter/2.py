import dbi,odbc
from gandalf.reporter import Reporter
from gandalf.ostreams import TextDocument


DSN = "DBFS"

SQL1 = "SELECT * FROM NAT ORDER BY idnat"

SQL2 = """
SELECT idpar,allo,vorname,firme,rue, ruenum, ruebte
FROM PAR where PAR.Pays = '%(idnat)s' ORDER BY firme,vorname
"""


class MainReporter(Reporter):
   def onHeader(self):
      self.write("Nations and Partners\n")
   
   def onEachRow(self):
      # print self.currentRow.ref
      self.write("%(idnat)s\t%(name)s\n" % self.currentRow)
      rpt = Reporter(self)
      rpt.initialize(SQL2 % self.currentRow)
      rpt.indent = 1
      rpt.addColumn("fullname","CHAR",
                    lambda row :
                    row.allo + row.vorname + row.firme)
      rpt.execute()
      if self.recno > 0:
         self.write("\n")
         self.write("%d partners in %s\n" % (
            rpt.recno, self.currentRow.name))
         self.write("\n")


if __name__ == "__main__":

   rpt = MainReporter()
   rpt.connect(odbc.odbc(DSN))

   rpt.initialize(SQL1)

   rpt.execute(TextDocument("tmp.txt"))

   rpt.close()


