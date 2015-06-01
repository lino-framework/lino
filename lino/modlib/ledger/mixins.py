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

# from .fields import MatchField


class PartnerRelated(dd.Model):
    """Base class for things that are related to one and only one trade
    partner (i.e. another organization or person). This is base class
    for trade documents (e.g. invoices or offers), entries of
    financial vouchers and ledger movements.

    .. attribute:: partner

        The recipient of this document. A pointer to
        :class:`lino.modlib.contacts.models.Partner`.

    .. attribute:: project

        If the :attr:`project_model
        <lino.modlib.ledger.Plugin.project_model>` setting of the
        :mod:`lino.modlib.vat` plugin is nonempty, above objects will
        have a

    """
    class Meta:
        abstract = True

    partner = dd.ForeignKey('contacts.Partner', blank=True, null=True)

    if dd.plugins.ledger.project_model:
        project = models.ForeignKey(
            dd.plugins.ledger.project_model,
            blank=True, null=True,
            related_name="%(app_label)s_%(class)s_set_by_project")
    else:
        project = dd.DummyField()

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super(PartnerRelated, cls).get_registrable_fields(site):
            yield f
        yield 'partner'
        if dd.plugins.ledger.project_model:
            yield 'project'

    def get_recipient(self):
        return self.partner
    recipient = property(get_recipient)


class Matchable(dd.Model):
    """Adds a field :attr:`match` and a chooser for it.

    Base class for :class:`AccountInvoice`
    (and e.g. `sales.Invoice`, `finan.DocItem`)
    
    Requires a field `partner`.

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

    @dd.chooser()
    def match_choices(cls, journal, partner):
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


class VoucherItem(Sequenced):
    """Base class for items of a voucher.

    Subclasses must define a field :attr:`voucher` which must be a
    ForeignKey with related_name='items'

    """

    allow_cascaded_delete = ['voucher']

    class Meta:
        abstract = True
        # verbose_name = _("Voucher item")
        # verbose_name_plural = _("Voucher items")

    title = models.CharField(_("Description"), max_length=200, blank=True)

    def get_siblings(self):
        return self.voucher.items.all()

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


def JournalRef(**kw):
    # ~ kw.update(blank=True,null=True) # Django Ticket #12708
    kw.update(related_name="%(app_label)s_%(class)s_set_by_journal")
    return dd.ForeignKey('ledger.Journal', **kw)


def VoucherNumber(**kw):
    return models.IntegerField(**kw)


