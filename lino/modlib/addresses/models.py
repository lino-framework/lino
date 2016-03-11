# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Database models of `lino.modlib.addresses`.

"""

from __future__ import unicode_literals
from __future__ import print_function
from builtins import object

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd
from lino.modlib.countries.mixins import AddressLocation
from lino.core.roles import SiteStaff

from .choicelists import AddressTypes, DataSources


@dd.python_2_unicode_compatible
class Address(AddressLocation):
    """Inherits fields from
    :class:`lino.modlib.countries.CountryRegionCity` (country, region,
    city. zip_code) and :class:`lino.modlib.contacts.AddresssLocation`
    (street, street_no, ...)

    .. attribute:: partner

    .. attribute:: address_type

    .. attribute:: data_source
    
        Pointer to :class:`choicelists.DataSources`.

        Specifies how this information entered into our database.

    .. attribute:: primary
    
        Whether this address is the primary address of its owner.
        Setting this field will automatically uncheck any previousl
        primary addresses and update the owner's address fields.

    """

    class Meta(object):
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    data_source = DataSources.field(
        editable=False,
        default=DataSources.manually.as_callable)
    # address_type = AddressTypes.field(blank=True, null=True)
    address_type = AddressTypes.field(
        default=AddressTypes.official.as_callable)
    partner = dd.ForeignKey(
        'contacts.Partner',
        related_name='addresses_by_partner')
    remark = dd.CharField(_("Remark"), max_length=50, blank=True)

    primary = models.BooleanField(
        _("Primary"),
        default=False,
        help_text=_(
            "Checking this field will automatically uncheck any "
            "previous primary addresses and update "
            "the partner's address data fields."))

    allow_cascaded_delete = ['partner']

    def __str__(self):
        return self.address_location(', ')

    def after_ui_save(self, ar, cw):
        super(Address, self).after_ui_save(ar, cw)
        mi = self.partner
        if mi is None:
            return
        if self.primary:
            for o in mi.addresses_by_partner.exclude(id=self.id):
                if o.primary:
                    o.primary = False
                    o.save()
                    ar.set_response(refresh_all=True)
        mi.sync_primary_address(ar.request)

    def living_at_text(self):
        lines = list(self.address_location_lines())
        return self.address_type.living_text + ' ' + ', '.join(lines)


Address.ADDRESS_FIELDS = dd.fields_list(
    Address,
    'street street_no street_box addr1 addr2 zip_code city region country')


@dd.receiver(dd.pre_ui_delete, sender=Address)
def clear_partner_on_delete(sender=None, request=None, **kw):
    self = sender
    mi = self.partner
    if mi:
        mi.sync_primary_address(request)


class Addresses(dd.Table):
    model = 'addresses.Address'
    required_roles = dd.required(dd.SiteStaff)
    column_names = (
        "partner address_type:10 remark:10 "
        "address_column:30 primary data_source *")
    insert_layout = """
    country city
    street street_no street_box
    address_type remark
    """
    detail_layout = dd.FormLayout("""
    country city zip_code
    addr1
    street street_no street_box
    addr2
    address_type remark
    data_source partner
    """, window_size=(60, 'auto'))


class AddressesByPartner(Addresses):
    required_roles = dd.required()
    master_key = 'partner'
    column_names = 'address_type:10 remark:10 address_column:30 primary:5'
    label = _("Addresses")
    auto_fit_column_widths = True
    stay_in_grid = True
    window_size = (80, 20)

    # slave_grid_format = 'summary'

    # @classmethod
    # def get_slave_summary(self, obj, ar):
    #     return obj.get_overview_elems(ar)



