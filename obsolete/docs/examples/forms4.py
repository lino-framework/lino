#from lino.apps.pinboard.pinboard_demo import startup
#from lino.apps.pinboard.pinboard_tables import QuotesReport
#from lino.config import tempdirfilename
from lino.apps.contacts.contacts_demo import startup
from lino.apps.contacts.contacts_tables import ContactsReport
from lino.forms.dbforms import ReportRowForm

#dbc=startup(filename=tempdirfilename("tmp.db"))
dbc=startup()

class MyContactsReport(ContactsReport):
    columnSpec="""
    name
    org 
    person function
    phone gsm fax
    email website
    street house box
    nation city zip
    id lang
    """

#rpt=QuotesReport(dbc)
#rpt=PartnersReport(dbc)
rpt=MyContactsReport(dbc)

ReportRowForm(rpt,enabled=False).main()

#del rpt,dbc

dbc.shutdown()
