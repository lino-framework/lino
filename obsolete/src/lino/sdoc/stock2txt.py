from reporter import OdbcReporter


DSN = "Test"
CAT = "ETC"
REF1 = ""
REF2 = ""
DATE1 = "{01/01/2002}"
DATE2 = "{01/31/2002}"



SQL1 = """
SELECT NUM, REF, HEADING1,HEADING2,
  (SELECT QTYINSTOCK
          FROM PCIWAREH W WHERE W.ARTNUM=ART.NUM) as curr_stk,
  (SELECT SUM(QTYMVT) 
               FROM   PCIHISTO HSTI
               WHERE  HSTI.ARTNUM=ART.NUM
                      AND HSTI.DOCDATE > %(DATE2)s) as mvt_after,
  (SELECT SUM(QTYMVT) 
               FROM PCIHISTO HSTF
               WHERE HSTF.ARTNUM=ART.NUM
                     AND HSTF.DOCDATE >= %(DATE1)s
                     AND HSTF.DOCDATE <= %(DATE2)s) as mvt_between
  FROM PCIART ART
  ORDER BY REF
""" % globals()

SQL1 += """
  WHERE REF BETWEEN "1" and "9" 
"""



SQL2 = """
  SELECT HST.DBK,HST.DOCNO,
         HST.DOCDATE,
         HST.CPID,
         HST.QTYMVT,
         DOC.INTREM
         
  FROM PCIHISTO HST
       LEFT JOIN PCIHDDOC DOC on (DOC.DOCNO = HST.DOCNO)
       
       
  WHERE HST.ARTNUM = %d
    AND HST.DOCDATE >= %s
    AND HST.DOCDATE <= %s
  ORDER BY HST.DOCDATE
"""

class ArtReporter(OdbcReporter):
   def onHeader(self):
      self.writer.write("Historique stock\n")
      self.writer.write("%(DATE1)s - %(DATE2)s\n" % globals())
   
   def onEachRow(self):
      # print self.currentRow.ref
      self.writer.write(
         ("%(ref)s\t%(heading1)s\tstock initial\t" \
         + "%(stk1)d\n") %
         self.currentRow)
      rpt = OdbcReporter(self.conn)
      sql = SQL2 % (self.currentRow.num, DATE1, DATE2)
      rpt.setSQL(sql)
      rpt.indent = 1
      rpt.go(self.writer)
      if self.recno > 0:
         self.writer.write("\n")
         self.writer.write(
            ("%(ref)s\t%(heading1)s\t%(heading2)s\tstock final\t"
             + "%(stk2)d\n") %
            self.currentRow)
         self.writer.write("\n")


if __name__ == "__main__":


   rpt = ArtReporter()
   rpt.setDSN(DSN)
   rpt.setSQL(SQL1)

   rpt.addColumn("stk1","NUMBER",
                 lambda row :
                 row.curr_stk - row.mvt_after - row.mvt_between)
   rpt.addColumn("stk2","NUMBER",
                 lambda row :
                 row.curr_stk - row.mvt_after)

   if 1:
      w = file("tmp.txt","w")
      rpt.go(w)
   else:
      rpt.go()
   w.close()
