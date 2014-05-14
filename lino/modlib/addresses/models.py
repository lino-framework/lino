# Copyright 2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
The :xfile:`models.py` module of the :mod:`lino.modlib.addresses` app.

Defines the following actors:

- the :class:`Address` model
- the :class:`DataSources` choicelist
- the the :class:`AddressTypes` choicelist

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino import dd

contacts = dd.resolve_app('contacts')


class AddressTypes(dd.ChoiceList):
    verbose_name = _("Address type")
    verbose_name_plural = _("Address types")

add = AddressTypes.add_item
add('01', _("Official address"), 'official')  # IT020
add('02', _("Unverified address"), 'unverified')  # IT042
add('03', _("Declared address"), 'declared')  # IT214
add('04', _("Reference address"), 'reference')


class DataSources(dd.ChoiceList):
    verbose_name = _("Data source")
    verbose_name_plural = _("Data sources")

add = DataSources.add_item
add('01', _("Manually entered"), 'manually')
add('02', _("Read from eID"), 'eid')


class AddressOwner(dd.Model):
    """
    Base class for the "addressee" of any address.
    """
    class Meta:
        abstract = True

    def get_primary_address(self):
        # Address = dd.modules.addresses.Address
        # AddressTypes = dd.modules.addresses.AddressTypes
        # ADDRESS_FIELDS = dd.modules.addresses.ADDRESS_FIELDS

        kw = dict(partner=self, primary=True)
        try:
            return Address.objects.get(**kw)
        except Address.DoesNotExist:
            kw.update(address_type=AddressTypes.official)
            has_values = False
            for fldname in Address.ADDRESS_FIELDS:
                v = getattr(self, fldname)
                kw[fldname] = v
                if v:
                    has_values = True
            if has_values:
                addr = Address(**kw)
                addr.full_clean()
                addr.save()
                return addr

    
class Address(contacts.AddressLocation):

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    data_source = DataSources.field(
        editable=False, default=DataSources.manually)
    address_type = AddressTypes.field(blank=True, null=True)
    partner = dd.ForeignKey(
        'contacts.Partner',
        related_name='addresses_by_partner')
    remark = dd.CharField(_("Remark"), max_length=50, blank=True)

    primary = models.BooleanField(
        _("Primary"),
        default=False,
        help_text=_(
            "Enabling this field will automatically disable any "
            "previous primary addresses and update "
            "the partner's address data fields."))

    allow_cascaded_delete = ['partner']

    def __unicode__(self):
        return self.address_location(', ')

    def after_ui_save(self, ar):
        super(Address, self).after_ui_save(ar)
        if self.primary:
            mi = self.partner
            for o in mi.addresses_by_partner.exclude(id=self.id):
                if o.primary:
                    o.primary = False
                    o.save()
                    ar.set_response(refresh_all=True)
            watcher = dd.ChangeWatcher(mi)
            for k in self.ADDRESS_FIELDS:
                setattr(mi, k, getattr(self, k))
            mi.save()
            watcher.send_update(ar.request)

Address.ADDRESS_FIELDS = dd.fields_list(
    Address,
    'street street_no street_box addr1 addr2 zip_code city region country')


@dd.receiver(dd.pre_ui_delete)
def on_delete(sender=None, request=None, **kw):
    self = sender
    mi = self.partner
    if self.primary and mi:
        watcher = dd.ChangeWatcher(mi)
        for k in self.ADDRESS_FIELDS:
            fld = self._meta.get_field(k)
            setattr(mi, k, fld.get_default())
        mi.save()
        watcher.send_update(request)
        

class Addresses(dd.Table):
    model = 'addresses.Address'
    required = dd.required(user_level='admin')
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
    required = dd.required()
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

config = dd.apps.contacts


def setup_explorer_menu(site, ui, profile, m):
    m = m.add_menu(config.app_label, config.verbose_name)
    m.add_action('addresses.AddressTypes')
    m.add_action('addresses.Addresses')


__all__ = [
    'AddressTypes',
    'DataSources',
    'AddressOwner',
    'Address',
    'Addresses',
    'AddressesByPartner']  # 'ADDRESS_FIELDS']
