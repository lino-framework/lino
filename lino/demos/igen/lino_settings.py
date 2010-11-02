#lino_site.help_url = "http://code.google.com/p/lino/wiki/IgenUserManual"
lino.help_url = "http://lino.saffre-rumma.ee/igen/index.html"
lino.title = "iGen demo"
lino.index_html = """
Welcome to iGen, the first Lino application.

<p>iGen lets you write recurrent invoices to your customers, and manage their payments.

<p>This is a demo database.
You can change data and play with it, 
but keep in mind that the data is being reset 
to an initial state when necessary."""

#~ lino.index_html += """<p>
#~ You can log in as user "user" or "root", both with password "1234".
#~ Note how the menu changes depending on which user you are.
#~ """

lino.index_html += """<ul>"""
lino.index_html += """<li><a href="%s">User manual</a></li>""" % lino.help_url
lino.index_html += """</ul>"""

# this creates a (useless) vertical scrollbar in the main viewport:
# lino.index_html += "<br/>" * 500

from django.db import models

#~ system = models.get_app('system')
countries = models.get_app('countries')
contacts = models.get_app('contacts')
products = models.get_app('products')
#~ documents = models.get_app('documents')
ledger = models.get_app('ledger')
sales = models.get_app('sales')
finan = models.get_app('finan')
journals = models.get_app('journals')

from lino.utils import perms
from lino import models as system


ledger.set_accounts(
  #providers='4400',
  #customers='4000',
  sales_base='7000',
  sales_vat='4510',
)

  
m = lino.add_menu("contacts","~Contacts")
m.add_action('contacts.Companies')
m.add_action('contacts.Persons')
m.add_action('sales.Customers')

m = lino.add_menu("prods","~Products")
m.add_action('products.Products')
m.add_action('products.ProductCats')

m = lino.add_menu("journals","~Journals",can_view=perms.is_staff)
for jnl in journals.Journal.objects.all().order_by('pos'):
    #m.add_action(jnl.get_doc_report())
    m.add_action(str(jnl.get_doc_report()),params={'base_params':{'mk':jnl.pk}})
    # m.add_action(jnl.get_doc_report(),args=[jnl.pk])
    #~ m.add_action(str(jnl.get_doc_report()))
    
m = lino.add_menu("sales","~Sales",
  can_view=perms.is_authenticated)
#m.add_action(Orders())
#m.add_action(Invoices())
m.add_action('sales.DocumentsToSign')
m.add_action('sales.PendingOrders')

#~ m = lino.add_menu("admin","~Administration",
  #~ can_view=perms.is_staff)
#~ m.add_action(MakeInvoicesDialog())

m = lino.add_menu("config","~Configuration",
  can_view=perms.is_staff)
m.add_action('sales.InvoicingModes')
m.add_action('sales.ShippingModes')
m.add_action('sales.PaymentTerms')
m.add_action('journals.Journals')
#~ m = lino.add_menu("ledger","~Ledger",
  #~ can_view=perms.is_authenticated)
m.add_action('ledger.Accounts')

m.add_action('countries.Countries')
#m.add_action(contacts.Countries())
m.add_action('contenttypes.ContentTypes')
#m = lino.add_menu("system","~System")
m.add_action('auth.Permissions')
m.add_action('auth.Users')
m.add_action('auth.Groups')
#m.can_view = perms.is_staff

system.add_site_menu(lino)
