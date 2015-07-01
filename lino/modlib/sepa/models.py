# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
:xfile:`models.py` module for the :mod:`lino.modlib.sepa` app.

Defines the :class:`EventType` and :class:`Event` models and their tables.

There are some test cases in :mod:`lino.tutorials.mini.tests`

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd

from lino.core.utils import ChangeWatcher

config = dd.apps.sepa

from ..iban.fields import IBANField, BICField
from ..iban.utils import belgian_nban_to_iban_bic, iban2bic

from lino.modlib.contacts.roles import ContactsUser, ContactsStaff


class IbanBicHolder(dd.Model):

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
        super(IbanBicHolder, self).full_clean()


class Account(IbanBicHolder):
    """A bank account related to a given :class:`ml.contacts.Partner`.

    """
    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Account')
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    partner = dd.ForeignKey(
        'contacts.Partner',
        related_name='sepa_accounts')
    remark = models.CharField(_("Remark"), max_length=200, blank=True)

    primary = models.BooleanField(
        _("Primary"),
        default=False,
        help_text=_(
            "Enabling this field will automatically disable any "
            "previous primary account and update "
            "the partner's IBAN and BIC"))

    allow_cascaded_delete = ['partner']

    def after_ui_save(self, ar, cw):
        super(Account, self).after_ui_save(ar, cw)
        if self.primary:
            mi = self.partner
            for o in mi.sepa_accounts.exclude(id=self.id):
                if o.primary:
                    o.primary = False
                    o.save()
                    ar.set_response(refresh_all=True)
            watcher = ChangeWatcher(mi)
            for k in PRIMARY_FIELDS:
                setattr(mi, k, getattr(self, k))
            mi.save()
            watcher.send_update(ar.request)

PRIMARY_FIELDS = dd.fields_list(Account, 'iban bic')


class Accounts(dd.Table):
    required_roles = dd.login_required(ContactsStaff)
    model = 'sepa.Account'


class AccountsByPartner(Accounts):
    required_roles = dd.login_required(ContactsUser)
    master_key = 'partner'
    column_names = 'iban bic remark'
    order_by = ['iban']
    auto_fit_column_widths = True


