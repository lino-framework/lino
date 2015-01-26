======
Ledger
======

.. module:: ml.ledger


Model mixins
============

.. class:: Matchable

    Base class for :class:`AccountInvoice`
    (and e.g. `sales.Invoice`, `finan.DocItem`)
    
    Adds a field `match` and a chooser for it.
    Requires a field `partner`.

.. class:: VoucherItem

    Base class for items of a voucher.

    Subclasses must define a field `voucher` which must 
    be a ForeignKey with related_name='items'



ChoiceLists
===========

.. class:: VoucherType

    .. method:: get_journals

    Return a list of the :class:`Journal` objects that work on this
    voucher type.

.. class:: VoucherTypes


    .. method:: get_for_model

    Return the :class:`VoucherType` for the given model.

.. class:: InvoiceStates


Tables
======

.. class:: InvoicesByJournal

    Shows all invoices of a given journal (whose
    :attr:`Journal.voucher_type` must be :class:`AccountInvoice`)




Custom fields
=============

.. class:: MatchField

    A simple extension to CharField, with default values for
    `verbose_name` and `max_length`.

.. class:: DcAmountField

    An editable virtual field to set both fields `amount` and `dc`


Miscellaneous
=============

.. class:: Balance

    .. attribute:: d

    The amount of this balance when it is debiting.

    .. attribute:: c

    The amount of this balance when it is crediting.


.. class:: DueMovement

    Volatile object representing a group of "matching" movements.
    
    The "matching" movements of a given movement are those whose
    `match`, `partner` and `account` fields have the same values.
    
    These movements are themselves grouped into "debts" and "payments".
    A "debt" increases the debt and a "payment" decreases it.
    
    The value of `dc` specifies whether I mean *my* debts and payments
    (towards that partner) or those *of the partner* (towards me).


.. function:: get_due_movements(dc, **flt)

    Generates and yields a list of the :class:`DueMovement` objects
    specified by the filter criteria.

    :param dc: The caller must specify whether he means the debts and
               payments *towards the partner* or *towards myself*.

    :param flt: Any keyword argument is forwarded to Django's
                `filter()
                <https://docs.djangoproject.com/en/dev/ref/models/querysets/#filter>`_
                method, used to specifiy which :class:`Movement`
                objects to consider.


Debts
-----

.. class:: ExpectedMovements

    A :class:`dd.VirtualTable` of :class:`DueMovement` rows, showing
    all "expected" "movements (payments)".

    Subclassed by :class:`ml.finan.SuggestionsByVoucher`.



.. class:: DebtsByAccount

    The :class:`ExpectedMovements` accessible by clicking the "Debts"
    action button on an :class:`Account <ml.accounts.Account>`.

.. class:: DebtsByPartner

    This is the table being printed in a Payment Reminder.  Usually
    this table has one row per sales invoice which is not fully paid.
    But several invoices ("debts") may be grouped by match.  If the
    partner has purchase invoices, these are deduced from the balance.

    This table is accessible by clicking the "Debts" action button on
    a :class:`Partner <ml.contacts.Partner>`.


Account balances
----------------

.. class:: AccountsBalance

    A :class:`dd.VirtualTable`, the base class for different reports
    that show a list of accounts with the following columns:

      ref description old_d old_c during_d during_c new_d new_c

    Subclasses are 
    :class:'GeneralAccountsBalance`,
    :class:'ClientAccountsBalance`
    and
    :class:'SupplierAccountsBalance`.


.. class:: GeneralAccountsBalance

    An :class:`AccountsBalance` for general accounts.

.. class:: PartnerAccountsBalance

    An :class:`AccountsBalance` for partner accounts.


.. class:: ClientAccountsBalance

    A :class:`PartnerAccountsBalance` for the TradeType "sales".

.. class:: SupplierAccountsBalance

    A :class:`PartnerAccountsBalance` for the TradeType "purchases".



.. class:: DebtorsCreditors

    Abstract base class for different tables showing a list of
    partners with the following columns:

    partner due_date balance actions


.. class:: Debtors

    Lists those partners who have some debt against us.
    :class:`DebtorsCreditors`.

.. class:: Creditors

    Lists those partners who give us some form of credit.
    :class:`DebtorsCreditors`.




Reports
-------

.. class:: Situation

    A report consisting of the following tables:

   -  :class:`Debtors`
   -  :class:`Creditors`

.. class:: ActivityReport

    A report consisting of the following tables:

    - :class:`GeneralAccountsBalance`
    - :class:`ClientAccountsBalance`
    - :class:`SupplierAccountsBalance`

