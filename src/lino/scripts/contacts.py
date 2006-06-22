## from lino.apps.contacts.contacts_forms import Contacts
## from lino.apps.contacts.contacts_demo import startup

## dbc=startup(filename="contacts.db")
## app=Contacts(dbc)
## app.main()

from lino.apps.contacts.contacts_demo import DemoContacts
app=DemoContacts(filename="contacts.db",dump=True)
#app.quickStartup(filename="contacts.db")
#app.setFilename("contacts.db")
app.main()
