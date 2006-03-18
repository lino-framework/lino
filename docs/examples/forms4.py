#from lino.apps.pinboard.pinboard_demo import startup
#from lino.apps.pinboard.pinboard_tables import QuotesReport
from lino.apps.contacts.contacts_demo import startup
from lino.apps.contacts.contacts_tables import PartnersReport
from lino.forms.forms import ReportRowForm

dbc=startup()

class MyPartnersReport(PartnersReport):
    columnSpec="""
    firstName name
    email phone gsm fax
    website
    street house box
    nation city zip
    id type lang
    """

#rpt=QuotesReport(dbc)
rpt=PartnersReport(dbc)
rpt=MyPartnersReport(dbc)

ReportRowForm(rpt,enabled=False).main()
