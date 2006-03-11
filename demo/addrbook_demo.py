from lino.forms import GuiApplication
from lino.forms import gui
from lino.apps.addrbook.addrbook import MyMainForm
from lino.apps.addrbook import demo

#sess=demo.startup() # filename="addrbook.db",big=False)
#frm=MyMainForm(sess)
#gui.show(frm)



class AddressBook(GuiApplication):
    name="Lino AdressBook"
    version="0.0.1"
    author="Luc"
    mainFormClass=MyMainForm
        
    def beginSession(self,*args,**kw):
        return demo.startup(*args,**kw)
    
if __name__ == '__main__':
    AddressBook().main()
