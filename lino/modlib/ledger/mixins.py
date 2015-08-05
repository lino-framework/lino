# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Model mixins for `lino.modlib.ledger`.

.. autosummary::

"""

from __future__ import unicode_literals

from django.db import models

from lino.api import dd, rt, _
from lino.mixins import Sequenced


class ProjectRelated(dd.Model):
    """Model mixin for objects that are related to a :attr:`project`.

    .. attribute:: project

        Pointer to the "project". This field exists only if the
        :attr:`project_model
        <lino.modlib.ledger.Plugin.project_model>` setting of the
        :mod:`lino.modlib.ledger` plugin is nonempty.

    """
    class Meta:
        abstract = True

    if dd.plugins.ledger.project_model:
        project = models.ForeignKey(
            dd.plugins.ledger.project_model,
            blank=True, null=True,
            related_name="%(app_label)s_%(class)s_set_by_project")
    else:
        project = dd.DummyField()

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super(ProjectRelated, cls).get_registrable_fields(site):
            yield f
        if dd.plugins.ledger.project_model:
            yield 'project'


class PartnerRelated(dd.Model):
    """Base class for things that are related to one and only one trade
    partner (i.e. another organization or person). This is base class
    for both (1) trade document vouchers (e.g. invoices or offers) and
    (2) for the individual entries of financial vouchers and ledger
    movements.

    .. attribute:: partner

        The recipient of this document. A pointer to
        :class:`lino.modlib.contacts.models.Partner`.

    .. attribute:: payment_term

        The payment terms to be used in this document.  A pointer to
        :class:`PaymentTerm`.

    """
    class Meta:
        abstract = True

    partner = dd.ForeignKey(
        'contacts.Partner',
        related_name="%(app_label)s_%(class)s_set_by_partner",
        blank=True, null=True)
    payment_term = dd.ForeignKey(
        'ledger.PaymentTerm',
        related_name="%(app_label)s_%(class)s_set_by_payment_term",
        blank=True, null=True)

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super(PartnerRelated, cls).get_registrable_fields(site):
            yield f
        yield 'partner'
        yield 'payment_term'

    def get_recipient(self):
        return self.partner
    recipient = property(get_recipient)


class Matching(dd.Model):
    """Model mixin for database objects that are considered *matching
    transactions*.  A **matching transaction** is a transaction that
    matches some other movement to be cleared.

    Adds a field :attr:`match` and a chooser for it.  Requires a field
    `partner`.  The default implementation of the chooser for
    :attr:`match` requires a `journal`.

    Base class for :class:`vat.AccountInvoice`
    (and e.g. `sales.Invoice`, `finan.DocItem`)
    
    .. attribute:: match

       Pointer to the :class:`voucher
       <lino.modlib.ledger.mixins.Voucher>` which is being cleared by
       this movement.

    """
    class Meta:
        abstract = True

    match = dd.ForeignKey(
        'ledger.Movement',
        help_text=_("The movement to be matched."),
        verbose_name=_("Match"),
        related_name="%(app_label)s_%(class)s_set_by_match",
        blank=True, null=True)

    @classmethod
    def get_match_choices(cls, journal, partner):
        """This is the general algorithm.
        """
        matchable_accounts = rt.modules.accounts.Account.objects.filter(
            matchrule__journal=journal)
        fkw = dict(account__in=matchable_accounts)
        fkw.update(satisfied=False)
        if partner:
            fkw.update(partner=partner)
        qs = rt.modules.ledger.Movement.objects.filter(**fkw)
        qs = qs.order_by('voucher__date')
        #~ qs = qs.distinct('match')
        return qs
        # return qs.values_list('match', flat=True)

    @dd.chooser()
    def match_choices(cls, journal, partner):
        # todo: move this to implementing classes?
        return cls.get_match_choices(journal, partner)


class VoucherItem(dd.Model):
    """Base class for items of a voucher.

    Subclasses must define the following fields:

    .. attribute:: voucher

        Pointer to the voucher which contains this item.  Non
        nullable.  The voucher must be a subclass of
        :class:`ledger.Voucher<lino.modlib.ledger.models.Voucher>`.
        The `related_name` must be `'items'`.
    

    .. attribute:: title

        The title of this voucher.

        Currently (because of :djangoticket:`19465`), this field is
        not implemented here but in the subclasses:

        :class:`lino.modlib.vat.models.AccountInvoice`
        :class:`lino.modlib.vat.models.InvoiceItem`

    """

    allow_cascaded_delete = ['voucher']

    class Meta:
        abstract = True

    # title = models.CharField(_("Description"), max_length=200, blank=True)

    def get_row_permission(self, ar, state, ba):
        """
        Items of registered invoices may not be edited
        """
        #~ logger.info("VoucherItem.get_row_permission %s %s %s",self.voucher,state,ba)
        if not self.voucher.state.editable:
            #~ if not ar.bound_action.action.readonly:
            if not ba.action.readonly:
                return False
        #~ if not self.voucher.get_row_permission(ar,self.voucher.state,ba):
            #~ return False
        return super(VoucherItem, self).get_row_permission(ar, state, ba)


class SequencedVoucherItem(Sequenced):

    class Meta:
        abstract = True

    def get_siblings(self):
        return self.voucher.items.all()


class AccountVoucherItem(VoucherItem, SequencedVoucherItem):
    """Abstract base class for voucher items which point to an account.
    This is subclassed by
    :class:`lino.modlib.vat.models.InvoiceItem`
    and
    :class:`lino.modlib.vatless.models.InvoiceItem`.
    It defines the :attr:`account` field and some related methods.

    .. attribute:: account

        ForeignKey pointing to the account (:class:`accounts.Account
        <lino.modlib.accounts.models.Account>`) that is to be moved.

    """

    class Meta:
        abstract = True

    account = models.ForeignKey(
        'accounts.Account',
        related_name="%(app_label)s_%(class)s_set_by_account")

    def get_base_account(self, tt):
        return self.account

    @dd.chooser()
    def account_choices(self, voucher):
        if voucher and voucher.journal:
            fkw = {voucher.journal.trade_type.name + '_allowed': True}
            return rt.modules.accounts.Account.objects.filter(
                chart=voucher.journal.chart, **fkw)
        return []


def JournalRef(**kw):
    # ~ kw.update(blank=True,null=True) # Django Ticket #12708
    kw.update(related_name="%(app_label)s_%(class)s_set_by_journal")
    return dd.ForeignKey('ledger.Journal', **kw)


def VoucherNumber(**kw):
    return models.IntegerField(**kw)


