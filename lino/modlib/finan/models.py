# Copyright 2008-2013 Luc Saffre
# License: BSD (see file COPYING for details)
"""
The :xfile:`models` module for the :mod:`lino.modlib.finan` app.
"""


import logging
logger = logging.getLogger(__name__)

import sys
import decimal

#~ from django import forms

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


from lino import dd, rt
from lino import mixins

from decimal import Decimal
ZERO = Decimal()


#~ from lino import fields
#~ from lino.core.dbutils import resolve_model

partners = dd.resolve_app(settings.SITE.partners_app_label)
ledger = dd.resolve_app('ledger')
#~ from lino.modlib.ledger import models as ledger
#~ journals = dd.resolve_app('journals')
accounts = dd.resolve_app('accounts')

partner_model = settings.SITE.partners_app_label + '.Partner'


#~ Contact = dd.resolve_model('contacts.Contact')
#~ Person = resolve_model('contacts.Person')
#~ Company = resolve_model('contacts.Company')

#~ def _functionId(nFramesUp):
    # ~ # thanks to:
    # ~ # http://nedbatchelder.com/blog/200410/file_and_line_in_python.html
    #~ """ Create a string naming the function n frames up on the stack.
    #~ """
    #~ co = sys._getframe(nFramesUp+1).f_code
    #~ return "%s (%s:%d)" % (co.co_name, co.co_filename, co.co_firstlineno)
#~

#~ def todo_notice(msg):
    #~ print "[todo] in %s :\n       %s" % (_functionId(1),msg)


class VoucherStates(dd.Workflow):
    #~ label = _("State")
    pass
add = VoucherStates.add_item
add('10', _("Draft"), 'draft', editable=True)
add('20', _("Registered"), 'registered', editable=False)

VoucherStates.registered.add_transition(
    _("Register"), states='draft', icon_name='accept')
VoucherStates.draft.add_transition(
    _("Deregister"), states="registered", icon_name='pencil')


class Voucher(ledger.Voucher):

    state = VoucherStates.field(default=VoucherStates.draft)

    class Meta:
        abstract = True

    def register(self, ar):
        super(Voucher, self).register(ar)
        self.update_satisfied()

    def deregister(self, ar):
        super(Voucher, self).deregister(ar)
        self.update_satisfied()

    def update_satisfied(self):
        partners = set()
        #~ matches = dict()
        for i in self.items.all():
            if i.partner:
                partners.add(i.partner)
        for p in partners:
            ledger.update_partner_satisfied(p)

    def get_wanted_movements(self):
        amount, movements = self.get_finan_movements()
        if amount:
            raise Exception("Missing amount %s in movements" % amount)
        return movements

    def get_finan_movements(self):
        amount = decimal.Decimal(0)
        mvts = []
        for i in self.items.all():
            if i.dc == self.journal.dc:
                amount += i.amount
            else:
                amount -= i.amount
            if i.match:
                match = i.match
            elif i.partner:
                match = "%s#%s-%s" % (self.journal.ref, self.pk, i.seqno)
            else:
                match = ''
            b = self.create_movement(
                i.account, i.dc, i.amount,
                seqno=i.seqno,
                match=match,
                partner=i.partner)
            mvts.append(b)

        return amount, mvts


class JournalEntry(Voucher):

    """
    This is the model for "operations diverses" ("journal entries")
    but also base for :class:`PaymentOrder`
    and :class:`BankStatement`.
    """
    class Meta:
        verbose_name = _("Journal Entry")
        verbose_name_plural = _("Journal Entries")


class PaymentOrder(Voucher):

    class Meta:
        verbose_name = _("Payment Order")
        verbose_name_plural = _("Payment Orders")

    total = dd.PriceField(_("Total"), blank=True, null=True)
    execution_date = models.DateField(
        _("Execution date"), blank=True, null=True)

    def get_wanted_movements(self):
        a = self.journal.account
        if not a:
            raise Exception("No account in %s" % self.journal)
        amount, movements = self.get_finan_movements()
        self.total = - amount
        for m in movements:
            yield m
        yield self.create_movement(a, self.journal.dc, -amount)


class BankStatement(Voucher):

    class Meta:
        verbose_name = _("Bank Statement")
        verbose_name_plural = _("Bank Statements")

    balance1 = dd.PriceField(_("Old balance"), default=ZERO)
    #~ balance2 = dd.PriceField(_("New balance"),blank=True,null=True)
    balance2 = dd.PriceField(_("New balance"), default=ZERO)

    def get_previous_voucher(self):
        if not self.journal_id:
            #~ logger.info("20131005 no journal")
            return None
        qs = self.__class__.objects.filter(
            journal=self.journal).order_by('-date')
        if qs.count() > 0:
            #~ logger.info("20131005 no other vouchers")
            return qs[0]

    def on_create(self, ar):
        super(BankStatement, self).on_create(ar)
        if self.balance1 == ZERO:
            prev = self.get_previous_voucher()
            if prev is not None:
                #~ logger.info("20131005 prev is %s",prev)
                self.balance1 = prev.balance2

    def get_wanted_movements(self):
        a = self.journal.account
        if not a:
            raise Exception("No account in %s" % self.journal)
        amount, movements = self.get_finan_movements()
        self.balance2 = self.balance1 + amount
        for m in movements:
            yield m
        yield self.create_movement(a, not self.journal.dc, amount)


class VoucherItem(mixins.Sequenced, ledger.VoucherItem, ledger.Matchable):

    """
    """
    class Meta:
        abstract = True
        verbose_name = _("Item")
        verbose_name_plural = _("Items")

    amount = dd.PriceField(default=0)
    dc = accounts.DebitOrCreditField()
    remark = models.CharField(_("Remark"), max_length=200, blank=True)
    account = dd.ForeignKey('accounts.Account', blank=True)
    partner = dd.ForeignKey(partner_model, blank=True, null=True)

    def get_default_match(self):
        return str(self.date)

    def get_siblings(self):
        return self.voucher.items.all()

    def match_changed(self, ar):
        if self.match:
            dc = not self.voucher.journal.dc
            m = ledger.DueMovement(dc, self)
            self.dc = dc
            self.amount = m.balance
            #~ if m.balance > 0:
                #~ self.dc = not self.voucher.journal.dc
                #~ self.amount = m.balance
            #~ else:
                #~ self.dc = self.voucher.journal.dc
                #~ self.amount = - m.balance

    def full_clean(self, *args, **kw):
        if self.account_id is None:
            if self.partner is not None:
                flt = dict(partner=self.partner, satisfied=False)
                if self.match:
                    flt.update(match=self.match)
                matches = ledger.get_due_movements(
                    self.voucher.journal.dc, **flt)
                try:
                    match = matches.next()
                except StopIteration:
                    pass
                else:
                    if match.trade_type is not None:
                        self.account = match.trade_type.get_partner_account()
                    self.dc = match.dc
                    self.amount = match.balance
                    self.match = match.match
                if self.account_id is None:
                    raise ValidationError(
                        _("Could not determine the general account"))
        if self.dc is None:
            self.dc = self.voucher.journal.dc
        #~ if self.amount < 0:
            #~ self.amount = - self.amount
            #~ self.dc = not self.dc
        return super(VoucherItem, self).full_clean(*args, **kw)


class JournalEntryItem(VoucherItem):
    voucher = dd.ForeignKey(JournalEntry, related_name='items')
    date = models.DateField(blank=True, null=True)
    debit = ledger.DcAmountField(accounts.DEBIT, _("Debit"))
    credit = ledger.DcAmountField(accounts.CREDIT, _("Credit"))


class BankStatementItem(VoucherItem):
    voucher = dd.ForeignKey(BankStatement, related_name='items')
    date = models.DateField(blank=True, null=True)
    debit = ledger.DcAmountField(accounts.DEBIT, _("Income"))
    credit = ledger.DcAmountField(accounts.CREDIT, _("Expense"))


class PaymentOrderItem(VoucherItem):
    voucher = dd.ForeignKey(PaymentOrder, related_name='items')


class JournalEntryDetail(dd.FormLayout):
    main = "general ledger"

    general = dd.Panel("""
    date user narration workflow_buttons
    finan.ItemsByJournalEntry
    """, label=_("General"))

    ledger = dd.Panel("""
    id journal year number
    ledger.MovementsByVoucher
    """, label=_("Ledger"))


class PaymentOrderDetail(JournalEntryDetail):
    general = dd.Panel("""
    date user narration total execution_date workflow_buttons
    finan.ItemsByPaymentOrder
    """, label=_("General"))


class BankStatementDetail(JournalEntryDetail):
    general = dd.Panel("""
    date balance1 balance2 user workflow_buttons
    finan.ItemsByBankStatement
    """, label=_("General"))


class JournalEntries(dd.Table):
    model = 'finan.JournalEntry'
    params_panel_hidden = True
    order_by = ["date", "id"]
    parameters = dict(
        pyear=ledger.FiscalYears.field(blank=True),
        #~ ppartner=models.ForeignKey('contacts.Partner',blank=True,null=True),
        pjournal=ledger.JournalRef(blank=True))
    params_layout = "pjournal pyear"
    detail_layout = JournalEntryDetail()
    insert_layout = dd.FormLayout("""
    date user
    narration 
    """, window_size=(40, 'auto'))

    @classmethod
    def get_request_queryset(cls, ar):
        qs = super(JournalEntries, cls).get_request_queryset(ar)
        if not isinstance(qs, list):
            if ar.param_values.pyear:
                qs = qs.filter(year=ar.param_values.pyear)
            if ar.param_values.pjournal:
                qs = qs.filter(journal=ar.param_values.pjournal)
        return qs


class PaymentOrders(JournalEntries):
    model = 'finan.PaymentOrder'
    column_names = "date id number user *"
    detail_layout = PaymentOrderDetail()


class BankStatements(JournalEntries):
    model = 'finan.BankStatement'
    column_names = "date id number balance1 balance2 user *"
    insert_layout = dd.FormLayout("""
    date user
    balance1 
    balance2
    """, window_size=(40, 'auto'))

    detail_layout = BankStatementDetail()


class PaymentOrdersByJournal(PaymentOrders, ledger.ByJournal):
    pass


class JournalEntriesByJournal(JournalEntries, ledger.ByJournal):
    pass


class BankStatementsByJournal(BankStatements, ledger.ByJournal):
    pass


class ItemsByVoucher(dd.Table):
    order_by = ["seqno"]
    column_names = "date partner account match remark debit credit seqno *"
    master_key = 'voucher'
    auto_fit_column_widths = True
    hidden_columns = 'id amount dc seqno'


class ItemsByJournalEntry(ItemsByVoucher):
    model = JournalEntryItem
    column_names = "date partner account match remark debit credit seqno *"


class ItemsByBankStatement(ItemsByVoucher):
    model = BankStatementItem
    column_names = "date partner account match remark debit credit seqno *"


class ItemsByPaymentOrder(ItemsByVoucher):
    model = PaymentOrderItem
    column_names = "seqno partner match amount remark"
    hidden_columns = 'id dc'


class FillSuggestions(dd.Action):
    label = _("Fill")
    icon_name = 'lightning'
    http_method = 'POST'
    select_rows = False

    def run_from_ui(self, ar, **kw):
        voucher = ar.master_instance
        seqno = None
        n = 0
        for obj in ar.selected_rows:
            i = voucher.add_voucher_item(obj.account,
                                         dc=not obj.dc,
                                         seqno=seqno,
                                         amount=obj.balance,
                                         partner=obj.partner,
                                         match=obj.match)
                #~ match=obj.voucher.get_default_match())
            if i.amount < 0:
                i.amount = - i.amount
                i.dc = not i.dc
            i.full_clean()
            i.save()
            seqno = i.seqno + 1
            n += 1

        msg = _("%d items have been added to %s.") % (n, voucher)
        logger.info(msg)
        kw.update(close_window=True)
        ar.success(msg, **kw)


class SuggestionsByVoucher(ledger.ExpectedMovements):

    """
    Shows a list of suggested items for a given voucher,,
    with a button to fill them into the current voucher.
    
    This is an abstract virtual slave table,
    inherited by
    :class:`SuggestionsByJournalEntry`
    :class:`SuggestionsByBankStatement`
    and :class:`SuggestionsByPaymentOrder`
    who define the class of the `master_instance`.
    
    """

    label = _("Suggestions")
    column_names = 'partner match account due_date debts payments balance'
    #~ column_names = 'voucher__date partner account voucher_link:5 debit credit'
    window_size = (70, 20)  # (width, height)

    editable = False
    auto_fit_column_widths = True
    cell_edit = False

    do_fill = FillSuggestions()

    @classmethod
    def get_dc(cls, ar=None):
        if ar is None:
            return None
        voucher = ar.master_instance
        if voucher is None:
            return None
        return voucher.journal.dc

    @classmethod
    def param_defaults(cls, ar, **kw):
        voucher = ar.master_instance
        kw = super(SuggestionsByVoucher, cls).param_defaults(ar, **kw)
        #~ kw = super(MyEvents,self).param_defaults(ar,**kw)
        #~ kw.update(journal=voucher.journal)
        kw.update(date_until=voucher.date)
        #~ kw.update(trade_type=vat.TradeTypes.purchases)
        return kw

    @classmethod
    def get_data_rows(cls, ar, **flt):
        #~ partner = ar.master_instance
        #~ if partner is None: return []
        flt.update(satisfied=False)
        flt.update(account__clearable=True)
        return super(SuggestionsByVoucher, cls).get_data_rows(ar, **flt)


class SuggestionsByJournalEntry(SuggestionsByVoucher):

    """
    Shows a list of suggested items for this :class:`JournalEntry`,
    with a button to fill them into the current voucher.
    
    """
    master = 'finan.JournalEntry'


JournalEntriesByJournal.suggest = dd.ShowSlaveTable(SuggestionsByJournalEntry)


class SuggestionsByPaymentOrder(SuggestionsByVoucher):

    """
    This is not a docstring.
    """

    master = 'finan.PaymentOrder'

    @classmethod
    def param_defaults(cls, ar, **kw):
        kw = super(SuggestionsByPaymentOrder, cls).param_defaults(ar, **kw)
        voucher = ar.master_instance
        #~ kw.update(journal=voucher.journal)
        kw.update(date_until=voucher.execution_date or voucher.date)
        if voucher.journal.trade_type is not None:
            kw.update(trade_type=voucher.journal.trade_type)
        #~ kw.update(trade_type=vat.TradeTypes.purchases)
        return kw


PaymentOrdersByJournal.suggest = dd.ShowSlaveTable(SuggestionsByPaymentOrder)


class SuggestionsByBankStatement(SuggestionsByVoucher):
    master = 'finan.BankStatement'


BankStatementsByJournal.suggest = dd.ShowSlaveTable(SuggestionsByBankStatement)


ledger.VoucherTypes.add_item(JournalEntry, JournalEntriesByJournal)
ledger.VoucherTypes.add_item(PaymentOrder, PaymentOrdersByJournal)
ledger.VoucherTypes.add_item(BankStatement, BankStatementsByJournal)

MODULE_LABEL = _("Financial")


def setup_main_menu(site, ui, profile, m):
    m = m.add_menu('finan', MODULE_LABEL)

    for jnl in ledger.Journal.objects.filter(trade_type=''):
        m.add_action(jnl.voucher_type.table_class,
                     label=unicode(jnl),
                     params=dict(master_instance=jnl))


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu('finan', MODULE_LABEL)
    m.add_action('finan.BankStatements')
    m.add_action('finan.JournalEntries')
    m.add_action('finan.PaymentOrders')
