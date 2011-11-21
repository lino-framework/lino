from lino.forms import Form

class PrivacyForm(Form):
    
    title = "Privacy statement"
    
    def layout(self,panel):
        
        panel.label("""\

(imagine our privacy statement here)

Note that this form is not modal, so you don't need to close it if you
want to continue registering.

""")
        panel.closeButton()
        
class MyForm(Form):
    
    title = "The First Lino Form"

    def layout(self,panel):
    
        panel.label("""\
Please enter your personal data.
Don't worry about your privacy.
You can trust us.
    """)
        self.firstName = panel.entry(label="First name")
        self.name = panel.entry(label="Name")
        panel.formButton(PrivacyForm())
        panel.okButton()
        panel.cancelButton()

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
