from lino.apps.contacts.contacts_demo import DemoContacts

def main(*args,**kw):
    app=DemoContacts(filename="contacts.db")
    app.main()

    
if __name__ == '__main__':
    main()
