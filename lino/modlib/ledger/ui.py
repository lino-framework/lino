# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.ledger`.

- Models :class:`Journal`, :class:`Voucher` and :class:`Movement`

- :class:`DebtsByAccount` and :class:`DebtsByPartner` are two reports
  based on :class:`ExpectedMovements`

- :class:`GeneralAccountsBalance`, :class:`ClientAccountsBalance` and
  :class:`SupplierAccountsBalance` three reports based on
  :class:`AccountsBalance` and :class:`PartnerAccountsBalance`

- :class:`Debtors` and :class:`Creditors` are tables with one row for
  each partner who has a positive balance (either debit or credit).
  Accessible via :menuselection:`Reports --> Ledger --> Debtors` and
  :menuselection:`Reports --> Ledger --> Creditors`




"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.db import models

from lino.api import dd, rt, _
from lino import mixins
from lino.utils.report import Report
from lino.utils.xmlgen.html import E
from lino.utils import join_elems

from lino.modlib.accounts.utils import DEBIT, CREDIT, ZERO

from .utils import Balance, DueMovement, get_due_movements
from .choicelists import TradeTypes, FiscalYears
from .choicelists import VoucherStates
from .mixins import JournalRef
from .roles import AccountingReader, LedgerUser, LedgerStaff


class Journals(dd.Table):
    """The default table showing all instances of :class:`Journal`.

    """
    required_roles = dd.login_required(LedgerStaff)
    model = 'ledger.Journal'
    order_by = ["seqno"]
    column_names = "ref:5 name trade_type journal_group " \
                   "voucher_type force_sequence * seqno id"
    detail_layout = """
    ref:5 trade_type seqno id voucher_type:10 journal_group:10
    force_sequence account dc build_method template
    name
    printed_name
    MatchRulesByJournal
    """
    insert_layout = dd.FormLayout("""
    ref name
    trade_type
    voucher_type
    """, window_size=(60, 'auto'))


class ByJournal(dd.Table):
    order_by = ["-date", '-id']
    # order_by = ["-number"]
    master_key = 'journal'  # see django issue 10808
    # start_at_bottom = True
    required_roles = dd.required(LedgerUser)

    @classmethod
    def get_title_base(self, ar):
        """Without this override we would have a title like "Invoices of
        journal <Invoices>".  But we want just "Invoices".

        """
        return unicode(ar.master_instance)


class PaymentTerms(dd.Table):
    required_roles = dd.login_required(LedgerStaff)
    model = 'ledger.PaymentTerm'
    order_by = ["id"]


class Vouchers(dd.Table):
    """
    The base table for all tables working on :class:`Voucher`.
    """
    required_roles = dd.login_required(LedgerStaff)
    model = 'ledger.Voucher'
    editable = False
    order_by = ["date", "number"]
    column_names = "date number *"
    parameters = dict(
        year=FiscalYears.field(blank=True),
        journal=JournalRef(blank=True))
    params_layout = "year journal"

    @classmethod
    def get_request_queryset(cls, ar):
        qs = super(Vouchers, cls).get_request_queryset(ar)
        if not isinstance(qs, list):
            pv = ar.param_values
            if pv.year:
                qs = qs.filter(year=pv.year)
            if pv.journal:
                qs = qs.filter(journal=pv.journal)
        return qs


class MatchRules(dd.Table):
    required_roles = dd.login_required(LedgerStaff)
    model = 'ledger.MatchRule'


class MatchRulesByAccount(MatchRules):
    master_key = 'account'


class MatchRulesByJournal(ByJournal, MatchRules):
    master_key = 'journal'


class ExpectedMovements(dd.VirtualTable):
    """
    A virtual table of :class:`DueMovement` rows, showing
    all "expected" "movements (payments)".

    Subclassed by :class:`lino.modlib.finan.models.SuggestionsByVoucher`.


    """
    required_roles = dd.required(AccountingReader)
    label = _("Debts")
    icon_name = 'book_link'
    #~ column_names = 'match due_date debts payments balance'
    column_names = 'due_date:15 balance debts payments'
    auto_fit_column_widths = True
    parameters = dd.ParameterPanel(
        date_until=models.DateField(_("Date until"), blank=True, null=True),
        trade_type=TradeTypes.field(blank=True),
        for_journal=dd.ForeignKey('ledger.Journal', blank=True))
        #~ dc=DebitOrCreditField(default=accounts.DEBIT))
    params_layout = "trade_type date_until for_journal"

    #~ DUE_DC = accounts.DEBIT

    @classmethod
    def get_dc(cls, ar=None):
        return DEBIT

    @classmethod
    def get_data_rows(cls, ar, **flt):
        #~ if ar.param_values.journal:
            #~ pass
        pv = ar.param_values
        if pv.trade_type:
            flt.update(account=pv.trade_type.get_partner_account())
        if pv.date_until is not None:
            flt.update(voucher__date__lte=pv.date_until)
        if pv.for_journal is not None:
            accounts = rt.modules.accounts.Account.objects.filter(
                matchrule__journal=pv.for_journal).distinct()
            flt.update(account__in=accounts)
        return get_due_movements(cls.get_dc(ar), **flt)

    @classmethod
    def get_pk_field(self):
        return rt.modules.ledger.Movement._meta.pk

    @classmethod
    def get_row_by_pk(cls, ar, pk):
        mvt = rt.modules.ledger.Movement.objects.get(pk=pk)
        return cls.get_row_for(mvt, ar)

    @classmethod
    def get_row_for(cls, mvt, ar):
        return DueMovement(cls.get_dc(ar), mvt)

    @dd.displayfield(_("Match"))
    def match(self, row, ar):
        return row.match

    @dd.virtualfield(
        models.DateField(
            _("Due date"),
            help_text=_("Due date of the eldest debt in this match group")))
    def due_date(self, row, ar):
        return row.due_date

    @dd.displayfield(
        _("Debts"), help_text=_("List of invoices in this match group"))
    def debts(self, row, ar):
        return E.span(*join_elems([   # E.p(...) until 20150128
            ar.obj2html(i.voucher.get_mti_leaf()) for i in row.debts]))

    @dd.displayfield(
        _("Payments"), help_text=_("List of payments in this match group"))
    def payments(self, row, ar):
        return E.span(*join_elems([    # E.p(...) until 20150128
            ar.obj2html(i.voucher.get_mti_leaf()) for i in row.payments]))

    @dd.virtualfield(dd.PriceField(_("Balance")))
    def balance(self, row, ar):
        return row.balance

    @dd.virtualfield(dd.ForeignKey('contacts.Partner'))
    def partner(self, row, ar):
        return row.partner

    @dd.virtualfield(dd.ForeignKey('accounts.Account'))
    def account(self, row, ar):
        return row.account

    @dd.virtualfield(dd.ForeignKey(
        'sepa.Account', verbose_name=_("Bank account")))
    def bank_account(self, row, ar):
        return row.bank_account


class DebtsByAccount(ExpectedMovements):
    """
    The :class:`ExpectedMovements` accessible by clicking the "Debts"
    action button on an :class:`Account <ml.accounts.Account>`.

    """
    master = 'accounts.Account'

    @classmethod
    def get_data_rows(cls, ar, **flt):
        account = ar.master_instance
        if account is None:
            return []
        if not account.clearable:
            return []
        #~ return get_due_movements(cls.DUE_DC,account=account,satisfied=False)
        flt.update(satisfied=False, account=account)
        # ignore trade_type to avoid overriding account
        ar.param_values.trade_type = None
        return super(DebtsByAccount, cls).get_data_rows(ar, **flt)

dd.inject_action('accounts.Account', due=dd.ShowSlaveTable(DebtsByAccount))


class DebtsByPartner(ExpectedMovements):
    """
    This is the table being printed in a Payment Reminder.  Usually
    this table has one row per sales invoice which is not fully paid.
    But several invoices ("debts") may be grouped by match.  If the
    partner has purchase invoices, these are deduced from the balance.

    This table is accessible by clicking the "Debts" action button on
    a :class:`Partner <ml.contacts.Partner>`.

    """
    master = 'contacts.Partner'
    #~ column_names = 'due_date debts payments balance'

    @classmethod
    def get_dc(cls, ar=None):
        return CREDIT

    @classmethod
    def get_data_rows(cls, ar, **flt):
        partner = ar.master_instance
        if partner is None:
            return []
        flt.update(satisfied=False, partner=partner)
        return super(DebtsByPartner, cls).get_data_rows(ar, **flt)

dd.inject_action('contacts.Partner', due=dd.ShowSlaveTable(DebtsByPartner))


class PartnerVouchers(Vouchers):
    editable = True

    parameters = dict(
        project=dd.ForeignKey(
            dd.plugins.ledger.project_model, blank=True, null=True),
        state=VoucherStates.field(blank=True),
        partner=dd.ForeignKey('contacts.Partner', blank=True, null=True),
        **Vouchers.parameters)
    params_layout = "partner project state journal year"
    params_panel_hidden = True

    @classmethod
    def get_simple_parameters(cls):
        s = super(PartnerVouchers, cls).get_simple_parameters()
        s |= set(['partner', 'state'])
        return s


def mvtsum(**fkw):
    d = rt.modules.ledger.Movement.objects.filter(
        **fkw).aggregate(models.Sum('amount'))
    return d['amount__sum'] or ZERO


class AccountsBalance(dd.VirtualTable):
    """A virtual table, the base class for different reports that show a
    list of accounts with the following columns:

      ref description old_d old_c during_d during_c new_d new_c

    Subclasses are :class:'GeneralAccountsBalance`,
    :class:'ClientAccountsBalance` and
    :class:'SupplierAccountsBalance`.

    """
    auto_fit_column_widths = True
    column_names = "ref description old_d old_c during_d during_c new_d new_c"
    slave_grid_format = 'html'
    abstract = True

    @classmethod
    def rowmvtfilter(self, row):
        raise NotImplementedError()

    @classmethod
    def get_request_queryset(self, ar):
        raise NotImplementedError()

    @classmethod
    def get_data_rows(self, ar):
        mi = ar.master_instance
        if mi is None:
            return
        qs = self.get_request_queryset(ar)
        for row in qs:
            flt = self.rowmvtfilter(row)
            row.old = Balance(
                mvtsum(
                    voucher__date__lt=mi.start_date,
                    dc=DEBIT, **flt),
                mvtsum(
                    voucher__date__lt=mi.start_date,
                    dc=CREDIT, **flt))
            row.during_d = mvtsum(
                voucher__date__gte=mi.start_date,
                voucher__date__lte=mi.end_date,
                dc=DEBIT, **flt)
            row.during_c = mvtsum(
                voucher__date__gte=mi.start_date,
                voucher__date__lte=mi.end_date,
                dc=CREDIT, **flt)
            if row.old.d or row.old.c or row.during_d or row.during_c:
                row.new = Balance(row.old.d + row.during_d,
                                  row.old.c + row.during_c)
                yield row

    @dd.displayfield(_("Description"))
    def description(self, row, ar):
        #~ return unicode(row)
        return ar.obj2html(row)

    @dd.virtualfield(dd.PriceField(_("Debit\nbefore")))
    def old_d(self, row, ar):
        return row.old.d

    @dd.virtualfield(dd.PriceField(_("Credit\nbefore")))
    def old_c(self, row, ar):
        return row.old.c

    @dd.virtualfield(dd.PriceField(_("Debit")))
    def during_d(self, row, ar):
        return row.during_d

    @dd.virtualfield(dd.PriceField(_("Credit")))
    def during_c(self, row, ar):
        return row.during_c

    @dd.virtualfield(dd.PriceField(_("Debit\nafter")))
    def new_d(self, row, ar):
        return row.new.c

    @dd.virtualfield(dd.PriceField(_("Credit\nafter")))
    def new_c(self, row, ar):
        return row.new.d


class GeneralAccountsBalance(AccountsBalance):
    """An :class:`AccountsBalance` for general accounts.

    """

    label = _("General Accounts Balances")

    @classmethod
    def get_request_queryset(self, ar):
        return rt.modules.accounts.Account.objects.order_by(
            'group__ref', 'ref')

    @classmethod
    def rowmvtfilter(self, row):
        return dict(account=row)

    @dd.displayfield(_("Ref"))
    def ref(self, row, ar):
        return ar.obj2html(row.group)


class PartnerAccountsBalance(AccountsBalance):
    """An :class:`AccountsBalance` for partner accounts.

    """
    trade_type = NotImplementedError

    @classmethod
    def get_request_queryset(self, ar):
        return rt.modules.contacts.Partner.objects.order_by('name')

    @classmethod
    def rowmvtfilter(self, row):
        a = self.trade_type.get_partner_account()
        # TODO: what if a is None?
        return dict(partner=row, account=a)

    @dd.displayfield(_("Ref"))
    def ref(self, row, ar):
        return str(row.pk)


class ClientAccountsBalance(PartnerAccountsBalance):
    """
    A :class:`PartnerAccountsBalance` for the TradeType "sales".

    """
    label = _("Client Accounts Balances")
    trade_type = TradeTypes.sales


class SupplierAccountsBalance(PartnerAccountsBalance):
    """
    A :class:`PartnerAccountsBalance` for the TradeType "purchases".
    """
    label = _("Supplier Accounts Balances")
    trade_type = TradeTypes.purchases


##


class DebtorsCreditors(dd.VirtualTable):
    """
    Abstract base class for different tables showing a list of
    partners with the following columns:

      partner due_date balance actions


    """
    required_roles = dd.required(AccountingReader)
    auto_fit_column_widths = True
    column_names = "age due_date partner balance actions"
    slave_grid_format = 'html'
    abstract = True

    parameters = mixins.Today()
    # params_layout = "today"

    d_or_c = NotImplementedError

    @classmethod
    def rowmvtfilter(self, row):
        raise NotImplementedError()

    @classmethod
    def get_data_rows(self, ar):
        rows = []
        mi = ar.master_instance
        if mi is None:  # called directly from main menu
            if ar.param_values is None:
                return rows
            end_date = ar.param_values.today
        else:   # called from Situation report
            end_date = mi.today
        
        qs = rt.modules.contacts.Partner.objects.order_by('name')
        for row in qs:
            row._balance = ZERO
            row._due_date = None
            for dm in get_due_movements(
                    self.d_or_c,
                    partner=row,
                    voucher__date__lte=end_date):
                row._balance += dm.balance
                if dm.due_date is not None:
                    if row._due_date is None or row._due_date > dm.due_date:
                        row._due_date = dm.due_date
                # logger.info("20140105 %s %s", row, dm)

            if row._balance > ZERO:
                rows.append(row)

        def f(a, b):
            return cmp(a._due_date, b._due_date)
        rows.sort(f)
        return rows

    @dd.displayfield(_("Partner"))
    def partner(self, row, ar):
        return ar.obj2html(row)

    @dd.virtualfield(dd.PriceField(_("Balance")))
    def balance(self, row, ar):
        return row._balance

    @dd.virtualfield(models.DateField(_("Due date")))
    def due_date(self, row, ar):
        return row._due_date

    @dd.virtualfield(models.IntegerField(_("Age")))
    def age(self, row, ar):
        dd = ar.param_values.today - row._due_date
        return dd.days

    @dd.displayfield(_("Actions"))
    def actions(self, row, ar):
        # TODO
        return E.span("[Show debts] [Issue reminder]")


class Debtors(DebtorsCreditors):
    """
    Lists those partners who have some debt against us.
    :class:`DebtorsCreditors`.

    """
    label = _("Debtors")
    help_text = _("List of partners (usually clients) \
    who are in debt towards us.")
    d_or_c = CREDIT


class Creditors(DebtorsCreditors):
    """
    Lists those partners who give us some form of credit.
    :class:`DebtorsCreditors`.
    """
    label = _("Creditors")
    help_text = _("List of partners (usually suppliers) \
    who are giving credit to us.")

    d_or_c = DEBIT

##


class Situation(Report):
    """
    A report consisting of the following tables:

   -  :class:`Debtors`
   -  :class:`Creditors`

    """
    label = _("Situation")
    help_text = _("Overview of the financial situation on a given date.")
    required_roles = dd.required(AccountingReader)

    parameters = mixins.Today()

    report_items = (Debtors, Creditors)


class ActivityReport(Report):
    """
    A report consisting of the following tables:

    - :class:`GeneralAccountsBalance`
    - :class:`ClientAccountsBalance`
    - :class:`SupplierAccountsBalance`

    """
    label = _("Activity Report")
    help_text = _("Overview of the financial activity during a given period.")
    required_roles = dd.required(AccountingReader)

    parameters = mixins.Yearly(
        # include_vat = models.BooleanField(
        #     verbose_name=dd.apps.vat.verbose_name),
    )

    params_layout = "start_date end_date"
    #~ params_panel_hidden = True

    report_items = (
        GeneralAccountsBalance,
        ClientAccountsBalance,
        SupplierAccountsBalance)


# MODULE_LABEL = dd.plugins.accounts.verbose_name

# def site_setup(site):
#     c = site.modules.contacts
#     for T in (c.Partners, c.Companies, c.Persons):
#         if not hasattr(T.detail_layout, 'ledger'):
#             T.add_detail_tab(
#                 "ledger",
#                 """
#                 ledger.VouchersByPartner
#                 ledger.MovementsByPartner
#                 """,
#                 label=MODULE_LABEL)


class Movements(dd.Table):
    """
    The base table for all tables working on :class:`Movement`.

    Displayed by :menuselection:`Explorer --> Accounting --> Movements`.

    This is also the base class for :class:`MovementsByVoucher`,
    :class:`MovementsByAccount` and :class:`MovementsByPartner` and
    defines e.g. filtering parameters.
    """
    
    required_roles = dd.login_required(LedgerStaff)
    model = 'ledger.Movement'
    column_names = 'voucher_link account debit credit *'
    editable = False
    parameters = mixins.ObservedPeriod(
        pyear=FiscalYears.field(blank=True),
        ppartner=models.ForeignKey('contacts.Partner', blank=True, null=True),
        paccount=models.ForeignKey('accounts.Account', blank=True, null=True),
        pjournal=JournalRef(blank=True),
        cleared=dd.YesNo.field(_("Show cleared movements"), blank=True))
    params_layout = """
    start_date end_date cleared
    pjournal pyear ppartner paccount"""

    @classmethod
    def get_request_queryset(cls, ar):
        qs = super(Movements, cls).get_request_queryset(ar)

        if ar.param_values.cleared == dd.YesNo.yes:
            qs = qs.filter(satisfied=True)
        elif ar.param_values.cleared == dd.YesNo.no:
            qs = qs.filter(satisfied=False)

        if ar.param_values.ppartner:
            qs = qs.filter(partner=ar.param_values.ppartner)
        if ar.param_values.paccount:
            qs = qs.filter(account=ar.param_values.paccount)
        if ar.param_values.pyear:
            qs = qs.filter(voucher__year=ar.param_values.pyear)
        if ar.param_values.pjournal:
            qs = qs.filter(voucher__journal=ar.param_values.pjournal)
        return qs


class MovementsByVoucher(Movements):
    master_key = 'voucher'
    column_names = 'seqno project partner account debit credit match satisfied'
    # auto_fit_column_widths = True
    slave_grid_format = "html"


class MovementsByPartner(Movements):
    master_key = 'partner'
    order_by = ['-voucher__date']
    column_names = ('voucher__date voucher_link debit credit '
                    'match project satisfied *')
    slave_grid_format = "html"
    # auto_fit_column_widths = True

    @classmethod
    def param_defaults(cls, ar, **kw):
        kw = super(MovementsByPartner, cls).param_defaults(ar, **kw)
        kw.update(cleared=dd.YesNo.no)
        kw.update(pyear='')
        return kw


class MovementsByProject(MovementsByPartner):
    master_key = 'project'
    column_names = ('voucher__date voucher_link account partner debit credit '
                    'match satisfied *')
    slave_grid_format = "html"


class MovementsByAccount(Movements):
    master_key = 'account'
    order_by = ['-voucher__date']
    column_names = 'voucher__date voucher_link debit credit \
    partner match satisfied'
    # auto_fit_column_widths = True
    slave_grid_format = "html"

    @classmethod
    def param_defaults(cls, ar, **kw):
        kw = super(MovementsByAccount, cls).param_defaults(ar, **kw)
        if ar.master_instance is not None and ar.master_instance.clearable:
            kw.update(cleared=dd.YesNo.no)
            kw.update(pyear='')
        return kw


