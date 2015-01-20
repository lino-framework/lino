=====
Sales
=====

.. module:: ml.sales

This module provides data definitions for writing "sales invoices".

It is implemented by :mod:`lino.modlib.sales` (basic functionality) or
:mod:`lino.modlib.auto.sales` (adds common definitions for automatic
generation of invoices).


Choicelists
===========

.. class:: InvoiceStates(dd.Workflow)

    List of the possible values for the state of an :class:`Invoice`.

    Typical content is as follows (but applications may redefine or
    extend this list in :meth:`lino.core.site.Site.setup_choicelists`):

    .. django2rst:: rt.show("sales.InvoiceStates")


Mixins
======

.. class:: SalesDocument

    Common base class for `orders.Order` and :class:`Invoice`.

.. class:: Invoiceable

    Available only in :mod:`lino.modlib.auto.sales`.

    Mixin for things that are "invoiceable", i.e. for which a customer
    is going to receive an invoice.

  .. attribute:: invoice

  .. attribute:: invoiceable_date_field

      To be set by subclasses.
      The name of the field which holds the invoiceable date.

  .. method:: get_partner_filter(cls, partner)

      To be implemented by subclasses.
      Return the filter to apply to :class:`ml.contacts.Partner` in
      order to get the partner who must receive the invoice.

  .. method:: get_invoiceable_product(self)

      To be implemented by subclasses.
      Return the product to put into the invoice item.

  .. method:: get_invoiceable_qty(self)

      To be implemented by subclasses.
      Return the quantity to put into the invoice item.

  .. method:: get_invoiceable_title(self)

      Return the title to put into the invoice item.
      May be overridden by subclasses.

  .. method:: get_invoiceables_for(cls, partner, max_date=None)



Models
======

.. class:: ShippingMode

  Represents a possible method of how the items described in a
  :class:`SalesDocument` are to be transferred from us to our customer.

  .. attribute:: price

.. class:: Invoice(SalesDocument)

  A sales invoice is a legal document which describes that something
  (the invoice items) has been sold to a given partner. The partner
  can be either a private person or an organization.

  Inherits from :class:`ml.ledger.Voucher`.

.. class:: InvoiceItem

  .. attribute:: invoiceable

.. class:: InvoicingMode

    Available only in :mod:`lino.modlib.auto.sales`.

    Represents a method of issuing/sending invoices.

  .. attribute:: price

  .. attribute:: advance_days

      How many days in advance invoices should be posted so that the
      customer has a chance to pay them in time.

Tables
======

.. class:: InvoicesByJournal

    Shows all invoices of a given journal (whose :attr:`voucher_type
    <ml.ledger.Journal.voucher_type>` must be :class:`Invoice`)

.. class:: ItemsByInvoice


.. class:: InvoiceablesByPartner(dd.VirtualTable)

  List of invoiceable items for this partner.

.. class:: InvoicesToCreate(dd.VirtualTable)

  Table of all partners who should receive an invoice.

  This table holds the :class:`CreateAllInvoices` action.



Actions
=======

.. class:: CreateAllInvoices

Create and print the invoice for each selected row, making these rows disappear from this table

.. class:: CreateInvoice

    Available only in :mod:`lino.modlib.auto.sales`.
    
    Create invoice from invoiceables for this partner.


.. class:: CreateInvoiceForPartner(CreateInvoice)

    Available only in :mod:`lino.modlib.auto.sales`.
    
    Create invoice from invoiceables for this partner.

