#from lino.apps.pinboard.pinboard_demo import startup
#from lino.apps.pinboard.pinboard_tables import QuotesReport
from lino.apps.contacts.contacts_demo import startup
from lino.apps.contacts.contacts_tables import ContactsReport
from lino.forms.forms import ReportGridForm

dbc=startup()
#rpt=QuotesReport(dbc)
rpt=ContactsReport(dbc)
ReportGridForm(rpt).main()
    
