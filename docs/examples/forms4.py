#from lino.apps.pinboard.pinboard_demo import startup
#from lino.apps.pinboard.pinboard_tables import QuotesReport
from lino.apps.contacts.contacts_demo import startup
from lino.apps.contacts.contacts_tables import PartnersReport
from lino.forms.forms import ReportRowForm

dbc=startup()
#rpt=QuotesReport(dbc)
rpt=PartnersReport(dbc)
ReportRowForm(rpt).main()
    
