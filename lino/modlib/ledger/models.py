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

import datetime
from dateutil.relativedelta import relativedelta

from django.db import models

from lino.api import dd, rt, _
from lino import mixins
from lino.utils import mti

from lino.modlib.users.mixins import UserAuthored
from lino.modlib.accounts.utils import DEBIT, CREDIT, ZERO
from lino.modlib.accounts.choicelists import AccountTypes, AccountCharts
from lino.modlib.accounts.fields import DebitOrCreditField

from .utils import get_due_movements
from .choicelists import (FiscalYears, VoucherTypes, VoucherStates,
                          JournalGroups, TradeTypes)
from .mixins import PartnerRelated, VoucherNumber, JournalRef
from .ui import *


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
    chart = AccountCharts.field()
    # chart = dd.ForeignKey('accounts.Chart')
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


class PaymentTerm(mixins.BabelNamed):
    """A convention on how an invoice should be paid.

    """

    class Meta:
        verbose_name = _("Payment Term")
        verbose_name_plural = _("Payment Terms")

    days = models.IntegerField(default=0)
    months = models.IntegerField(default=0)
    end_of_month = models.BooleanField(default=False)

    def get_due_date(self, date1):
        assert isinstance(date1, datetime.date), \
            "%s is not a date" % date1
        d = date1 + relativedelta(months=self.months, days=self.days)
        if self.end_of_month:
            d = datetime.date(d.year, d.month + 1, 1)
            d = relativedelta(d, days=-1)
        return d


class Voucher(UserAuthored, mixins.Registrable):
    """A Voucher is a document that represents a monetary transaction.

    It is *not* abstract so that :class:`Movement` can have a ForeignKey
    to a Voucher.

    A voucher is never instantiated using this base model but using
    one of its subclasses. Examples of subclassed are sales.Invoice,
    vat.AccountInvoice (or vatless.AccountInvoice), finan.Statement
    etc...
    
    Subclasses must define a field `state`.

    """

    class Meta:
        verbose_name = _("Voucher")
        verbose_name_plural = _("Vouchers")

    date = models.DateField(_("Date"), default=dd.today)
    journal = JournalRef()
    year = FiscalYears.field(blank=True)
    number = VoucherNumber(blank=True, null=True)
    narration = models.CharField(_("Narration"), max_length=200, blank=True)
    state = VoucherStates.field(default=VoucherStates.draft)
    workflow_state_field = 'state'

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


class Movement(PartnerRelated):
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


for tt in TradeTypes.objects():
    dd.inject_field(
        'accounts.Account',
        tt.name + '_allowed',
        models.BooleanField(verbose_name=tt.text, default=False))

dd.inject_field(
    'accounts.Account',
    'clearable', models.BooleanField(_("Clearable"), default=False))


def update_partner_satisfied(p):
    """This is called when a voucher has been (un)registered on each
    partner for whom the voucher caused at least one movement.

    """
    for m in get_due_movements(DEBIT, partner=p):
        m.update_satisfied()

