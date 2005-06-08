from lino.reports.reports import DictReport

d = dict(
    name="Ausdemwald",
    firstName="Norbert",
    size=12,
    description="""\
Norbert ist unser treuer Mitarbeiter im Vurt. Er wohnt in der Fremereygasse in Eupen."""
    )

rpt = DictReport(d)
rpt.show()

