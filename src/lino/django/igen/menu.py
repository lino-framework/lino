from lino.django.utils import perms
from lino.django.igen import models as igen
from lino.django.utils import sysadm
from lino.django.ledger import models as ledger

def lino_setup(lino):
    m = lino.add_menu("contacts","~Contacts")
    m.add_action(igen.Companies())
    m.add_action(igen.Persons())
    m.add_action(igen.Contacts(),label="All")
    m = lino.add_menu("prods","~Products")
    m.add_action(igen.Products())
    m.add_action(igen.ProductCats())
    m = lino.add_menu("sales","~Sales",
      can_view=perms.is_authenticated)
    m.add_action(igen.Orders())
    m.add_action(igen.Invoices())
    m.add_action(igen.DocumentsToSign())
    m.add_action(igen.PendingOrders())
    
    m = lino.add_menu("ledger","~Ledger",
      can_view=perms.is_authenticated)
    m.add_action(ledger.FinancialDocuments())
    m.add_action(ledger.Accounts())

#~ m = lino.add_menu("admin","~Administration",
      #~ can_view=perms.is_staff)
    #~ m.add_action(MakeInvoicesDialog())
    
    m = lino.add_menu("config","~Configuration",
      can_view=perms.is_staff)
    m.add_action(igen.InvoicingModes())
    m.add_action(igen.ShippingModes())
    m.add_action(igen.PaymentTerms())
    m.add_action(igen.Languages())
    m.add_action(igen.Countries())

    m = lino.add_menu("system","~System")
    m.add_action(sysadm.Permissions())
    m.add_action(sysadm.Users())
    m.add_action(sysadm.Groups())
    m.can_view = perms.is_staff
