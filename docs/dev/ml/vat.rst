=====
VAT
=====

.. module:: ml.vat

This module provides data definitions and business logic for handling
value-added tax (VAT).

It is implemented by :mod:`lino.modlib.vat`.

This module is designed to work both *with* and *without*
:mod:`ml.ledger` and :mod:`ml.declarations` installed.


Configuration
=============

.. class:: Plugin

  Extends :class:`ad.Plugin`. See also :doc:`/dev/ad`.

  vat_quarterly = False
    
  Set this to True to support quarterly VAT declarations.
  Used by :mod:`ml.declarations`.
    
  .. attribute:: VAT_CLASS_TO_RATE

  A dictionary object mapping VatClasses to their rate.
    
  Default value is::

    from decimal import Decimal
    VAT_CLASS_TO_RATE = dict(
        exempt=Decimal(),
        reduced=Decimal('0.07'),
        normal=Decimal('0.20')
    )



  .. attribute:: default_vat_regime 'private'

  .. attribute:: default_vat_class = 'normal'

  .. method:: get_vat_class(self, tt, item)

  .. method:: get_vat_rate(self, tt, vc, vr)





Choicelists
===========

.. class:: TradeTypes(dd.Choicelist)

  Typical content is as follows (but applications may redefine or
  extend this list in :meth:`ad.Site.setup_choicelists`):

  .. django2rst:: rt.show("vat.TradeTypes")

.. class:: TradeType(dd.Choice)

  Base class for choices of :class:`TradeTypes`.

  .. attribute:: price_field_name = None
  .. attribute:: price_field_label = None
  .. attribute:: partner_account_field_name = None
  .. attribute:: partner_account_field_label = None
  .. attribute:: base_account_field_name = None
  .. attribute:: base_account_field_label = None
  .. attribute:: vat_account_field_name = None
  .. attribute:: vat_account_field_label = None
  .. attribute:: dc = accounts.DEBIT

  .. method:: get_base_account(self)

  Return the :class:`ml.accounts.Account` into which the **base amount** of
  any operation should be booked.

  .. method:: get_vat_account(self)

  Return the :class:`ml.accounts.Account` into which the **VAT amount** of
  any operation should be booked.

  .. method:: get_partner_account(self)

  Return the :class:`ml.accounts.Account` into which the **total
  amount** of any operation (base + VAT) should be booked.

  .. method:: get_product_base_account(self, product)

  Return the :class:`ml.accounts.Account` into which the **base amount** of
  any operation should be booked.

  .. method:: get_catalog_product(self, product)

  Return the catalog price of the given product for this trade type.


.. class:: VatClasses(dd.Choicelist)

    A VAT class is a direct or indirect property of a trade object
    (e.g. a Product) which determines the VAT *rate* to be used.  It
    does not contain the actual rate because this still varies
    depending on your country, the time and type of the operation, and
    possibly other factors.

    Typical content is as follows (but applications may redefine or
    extend this list in :meth:`ad.Site.setup_choicelists`):

    .. django2rst:: rt.show("vat.VatRegimes")

.. class:: VatRegime(dd.Choice)

    Base class for choices of :class:`VatRegimes`.

    .. attribute:: item_vat = True

    Whether unit prices are VAT included or not.


.. class:: VatRegimes(dd.Choicelist)

    The VAT regime is a classification of the way how VAT is being
    handled.

    Typical content is as follows (but applications may redefine or
    extend this list in :meth:`ad.Site.setup_choicelists`):

    .. django2rst:: rt.show("vat.VatClasses")

Models
======

.. class:: PaymentTerm(dd.BabelNamed)

    A convention on how an Invoice should be paid.

Model mixins
============


.. class:: VatTotal(dd.Model)

    Model mixin which defines the fields `total_incl`, `total_base`
    and `total_vat`.  Used for both the document header
    (:class:`VatDocument`) and for each item (:class:`VatItemBase`).

    .. attribute:: auto_compute_totals = False

    Set this to `True` on subclasses who compute their totals
    automatically.


    .. attribute:: total_incl
    
    A :class:`dd.PriceField` which stores the total amount VAT
    *included*.

    .. attribute:: total_base

    A :class:`dd.PriceField` which stores the total amount VAT
    *excluded*.

    .. attribute:: total_vat

    A :class:`dd.PriceField` which stores the amount of VAT.


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

   
