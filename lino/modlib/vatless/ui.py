# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Database models for `lino.modlib.vatless`.



"""

from __future__ import unicode_literals

from lino.api import dd, rt, _

from lino.utils.xmlgen.html import E

from lino.modlib.ledger.choicelists import VoucherTypes
from lino.modlib.ledger.ui import PartnerVouchers, ByJournal

from .models import AccountInvoice


class InvoiceItems(dd.Table):
    model = 'vatless.InvoiceItem'
    auto_fit_column_widths = True
    order_by = ['voucher', "seqno"]


class ItemsByInvoice(InvoiceItems):
    column_names = "account title amount"
    master_key = 'voucher'
    order_by = ["seqno"]


class InvoiceDetail(dd.FormLayout):
    main = "general ledger"

    general = dd.Panel("""
    id date project partner user
    due_date your_ref workflow_buttons amount
    ItemsByInvoice
    """, label=_("General"))

    ledger = dd.Panel("""
    journal year number narration state
    ledger.MovementsByVoucher
    """, label=_("Ledger"))


class Invoices(PartnerVouchers):
    model = 'vatless.AccountInvoice'
    order_by = ["-id"]
    # parameters = dict(
    #     state=VoucherStates.field(blank=True),
    #     **PartnerVouchers.parameters)
    # params_layout = "project partner state journal year"
    # params_panel_hidden = True
    column_names = "date id number project partner amount user *"
    detail_layout = InvoiceDetail()
    insert_layout = """
    journal project
    partner
    date amount
    """
    # start_at_bottom = True

    # @classmethod
    # def get_request_queryset(cls, ar):
    #     qs = super(Invoices, cls).get_request_queryset(ar)
    #     pv = ar.param_values
    #     if pv.state:
    #         qs = qs.filter(state=pv.state)
    #     return qs

    # @classmethod
    # def unused_param_defaults(cls, ar, **kw):
    #     kw = super(Invoices, cls).param_defaults(ar, **kw)
    #     kw.update(pyear=FiscalYears.from_date(settings.SITE.today()))
    #     return kw


class InvoicesByJournal(Invoices, ByJournal):
    """Shows all simple invoices of a given journal (whose
    :attr:`Journal.voucher_type` must be
    :class:`lino.modlib.sales.models.AccountInvoice`).

    """
    params_layout = "project partner state year"
    column_names = "number date " \
        "project partner amount due_date user workflow_buttons *"
                  #~ "ledger_remark:10 " \
    insert_layout = """
    project
    partner
    date amount
    """
    order_by = ["-number"]

VoucherTypes.add_item(AccountInvoice, InvoicesByJournal)


class VouchersByPartner(dd.VirtualTable):
    """Shows all ledger vouchers of a given partner.
    
    This is a :class:`lino.core.tables.VirtualTable` with a customized
    slave summary.

    """
    label = _("Partner vouchers")
    order_by = ["-date", '-id']
    master = 'contacts.Partner'
    slave_grid_format = 'summary'

    column_names = "date voucher project amount state"
    _master_field_name = 'partner'

    @classmethod
    def get_data_rows(self, ar):
        obj = ar.master_instance
        rows = []
        if obj is not None:
            flt = {self._master_field_name: obj}
            for M in rt.models_by_base(AccountInvoice):
                rows += list(M.objects.filter(**flt))

            def by_date(a, b):
                return cmp(b.date, a.date)

            rows.sort(by_date)
        return rows

    @dd.displayfield(_("Voucher"))
    def voucher(self, row, ar):
        return ar.obj2html(row)

    if dd.plugins.ledger.project_model:
        @dd.virtualfield('ledger.Movement.project')
        def project(self, row, ar):
            return row.project

    @dd.virtualfield('ledger.Movement.partner')
    def partner(self, row, ar):
        return row.partner

    @dd.virtualfield('ledger.Voucher.date')
    def date(self, row, ar):
        return row.date

    @dd.virtualfield('ledger.Voucher.state')
    def state(self, row, ar):
        return row.state

    @dd.virtualfield('vatless.AccountInvoice.amount')
    def amount(self, row, ar):
        return row.amount

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
        for m in rt.models_by_base(AccountInvoice):
            vtypes.add(
                VoucherTypes.get_by_value(dd.full_model_name(m)))

        actions = []

        def add_action(btn):
            if btn is None:
                return False
            actions.append(btn)
            return True

        if not ar.get_user().profile.readonly:
            flt = {self._master_field_name: obj}
            for vt in vtypes:
                for jnl in vt.get_journals():
                    sar = vt.table_class.insert_action.request_from(
                        ar, master_instance=jnl,
                        known_values=flt)
                    actions.append(
                        sar.ar2button(label=unicode(jnl), icon_name=None))
                    actions.append(' ')

            elems += [E.br(), _("Create voucher in journal ")] + actions
        return E.div(*elems)


class VouchersByProject(VouchersByPartner):
    label = _("Project vouchers")
    _master_field_name = 'project'
    column_names = "date voucher partner amount state"
