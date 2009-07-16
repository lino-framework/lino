from django.db.models.loading import get_model

Order = get_model('sales','order')
Invoice = get_model('sales','invoice')
BankStatement = get_model('finan','BankStatement')

Order.create_journal("ORD")
Invoice.create_journal("INV","400000")
BankStatement.create_journal("BANK","550000")
