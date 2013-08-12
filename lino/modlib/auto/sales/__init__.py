from lino import ad
    
class App(ad.App):

    extends = 'lino.modlib.sales'
    extends_models = ['sales.Invoice',  'sales.InvoiceItem']
