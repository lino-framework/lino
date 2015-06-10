# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

from lino.api import dd, rt, _

from lino.modlib.contacts.models import *

from lino.modlib.cal.workflows import take, feedback
from lino.modlib.addresses.mixins import AddressOwner


class Partner(Partner, AddressOwner, mixins.CreatedModified):

    class Meta:
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")

    isikukood = models.CharField(
        _("isikukood"), max_length=20, blank=True)

    hidden_columns = 'created modified'

    def get_overview_elems(self, ar):
        # In the base classes, Partner must come first because
        # otherwise Django won't inherit `meta.verbose_name`. OTOH we
        # want to get the `get_overview_elems` from AddressOwner, not
        # from Partner (i.e. AddressLocation).
        elems = super(Partner, self).get_overview_elems(ar)
        elems += AddressOwner.get_overview_elems(self, ar)
        return elems


class PartnerDetail(PartnerDetail):

    main = "general contact #tickets ledger misc "

    general = dd.Panel("""
    overview:20 general2:20 general3:40
    # notes.NotesByPartner
    """, label=_("General"))

    general2 = """
    id language
    url
    """

    # tickets = "tickets.SponsorshipsByPartner"

    general3 = """
    email:40
    phone
    gsm
    fax
    """

    contact = dd.Panel("""
    address_box
    remarks:30 sepa.AccountsByPartner
    """, label=_("Contact"))

    address_box = """
    country region city zip_code:10
    addr1
    street_prefix street:25 street_no street_box
    addr2
    """

    ledger = dd.Panel("""
    vat.VouchersByPartner
    ledger.MovementsByPartner
    """, label=dd.plugins.ledger.verbose_name)

    misc = dd.Panel("""
    created modified
    """, label=_("Miscellaneous"))


class Person(Partner, Person):
    """
    Represents a physical person.
    """

    class Meta(Person.Meta):
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")
        #~ ordering = ['last_name','first_name']

    def get_queryset(self, ar):
        return self.model.objects.select_related('country', 'city')

    def get_print_language(self):
        "Used by DirectPrintAction"
        return self.language

dd.update_field(Person, 'first_name', blank=False)
dd.update_field(Person, 'last_name', blank=False)


class PersonDetail(PersonDetail):

    main = "general contact #tickets misc"

    general = dd.Panel("""
    overview:20 general2:40 general3:40
    contacts.RolesByPerson:20 households.MembersByPerson:40 \
    humanlinks.LinksByHuman
    """, label=_("General"))

    general2 = """
    title first_name:15 middle_name:15
    last_name
    gender:10 birth_date age:10
    id language
    """

    general3 = """
    email:40
    phone
    gsm
    fax
    """

    contact = dd.Panel("""
    lists.MembersByPartner
    remarks:30 sepa.AccountsByPartner
    """, label=_("Contact"))

    address_box = """
    country region city zip_code:10
    addr1
    street_prefix street:25 street_no street_box
    addr2
    """

    # tickets = "tickets.SponsorshipsByPartner"

    misc = dd.Panel("""
    url
    created modified
    # notes.NotesByPartner
    """, label=_("Miscellaneous"))


class Persons(Persons):

    detail_layout = PersonDetail()


class Company(Partner, Company):
    pass

    # class Meta:
    #     verbose_name = _("Organisation")
    #     verbose_name_plural = _("Organisations")

    # vat_id = models.CharField(_("VAT id"), max_length=200, blank=True)


class CompanyDetail(CompanyDetail):

    main = "general contact #tickets misc"

    general = dd.Panel("""
    overview:20 general2:40 general3:40
    contacts.RolesByCompany
    """, label=_("General"))

    general2 = """
    prefix:20 name:40
    type vat_id
    url
    """

    general3 = """
    email:40
    phone
    gsm
    fax
    """

    contact = dd.Panel("""
    lists.MembersByPartner
    remarks:30 sepa.AccountsByPartner
    """, label=_("Contact"))

    address_box = """
    country region city zip_code:10
    addr1
    street_prefix street:25 street_no street_box
    addr2
    """

    # tickets = "tickets.SponsorshipsByPartner"

    misc = dd.Panel("""
    id language
    created modified
    # notes.NotesByPartner
    """, label=_("Miscellaneous"))


class Companies(Companies):
    detail_layout = CompanyDetail()


@dd.receiver(dd.post_analyze)
def my_details(sender, **kw):
    contacts = sender.modules.contacts

    contacts.Partners.set_detail_layout(contacts.PartnerDetail())
    contacts.Companies.set_detail_layout(contacts.CompanyDetail())


