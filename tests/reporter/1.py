import dbi,odbc
from gandalf.reporter import Reporter
from gandalf.ostreams import TextDocument


DSN = "DBFS"

if __name__ == "__main__":

   rpt = Reporter()
   rpt.connect(odbc.odbc(DSN))
   rpt.initialize("SELECT * FROM PAR")

   rpt.execute(TextDocument("tmp.txt"))
   rpt.close()

