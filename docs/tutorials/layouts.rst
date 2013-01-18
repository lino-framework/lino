==========================
An introduction to layouts
==========================

:doc:`/topics/layouts`
are one of Lino's important and innovative features.
They provide a way to design forms independently from the chosen user-interface.
Concept and implementation is fully the author's idea, and we 
didn't yet find a similar approach in any other framework.


TODO: continue this tutorial.

If you want a modal window (not a full-screen window), then 
you need to specify the `window_size` keyword argument. 
A simple FormLayout


.. textimage:: layouts1.jpg
  :scale: 40 %
  
  ::

    class Invoices(SalesDocuments):
        ...
        insert_layout = dd.FormLayout("""
        partner date 
        subject
        """,window_size=(40,'auto'))


If the ``main`` panel of a FormLayout is *horizontal* (i.e.) 
doesn't contain any newline, then the Layout will be rendered 
as a tabbed panel.

.. textimage:: layouts2.jpg layouts3.jpg layouts4.jpg
  :scale: 40 %
  
  ::
  
    class InvoiceDetail(dd.FormLayout):
        main = "general more ledger"
        
        totals = dd.Panel("""
        # discount
        total_base
        total_vat
        total_incl
        workflow_buttons
        """,label=_("Totals"))
        
        invoice_header = dd.Panel("""
        date partner vat_regime 
        order subject your_ref 
        payment_term due_date:20 
        imode shipping_mode     
        """,label=_("Header")) # sales_remark 
        
        general = dd.Panel("""
        invoice_header:60 totals:20
        ItemsByInvoice
        """,label=_("General"))
        
        more = dd.Panel("""
        id user language project item_vat
        intro
        """,label=_("More"))
        
        ledger = dd.Panel("""
        journal year number narration
        ledger.MovementsByVoucher
        """,label=_("Ledger"))
    
    class Invoices(SalesDocuments):
        ...
        detail_layout = InvoiceDetail()  
        