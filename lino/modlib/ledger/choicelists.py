# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Choicelists for `lino.modlib.ledger`.

.. autosummary::

"""

from django.conf import settings

from lino.api import dd, rt, _

from lino.modlib.accounts.utils import DEBIT, CREDIT
from .roles import LedgerStaff


class JournalGroups(dd.ChoiceList):
    """The list of possible journal groups.

    This list is used to build the main menu. For each journal group
    there will be a menu item in the main menu.

    Journals whose :attr:`journal_group
    <lino.modlib.ledger.models.Journal.journal_group>` is empty will
    not be available through the main user menu.

    The default configuration has the following journal groups:

    .. attribute:: sales

        For sales journals.

    .. attribute:: purchases

        For purchases journals.

    .. attribute:: wages

        For wages journals.

    .. attribute:: financial

        For financial journals (bank statements and cash reports)

    """

add = JournalGroups.add_item
add('10', _("Sales"), 'sales')
add('20', _("Purchases"), 'purchases')
add('30', _("Wages"), 'wages')
add('40', _("Financial"), 'financial')


class FiscalYear(dd.Choice):
    pass


class FiscalYears(dd.ChoiceList):

    """A list of the fiscal years available in this database.

    The default value for this list is 5 years starting from
    :attr:`lino.core.site.Site.start_year`.  If the fiscal year of
    your company is the same as the calendar year, then the default
    entries in this should do.  Otherwise you can always override this
    in your :meth:`lino.core.site.Site.setup_choicelists`.

    """
    required_roles = dd.login_required(LedgerStaff)
    item_class = FiscalYear
    verbose_name = _("Fiscal Year")
    verbose_name_plural = _("Fiscal Years")
    # ~ preferred_width = 4 # would be 2 otherwise

    @classmethod
    def from_int(cls, year):
        return cls.get_by_value(str(year)[2:])

    @classmethod
    def from_date(cls, date):
        return cls.from_int(date.year)

for y in range(settings.SITE.start_year, dd.today().year + 5):
    s = str(y)
    FiscalYears.add_item(s[2:], s)


class VoucherType(dd.Choice):

    def __init__(self, model, table_class):
        self.table_class = table_class
        model = dd.resolve_model(model)
        self.model = model
        value = dd.full_model_name(model)
        text = model._meta.verbose_name + ' (%s)' % dd.full_model_name(model)
        # text = model._meta.verbose_name + ' (%s.%s)' % (
        #     model.__module__, model.__name__)
        name = None
        super(VoucherType, self).__init__(value, text, name)

    def get_journals(self):
        """Return a list of the :class:`Journal` objects that work on this
        voucher type.

        """
        return rt.modules.ledger.Journal.objects.filter(voucher_type=self)


class VoucherTypes(dd.ChoiceList):
    """A list of the available voucher types (i.e. the database models
    subclasses of ledger.Voucher`).

    """

    required_roles = dd.login_required(LedgerStaff)
    verbose_name = _("Voucher type")
    verbose_name_plural = _("Voucher types")

    item_class = VoucherType
    max_length = 100

    @classmethod
    def get_for_model(self, model):
        """
        Return the :class:`VoucherType` for the given model.
        """
        for o in self.objects():
            # ~ o.model = dd.resolve_model(o.model) # TODO: resolve only once
            if o.model is model:
                return o

    @classmethod
    def add_item(cls, model, table_class):
        return cls.add_item_instance(VoucherType(model, table_class))


class TradeType(dd.Choice):
    """Base class for the choices of :class:`TradeTypes`.

    """
    price_field_name = None
    price_field_label = None
    partner_account_field_name = None
    partner_account_field_label = None
    base_account_field_name = None
    base_account_field_label = None
    vat_account_field_name = None
    vat_account_field_label = None
    dc = DEBIT

    def get_base_account(self):
        """Return the :class:`lino.modlib.accounts.models.Account` into which
        the **base amount** of any operation should be booked.

        """
        if self.base_account_field_name is None:
            return None
            # raise Exception("%s has no base_account_field_name!" % self)
        return getattr(settings.SITE.site_config,
                       self.base_account_field_name)

    def get_vat_account(self):
        """Return the :class:`ml.accounts.Account` into which the **VAT
        amount** of any operation should be booked.

        """
        if self.vat_account_field_name is None:
            return None
            # raise Exception("%s has no vat_account_field_name!" % self)
        return getattr(settings.SITE.site_config, self.vat_account_field_name)

    def get_partner_account(self):
        """Return the :class:`ml.accounts.Account` into which the **total
      amount** of any operation (base + VAT) should be booked.

        """
        if self.partner_account_field_name is None:
            return None
        return getattr(
            settings.SITE.site_config, self.partner_account_field_name)

    def get_product_base_account(self, product):
        """Return the :class:`ml.accounts.Account` into which the **base
        amount** of any operation should be booked.

        """
        if self.base_account_field_name is None:
            raise Exception("%s has no base_account_field_name" % self)
        return getattr(product, self.base_account_field_name) or \
            getattr(settings.SITE.site_config, self.base_account_field_name)

    def get_catalog_price(self, product):
        """Return the catalog price of the given product for operations with
this trade type.

        """
        return getattr(product, self.price_field_name)


class TradeTypes(dd.ChoiceList):
    """A choicelist with the **trade types** defined for this application.

    The trade type is one of the basic properties of every accountable
    operation where are partner is involved.

    The default configuration defines the following trade types:

    .. attribute:: sales

        A sale transaction is when you write an invoice to a customer
        and then expect the customer to pay it.

    .. attribute:: purchases

        A purchase transaction is when you get an invoice from a
        provider who expects you to pay it.


    .. attribute:: wages

        A wage transaction is when you write a payroll (declare the
        fact that you owe some wage to an employee) and later pay it
        (e.g. via a payment order).


    .. attribute:: clearings

        A clearing transaction is when an employee declares that he
        paid some invoice for you, and later you pay that money back
        to his account.

    """

    required_roles = dd.login_required(LedgerStaff)
    verbose_name = _("Trade type")
    verbose_name_plural = _("Trade types")
    item_class = TradeType
    help_text = _("The type of trade: usually either `sales` or `purchases`.")

TradeTypes.add_item('S', _("Sales"), 'sales', dc=CREDIT)
TradeTypes.add_item('P', _("Purchases"), 'purchases', dc=DEBIT)
TradeTypes.add_item('W', _("Wages"), 'wages', dc=DEBIT)
TradeTypes.add_item('C', _("Clearings"), 'clearings', dc=DEBIT)

# Note that :mod:`lino.modlib.sales.models` and/or
# :mod:`lino.modlib.ledger.models` (if installed) will modify
# `TradeTypes.sales` at module level so that the following
# `inject_vat_fields` will inject the required fields to
# system.SiteConfig and products.Product (if these are installed).


@dd.receiver(dd.pre_analyze)
def inject_vat_fields(sender, **kw):
    for tt in TradeTypes.items():
        if tt.partner_account_field_name is not None:
            dd.inject_field(
                'system.SiteConfig',
                tt.partner_account_field_name,
                dd.ForeignKey(
                    'accounts.Account',
                    verbose_name=tt.partner_account_field_label,
                    related_name='configs_by_' + tt.partner_account_field_name,
                    blank=True, null=True))
        if tt.vat_account_field_name is not None:
            dd.inject_field('system.SiteConfig', tt.vat_account_field_name,
                            dd.ForeignKey(
                                'accounts.Account',
                                verbose_name=tt.vat_account_field_label,
                                related_name='configs_by_' +
                                tt.vat_account_field_name,
                                blank=True, null=True))
        if tt.base_account_field_name is not None:
            dd.inject_field('system.SiteConfig', tt.base_account_field_name,
                            dd.ForeignKey(
                                'accounts.Account',
                                verbose_name=tt.base_account_field_label,
                                related_name='configs_by_' +
                                tt.base_account_field_name,
                                blank=True, null=True))
            dd.inject_field('products.Product', tt.base_account_field_name,
                            dd.ForeignKey(
                                'accounts.Account',
                                verbose_name=tt.base_account_field_label,
                                related_name='products_by_' +
                                tt.base_account_field_name,
                                blank=True, null=True))
        if tt.price_field_name is not None:
            dd.inject_field('products.Product', tt.price_field_name,
                            dd.PriceField(verbose_name=tt.price_field_label,
                                          blank=True, null=True))


class VoucherStates(dd.Workflow):
    #~ label = _("State")
    pass
add = VoucherStates.add_item
add('10', _("Draft"), 'draft', editable=True)
add('20', _("Registered"), 'registered', editable=False)
add('30', _("Fixed"), 'fixed', editable=False)


@dd.receiver(dd.pre_analyze)
def setup_vat_workflow(sender=None, **kw):
    if False:
        VoucherStates.registered.add_transition(
            _("Register"), required_states='draft', icon_name='accept')
        VoucherStates.draft.add_transition(
            _("Deregister"), required_states="registered", icon_name='pencil')
    else:
        VoucherStates.registered.add_transition(
            unichr(0x25c6),  # ◆
            help_text=_("Register"), required_states='draft')
        VoucherStates.draft.add_transition(
            unichr(0x25c7),  # ◇
            help_text=_("Deregister"),
            required_states="registered")


