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
from django.conf import settings

from lino.api import dd, rt, _
from lino import mixins
from lino.utils.report import Report
from lino.utils.xmlgen.html import E
from lino.utils import join_elems
from lino.utils import mti

from lino.modlib.users.mixins import UserAuthored
from lino.modlib.accounts.utils import DEBIT, CREDIT, ZERO
from lino.modlib.accounts.choicelists import AccountTypes
from lino.modlib.accounts.fields import DebitOrCreditField
from lino.modlib.vat.choicelists import TradeTypes
from lino.modlib.vat.mixins import VatDocument, VatItemBase

from .utils import Balance, DueMovement, get_due_movements
from .choicelists import FiscalYears, VoucherTypes, JournalGroups
from .mixins import Matchable, VoucherItem


TradeTypes.purchases.update(
    #~ price_field_name='sales_price',
    #~ price_field_label=_("Sales price"),
    base_account_field_name='purchases_account',
    base_account_field_label=_("Purchases Base account"),
    vat_account_field_name='purchases_vat_account',
    vat_account_field_label=_("Purchases VAT account"),
    partner_account_field_name='suppliers_account',
    partner_account_field_label=_("Suppliers account"))


class Journal(mixins.BabelNamed,
              mixins.Sequenced,
              mixins.Referrable,
              mixins.PrintableType):
    """A sequence of numbered vouchers.

    **Fields:**

    .. attribute:: ref
    .. attribute:: trade_type

        Pointer to :class:`TradeTypes`.

    .. attribute:: voucher_type

        Pointer to an item of :class:`VoucherTypes`.

    .. attribute:: journal_group

        Pointer to an item of :class:`JournalGroups`.

    .. attribute:: force_sequence

    .. attribute:: chart
    .. attribute:: account
    .. attribute:: printed_name
    .. attribute:: dc

    .. attribute:: template

        See :attr:`PrintableType.template
        <lino.mixins.printable.PrintableType.template>`.


    """

    class Meta:
        verbose_name = _("Journal")
        verbose_name_plural = _("Journals")

    trade_type = TradeTypes.field(blank=True)
    voucher_type = VoucherTypes.field()
    journal_group = JournalGroups.field()

    force_sequence = models.BooleanField(
        _("Force chronological sequence"), default=False)
    chart = dd.ForeignKey('accounts.Chart')
    account = dd.ForeignKey('accounts.Account', blank=True, null=True)
    printed_name = dd.BabelCharField(max_length=100, blank=True)
    dc = DebitOrCreditField()

    @dd.chooser()
    def account_choices(cls, chart):
        fkw = dict(type=AccountTypes.bank_accounts)
        return rt.modules.accounts.Account.objects.filter(chart=chart, **fkw)

    def get_doc_model(self):
        """The model of vouchers in this Journal.

        """
        # print self,DOCTYPE_CLASSES, self.doctype
        return self.voucher_type.model
        #~ return DOCTYPES[self.doctype][0]

    def get_doc_report(self):
        return self.voucher_type.table_class
        #~ return DOCTYPES[self.doctype][1]

    def get_voucher(self, year=None, number=None, **kw):
        cl = self.get_doc_model()
        kw.update(journal=self, year=year, number=number)
        return cl.objects.get(**kw)

    def create_voucher(self, **kw):
        """Create an instance of this Journal's voucher model
        (:meth:`get_doc_model`).

        """
        cl = self.get_doc_model()
        kw.update(journal=self)
        try:
            doc = cl()
            # ~ doc = cl(**kw) # wouldn't work. See Django ticket #10808
            #~ doc.journal = self
            for k, v in kw.items():
                setattr(doc, k, v)
            #~ print 20120825, kw
        except TypeError:
            #~ print 20100804, cl
            raise
        doc.on_create(None)
        #~ doc.full_clean()
        #~ doc.save()
        return doc

    def get_allowed_accounts(self, **kw):
        if self.trade_type:
            kw[self.trade_type.name + '_allowed'] = True
        kw.update(chart=self.chart)
        return rt.modules.accounts.Account.objects.filter(**kw)

    def get_next_number(self, voucher):
        # ~ self.save() # 20131005 why was this?
        cl = self.get_doc_model()
        d = cl.objects.filter(journal=self, year=voucher.year).aggregate(
            models.Max('number'))
        number = d['number__max']
        #~ logger.info("20121206 get_next_number %r",number)
        if number is None:
            return 1
        return number + 1

    def __unicode__(self):
        s = super(Journal, self).__unicode__()
        if self.ref:
            s += " (%s)" % self.ref
            #~ return '%s (%s)' % (d.BabelNamed.__unicode__(self),self.ref or self.id)
        return s
            #~ return self.ref +'%s (%s)' % mixins.BabelNamed.__unicode__(self)
            #~ return self.id +' (%s)' % mixins.BabelNamed.__unicode__(self)

    def save(self, *args, **kw):
        #~ self.before_save()
        r = super(Journal, self).save(*args, **kw)
        self.after_save()
        return r

    def after_save(self):
        pass

    def full_clean(self, *args, **kw):
        if self.dc is None:
            if self.trade_type:
                self.dc = self.trade_type.dc
            elif self.account:
                self.dc = self.account.type.dc

        if not self.name:
            self.name = self.id
        #~ if not self.pos:
            #~ self.pos = self.__class__.objects.all().count() + 1
        super(Journal, self).full_clean(*args, **kw)

    def disable_voucher_delete(self, doc):
        # print "pre_delete_voucher", doc.number, self.get_next_number()
        if self.force_sequence:
            if doc.number + 1 != self.get_next_number(doc):
                return _("%s is not the last voucher in journal"
                         % unicode(doc))

    def get_template_groups(self):
        """Here we override the class method by an instance method.  This
        means that we must also override all other methods of
        Printable who call the *class* method.  This is currently only
        :meth:`template_choices`.

        """
        return [self.voucher_type.model.get_template_group()]

    @dd.chooser(simple_values=True)
    def template_choices(cls, build_method, voucher_type):
        # Overrides PrintableType.template_choices to not use the class
        # method `get_template_groups`.

        if not voucher_type:
            return []
        #~ print 20131006, voucher_type
        template_groups = [voucher_type.model.get_template_group()]
        return cls.get_template_choices(build_method, template_groups)


class Journals(dd.Table):
    """The default table showing all instances of :class:`Journal`.

    """
    model = Journal
    order_by = ["seqno"]
    column_names = "ref:5 name trade_type journal_group voucher_type force_sequence * seqno id"
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


def JournalRef(**kw):
    # ~ kw.update(blank=True,null=True) # Django Ticket #12708
    kw.update(related_name="%(app_label)s_%(class)s_set_by_journal")
    return dd.ForeignKey('ledger.Journal', **kw)


def VoucherNumber(**kw):
    return models.IntegerField(**kw)


class Voucher(UserAuthored, mixins.Registrable):
    """
    A Voucher is a document that represents a monetary transaction.
    Subclasses must define a field `state`.  This model is subclassed
    by sales.Invoice, ledger.AccountInvoice, finan.Statement etc...
    
    It is *not* abstract so that :class:`Movement` can have a ForeignKey
    to a Voucher. Otherwise we would have to care ourselves about data
    integrity, and we couln't make queries on `voucher__xxx`.

    """

    class Meta:
        verbose_name = _("Voucher")
        verbose_name_plural = _("Vouchers")

    date = models.DateField(_("Date"), default=dd.today)
    journal = JournalRef()
    year = FiscalYears.field(blank=True)
    number = VoucherNumber(blank=True, null=True)
    narration = models.CharField(_("Narration"), max_length=200, blank=True)

    #~ @classmethod
    #~ def create_journal(cls,id,**kw):
        #~ doctype = get_doctype(cls)
        #~ jnl = Journal(doctype=doctype,id=id,**kw)
        #~ return jnl

    def get_due_date(self):
        return self.date

    def get_trade_type(self):
        return self.journal.trade_type

    @classmethod
    def get_journals(cls):
        vt = VoucherTypes.get_by_value(dd.full_model_name(cls))
        #~ doctype = get_doctype(cls)
        return Journal.objects.filter(voucher_type=vt).order_by('seqno')

    @dd.chooser()
    def journal_choices(cls):
        # logger.info("20140603 journal_choices %r", cls)
        return cls.get_journals()

    @classmethod
    def create_journal(cls, trade_type=None, account=None, chart=None, **kw):
    #~ def create_journal(cls,jnl_id,trade_type,**kw):
        #~ doctype = get_doctype(cls)
        #~ jnl = Journal(doctype=doctype,id=jnl_id,*args,**kw)
        if isinstance(trade_type, basestring):
            trade_type = TradeTypes.get_by_name(trade_type)
        if isinstance(account, basestring):
            account = chart.get_account_by_ref(account)
            #~ account = account.Account.objects.get(chart=chart,ref=account)
        vt = VoucherTypes.get_by_value(dd.full_model_name(cls))
        kw.update(chart=chart)
        if account is not None:
            kw.update(account=account)
        return Journal(trade_type=trade_type, voucher_type=vt, **kw)

    def __unicode__(self):
        return "%s#%s" % (self.journal.ref, self.id)
        #~ if self.number is None:
            # ~ return "%s #%s (not registered)" % (
                #~ unicode(self.journal.voucher_type.model._meta.verbose_name),self.id)
        #~ if self.journal.ref:
            # ~ return "%s#%s" % (self.journal.ref,self.number)
        # ~ return "#%s (%s %s)" % (self.number,self.journal,self.year)

    def get_default_match(self):
        # ~ return "%s#%s" % (self.journal.ref,self.number)
        return "%s%s" % (self.id, self.journal.ref)

    #~ def on_create(self,*args,**kw):
        #~ super(Voucher,self).on_create(*args,**kw)
        #~ settings.SITE.on_create_voucher(self)

    def before_state_change(self, ar, old, new):
        if new.name == 'registered':
            self.register_voucher(ar)
        elif new.name == 'draft':
            self.deregister_voucher(ar)
        super(Voucher, self).before_state_change(ar, old, new)

    def register_voucher(self, ar):
        """
        delete any existing movements and re-create them
        """
        #~ if self.year is None:
        self.year = FiscalYears.from_date(self.date)
        if self.number is None:
            self.number = self.journal.get_next_number(self)
        assert self.number is not None
        self.movement_set.all().delete()
        seqno = 0
        for m in self.get_wanted_movements():
            seqno += 1
            m.seqno = seqno
            m.full_clean()
            m.save()
        #~ super(Voucher,self).register(ar)

    def deregister_voucher(self, ar):
        self.number = None
        self.movement_set.all().delete()
        #~ super(Voucher,self).deregister(ar)

    def disable_delete(self, ar):
        msg = self.journal.disable_voucher_delete(self)
        if msg is not None:
            return msg
        return super(Voucher, self).disable_delete(ar)

    def get_wanted_movements(self):
        """Subclasses must implement this.  Supposed to return or yield a
        list of unsaved :class:`Movement` instances.

        """
        raise NotImplementedError()

    def create_movement(self, account, dc, amount, **kw):
        assert isinstance(account, rt.modules.accounts.Account)
        kw['voucher'] = self
        #~ account = accounts.Account.objects.get(group__ref=account)
        #~ account = self.journal.chart.get_account_by_ref(account)
        kw['account'] = account
        if amount < 0:
            amount = - amount
            dc = not dc
        kw['amount'] = amount
        kw['dc'] = dc

        #~ kw['journal'] = self.journal
        #~ kw['year'] = self.year
        #~ kw['number'] = self.number
        #~ kw['voucher'] = self
        #kw['number'] = self.number
        #~ kw.setdefault('date',self.date)
        #~ if not kw.get('date',None):
            #~ kw['date'] = self.value_date
        b = Movement(**kw)
        # print b.date
        # b.save()
        return b

    #~ def get_row_permission(self,ar,state,ba):
        #~ """
        #~ Only invoices in an editable state may be edited.
        #~ """
        #~ if not ba.action.readonly and self.state is not None and not self.state.editable:
            #~ return False
        #~ return super(Voucher,self).get_row_permission(ar,state,ba)

    def get_mti_leaf(self):
        """
        Return the specialized form of this voucher.

        For example if we have :class:`ml.ledger.Voucher` instance, we
        can get the actual document (Invoice, PaymentOrder,
        BankStatement, ...) by calling this method.


        """
        return mti.get_child(self, self.journal.voucher_type.model)

    def obj2html(self, ar):
        mc = self.get_mti_leaf()
        if mc is None:
            return ''
        return ar.obj2html(mc)

    #~ def add_voucher_item(self,account=None,**kw):
        #~ if account is not None:
            #~ if not isinstance(account,accounts.Account):
            #~ if isinstance(account,basestring):
                #~ account = self.journal.chart.get_account_by_ref(account)
            #~ kw['account'] = account
    def add_voucher_item(self, account=None, **kw):
        if account is not None:
            if isinstance(account, basestring):
                account = self.journal.chart.get_account_by_ref(account)
            kw['account'] = account
        kw.update(voucher=self)
        #~ logger.info("20131116 %s",self.items.model)
        return self.items.model(**kw)
        #~ return super(AccountInvoice,self).add_voucher_item(**kw)


class Vouchers(dd.Table):
    """
    The default table for all tables working on :class:`Voucher`.
    """
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


class ByJournal(dd.Table):
    order_by = ["-date", '-id']
    # order_by = ["-number"]
    master_key = 'journal'  # see django issue 10808
    # start_at_bottom = True

    @classmethod
    def get_title_base(self, ar):
        """Without this override we would have a title like "Invoices of
        journal <Invoices>".  But we want just "Invoices".

        """
        return unicode(ar.master_instance)


class VouchersByPartner(dd.VirtualTable):
    """A :class:`dd.VirtualTable` which shows all VatDocument
    vouchers by :class:`lino.modlib.contacts.models.Partner`. It has a
    customized slave summary.

    """
    label = _("VAT vouchers")
    order_by = ["-date", '-id']
    master = 'contacts.Partner'
    column_names = "date voucher total_incl total_base total_vat"

    slave_grid_format = 'summary'

    @classmethod
    def get_data_rows(self, ar):
        obj = ar.master_instance
        rows = []
        if obj is not None:
            for M in rt.models_by_base(VatDocument):
                rows += list(M.objects.filter(partner=obj))

            def by_date(a, b):
                return cmp(b.date, a.date)

            rows.sort(by_date)
        return rows

    @dd.displayfield(_("Voucher"))
    def voucher(self, row, ar):
        return ar.obj2html(row)

    @dd.virtualfield('ledger.Voucher.date')
    def date(self, row, ar):
        return row.date

    @dd.virtualfield('ledger.AccountInvoice.total_incl')
    def total_incl(self, row, ar):
        return row.total_incl

    @dd.virtualfield('ledger.AccountInvoice.total_base')
    def total_base(self, row, ar):
        return row.total_base

    @dd.virtualfield('ledger.AccountInvoice.total_vat')
    def total_vat(self, row, ar):
        return row.total_vat

    @classmethod
    def get_slave_summary(self, obj, ar):

        elems = []
        sar = self.request(master_instance=obj)
        # elems += ["Partner:", unicode(ar.master_instance)]
        for voucher in sar:
            vc = voucher.get_mti_leaf()
            if vc and vc.state.name == "draft":
                elems += [ar.obj2html(vc), " "]

        vtypes = set()
        for m in rt.models_by_base(VatDocument):
            vtypes.add(
                VoucherTypes.get_by_value(dd.full_model_name(m)))

        actions = []

        def add_action(btn):
            if btn is None:
                return False
            actions.append(btn)
            return True

        for vt in vtypes:
            for jnl in vt.get_journals():
                sar = vt.table_class.insert_action.request_from(
                    ar, master_instance=jnl,
                    known_values=dict(partner=obj))
                actions.append(
                    sar.ar2button(label=unicode(jnl), icon_name=None))
                actions.append(' ')

        elems += [E.br(), _("Create voucher in journal ")] + actions
        return E.div(*elems)


class Movement(dd.Model):
    """Represents an accounting movement in the ledger.

    """
    allow_cascaded_delete = ['voucher']

    class Meta:
        verbose_name = _("Movement")
        verbose_name_plural = _("Movements")

    voucher = models.ForeignKey(Voucher)

    seqno = models.IntegerField(
        #~ blank=True,null=False,
        verbose_name=_("Seq.No."))

    account = dd.ForeignKey('accounts.Account')
    partner = dd.ForeignKey('contacts.Partner', blank=True, null=True)
    amount = dd.PriceField(default=0)
    dc = DebitOrCreditField()

    match = models.ForeignKey(
        'ledger.Movement', verbose_name=_("Match"),
        help_text=_("The movement matched by this one."),
        related_name="%(app_label)s_%(class)s_set_by_match",
        blank=True, null=True)

    # match = MatchField(blank=True, null=True)

    satisfied = models.BooleanField(_("Satisfied"), default=False)
    # TODO: rename "satisfied" to "cleared"

    @dd.chooser(simple_values=True)
    def match_choices(cls, partner, account):
        #~ DC = voucher.journal.dc
        #~ choices = []
        qs = cls.objects.filter(
            partner=partner, account=account, satisfied=False)
        qs = qs.order_by('voucher__date')
        #~ qs = qs.distinct('match')
        return qs.values_list('match', flat=True)

    #~ def full_clean(self,*args,**kw):
        #~ if not self.match:
            #~ self.match = self.voucher.get_default_match()
        #~ super(Matchable,self).full_clean(*args,**kw)
    #~ def get_default_match(self):
        #~ return unicode(self.voucher)
    def select_text(self):
        v = self.voucher.get_mti_leaf()
        return "%s (%s)" % (v, v.date)

    @dd.virtualfield(dd.PriceField(_("Debit")))
    def debit(self, ar):
        if self.dc:
            #~ return ZERO
            return None
        return self.amount

    @dd.virtualfield(dd.PriceField(_("Credit")))
    def credit(self, ar):
        if self.dc:
            return self.amount
        #~ return ZERO
        return None

    @dd.displayfield(_("Voucher"))
    def voucher_link(self, ar):
        #~ return self.voucher.get_mti_leaf().obj2html(ar)
        return ar.obj2html(self.voucher.get_mti_leaf())

    #~ @dd.displayfield(_("Matched by"))
    #~ def matched_by(self,ar):
        #~ elems = [obj.voucher_link(ar) for obj in Movement.objects.filter(match=self)]
        #~ return E.div(*elems)

    def get_siblings(self):
        return self.voucher.movement_set.order_by('seqno')
        #~ return self.__class__.objects.filter().order_by('seqno')

    def __unicode__(self):
        return "%s.%d" % (unicode(self.voucher), self.seqno)


class Movements(dd.Table):
    """
    The base table for all tables working on :class:`Movement`.

    Displayed by :menuselection:`Explorer --> Accounting --> Movements`.

    This is also the base class for :class:`MovementsByVoucher`,
    :class:`MovementsByAccount` and :class:`MovementsByPartner` and
    defines e.g. filtering parameters.
    """
    
    model = Movement
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
    column_names = 'seqno account debit credit match satisfied'
    auto_fit_column_widths = True


class MovementsByPartner(Movements):
    master_key = 'partner'
    order_by = ['-voucher__date']
    column_names = ('voucher__date voucher_link debit credit '
                    'account match satisfied')
    auto_fit_column_widths = True

    @classmethod
    def param_defaults(cls, ar, **kw):
        kw = super(MovementsByPartner, cls).param_defaults(ar, **kw)
        kw.update(cleared=dd.YesNo.no)
        kw.update(pyear='')
        return kw


class MovementsByAccount(Movements):
    master_key = 'account'
    order_by = ['-voucher__date']
    column_names = 'voucher__date voucher_link debit credit \
    partner match satisfied'
    auto_fit_column_widths = True

    @classmethod
    def param_defaults(cls, ar, **kw):
        kw = super(MovementsByAccount, cls).param_defaults(ar, **kw)
        if ar.master_instance is not None and ar.master_instance.clearable:
            kw.update(cleared=dd.YesNo.no)
            kw.update(pyear='')
        return kw


class MatchRule(dd.Model):
    """A **match rule** specifies that a movement into given account can
be cleared using a given journal.

    """
    # allow_cascaded_delete = ['account', 'journal']

    class Meta:
        verbose_name = _("Match rule")
        verbose_name_plural = _("Match rules")
        unique_together = ['account', 'journal']

    account = dd.ForeignKey('accounts.Account')
    journal = JournalRef()


class MatchRules(dd.Table):
    model = 'ledger.MatchRule'


class MatchRulesByAccount(MatchRules):
    master_key = 'account'


class MatchRulesByJournal(MatchRules):
    master_key = 'journal'


class ExpectedMovements(dd.VirtualTable):
    """
    A virtual table of :class:`DueMovement` rows, showing
    all "expected" "movements (payments)".

    Subclassed by :class:`lino.modlib.finan.models.SuggestionsByVoucher`.


    """
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
        return Movement._meta.pk

    @classmethod
    def get_row_by_pk(cls, ar, pk):
        mvt = Movement.objects.get(pk=pk)
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


class InvoiceStates(dd.Workflow):
    #~ label = _("State")
    pass
add = InvoiceStates.add_item
add('10', _("Draft"), 'draft', editable=True)
add('20', _("Registered"), 'registered', editable=False)
#~ add('20',_("Signed"),'signed')
#~ add('30',_("Sent"),'sent')
add('40', _("Paid"), 'paid', editable=False)


@dd.receiver(dd.pre_analyze)
def setup_ledger_workflow(sender=None, **kw):
    InvoiceStates.registered.add_transition(
        _("Register"), states='draft', icon_name='accept')
    InvoiceStates.draft.add_transition(
        _("Deregister"), states="registered", icon_name='pencil')


class AccountInvoice(VatDocument, Voucher, Matchable):
    """An invoice for which the user enters just the bare accounts and
    amounts (not e.g. products, quantities, discounts).

    An account invoice does not usually produce a printable
    document. This model is typically used to store incoming purchase
    invoices, but exceptions in both directions are possible: (1)
    purchase invoices can be stored using `purchases.Invoice` if stock
    management is important, or (2) outgoing sales invoice can have
    been created using some external tool and are entered into Lino
    just for the general ledger.

    """
    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")

    your_ref = models.CharField(
        _("Your reference"), max_length=200, blank=True)
    due_date = models.DateField(_("Due date"), blank=True, null=True)
    state = InvoiceStates.field(default=InvoiceStates.draft)
    workflow_state_field = 'state'

    def get_due_date(self):
        return self.due_date or self.date


class InvoiceDetail(dd.FormLayout):
    main = "general ledger"

    totals = """
    total_base
    total_vat
    total_incl
    workflow_buttons
    """

    general = dd.Panel("""
    id date partner user
    due_date your_ref vat_regime #item_vat
    ItemsByInvoice:60 totals:20
    """, label=_("General"))

    ledger = dd.Panel("""
    journal year number narration
    MovementsByVoucher
    """, label=_("Ledger"))


class PartnerVouchers(Vouchers):
    editable = True

    parameters = dict(
        partner=models.ForeignKey(
            'contacts.Partner', blank=True, null=True),
        **Vouchers.parameters)
    params_layout = "journal year partner"

    @classmethod
    def get_request_queryset(cls, ar):
        qs = super(PartnerVouchers, cls).get_request_queryset(ar)
        pv = ar.param_values
        if pv.partner:
            qs = qs.filter(partner=pv.partner)
        return qs


class AccountInvoices(PartnerVouchers):
    model = 'ledger.AccountInvoice'
    order_by = ["-id"]
    parameters = dict(
        state=InvoiceStates.field(blank=True),
        **PartnerVouchers.parameters)
    params_layout = "partner state journal year"
    params_panel_hidden = True
    column_names = "date id number partner total_incl user *"
    detail_layout = InvoiceDetail()
    insert_layout = """
    journal partner
    date total_incl
    """
    # start_at_bottom = True

    @classmethod
    def get_request_queryset(cls, ar):
        qs = super(AccountInvoices, cls).get_request_queryset(ar)
        pv = ar.param_values
        if pv.state:
            qs = qs.filter(state=pv.state)
        return qs

    @classmethod
    def unused_param_defaults(cls, ar, **kw):
        kw = super(AccountInvoices, cls).param_defaults(ar, **kw)
        kw.update(pyear=FiscalYears.from_date(settings.SITE.today()))
        return kw


class InvoicesByJournal(AccountInvoices, ByJournal):
    """
    Shows all invoices of a given journal (whose
    :attr:`Journal.voucher_type` must be :class:`AccountInvoice`)
    """
    params_layout = "partner state year"
    column_names = "number date due_date " \
        "partner " \
        "total_incl " \
        "total_base total_vat user workflow_buttons *"
                  #~ "ledger_remark:10 " \
    insert_layout = """
    partner
    date total_incl
    """


VoucherTypes.add_item(AccountInvoice, InvoicesByJournal)


class InvoiceItem(VoucherItem, VatItemBase):
    voucher = dd.ForeignKey('ledger.AccountInvoice', related_name='items')

    #~ account = models.ForeignKey('accounts.Account',blank=True,null=True)
    account = models.ForeignKey('accounts.Account')

    def get_base_account(self, tt):
        return self.account

    @dd.chooser()
    def account_choices(self, voucher):
        if voucher and voucher.journal:
            fkw = {voucher.journal.trade_type.name + '_allowed': True}
            return rt.modules.accounts.Account.objects.filter(
                chart=voucher.journal.chart, **fkw)
        return []


class ItemsByInvoice(dd.Table):
    model = 'ledger.InvoiceItem'
    column_names = "account title vat_class total_base total_vat total_incl"
    master_key = 'voucher'
    order_by = ["seqno"]
    auto_fit_column_widths = True


def mvtsum(**fkw):
    d = Movement.objects.filter(**fkw).aggregate(models.Sum('amount'))
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
        return rt.modules.accounts.Account.objects.order_by('group__ref', 'ref')

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
    required = dd.required(user_groups='accounts')

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
    required = dd.required(user_groups='accounts')

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


MODULE_LABEL = settings.SITE.plugins.accounts.verbose_name


def site_setup(site):
    c = site.modules.contacts
    for T in (c.Partners, c.Companies, c.Persons):
        if not hasattr(T.detail_layout, 'ledger'):
            T.add_detail_tab(
                "ledger",
                """
                ledger.VouchersByPartner
                ledger.MovementsByPartner
                """,
                label=MODULE_LABEL)


def customize_accounts():

    for tt in TradeTypes.objects():
        dd.inject_field(
            'accounts.Account',
            tt.name + '_allowed',
            models.BooleanField(verbose_name=tt.text, default=False))

    dd.inject_field(
        'accounts.Account',
        'clearable', models.BooleanField(_("Clearable"), default=False))


customize_accounts()


def update_partner_satisfied(p):
    """This is called when a voucher has been (un)registered on each
    partner for whom the voucher caused at least one movement.

    """
    for m in get_due_movements(DEBIT, partner=p):
        m.update_satisfied()
