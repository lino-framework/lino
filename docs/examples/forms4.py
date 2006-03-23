#from lino.apps.pinboard.pinboard_demo import startup
#from lino.apps.pinboard.pinboard_tables import QuotesReport
from lino.config import tempdirfilename
from lino.apps.contacts.contacts_demo import startup
from lino.apps.contacts.contacts_tables import PartnersReport
from lino.forms.forms import ReportRowForm

dbc=startup(filename=tempdirfilename("tmp.db"))

class MyPartnersReport(PartnersReport):
    columnSpec="""
    firstName name
    phone gsm fax
    email website
    street house box
    nation city zip
    id type lang
    memo
    """

#rpt=QuotesReport(dbc)
rpt=PartnersReport(dbc)
rpt=MyPartnersReport(dbc)

ReportRowForm(rpt,enabled=False).main()
