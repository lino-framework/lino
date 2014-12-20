=====
VAT
=====

.. module:: ml.vat

Content moved to :mod:`lino.modlib.vat`.


Model mixins
============


.. class:: VatTotal(dd.Model)

    .. attribute:: auto_compute_totals = False


.. class:: VatDocument(VatTotal)

    Abstract base class for invoices, offers and other vouchers.

    .. attribute:: refresh_after_item_edit = False
 
    See :doc:`/tickets/68`

    .. attribute:: partner

    The recipient of this document. A pointer to
    :class:`ml.contacts.Partner`.

    .. attribute:: vat_regime

    The VAT regime to be used in this document.  A pointer to
    :class:`VatRegimes`.

    .. attribute:: payment_term

    The payment terms to be used in this document.  A pointer to
    :class:`PaymentTerm`.



.. class:: VatItemBase(mixins.Sequenced, VatTotal)

    Abstract Base class for :class:`ml.ledger.InvoiceItem`, i.e. the
    lines of invoices *without* unit prices and quantities.

    Subclasses must define a field called "voucher" which must be a
    ForeignKey with related_name="items" to the "owning document",
    which in turn must be a subclass of :class:`VatDocument`).

    .. attribute:: vat_class

    The VAT class to be applied for this item. A pointer to
    :class:`VatClasses`.


.. class:: QtyVatItemBase(VatItemBase)

    Abstract Base class for :class:`ml.sales.InvoiceItem` and
    :class:`ml.sales.OrderItem`, i.e. the lines of invoices *with*
    unit prices and quantities.

   
