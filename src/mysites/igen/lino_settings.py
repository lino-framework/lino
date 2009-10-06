#lino_site.help_url = "http://code.google.com/p/lino/wiki/IgenUserManual"
lino.help_url = "http://lino.saffre-rumma.ee/django/igen/userman.html"
lino.title = "iGen demo"
lino.index_html = """
Welcome to iGen, the first Lino application.

<p>iGen lets you write recurrent invoices to your customers, and manage their payments.

<p>This is a demo database.
You can change data and play with it, 
but keep in mind that the data is being reset 
to an initial state when necessary.

<p>
You can log in as user "user" or "root", both with password "1234".
Note how the menu changes depending on which user you are.
<a href="%s">More</a>""" % lino.help_url

# this creates a (useless) vertical scrollbar in the main viewport:
# lino.index_html += "<br/>" * 500

from django.db import models

system = models.get_app('system')
countries = models.get_app('countries')
contacts = models.get_app('contacts')
products = models.get_app('products')
documents = models.get_app('documents')
ledger = models.get_app('ledger')
sales = models.get_app('sales')
finan = models.get_app('finan')
journals = models.get_app('journals')

from lino.django.utils import perms

#~ from django.db.models.loading import get_model

#~ Order = get_model('sales','order')
#~ Invoice = get_model('sales','invoice')
#~ BankStatement = get_model('finan','BankStatement')

#~ Order.create_journal("ORD")
#~ Invoice.create_journal("INV","4000")
#~ BankStatement.create_journal("BANK","5500")

ledger.set_accounts(
  #providers='4400',
  #customers='4000',
  sales_base='7000',
  sales_vat='4510',
)

  
m = lino.add_menu("contacts","~Contacts")
m.add_action(contacts.Companies())
m.add_action(contacts.Persons())
m.add_action(contacts.Contacts(),label="All")
m.add_action(sales.Customers())

m = lino.add_menu("prods","~Products")
m.add_action(products.Products())
m.add_action(products.ProductCats())

m = lino.add_menu("journals","~Journals",can_view=perms.is_staff)
for jnl in journals.Journal.objects.all().order_by('pos'):
    #m.add_action(jnl.get_doc_report())
    #m.add_action(jnl.get_doc_report(),params={'master':jnl})
    m.add_action(jnl.get_doc_report(),args=[jnl.pk])
    
m = lino.add_menu("sales","~Sales",
  can_view=perms.is_authenticated)
#m.add_action(Orders())
#m.add_action(Invoices())
m.add_action(sales.DocumentsToSign())
m.add_action(sales.PendingOrders())

#~ m = lino.add_menu("admin","~Administration",
  #~ can_view=perms.is_staff)
#~ m.add_action(MakeInvoicesDialog())

m = lino.add_menu("config","~Configuration",
  can_view=perms.is_staff)
m.add_action(sales.InvoicingModes())
m.add_action(sales.ShippingModes())
m.add_action(sales.PaymentTerms())
m.add_action(journals.Journals())
#~ m = lino.add_menu("ledger","~Ledger",
  #~ can_view=perms.is_authenticated)
m.add_action(ledger.Accounts())

m.add_action(countries.Languages())
#m.add_action(countries.Countries())
m.add_action(contacts.Countries())

#m = lino.add_menu("system","~System")
m.add_action(system.Permissions())
m.add_action(system.Users())
m.add_action(system.Groups())
#m.can_view = perms.is_staff

lino.add_program_menu()
#m.add_action()

