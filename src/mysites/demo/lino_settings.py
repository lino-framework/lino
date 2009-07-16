from django.db.models.loading import get_model

Order = get_model('sales','order')
Invoice = get_model('sales','invoice')
BankStatement = get_model('finan','BankStatement')

Order.create_journal("ORD")
Invoice.create_journal("INV","4000")
BankStatement.create_journal("BANK","5500")

from lino.django.apps.ledger import models as ledger
ledger.set_accounts(
  providers='4400',
  customers='4000',
  sales_base='7000',
  sales_vat='4510',
)
