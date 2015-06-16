# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Adds demo journals and some bookings for usage by Lino Welfare.

"""

from lino.utils import Cycler
from lino.api import dd, rt

current_group = None


def objects():
    Partner = rt.modules.contacts.Partner
    Client = rt.modules.pcsw.Client
    ClientContactType = rt.modules.pcsw.ClientContactType
    ClientStates = rt.modules.pcsw.ClientStates
    Journal = rt.modules.ledger.Journal
    Invoice = rt.modules.vatless.AccountInvoice
    InvoiceItem = rt.modules.vatless.InvoiceItem
    Account = rt.modules.accounts.Account
    AccountCharts = rt.modules.accounts.AccountCharts
    AccountTypes = rt.modules.accounts.AccountTypes

    CLIENTS = Cycler(Client.objects.filter(client_state=ClientStates.coached))

    l = []
    qs = ClientContactType.objects.filter(can_refund=True)
    for cct in qs:
        qs2 = Partner.objects.filter(client_contact_type=cct)
        if qs2.count():
            # i = (cct, Cycler(qs2))
            l.append(Cycler(qs2))
    RECIPIENTS = Cycler(l)
    ACCOUNTS = Cycler(Account.objects.filter(
        chart=AccountCharts.default, type=AccountTypes.expenses))
    AMOUNTS = Cycler(10, '12.50', 25, '29.95', 120, '5.33')

    ses = rt.login('robin')
    PRC = Journal.get_by_ref('PRC')
    for i in range(20):
        kw = dict()
        kw.update(partner=RECIPIENTS.pop())
        if i % 9 != 0:
            kw.update(project=CLIENTS.pop())
        kw.update(date=dd.today(-5*i))
        kw.update(journal=PRC)
        kw.update(user=ses.get_user())
        obj = Invoice(**kw)
        yield obj
        yield InvoiceItem(
            voucher=obj, amount=AMOUNTS.pop(), account=ACCOUNTS.pop())
        if i % 5 == 0:
            yield InvoiceItem(
                voucher=obj, amount=AMOUNTS.pop(), account=ACCOUNTS.pop())
        obj.register(ses)
        obj.save()
