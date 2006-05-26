from lino.forms import Form

class MyForm(Form):
    
    title = "The First Lino Form"
    
    def layout(self,doc):
    
        doc.label("""\
Please enter your personal data.
Don't worry about your privacy.
You can trust us.
    """)
        self.firstName = doc.entry(label="First name")
        self.name = doc.entry(label="Name")
        doc.okButton()
        doc.cancelButton()

    def ok(self):
        if not self.firstName.getValue():
            self.notice("First name is mandatory")
            return
        if not self.name.getValue():
            self.notice("Name is mandatory")
            return
        self.message(
            "Hello %s %s. Thank you for registering.",
            self.firstName.getValue(),
            self.name.getValue())
        self.close()
        
    def cancel(self):
        if self.confirm("This will end our relation. Are you sure?"):
            self.close()

if __name__ == '__main__':
    MyForm().main()
