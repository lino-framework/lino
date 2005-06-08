from lino.console.application import Application
from lino.reports.reports import DictReport

class MyReport(Application):
    
    def run(self,sess):

        d = dict(
            name="Ausdemwald",
            firstName="Norbert",
            size=12,
            description="""\
Norbert ist unser treuer Mitarbeiter im Vurt. Er wohnt in der Fremereygasse in Eupen."""
            )

        rpt = DictReport(d)
        sess.report(rpt)
        
if __name__ == "__main__":
    MyReport().main()
