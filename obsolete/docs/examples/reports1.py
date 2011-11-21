#coding: iso-8859-1
from lino.reports.reports import DictReport

d = dict(
    name="Ausdemwald",
    firstName="Norbert",
    size=12,
    description=u"""\
Norbert ist unser treuer Mitarbeiter im Vurt. Er wohnt in der Gülcherstraße in Eupen."""
    )

rpt = DictReport(d)
rpt.show()

