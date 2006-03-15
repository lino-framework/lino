#from lino.forms import GuiApplication
from lino.apps.addrbook.addrbook import Contacts
from lino.apps.addrbook import demo

## class AddressBook(GuiApplication):
##     name="Lino AdressBook"
##     version="0.0.1"
##     author="Luc"
## ##     mainFormClass=MyMainForm
        
##     def createMainForm(self):
##         return AddressBookMainForm(demo.startup())
    
##     def beginSession(self,*args,**kw):
##         return demo.startup(*args,**kw)
    
Contacts(demo.startup()).main()
