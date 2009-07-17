#lino_site.help_url = "http://code.google.com/p/lino/wiki/IgenUserManual"
lino.help_url = "http://lino.saffre-rumma.ee/django/igen/userman.html"
#lino.sort_menu_items(back='config system')

from lino.django.apps.system import models as system
from lino.django.apps.countries import models as countries
from lino.django.apps.contacts import models as contacts
from lino.django.apps.products import models as products
from lino.django.apps.documents import models as documents
from lino.django.apps.ledger import models as ledger
from lino.django.apps.sales import models as sales
from lino.django.apps.finan import models as finan 
from lino.django.apps.journals import models as journals 
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
    m.add_action(journals.DocumentsByJournal(jnl))
    
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
m.add_action(countries.Countries())

#m = lino.add_menu("system","~System")
m.add_action(system.Permissions())
m.add_action(system.Users())
m.add_action(system.Groups())
#m.can_view = perms.is_staff


