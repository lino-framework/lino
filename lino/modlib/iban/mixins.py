# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Model mixins for `lino.modlib.iban`.

"""

from __future__ import unicode_literals

from django.db import models

from lino.api import dd, rt, _

from .fields import IBANField, BICField
from .utils import belgian_nban_to_iban_bic, iban2bic


class BankAccount(dd.Model):
    """Model mixin for database objects that point to an IBAN account.

    """

    class Meta:
        abstract = True

    iban = IBANField(_("IBAN"))
    bic = BICField(_("BIC"), blank=True)

    def full_clean(self):
        if self.iban and not self.bic:
            if self.iban[0].isdigit():
                iban, bic = belgian_nban_to_iban_bic(self.iban)
                self.bic = bic
                self.iban = iban
            else:
                self.bic = iban2bic(self.iban) or ''
        super(BankAccount, self).full_clean()

    def get_iban_bic(self):
        if self.iban:
            return (self.iban, self.bic)


class Payable(BankAccount):
    """Model mixin for database objects that are considered *payable
    transactions*. To be combined with some mixin which defines a
    field `partner`.

    A **payable transaction** is a transaction that is expected to
    create a payment.

    Base class for :class:`vat.AccountInvoice`
    (and e.g. `sales.Invoice`, `finan.DocItem`)
    
    .. attribute:: your_ref
    .. attribute:: due_date
    .. attribute:: title

       A char field with a description for this transaction.

    """
    class Meta:
        abstract = True

    your_ref = models.CharField(
        _("Your reference"), max_length=200, blank=True)
    due_date = models.DateField(_("Due date"), blank=True, null=True)
    title = models.CharField(_("Description"), max_length=200, blank=True)

    def partner_changed(self, ar):
        if self.partner:
            self.iban = self.partner.iban
            self.bic = self.partner.bic
        super(Payable, self).partner_changed(ar)

    def get_due_date(self):
        return self.due_date or self.date

    @dd.chooser()
    def iban_choices(cls, partner):
        if not dd.is_installed('sepa'):
            return []
        return rt.modules.sepa.Account.objects.filter(partner=partner)
        

    # def get_iban_bic(self):
    #     if self.iban:
    #         return (self.iban, self.bic)
    #     if self.partner.iban:
    #         return (self.partner.iban, self.partner.bic)
    #     return None

dd.update_field(Payable, 'iban', blank=True)


